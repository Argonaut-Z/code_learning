import argparse

parser = argparse.ArgumentParser(description="文件处理示例")

parser.add_argument("filename", type=str, help="输入的文件名")
parser.add_argument("--mode", type=str, default="read", choices=["read", "write"], help="操作模式")
parser.add_argument("--verbose", action="store_true", help="是否打印详细日志")

args = parser.parse_args()

print(args)
print("文件名:", args.filename)
print("模式:", args.mode)
print("是否详细打印:", args.verbose)

# python script2.py myfile.txt --mode write --verbose
# Namespace(filename='myfile.txt', mode='write', verbose=True)
# 文件名: myfile.txt
# 模式: write
# 是否详细打印: True