from typing import Callable, Dict, Any


class Singleton(type):
    """Meta clas for singleton"""

    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        return new_cls


class ValidationCallbackRepo(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self._callback_map: Dict[str, Callable] = {}

    def add_callback(self, name: str, callback: Callable):
        self._callback_map[name] = callback

    def get_callback(self, name: str) -> Callable:
        return self._callback_map.get(name, None)


# 假设我们定义了两个验证函数：
def validate_structure(gt, pred):
    print("结构特征验证执行")
    return gt == pred

def validate_proto(gt, pred):
    print("Proto字段验证执行")
    return abs(gt - pred) < 1e-3

# 创建回调注册器（会自动成为单例）
repo = ValidationCallbackRepo()

# 注册回调函数（通过名字）
repo.add_callback("structure", validate_structure)
repo.add_callback("proto", validate_proto)

# 获取并使用回调函数
gt_val = {"agent_count": 5}
pred_val = {"agent_count": 5}

callback = repo.get_callback("structure")
if callback:
    result = callback(gt_val, pred_val)
    print("验证结果:", result)

# 调用另一个
callback2 = repo.get_callback("proto")
if callback2:
    result2 = callback2(0.123456, 0.123455)
    print("Proto验证结果:", result2)
