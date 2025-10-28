# centralized_logger.py
import os
import sys
import time
import uuid
from loguru import logger
from multiprocessing import Process, Queue, current_process
from logging.handlers import QueueHandler, QueueListener

# 日志队列和监听器（全局单例）
_log_queue = Queue()
_listener = None


def init_logging_system():
    """初始化日志系统（主进程调用）"""
    global _listener

    # 创建日志目录
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    # 生成唯一日志文件名
    log_name = f"log_{time.strftime('%Y-%m-%d-%H%M%S')}_{uuid.uuid4().hex[:8]}.log"
    log_path = os.path.join(log_dir, log_name)

    # 移除默认日志处理器
    logger.remove()

    # 定义日志格式 - 保留原始位置信息
    fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[process_name]}</cyan> | "
        "<magenta>{extra[module_tag]}</magenta> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 控制台输出（只显示INFO及以上）
    logger.add(sys.stderr, level="INFO", format=fmt, enqueue=True)
    # 文件输出（所有DEBUG及以上）
    logger.add(log_path, level="DEBUG", format=fmt, enqueue=True)

    # 创建队列监听器（处理子进程日志）
    _listener = QueueListener(_log_queue, *logger._core.handlers.values())
    _listener.start()


def worker_log_configurer(queue):
    """子进程日志配置器"""
    logger.remove()
    # 添加队列处理器，保留位置信息
    logger.add(
        queue.put,
        level="DEBUG",
        enqueue=False,
        format="{message}",
        serialize=True  # 保留所有日志元数据
    )


def bind_process_context(process_name="", module_tag=""):
    """绑定进程上下文信息"""
    # 如果没有提供进程名，使用进程ID和进程名（来自multiprocessing）
    if not process_name:
        process_name = f"{os.getpid()}:{current_process().name}"

    return logger.bind(
        process_name=process_name,
        module_tag=module_tag or current_process().name
    )


# 示例使用
if __name__ == "__main__":
    # 主进程初始化
    init_logging_system()
    main_log = bind_process_context("MainProcess", "CoreModule")


    # 测试位置信息
    def test_function():
        main_log.info("This should show function name and line number")


    main_log.info("Application started")
    test_function()


    # 创建子进程
    def worker(module_tag):
        worker_log_configurer(_log_queue)
        worker_log = bind_process_context(module_tag=module_tag)
        worker_log.info(f"Worker in module {module_tag} started")
        time.sleep(0.5)
        worker_log.success("Task completed")


    processes = []
    for i, tag in enumerate(["DataLoader", "AI_Engine", "OutputHandler"]):
        p = Process(target=worker, args=(tag,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    main_log.info("All workers finished")
    _listener.stop()