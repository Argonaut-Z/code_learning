from plugin_utils import scan_plugins


if __name__ == "__main__":
    print("开始扫描 plugins")
    scan_plugins("plugins", "__reg", "_reg")  # 只扫描名字中包含 _reg 的 .py 文件
