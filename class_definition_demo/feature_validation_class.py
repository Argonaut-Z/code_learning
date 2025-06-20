"""feature validation"""

import pandas as pd
import argparse
import tempfile
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class ValidationField:
    key: str
    value: str = ""
    match_cnt: int = -1
    total_cnt: int = -1
    ratio_threshold: float = -1
    start_timestamp: int = -1
    end_timestamp: int = -1
    valid: bool = False
    
    @property
    def check_timestamp(self) -> bool:
        return self.start_timestamp > 0 and self.end_timestamp > 0

    def desc(self, gt : bool = True) -> str:
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
    
    
def test_validation_field():
    # 创建一个完整的 ValidationField 实例
    vf = ValidationField(
        key="weather",
        value="sunny",
        # match_cnt=95,
        # total_cnt=100,
        ratio_threshold=0.9,
        # start_timestamp=1620000000,
        # end_timestamp=1620086400,
        valid=True
    )

    print("原始数据:")
    print(asdict(vf))  # 将对象转换为字典打印出来

    print("\n属性检查:")
    print("check_timestamp:", vf.check_timestamp)  # True
    print("ratio:", vf.match_cnt / vf.total_cnt if vf.total_cnt > 0 else 0)

    print("\n描述信息:")
    print("GT 描述:", vf.desc(gt=True))   # 期望值描述
    print("实际描述:", vf.desc(gt=False)) # 实际匹配情况描述

if __name__ == "__main__":
    test_validation_field()