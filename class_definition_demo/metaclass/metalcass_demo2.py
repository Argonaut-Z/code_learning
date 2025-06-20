# 自定义元类
class MyMeta(type):
    def __new__(mcs, name, bases, attrs):
        print(f"mcs: {mcs}")       # 元类自身
        print(f"name: {name}")     # 类名
        print(f"bases: {bases}")   # 父类元组
        print(f"attrs: {attrs}")   # 类属性字典
        print(f"[MyMeta.__new__] 正在创建类 {name}")
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        print(f"[MyMeta.__init__] 初始化类 {name}")
        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        print(f"[MyMeta.__call__] 创建 {cls.__name__} 的实例")
        instance = super().__call__(*args, **kwargs)
        return instance


# 使用该元类创建一个类
class MyClass(metaclass=MyMeta):
    def __init__(self, x):
        print(f"[MyClass.__init__] 实例初始化，x={x}")
        self.x = x

    def __call__(self, x):  # 让 MyClass 的实例可调用
        print(f"[MyClass instance] 被调用，参数={x}")
        return x * 2

# 1. 验证 MyClass 是 MyMeta 的实例
print("MyClass 是 MyMeta 的实例:", isinstance(MyClass, MyMeta))

# 2. 实例化 MyClass（触发 MyMeta.__call__）
obj = MyClass(10)

# 3. 调用 MyClass 实例（触发 MyClass.__call__）
result = obj(3)

# 输出：
# [MyMeta.__new__] 正在创建类 MyClass
# [MyMeta.__init__] 初始化类 MyClass
# MyClass 是 MyMeta 的实例: True
# [MyMeta.__call__] 创建 MyClass 的实例
# [MyClass.__init__] 实例初始化，x=10
# [MyClass instance] 被调用，参数=3