# 自定义元类：会在类创建时执行 __new__ 和 __init__
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creating class {name}")
        attrs['added_attr'] = 'I was added by metaclass'
        return super().__new__(cls, name, bases, attrs)
    
    def __init__(cls, name, bases, attrs):
        print(f"Initializing class {name}")
        super().__init__(name, bases, attrs)
    
class MyClass(metaclass=MyMeta):
    def __init__(self):
        print("📦 Instance created")

    def original_method(self):
        print("I'm the original method.")

obj = MyClass()
print(obj.added_attr)
obj.original_method()




from hello import Hello

h = Hello()

print(type(Hello))
print(type(h))


class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

class MyList(list, metaclass=ListMetaclass):
    pass

L = MyList()
L.add(1)
print(L)

L2 = list()
# L2.add(1)

print(type(list))