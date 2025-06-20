from plugin_utils import PLUGIN_REGISTRY

class PluginB:
    def run(self):
        print("PluginB 正在运行")

def __reg():
    print("注册 PluginB 到仓库")
    PLUGIN_REGISTRY["plugin_b"] = PluginB
