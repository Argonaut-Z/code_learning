# type_meta_class_demo.py

"""
本示例演示type作为元类的核心功能：
1. 动态创建类的三种基础形式
2. 类属性、方法、继承关系的动态定义
3. 与类语法糖的等价性验证
4. 元类创建过程的执行顺序

type创建类的过程:
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  调用type(...)   │──────→│  type.__new__    │──────→│  创建类对象      │
└──────────────────┘       └──────────────────┘       └──────────────────┘
                                   │
                                   ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ 类对象已生成     │──────→│  type.__init__   │──────→│ 初始化类属性     │
└──────────────────┘       └──────────────────┘       └──────────────────┘
                                   │
                                   ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  调用类MyClass()  │──────→│  type.__call__   │──────→│  调用类的__new__ │
└──────────────────┘       └──────────────────┘       └──────────────────┘
                                   │
                                   ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ 实例对象已创建   │──────→│ 类的__init__     │──────→│ 初始化实例属性   │
└──────────────────┘       └──────────────────┘       └──────────────────┘
"""


# ----------------------------
# 1. 基础类创建：type的三参数语法
# ----------------------------
print("=== 1. 基础类创建 ===")

# 方式1：创建空类（等价于 class MyClass: pass）
MyClass1 = type('MyClass1', (), {})
obj1 = MyClass1()
print(f"类MyClass1的类型: {type(MyClass1)}")  # 输出: <class 'type'>
print(f"实例obj1的类型: {type(obj1)}")        # 输出: <class '__main__.MyClass1'>

# 方式2：创建带属性和方法的类
def greet(self, name='world'):
    """类方法：打印问候语"""
    print(f"[MyClass2.greet] Hello, {name}!")

MyClass2 = type('MyClass2', (), {
    'version': 1.0,       # 类属性
    'greet': greet        # 类方法
})
obj2 = MyClass2()
print(f"类属性version: {obj2.version}")     # 输出: 1.0
obj2.greet()                                # 输出: Hello, world!

# 方式3：创建继承类（等价于 class MySubclass(Base): ...）
class BaseClass:
    def base_method(self):
        print("[BaseClass] 基类方法被调用")

MySubclass = type('MySubclass', (BaseClass,), {
    'sub_method': lambda self: print("[MySubclass] 子类方法被调用")
})
obj_sub = MySubclass()
obj_sub.base_method()  # 输出: 基类方法被调用
obj_sub.sub_method()   # 输出: 子类方法被调用


# ----------------------------
# 2. 类定义与type的等价性验证
# ----------------------------
print("\n=== 2. 类定义等价性验证 ===")

# 方式A：使用type动态创建类
def dynamic_init(self, name):
    """动态定义的__init__方法"""
    self.name = name
    print(f"[动态类] 初始化实例: {self.name}")

def dynamic_method(self):
    """动态定义的实例方法"""
    print(f"[动态类] 方法被调用，实例属性name={self.name}")

DynamicClass = type('DynamicClass', (object,), {
    '__init__': dynamic_init,
    'method': dynamic_method,
    'class_attr': "动态类属性"
})

# 方式B：使用类语法糖定义类
class SyntaxSugarClass:
    """类语法糖定义的类"""
    class_attr = "语法糖类属性"
    
    def __init__(self, name):
        self.name = name
        print(f"[语法糖类] 初始化实例: {self.name}")
    
    def method(self):
        print(f"[语法糖类] 方法被调用，实例属性name={self.name}")

# 验证等价性
dyn_obj = DynamicClass("动态实例")
sugar_obj = SyntaxSugarClass("语法糖实例")

print(f"动态类属性: {dyn_obj.class_attr}")    # 输出: 动态类属性
print(f"语法糖类属性: {sugar_obj.class_attr}")  # 输出: 语法糖类属性

dyn_obj.method()  # 输出: 动态类方法被调用
sugar_obj.method()  # 输出: 语法糖类方法被调用


# ----------------------------
# 3. type创建类的执行顺序剖析
# ----------------------------
print("\n=== 3. type创建类的执行顺序 ===")

# 自定义元类（继承type，用于追踪类创建过程）
class MetaTracker(type):
    def __new__(mcs, name, bases, namespace):
        """元类的__new__方法：创建类对象"""
        print(f"\n[MetaTracker.__new__] 开始创建类: {name}")
        print(f"[MetaTracker.__new__] 基类: {bases}")
        print(f"[MetaTracker.__new__] 类命名空间: {list(namespace.keys())}")
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"[MetaTracker.__new__] 类对象创建完成，地址: {id(cls)}")
        return cls
    
    def __init__(cls, name, bases, namespace):
        """元类的__init__方法：初始化类对象"""
        print(f"[MetaTracker.__init__] 初始化类: {name}")
        print(f"[MetaTracker.__init__] 类对象地址: {id(cls)}")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        """元类的__call__方法：调用类创建实例"""
        print(f"\n[MetaTracker.__call__] 调用类 {cls.__name__} 创建实例")
        print(f"[MetaTracker.__call__] 传入参数: args={args}, kwargs={kwargs}")
        instance = super().__call__(*args, **kwargs)
        print(f"[MetaTracker.__call__] 实例创建完成，地址: {id(instance)}")
        return instance

def __init__(self, value):
    self.value = value
    print(f"[TrackedClass.__init__] 实例初始化，value={value}")

# 使用自定义元类创建类（等价于 type 的底层逻辑）
TrackedClass = MetaTracker('TrackedClass', (), {
    'def_attr': "默认属性",
    '__init__': __init__
})

# 验证类创建过程
print("\n--- 执行 TrackedClass(10) ---")
tracked_obj = TrackedClass(10)
print(f"实例属性value: {tracked_obj.value}")
print(f"类属性def_attr: {tracked_obj.def_attr}")


# ----------------------------
# 4. type创建类的内存机制验证
# ----------------------------
print("\n=== 4. 内存机制验证 ===")

# 创建类并打印内存地址
DynamicClassA = type('A', (), {'attr': 100})
DynamicClassB = type('B', (), {'attr': 200})

print(f"类DynamicClassA的地址: {id(DynamicClassA)}")
print(f"类DynamicClassB的地址: {id(DynamicClassB)}")

obj_a = DynamicClassA()
obj_b = DynamicClassB()
print(f"实例obj_a的地址: {id(obj_a)}")
print(f"实例obj_b的地址: {id(obj_b)}")

# 验证元类一致性
print(f"类A的元类: {type(DynamicClassA)}")  # 输出: <class 'type'>
print(f"类B的元类: {type(DynamicClassB)}")  # 输出: <class 'type'>
print(f"type的元类: {type(type)}")            # 输出: <class 'type'>