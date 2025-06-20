from loguru import logger

# 简单日志输出
logger.info("程序启动")
logger.warning("磁盘空间不足")
logger.error("发生错误：文件不存在")

# 带变量的日志
name = "fusion_map"
version = "1.2.3"
logger.info(f"加载特征: {name}，版本: {version}")

# 异常日志（自动捕获堆栈）
try:
    result = 10 / 0
except Exception as e:
    logger.exception("计算错误")