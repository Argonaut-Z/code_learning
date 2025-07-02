from typing import *


class DictToObj:
    """dict obj"""

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = DictToObj(value)
            setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)


def get_nested_attribute(obj: Any, attrs: str) -> Any:
    """get attr, eg func(obj, 'attr1.attr2.')"""
    attrs = attrs.split(".")
    result = obj
    for attr in attrs:
        if not hasattr(result, attr):
            return None
        result = getattr(result, attr)
    return result


def convert_to_nested_dict(obj: Any) -> Dict:
    "convert map to dict, eg obj=func({'inputs.proto.traffic_light': [1,2,3]}) -> obj['inputs']..."
    nested_dict = {}
    for key, value in obj.items():
        parts = key.split(".")
        current = nested_dict
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return nested_dict



flat_dict = {
    "inputs.proto.traffic_light": [1, 2, 3],
    "inputs.proto.adc_info": {"vel": 10, "acc": 0.5},
    "targets.structure.future_agent_info": {"id": 101}
}

nested = convert_to_nested_dict(flat_dict)
print(nested)

nested_obj = DictToObj(nested)

# 访问 traffic_light
val1 = get_nested_attribute(nested_obj, "inputs.proto.traffic_light")
print("traffic_light =", val1)

# 访问 adc_info.vel
val2 = get_nested_attribute(nested_obj, "inputs.proto.adc_info.vel")
print("vel =", val2)

# 访问不存在的字段
val3 = get_nested_attribute(nested_obj, "inputs.proto.xxx")
print("val3 =", val3)  # 应该是 None
