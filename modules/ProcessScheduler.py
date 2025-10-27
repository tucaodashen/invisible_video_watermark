import concurrent.futures
from typing import List, Any, Callable



def execute_concurrently(object_list: List[Any], max_workers: int) -> List[Any]:
    """
    并发执行一个对象列表中的每个对象的start方法，并收集所有结果。

    Args:
        object_list: 一个列表，其中的每个对象都必须有一个 `start` 方法。
                     `start` 方法应返回一个值（即任务的结果）。
        max_workers: 允许并发执行的最大工作进程数。

    Returns:
        List[Any]: 一个列表，按原始任务顺序包含每个对象 `start` 方法的返回结果。
    """
    # 检查对象是否都有 start 方法
    for obj in object_list:
        if not hasattr(obj, 'start') or not callable(getattr(obj, 'start')):
            raise TypeError(f"对象 {obj} 没有可调用的 'start' 方法")

    # 使用进程池执行器
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 使用列表推导式创建一个未来对象列表。
        # 每个未来对象代表一个异步提交的任务，该任务执行obj.start()。
        future_list = [executor.submit(obj.start) for obj in object_list]

        # 等待所有未来对象完成，并按任务提交顺序获取结果。
        # 如果某个任务引发异常，result() 会重新引发该异常。
        results = [future.result() for future in future_list]

    return results

if __name__ == '__main__':
    results = execute_concurrently([], max_workers=16)
    print("所有结果:", results)