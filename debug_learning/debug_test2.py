# === 新增代码用于调试按钮对比 ===

# 1. 简单函数调用
def calculate_sum(a, b):
    print(f"计算 {a} + {b}")
    result = a + b
    return result

# 2. 列表推导式
def generate_squares(n):
    print(f"生成 1 到 {n} 的平方")
    squares = [x**2 for x in range(1, n+1)]
    return squares

# 3. 嵌套函数调用
def process_data(data):
    print(f"处理数据: {data}")
    processed = [item * 2 for item in data]
    return processed

# 4. 条件分支
def check_value(value):
    print(f"检查值: {value}")
    if value > 10:
        return "大于10"
    elif value < 5:
        return "小于5"
    else:
        return "介于5和10之间"

# 5. 字典操作
def create_dict():
    print("创建字典")
    result = {
        "name": "调试示例",
        "numbers": [1, 2, 3, 4, 5],
        "nested": {"key": "value"}
    }
    return result

# 主流程
print("\n=== 调试功能对比示例 ===")

# 断点位置1: 函数调用前
sum_result = calculate_sum(5, 7)
print(f"计算结果: {sum_result}")

# 断点位置2: 列表推导式前
squares = generate_squares(5)
print(f"平方列表: {squares}")

# 断点位置3: 嵌套函数调用前
processed_data = process_data([1, 2, 3])
print(f"处理后的数据: {processed_data}")

# 断点位置4: 条件分支前
check_result = check_value(8)
print(f"检查结果: {check_result}")

# 断点位置5: 字典操作前
my_dict = create_dict()
print(f"创建的字典: {my_dict}")

# 断点位置6: 循环操作前
for i in range(3):
    print(f"循环迭代 {i+1}")
    if i == 1:
        print("跳过中间迭代")
        continue
    print(f"当前值: {i}")

print("\n=== 调试示例结束 ===")