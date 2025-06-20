import importlib
import os

# 全局插件仓库
PLUGIN_REGISTRY = {}

def scan_plugins(directory: str, register_fn: str, match_tag: str = None):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.find(match_tag) > 0 if match_tag else True:
                if filename.endswith(".py"):
                    file_path = os.path.join(root, filename)
                    __try_run_reg_plugin_function(file_path, register_fn)


def __try_run_reg_plugin_function(file_path, register_fn: str):
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, register_fn) and callable(getattr(module, register_fn)):
        getattr(module, register_fn)()
