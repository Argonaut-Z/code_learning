# type作为元类时的完整调用形式:
# NewClass = type(class_name, base_classes, attributes_dict)
# - class_name：字符串，表示新类的名称（对应 __name__ 属性）。
# - base_classes：元组，包含新类继承的基类（可以为空，或继承多个基类）。
# - attributes_dict：字典，包含类的属性和方法（键为名称，值为函数或变量）。

# 1. 创建简单类
# 等同于： class MyClass: pass
MyClass = type('MyClass', (), {})

obj = MyClass()
print(type(obj))    # 输出: <class '__main__.MyClass'>

# 2. 创建带属性和方法的类
def greet(self, name='world'):
    print(f"Hello, {name}")

# 等同于:
# class MyClass:
#     version = '1.0'
#     def greet(self, name='world'): ...
MyClass = type('MyClass', (),{
    'version': 1.0,
    'greet': greet
})

obj = MyClass()
print(obj.version)
obj.greet()

class Base:
    def base_method(self):
        print("Base method")

# 等同于:
# class MySubclass(Base):
#     def sub_method(self): ...
MySubclass = type('MySubclass', (Base,), {
    'sub_method': lambda self: print("Sub method")
})

obj = MySubclass()
obj.base_method()   # 输出: Base method
obj.sub_method()    # 输出: Sub method



'''type与类定义的等价关系'''
# 方式一：使用type动态创建
def __init__(self, name):
    self.name = name

def say_hello(self):
    print(f"Hello, {self.name}!")
    
MyCLass = type('MyClass', (object,), {
    '__init__': __init__,
    'say_hello': say_hello,
    'version': 1.0
})

# 方式二：使用类语法糖
class MyCLass:
    version = '1.0'
    
    def __init__(self, name):
        self.name = name
    
    def say_hello(self):
        print(f"Hello, {self.name}!")
        


# 方式一
def __init__(self, value):
    self.value = value
    print(f"{type(self)}初始化value={self.value}")

MyClass = type('MyClass', (object, ), {'version': 1.0, '__init__': __init__})
obj = MyClass(10)
print(obj.version)
print(obj.value)