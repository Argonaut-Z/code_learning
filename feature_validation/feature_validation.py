"""feature validation"""

import argparse
import tempfile
from dataclasses import dataclass, field
from typing import List

import pandas as pd
import yaml
from loguru import logger
from tabulate import tabulate

from trajcaching.abstract_feature import AbstractModelFeature
from trajcaching.abstract_feature_node import AbstractFeatureNode
from trajcaching.abstract_pd_graph import GraphConfig, PdRepo
from trajcaching.bmk_env import FEATURE_SCENE_IMAGE_TAG
from trajcaching.common.processor_utils import multi_thread_handle_wrapper
from trajcaching.common.utils import get_feature_stage, get_nested_attribute
from trajcaching.data_config_env import DataConfigInputType
from trajcaching.pd_graph_config import DataConfig
from trajcaching.pd_node.features.base_feature import ProtoFeature


@dataclass
class ValidationField:
    key: str
    value: int = ""
    match_cnt: int = -1
    total_cnt: int = -1
    ratio_threshold: float = -1
    start_timestamp: int = -1
    end_timestamp: int = -1
    valid: bool = False

    @property
    def check_timestamp(self) -> bool:
        return self.start_timestamp > 0 and self.end_timestamp > 0

    def desc(self, gt: bool = True) -> str:
        """desc"""
        timestamp_info = ""
        if self.check_timestamp:
            timestamp_info = (
                f"timestamp range: [{self.start_timestamp}, {self.end_timestamp}]"
            )
        if gt:
            return f"{timestamp_info} {self.key}={self.value} ratio>={self.ratio_threshold}"
        else:
            return f"{timestamp_info} {self.key}={self.value} ratio({self.match_cnt} / {self.total_cnt})={self.ratio_threshold} valid: {self.valid}"

    def get_total_cnt(self, timestamp_list: List[int], downsample: int) -> int:
        if len(timestamp_list) == 0:
            return 0
        if self.check_timestamp:
            return (
                int((self.end_timestamp - self.start_timestamp) / 100000 / downsample)
                + 1
            )
        return int((timestamp_list[-1] - timestamp_list[0]) / 100000 / downsample) + 1

    def equal(self, feature_data: AbstractModelFeature) -> bool:
        """equal value"""
        if self.value == "exists":
            return True
        if isinstance(feature_data.data, dict):
            pred_value = feature_data.data[self.key]
        elif isinstance(feature_data, ProtoFeature):
            pred_value = get_nested_attribute(feature_data.data, self.key)
        else:
            # TODO: add more feature type
            raise ValueError(f"not support feature type: {type(feature_data)}")
        return pred_value == self.value


@dataclass
class ValidationItem:
    trip_id: str
    case_id: str
    fields: List[ValidationField] = field(default_factory=list)
    pred_fields: List[ValidationField] = field(default_factory=list)


