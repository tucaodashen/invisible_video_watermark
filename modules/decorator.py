import time
from functools import wraps


def timer_decorator(func):
    @wraps(func)  # 保留原函数的名称和文档字符串等元信息
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 获取高精度开始时间
        result = func(*args, **kwargs)    # 执行被装饰的函数
        end_time = time.perf_counter()    # 获取结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        print(f"Function {func.__name__} executed in {elapsed_time:.4f} seconds.")
        return result  # 返回原函数的执行结果
    return wrapper