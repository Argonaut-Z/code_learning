import sys
import os
import argparse
import yaml

# 验证Python环境和解释器
print("\n=== Python环境验证 ===")
print(f"当前Python解释器: {sys.executable}")
print(f"Python版本: {sys.version}")
print(f"Python路径列表(sys.path):")
for path in sys.path:
    print(f"  - {path}")

# 验证环境变量
print("\n=== 环境变量验证 ===")
print(f"DPBAG_DP_USERNAME: {os.environ.get('DPBAG_DP_USERNAME', '未设置')}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', '未设置')}")

# 验证命令行参数
print("\n=== 命令行参数验证 ===")
parser = argparse.ArgumentParser(description='Feature Validation')
parser.add_argument('--config_path', type=str, help='配置文件路径')
args = parser.parse_args()
config_path = args.config_path

# 读取 YAML 配置文件
with open(config_path, "r") as f:
    config_yaml = yaml.safe_load(f)

print(type(config_yaml))
print(config_yaml.keys())

s0 = '林祖泉0'
s1 = '林祖泉1'
s2 = '林祖泉2'
ls0 = [s0] 
ls1 = [s0,s1] 
ls2 = [s0,s1,s2] 
print(ls0)
print(ls1)
print(ls2)
tup = (ls0,"aaa")
print(tup)
ls0.append("林麻子")
print(ls0)
print(tup)

names = ['Peter Anderson', 'Frank Bush', 'Tom Henry','Jack Lee', 'Dorothy Henry']

sName = "NOTFOUND"
for x in names:
    if x.endswith("Henry"):
        sName = x
        break
    print(x, "not ends with 'Henry'.")

print("I found a Henry:", sName)