@dataclass
class FeatureValidation:
    usage: str = ""
    feature_name: str = ""
    downsample: int = 1
    validations: List[ValidationItem] = field(default_factory=list)

    def get_diff_pd(self) -> pd.DataFrame:
        """feature desc"""
        diff_template = {
            "usage": [],
            "feature_name": [],
            "trip_case": [],
            "validation_gt": [],
            "validation_pred": [],
        }
        for validation in self.validations:
            for i, field in enumerate(validation.fields):
                diff_template["usage"].append(self.usage)
                diff_template["feature_name"].append(self.feature_name)
                diff_template["trip_case"].append(
                    f"{validation.trip_id}-{validation.case_id}"
                )
                diff_template["validation_gt"].append(field.desc())
                diff_template["validation_pred"].append(
                    validation.pred_fields[i].desc(gt=False)
                )
        diff_result = pd.DataFrame.from_dict(diff_template)
        return diff_result

    def get_data_config_list(self, save_dir: str) -> List[DataConfig]:
        """get data config list"""
        data_configs = []
        for validation in self.validations:
            data_configs.append(
                DataConfig(
                    name=validation.case_id,
                    trip_id=validation.trip_id,
                    image_tag=FEATURE_SCENE_IMAGE_TAG,
                    input_dir=FEATURE_SCENE_IMAGE_TAG,
                    input_type=DataConfigInputType.PERCEPTION_BACKFILL,
                    save_dir=save_dir,
                )
            )
        return data_configs

    def check(self, data_configs: List[DataConfig]) -> bool:
        """check validation ok or not"""
        ok = True
        for i, data_config in enumerate(data_configs):
            validation: ValidationItem = self.validations[i]
            pred_df = AbstractFeatureNode.read_feature_from_dir(
                data_config.features_pd_dir, optional_features=[self.feature_name]
            )
            for field in validation.fields:
                validation_field: ValidationField = field
                pred_field = ValidationField(
                    key=validation_field.key,
                    value=validation_field.value,
                )
                if self.feature_name not in pred_df:
                    pred_field.total_cnt = 0
                else:
                    check_timestamp = validation_field.check_timestamp
                    match_gt_len = 0
                    start_ts, end_ts = -1, -1
                    timestamp_list = pred_df["timestamp"].to_list()
                    for _, row in pred_df.iterrows():
                        pred_feature = AbstractModelFeature.unmarshal(
                            row[self.feature_name]
                        )
                        if check_timestamp:
                            if (
                                row["timestamp"] >= validation_field.start_timestamp
                                and row["timestamp"] <= validation_field.end_timestamp
                            ):
                                if start_ts < 0:
                                    start_ts = row["timestamp"]
                                end_ts = row["timestamp"]
                                if validation_field.equal(pred_feature):
                                    match_gt_len += 1
                        else:
                            if validation_field.equal(pred_feature):
                                match_gt_len += 1
                    # calc cnt
                    pred_field.match_cnt = match_gt_len
                    pred_field.total_cnt = validation_field.get_total_cnt(
                        timestamp_list, self.downsample
                    )
                    if pred_field.total_cnt > 0:
                        pred_field.ratio_threshold = round(
                            match_gt_len * 1.0 / pred_field.total_cnt, 2
                        )
                        pred_field.start_timestamp = start_ts
                        pred_field.end_timestamp = end_ts
                    else:
                        pred_field.ratio_threshold = 0
                    if pred_field.ratio_threshold < validation_field.ratio_threshold:
                        ok = False
                    else:
                        pred_field.valid = True
                    validation.pred_fields.append(pred_field)
        return ok


def run_feature_ppl(validation: FeatureValidation):
    ok = True
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = temp_dir
            data_config_list = validation.get_data_config_list(save_dir)

            stage = [
                [
                    {"name": "PdDpbagExtractorNode"},
                ],
                [
                    {
                        "name": "DownsampleNode",
                        "downsample_interval": validation.downsample,
                    },
                ],
            ] + [get_feature_stage([validation.feature_name])]

            PdRepo().run(
                GraphConfig(
                    graph_name="LayerPdGraphPool",
                    data_configs=data_config_list,
                    stage=stage,
                    config={},
                )
            )

            ok = validation.check(data_config_list)
    except Exception as e:
        logger.info(f"run {validation.usage} failed {e}")
        ok = False
    return ok


class FeatureValidationWrapper:

    def __init__(self) -> None:
        """init"""

    def parse(self, config_yaml: dict) -> List[FeatureValidation]:
        """parse feature validation"""
        validations = []
        for validation_dict in config_yaml["feature_validation"]:
            validation = FeatureValidation(**validation_dict)
            validation.validations = []
            for validation_item_dict in validation_dict["validations"]:
                validation_item = ValidationItem(**validation_item_dict)
                validation_item.fields = []
                for field_dict in validation_item_dict["fields"]:
                    validation_item.fields.append(ValidationField(**field_dict))
                validation.validations.append(validation_item)
            validations.append(validation)
        return validations

    def run(self, config_yaml: dict, raise_if_failed: bool = True) -> None:
        """run validation"""
        validations = self.parse(config_yaml)
        logger.info(f"run {len(validations)} validations")
        oks = multi_thread_handle_wrapper(run_feature_ppl, validations, thread_num=5)
        ok = all(oks)
        diff_pds = [validation.get_diff_pd() for validation in validations]
        concated_diff_pd = pd.concat(diff_pds, ignore_index=True)
        print(
            tabulate(
                concated_diff_pd, headers="keys", tablefmt="fancy_grid", showindex=False
            )
        )
        if not ok:
            logger.warning(f"validation has failed")
            if raise_if_failed:
                raise ValueError(f"validation has failed")
        else:
            logger.warning(f"all validation ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_path",
        help="feature validation config yaml path",
        default="",
        type=str,
    )
    args = parser.parse_args()
    config_path = args.config_path

    with open(config_path, "r") as f:
        config_yaml = yaml.safe_load(f)

    feature_validation = FeatureValidationWrapper()
    feature_validation.run(config_yaml)
