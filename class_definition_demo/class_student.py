from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    name: str                    # 表示 name 是一个字符串类型
    age: int                     # 表示 age 是一个整数类型
    grades: List[float] = field(default_factory=list)  
    # 表示 grades 是一个浮点数列表类型，初始值默认为空列表（使用 field 防止默认值共享问题）

    # @property：定义一个属性，像访问变量一样访问方法
    @property
    def average_grade(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    # @classmethod：定义一个类方法，不依赖实例，常用于构造器
    @classmethod
    def from_string(cls, student_str: str) -> "Student":
        # 例如输入 "Alice,20,90|85|88"
        name, age, grades_str = student_str.split(",")
        grades = list(map(float, grades_str.split("|")))
        return cls(name=name, age=int(age), grades=grades)

    # @staticmethod：不依赖类或实例，用于工具方法
    @staticmethod
    def is_passing(grade: float) -> bool:
        return grade >= 60.0

    # 普通方法：需要实例对象调用
    def add_grade(self, grade: float):
        self.grades.append(grade)

# 用构造函数创建实例
student1 = Student(name="Bob", age=21, grades=[88, 90, 79])

# 调用普通实例方法
student1.add_grade(92)

# 调用属性方法（注意不用加括号）
print("平均分：", student1.average_grade)  # ➜ 自动调用 average_grade() 方法

# 使用类方法从字符串创建对象
student2 = Student.from_string("Alice,20,90|85|88")
print(student2)

# 使用静态方法判断是否及格
print("85是否及格：", Student.is_passing(85))  # True
print("55是否及格：", Student.is_passing(55))  # False
