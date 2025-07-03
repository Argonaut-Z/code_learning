from typing import List, Dict, Set, Tuple, Optional

'''1.基本类型注解'''
# 变量类型注解
name: str = "Alice"
age: int = 30
is_student: bool = False

# 函数参数和返回值类型注解
def greet(name: str) -> str:
    return f"Hello, {name}"

# 容器类型
numbers: List[int] = [1, 2, 3]
person: Dict[str, str] = {"name": "Alice", "email": "alice@example.com"}
unique_numbers: Set[int] = {1, 2, 3}
coordinates: Tuple[float, float] = (10,5, 20,3)

# 可选类型
mayve_name: Optional[str] = None    

'''2.类型别名'''
from typing import List, Tuple

# 创建类型别名
Vector = List[float]
Point = Tuple[float, float]

def scale_vector(v: Vector, factor: float) -> Vector:
    return [x * factor for x in v]

def distance(p1: Point, p2: Point) -> float:
    return ((p1[0] - p2[0])**2 + (p1[1]-p2[1])**0.5)**0.5

'''5.函数类型'''
from typing import Callable

# Callable[[参数类型列表], 返回值类型]
def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def add(x: int, y: int) -> int:
    return x + y

print(apply_func(add, 3, 5))

# 返回str的无参数函数
def greet() -> str:
    return "Hello"

def run_func(func: Callable[[], str]) -> None:
    print(func())

run_func(greet)  # 正确