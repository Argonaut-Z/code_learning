"""Meta class for singleton"""

from typing import Any

class Singleton(type):
    
    _instances = {}   # 用来存放已经创建的单例对象
    
    def __call__(cls, *args, **kwds):
        print(f"{cls}正在实例化对象，此时的{cls}包含的实例化对象为{cls._instances}")
        if cls not in cls._instances:
            # 如果没有该类的实例，则创建一个并存储
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        # 直接返回已存在的实例
        return cls._instances[cls]

    def __new__(cls, name, bases, attrs):
        # 创建类本身（不是类的实例）
        print(f"[MyMeta.__new__] 正在创建类 {name}")
        new_cls = super().__new__(cls, name, bases, attrs)
        return new_cls


class MySingleton1(metaclass=Singleton):
    def __init__(self, value):
        print("init called")
        self.value = value

class MySingleton2(metaclass=Singleton):
    def __init__(self, value):
        print("init called")
        self.value = value


a = MySingleton1(10)
b = MySingleton1(20)

print(a is b)  # True：a和b是同一个对象
print(a.value)  # 10：第二次调用不会重新初始化
print(b.value)  # 10：值没有改变

c = MySingleton2(10)
d = MySingleton2(20)

print(c is d)  # True：a和b是同一个对象
print(c.value)  # 10：第二次调用不会重新初始化
print(d.value)  # 10：值没有改变




class Singleton(type):
    _instances = {"meta": "元类属性"}

class MyClass(metaclass=Singleton):
    pass

print(MyClass._instances)  # 输出: {"meta": "元类属性"}
print(MyClass._instances is Singleton._instances)  # 输出: True

print('-' * 50)