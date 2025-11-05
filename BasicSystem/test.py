# test_logging.py
import time
import threading
from multiprocessing import Pool
from log_client import setup_logger, get_logger


def worker_function(worker_id):
    """工作进程的函数"""
    logger = get_logger(f"Worker-{worker_id}")

    for i in range(3):
        logger.info(f"处理任务 {i}", tags=f"task-{i}")
        logger.debug(f"详细调试信息 {i}", tags="debug")
        time.sleep(0.1)

        if i == 2:
            logger.error(f"模拟错误发生在任务 {i}", tags="error")

    return f"Worker-{worker_id} 完成"


if __name__ == "__main__":
    # 初始化日志系统（UDP启用）
    setup_logger(default_tags="MainProcess", enable_udp=True, enable_console=True)
    main_logger = get_logger()

    main_logger.info("程序启动", tags={"startup":"AAA"})
