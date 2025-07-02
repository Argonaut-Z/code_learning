'''
演示类创建时内部方法的执行过程和逻辑:
'''
# 1.方法执行顺序：
# __new__ → __init__ → __call__（当实例被调用时）
# 2.地址信息验证：
# __new__ 返回的实例与 __init__ 接收的 self 是同一个对象
# 实例在整个生命周期中保持相同的内存地址
# 3.方法职责：
# __new__：创建对象并分配内存
# __init__：初始化对象的属性
# __call__：使对象可调用，类似函数


class DemoClass:
    def __new__(cls, *args, **kwargs):
        """创建实例的过程 - 分配内存空间"""
        print("\n=== 进入 __new__ 方法 ===")
        print(f"[__new__] cls 参数类型: {type(cls)}, 地址: {id(cls)}-{id(DemoClass)}")
        print(f"[__new__] 正在创建 {cls.__name__} 实例")
        
        # 调用父类的__new__方法分配内存
        instance = super().__new__(cls)
        print(f"[__new__] 已创建实例，地址: {id(instance)}")
        
        # 可以在这里设置预初始化状态
        instance._initialized = False
        print(f"[__new__] 实例预初始化状态: {instance._initialized}")
        
        return instance  # 返回未初始化的实例
    
    def __init__(self, value):
        """初始化实例的过程 - 设置属性值"""
        print("\n=== 进入 __init__ 方法 ===")
        print(f"[__init__] self 参数类型: {type(self)}, 地址: {id(self)}")
        print(f"[__init__] 检查 self 是否为 {self.__class__.__name__} 实例: {isinstance(self, self.__class__)}")
        
        # 确认 self 与 __new__ 返回的实例是同一个对象
        print(f"[__init__] self 与 __new__ 返回的实例是否相同: {id(self) == id(self)}")
        
        print(f"[__init__] 初始化实例, value={value}")
        # 设置实例属性
        self.value = value
        self._initialized = True
        print(f"[__init__] 实例初始化完成，状态: {self._initialized}")
    
    def __call__(self, multiplier):
        """使实例可调用 - 像函数一样使用"""
        print("\n=== 进入 __call__ 方法 ===")
        print(f"[__call__] self 参数类型: {type(self)}, 地址: {id(self)}")
        print(f"[__call__] 实例被调用，参数: {multiplier}")
        
        # 执行计算
        result = self.value * multiplier
        print(f"[__call__] 计算结果: {self.value} * {multiplier} = {result}")
        
        return result

# 测试类创建过程
print("\n=== 开始测试类创建过程 ===")
print(f"类对象 DemoClass 的地址: {id(DemoClass)}")

# 创建实例
print("\n--- 执行 DemoClass(5) ---")
obj = DemoClass(5)

# 调用实例
print("\n--- 执行 obj(3) ---")
result = obj(3)

# 输出最终结果
print("\n=== 测试完成 ===")
print(f"最终结果: {result}")
print(f"实例 obj 的属性: value={obj.value}, initialized={obj._initialized}")
print(f"实例 obj 的地址: {id(obj)}")
