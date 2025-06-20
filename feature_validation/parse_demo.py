import argparse
import yaml
from dataclasses import dataclass, field
from typing import List
import pandas as pd
import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config_path",
    help="feature validation config yaml path",
    default="",
    type=str
)

args = parser.parse_args()
config_path = args.config_path

# 读取 YAML 配置文件
with open(config_path, "r") as f:
    config_yaml = yaml.safe_load(f)

print(type(config_yaml))
print(config_yaml.keys())

validations = []
for validation_dict in config_yaml["feature_validation"]:
    print(validation_dict)
    
