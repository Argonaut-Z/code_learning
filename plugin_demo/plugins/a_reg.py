from plugin_utils import PLUGIN_REGISTRY

class PluginA:
    def run(self):
        print("PluginA 正在运行")

def __reg():
    print("注册 PluginA 到仓库")
    PLUGIN_REGISTRY["plugin_a"] = PluginA