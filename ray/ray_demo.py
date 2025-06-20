import ray

# 初始化 Ray（默认在本地创建一个集群）
ray.init()

# 定义远程函数，添加 @ray.remote 装饰器即可
@ray.remote
def square(x):
    return x * x

# 创建一个任务列表：计算 0~9 的平方（并行执行）
futures = [square.remote(i) for i in range(10)]

# 使用 ray.get 等待所有任务完成并返回结果
results = ray.get(futures)

print("平方结果：", results)

# 输出示例：[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 关闭 Ray
ray.shutdown()

@ray.remote
def process_chunk(chunk_id, data):
    print(f"正在处理块 {chunk_id}")
    return sum(data)  # 示例处理逻辑

# 假设你有 4 个数据块
data_chunks = {
    0: [1, 2, 3],
    1: [4, 5],
    2: [6, 7],
    3: [8, 9, 10],
}

# 分发任务
tasks = [process_chunk.remote(i, chunk) for i, chunk in data_chunks.items()]

# 获取全部结果
results = ray.get(tasks)

print("每个块的求和结果：", results)
# 输出：[6, 9, 13, 27]
