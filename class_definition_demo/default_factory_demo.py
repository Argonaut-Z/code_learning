from dataclasses import dataclass, field
from typing import List

"""
在 Python 中，函数 / 方法的默认参数是在定义时创建的，
而不是每次调用时创建。这意味着如果默认参数是可变对象（如列表、字典），所有实例将共享同一个对象。
"""
@dataclass
class ValidationItem:
    trip_id: str
    case_id: str
    fields: List[str] = field(default_factory=list)  # 使用可变对象作为默认参数

# 创建两个实例
item1 = ValidationItem("trip1", "case1")
item2 = ValidationItem("trip2", "case2")

# 向第一个实例的fields添加元素
item1.fields.append("field1")

# 查看第二个实例的fields
print(item1.fields)  # 输出: ['field1'] 
print(item2.fields)  # 输出: [] 


"""
default_factory是dataclass提供的一个特殊参数，用于指定默认值的创建函数。
每次实例化类时，它会调用这个函数来生成新的默认值，确保每个实例都有自己独立的对象。
"""
@dataclass
class ValidationItem:
    trip_id: str
    case_id: str
    fields: List[str] = field(default_factory=list)  # ✅ 正确写法

# 创建两个实例
item1 = ValidationItem("trip1", "case1")
item2 = ValidationItem("trip2", "case2")

# 向第一个实例的fields添加元素
item1.fields.append("field1")

# 查看第二个实例的fields
print(item2.fields)  # 输出: [] ✅ 每个实例有独立的列表