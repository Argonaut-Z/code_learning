from dataclasses import dataclass, field
from typing import List
import random

@dataclass
class Book:
    title: str                      # 普通字段，必须提供
    author: str                     # 普通字段，必须提供
    tags: List[str] = field(default_factory=list)  # 可变类型用 default_factory，防止多个实例共享同一列表
    isbn: str = field(init=False)   # 不需要在 __init__ 中传递，由 __post_init__ 生成
    id: int = field(default_factory=lambda: random.randint(1000, 9999))  # 每本书有一个随机 id

    def __post_init__(self):
        # 自动生成 isbn，模拟逻辑
        self.isbn = f"ISBN-{self.id}-{len(self.title)}"

# 创建两个实例
book1 = Book(title="Deep Learning", author="Ian Goodfellow")
book2 = Book(title="Python 101", author="Michael")

# 修改 tags
book1.tags.append("AI")
book2.tags.append("Programming")

# 打印两个对象
print(book1)
print(book2)

# 访问单个字段
print(f"{book1.title} has ISBN: {book1.isbn}")
