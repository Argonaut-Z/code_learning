"""
ABC 是一个特殊的基类，表示“这是一个抽象类”：
如果你定义了一个类继承自 ABC,就意味着这个类不能被直接使用,必须由子类去实现具体功能。
这样可以强制开发者在子类中实现某些重要的接口方法，防止遗漏。
"""

from abc import ABC, abstractmethod


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# a = Animal()  # ❌ 报错：Can't instantiate abstract class Animal with abstract method speak

class Dog(Animal):
    def speak(self):
        print("Woof!")

d = Dog()      # ✅ 正确
d.speak()      # 输出：Woof!
