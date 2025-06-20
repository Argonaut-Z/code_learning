class Myclass:
    def __new__(cls, *args, **kwargs):
        """创建实例的过程"""
        print(f"[MyCLass.__new__]: 正在创建 {cls.__name__} 实例")
        # 调用父类的__new__分配内存
        instance = super().__new__(cls)
        # 可以在这里设置预初始化状态
        instance._initialized = False
        
        return instance  # 返回未初始化的实例
    
    def __init__(self, value):
        """初始化实例的过程"""
        print(f"[MyCLass.__init__]: 初始化实例, value={value}")
        # 设置实例属性
        self.value = value
        self._initialized = True
    
    def __call__(self, msg):
        """使实例可调用"""
        print(f"[MyCLass.__call__]: 实例被当作函数调用，传入参数: {msg}")
        return self.value * msg

# 测试流程
obj = Myclass(10)  # 创建并初始化实例
result = obj(3)    # 调用实例

# 输出:
# [MyCLass.__new__]: 正在创建 Myclass 实例
# [MyCLass.__init__]: 初始化实例, value=10
# [MyCLass.__call__]: 实例被当作函数调用，传入参数: 3
# 30

class MyType(object):
    def __init__(self, *args, **kwargs):
        print(f"我是初始化方法,self的id为:{id(self)}")
        self.para1 = args[0]
        self.para2 = kwargs['para2']

    def __new__(cls, *args, **kwargs):
        print(f"我是构造方法,先执行的是我,cls的id为:{id(cls)}")
        new_obj = super(MyType, cls).__new__(cls)
        print(f"创建的对象id为:{id(new_obj)}")
        return new_obj


my_class = MyType("参数1", para2='参数2')
print(my_class.para1)
print(my_class.para2)
print(f"实例化出来的对象my_class的id为:{id(my_class)}")