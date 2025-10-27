import concurrent.futures
import os
import time
import signal
from typing import List, Any, Set
from multiprocessing import Manager
import threading
import psutil
import ctypes


def _task_wrapper(obj, shared_pids):
    pid = os.getpid()
    shared_pids.append(pid)  # 将PID添加到共享列表
    try:
        return obj.start()
    except Exception as e:
        # 捕获异常并返回，避免进程崩溃
        return e
    finally:
        # 任务完成后从共享列表中移除PID
        if pid in shared_pids:
            shared_pids.remove(pid)


class ConcurrentExecutor:
    def __init__(self):
        self.pids = set()  # 存储正在执行的进程PID
        self._manager = Manager()  # 创建管理器用于进程间共享数据
        self._shared_pids = self._manager.list()  # 共享列表用于跨进程存储PID
        self.terminated = False  # 标记是否已终止
        # 添加属性获取Manager进程的PID
        self.manager_pid = self._manager._process.pid
        self._executor = None  # 保存执行器实例
        self._futures = []  # 保存所有future对象

    def execute_concurrently(self, object_list: List[Any], max_workers: int) -> List[Any]:
        """
        并发执行一个对象列表中的每个对象的start方法，并收集所有结果。

        Args:
            object_list: 一个列表，其中的每个对象都必须有一个 `start` 方法。
                         `start` 方法应返回一个值（即任务的结果）。
            max_workers: 允许并发执行的最大工作进程数。

        Returns:
            List[Any]: 一个列表，按原始任务顺序包含每个对象 `start` 方法的返回结果。
        """
        # 重置终止标志
        self.terminated = False

        # 检查对象是否都有 start 方法
        for obj in object_list:
            if not hasattr(obj, 'start') or not callable(getattr(obj, 'start')):
                raise TypeError(f"对象 {obj} 没有可调用的 'start' 方法")

        # 清空之前的PID记录
        self._shared_pids[:] = []

        # 使用进程池执行器
        self._executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        self._futures = [self._executor.submit(_task_wrapper, obj, self._shared_pids) for obj in object_list]

        # 定期更新PID集合
        def update_pids():
            while True:
                self.pids = set(self._shared_pids)  # 从共享列表更新PID集合
                time.sleep(0.05)  # 短暂休眠，避免过于频繁的更新
                # 如果所有任务都完成了，退出循环
                if all(future.done() for future in self._futures) or self.terminated:
                    break

        # 启动一个线程来定期更新PID集合
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as monitor_executor:
            monitor_future = monitor_executor.submit(update_pids)

            # 等待所有任务完成并获取结果
            results = []
            for future in concurrent.futures.as_completed(self._futures):
                if self.terminated:
                    # 如果已终止，则取消所有未完成的任务
                    for f in self._futures:
                        if not f.done():
                            f.cancel()
                    break
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(e)  # 或者可以根据需要处理异常

            # 等待监控线程结束
            monitor_future.result()

            # 最后更新一次PID集合
            self.pids = set(self._shared_pids)

        # 关闭执行器
        self._executor.shutdown(wait=False)
        self._executor = None
        self._futures = []

        # 如果被终止，返回特殊值
        if self.terminated:
            return ["Terminated"]

        return results

    def terminate_all(self):
        """
        终止所有正在执行的任务。
        """
        self.terminated = True

        # 终止所有已知的进程
        for pid in self.pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                # 进程可能已经结束
                pass
            except Exception as e:
                print(f"终止进程 {pid} 时出错: {e}")

        # 取消所有未完成的future
        if self._futures:
            for future in self._futures:
                if not future.done():
                    future.cancel()

        # 关闭执行器
        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None
            self._futures = []

    def get_running_pids(self) -> Set[int]:
        """
        获取当前正在执行的所有进程的PID集合。

        Returns:
            Set[int]: 正在执行的进程PID集合
        """
        return self.pids

    def const_print(self):
        while True:
            time.sleep(0.5)
            print("Running PIDs after completion:", self.get_running_pids())

    def __del__(self):
        """
        析构函数，确保资源被正确释放。
        """
        if self._executor:
            self._executor.shutdown(wait=False)

def manage_process_by_pid(pid, action):
    """
    通过 PID 管理进程

    参数:
    pid: 进程 ID
    action: 操作类型，可以是 'suspend', 'resume' 或 'terminate'
    """
    try:
        # 获取进程对象
        process = psutil.Process(pid)

        if action == 'suspend':
            # 挂起进程
            process.suspend()
            print(f"进程 {pid} 已挂起")

        elif action == 'resume':
            # 恢复进程
            process.resume()
            print(f"进程 {pid} 已恢复")

        elif action == 'terminate':
            # 终止进程
            process.terminate()
            print(f"进程 {pid} 正在终止...")
            # 等待进程结束
            process.wait(timeout=3)
            print(f"进程 {pid} 已终止")

        else:
            print("无效的操作类型。请使用 'suspend', 'resume' 或 'terminate'")

    except psutil.NoSuchProcess:
        print(f"错误：找不到 PID 为 {pid} 的进程")
    except psutil.AccessDenied:
        print(f"错误：没有足够的权限操作进程 {pid}")
    except Exception as e:
        print(f"发生错误：{e}")





def terminate_thread(thread):
    """强制终止线程（不推荐，可能导致资源泄漏）"""
    if not thread.is_alive():
        return

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident),
        ctypes.py_object(SystemExit)
    )

    if res == 0:
        raise ValueError("无效的线程ID")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("终止线程失败")


# 使用示例
if __name__ == "__main__":

    executor = ConcurrentExecutor()

    # 创建任务列表
    tasks = [Task(f"Task-{i}", i * 0.5) for i in range(1, 600)]
    thre = threading.Thread(target=executor.const_print)
    thre.start()

    # 执行并发任务
    results = executor.execute_concurrently(tasks, max_workers=61)


    # 输出结果
    for result in results:
        print(result)

    # 检查执行过程中的PID（此时应该为空，因为所有任务已完成）
    print("Running PIDs after completion:", executor.get_running_pids())