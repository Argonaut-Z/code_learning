import pickle

# 示例类：表示一个简单的数据对象
class Person:
    def __init__(self, name, age, hobbies=None):
        self.name = name
        self.age = age
        self.hobbies = hobbies or []
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age}, hobbies={self.hobbies})"

# 示例 1：基本序列化与反序列化
def basic_serialization():
    # 创建对象
    alice = Person("Alice", 30, ["reading", "swimming"])
    
    # 序列化：对象 → 字节流
    serialized_data = pickle.dumps(alice)
    print(f"序列化后数据类型: {type(serialized_data)}")  # <class 'bytes'>
    print(f"序列化后数据长度: {len(serialized_data)} 字节")
    
    # 反序列化：字节流 → 对象
    deserialized_obj = pickle.loads(serialized_data)
    print(f"反序列化后对象类型: {type(deserialized_obj)}")  # <class '__main__.Person'>
    print(f"反序列化后对象内容: {deserialized_obj}")  # Person(name='Alice', age=30, hobbies=['reading', 'swimming'])

# 示例 2：序列化到文件与从文件反序列化
def file_serialization():
    # 创建对象
    bob = Person("Bob", 25, ["coding", "gaming"])
    
    # 序列化到文件
    with open("person_data.pkl", "wb") as f:
        pickle.dump(bob, f)  # 使用 dump() 直接写入文件
    
    # 从文件反序列化
    with open("person_data.pkl", "rb") as f:
        loaded_obj = pickle.load(f)  # 使用 load() 从文件读取
    
    print(f"从文件加载的对象: {loaded_obj}")  # Person(name='Bob', age=25, hobbies=['coding', 'gaming'])

# 示例 3：序列化复杂对象（包含自定义类的列表）
def complex_object_serialization():
    # 创建复杂对象
    people = [
        Person("Charlie", 40),
        Person("Diana", 28, ["painting"])
    ]
    
    # 序列化
    data_bytes = pickle.dumps(people)
    
    # 反序列化
    loaded_people = pickle.loads(data_bytes)
    
    # 验证
    for person in loaded_people:
        print(f"加载的人物: {person}")

# 示例 4：自定义序列化行为（使用 __getstate__ 和 __setstate__）
class CustomSerializablePerson(Person):
    def __getstate__(self):
        # 自定义序列化时要保存的状态
        state = self.__dict__.copy()
        # 添加额外信息
        state["created_at"] = "2025-06-17"
        return state
    
    def __setstate__(self, state):
        # 自定义反序列化时如何恢复状态
        self.__dict__.update(state)
        # 可以添加反序列化后的初始化逻辑
        if "created_at" in state:
            print(f"对象创建时间: {state['created_at']}")

def custom_serialization():
    eve = CustomSerializablePerson("Eve", 35)
    data = pickle.dumps(eve)
    loaded_eve = pickle.loads(data)  # 会打印 "对象创建时间: 2025-06-17"
    print(f"自定义序列化加载的对象: {loaded_eve}")

if __name__ == "__main__":
    print("=== 示例 1: 基本序列化与反序列化 ===")
    basic_serialization()
    
    print("\n=== 示例 2: 文件序列化 ===")
    file_serialization()
    
    print("\n=== 示例 3: 复杂对象序列化 ===")
    complex_object_serialization()
    
    print("\n=== 示例 4: 自定义序列化行为 ===")
    custom_serialization()