class MyMeta(type):
    """自定义元类，用于观察类创建和实例化的完整过程"""
    _instances = {}
    
    def __new__(mcs, name, bases, namespace):
        """创建类对象"""
        print("\n=== 元类 __new__ 被调用 ===")
        print(f"• 元类: {mcs.__name__}")
        print(f"• 类名: {name}")
        print(f"• 基类: {bases}")
        print(f"• 类属性: {list(namespace.keys())}")
        
        # 调用父类(type)的__new__创建类对象
        cls = super().__new__(mcs, name, bases, namespace)
        print(f"→ 类对象创建完成: {cls}")
        return cls
    
    def __init__(cls, name, bases, namespace):
        """初始化类对象"""
        print("\n=== 元类 __init__ 被调用 ===")
        print(f"• 类对象: {cls}")
        print(f"• 类名: {name}")
        print(f"• 基类: {bases}")
        print(f"• namespace属性: {list(namespace.keys())}")
        
        # 为类添加额外属性
        cls.meta_info = f"由 {cls.__class__.__name__} 元类创建"
        print(f"• 类属性: {dir(cls)}")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        """类实例化时被调用，控制实例创建过程"""
        print("\n=== 元类 __call__ 被调用 ===")
        print(f"• 类对象: {cls}")
        print(f"• 实例化参数: args={args}, kwargs={kwargs}")
        
        # 1. 调用类的__new__创建实例
        print("→ 调用类的 __new__ 方法")
        instance = cls.__new__(cls, *args, **kwargs)
        
        # 2. 如果实例创建成功，则调用__init__初始化
        if isinstance(instance, cls):
            print("→ 调用类的 __init__ 方法")
            cls.__init__(instance, *args, **kwargs)
        
        print(f"→ 实例创建完成: {instance}")
        return instance

# 验证类定义阶段（触发元类的__new__和__init__）
print("\n===== 类定义阶段 =====")
# 类定义时自动触发元类的__new__和__init__
print("正在定义 MyClass...")

# 定义类时指定元类
class MyClass(metaclass=MyMeta):
    """使用自定义元类的示例类"""
    version = 1.0
    
    def __new__(cls, *args, **kwargs):
        """创建实例对象"""
        print(f"[MyClass.__new__] 创建实例")
        return super().__new__(cls)
    
    def __init__(self, value):
        """初始化实例属性"""
        print(f"[MyClass.__init__] 初始化实例: value={value}")
        self.value = value
    
    def method(self):
        print("类方法被调用")


print(MyClass._instances)

# 验证类属性
print("\n===== 类属性验证 =====")
print(f"类对象: {MyClass}")
print(f"类名: {MyClass.__name__}")
print(f"元类信息: {MyClass.meta_info}")

# 验证实例化阶段（触发元类的__call__）
print("\n===== 实例化阶段 =====")
obj = MyClass(10)

# 验证实例属性
print("\n===== 实例属性验证 =====")
print(f"实例对象: {obj}")
print(f"实例属性 value: {obj.value}")