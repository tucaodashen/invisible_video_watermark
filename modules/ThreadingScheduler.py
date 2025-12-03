import threading
import queue
import time
from typing import List, Callable, Any, Optional
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="ThreadingScheduler", enable_udp=True, enable_console=True)
logger = get_logger()

class ThreadPoolManager:
    def __init__(self, max_workers: int = 5):
        """
        初始化线程池管理器

        Args:
            max_workers: 最大同时执行的线程数
        """
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.threads = []
        self.results = []
        self.lock = threading.Lock()
        self.completed_count = 0
        self.total_tasks = 0
        self.is_running = False

    def submit_tasks(self, func_list: List[Callable], *args, **kwargs) -> None:
        """
        提交任务列表到线程池

        Args:
            func_list: 函数列表
            *args: 传递给函数的参数
            **kwargs: 传递给函数的关键字参数
        """
        if self.is_running:
            logger.critical("Thread pool is running, cannot submit new tasks",tags="ThreadingScheduler:ThreadPoolManager:submit_tasks")
            raise RuntimeError("线程池正在运行中，请等待当前任务完成后再提交新任务")

        self.total_tasks = len(func_list)
        self.completed_count = 0
        self.results = [None] * self.total_tasks

        # 将任务放入队列
        for i, func in enumerate(func_list):
            self.task_queue.put((i, func, args, kwargs))

    def _worker(self) -> None:
        """工作线程函数"""
        while True:
            try:
                # 从队列中获取任务，设置超时时间以便能够优雅退出
                task_index, func, args, kwargs = self.task_queue.get(timeout=1)

                try:
                    # 执行函数
                    result = func(*args, **kwargs)

                    # 保存结果
                    with self.lock:
                        self.results[task_index] = result
                        self.completed_count += 1

                except Exception as e:
                    logger.error(f"{e} occur when task {task_index} execute: ",tags="ThreadingScheduler:ThreadPoolManager:_worker")
                    # 记录异常
                    with self.lock:
                        self.results[task_index] = e
                        self.completed_count += 1

                finally:
                    self.task_queue.task_done()

            except queue.Empty:
                # 如果队列为空且线程池停止运行，则退出线程
                if not self.is_running:
                    break

    def start(self) -> None:
        """启动线程池执行任务"""
        if self.task_queue.empty():
            logger.warning("No tasks to execute, please submit tasks first",tags="ThreadingScheduler:ThreadPoolManager:start")
            raise RuntimeError("没有任务可执行，请先提交任务")

        self.is_running = True

        # 创建并启动工作线程
        for i in range(min(self.max_workers, self.total_tasks)):
            thread = threading.Thread(target=self._worker, name=f"Worker-{i + 1}")
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def wait_completion(self, timeout: Optional[float] = None) -> bool:
        """
        等待所有任务完成

        Args:
            timeout: 超时时间（秒），None表示无限等待

        Returns:
            bool: 是否所有任务都已完成
        """
        if not self.is_running:
            logger.warning("Thread pool is not running, please start it first",tags="ThreadingScheduler:ThreadPoolManager:wait_completion")
            raise RuntimeError("线程池未启动")

        start_time = time.time()

        while self.completed_count < self.total_tasks:
            if timeout is not None and (time.time() - start_time) > timeout:
                return False
            time.sleep(0.1)  # 避免忙等待

        return True

    def get_results(self) -> List[Any]:
        """获取所有任务的结果"""
        if self.completed_count < self.total_tasks:
            logger.warning("Not all tasks have completed, cannot get results",tags="ThreadingScheduler:ThreadPoolManager:get_results")
            raise RuntimeError("任务尚未全部完成")

        return self.results

    def get_progress(self) -> float:
        """获取执行进度（0.0到1.0）"""
        if self.total_tasks == 0:
            return 0.0
        return self.completed_count / self.total_tasks

    def shutdown(self) -> None:
        """关闭线程池"""
        self.is_running = False

        # 等待所有线程结束
        for thread in self.threads:
            thread.join(timeout=5)

        self.threads.clear()
        logger.info("Thread pool shutdown completed",tags="ThreadingScheduler:ThreadPoolManager:shutdown")

    def execute(self, func_list: List[Callable], *args, **kwargs) -> List[Any]:
        """
        提交并执行任务，等待完成并返回结果

        Args:
            func_list: 函数列表
            *args: 传递给函数的参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            List[Any]: 所有任务的结果列表
        """
        self.submit_tasks(func_list, *args, **kwargs)
        self.start()
        self.wait_completion()
        results = self.get_results()
        self.shutdown()
        logger.success("All tasks have completed",tags="ThreadingScheduler:ThreadPoolManager:execute")
        return results


# 使用示例
if __name__ == "__main__":
    # 示例函数
    def task_function(name, duration=1):
        """示例任务函数"""
        print(f"任务 {name} 开始执行，耗时 {duration} 秒")
        time.sleep(duration)
        print(f"任务 {name} 完成")
        return f"任务 {name} 的结果"


    def task_with_error(name):
        """会抛出异常的任务函数"""
        print(f"任务 {name} 开始执行")
        time.sleep(0.5)
        raise ValueError(f"任务 {name} 执行出错")


    # 创建线程池管理器
    thread_pool = ThreadPoolManager(max_workers=3)

    # 准备任务列表
    tasks = [
        lambda: task_function("A", 2),
        lambda: task_function("B", 1),
        lambda: task_function("C", 3),
        lambda: task_function("D", 1),
        lambda: task_with_error("E"),
        lambda: task_function("F", 2)
    ]

    try:
        # 执行所有任务
        print("开始执行任务...")
        results = thread_pool.execute(tasks)

        # 输出结果
        print("\n所有任务完成！结果如下：")
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"任务 {i + 1}: 错误 - {result}")
            else:
                print(f"任务 {i + 1}: {result}")

    except Exception as e:
        print(f"执行过程中发生错误: {e}")

    # 另一种使用方式：分步骤执行
    print("\n" + "=" * 50)
    print("分步骤执行示例：")

    thread_pool2 = ThreadPoolManager(max_workers=2)

    # 1. 提交任务
    thread_pool2.submit_tasks([
        lambda: task_function("X", 1),
        lambda: task_function("Y", 2),
        lambda: task_function("Z", 1)
    ])

    # 2. 启动线程池
    thread_pool2.start()

    # 3. 等待完成并显示进度
    while not thread_pool2.wait_completion(timeout=0.5):
        progress = thread_pool2.get_progress() * 100
        print(f"执行进度: {progress:.1f}%")

    # 4. 获取结果
    results = thread_pool2.get_results()
    print("执行完成！")

    # 5. 关闭线程池
    thread_pool2.shutdown()