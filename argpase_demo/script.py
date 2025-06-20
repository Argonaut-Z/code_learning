import argparse

# 创建解析器对象
parser = argparse.ArgumentParser(description="示例：处理两个数字")

# 添加两个命令行参数
parser.add_argument("--x", type=int, help="第一个整数")
parser.add_argument("--y", type=int, help="第二个整数")
parser.add_argument(
        "--debug_mode",
        action="store_true",
        help="enable local pdb debug",
        default=False,
    )

# 解析参数
args = parser.parse_args()

print(args)

# python script.py --x 3 --y 5
# 输出：Namespace(debug_mode=False, x=3, y=5)

