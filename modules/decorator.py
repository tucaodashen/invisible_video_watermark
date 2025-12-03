import time
from functools import wraps
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="decorator", enable_udp=True, enable_console=True)
logger = get_logger()


def timer_decorator(func):
    @wraps(func)  # 保留原函数的名称和文档字符串等元信息
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 获取高精度开始时间
        result = func(*args, **kwargs)    # 执行被装饰的函数
        end_time = time.perf_counter()    # 获取结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        logger.debug(f"Function {func.__name__} executed in {elapsed_time:.4f} seconds.",tags="decorator:timer_decorator")
        return result  # 返回原函数的执行结果
    return wrapper