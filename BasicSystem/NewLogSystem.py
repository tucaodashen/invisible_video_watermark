import os
import time
import uuid
import logging
from loguru import logger
from multiprocessing import current_process
from typing import Dict, Any, Optional, Union
from uuid import UUID

# 定义类型别名
ProcessTraceType = Dict[str, Optional[Union[UUID, str]]]
LogConfigType = Dict[str, Optional[Union[str, UUID, ProcessTraceType]]]

# 全局配置字典（每个进程独立）
_log_config: LogConfigType = {
    "project_name": None,
    "project_uuid": None,
    "process_trace": {
        "process_uuid": None,
        "process_name": None
    }
}

# 已初始化标记（防止重复初始化）
_initialized: bool = False


def configure_logger(
        project_name: str,
        is_main_process: bool = False,
        process_name: Optional[str] = None
) -> None:
    """配置日志系统

    Args:
        project_name: 项目名称（必填）
        is_main_process: 是否主进程（默认False）
        process_name: 进程名称（子进程必填）
    """
    global _initialized, _log_config

    # 确保只初始化一次（进程内）
    if _initialized:
        return

    # 创建日志目录
    os.makedirs("./logs", exist_ok=True)

    # 配置项目信息
    _log_config["project_name"] = project_name
    _log_config["project_uuid"] = uuid.uuid4()

    # 配置进程信息
    proc = current_process()
    if is_main_process:
        process_name = "main"
    elif not process_name:
        process_name = f"child-{proc.pid}"

    # 类型注解确保类型一致性
    process_trace: ProcessTraceType = {
        "process_uuid": uuid.uuid4(),
        "process_name": process_name
    }
    _log_config["process_trace"] = process_trace

    # 生成日志文件名
    timestamp = time.strftime("%Y-%m-%d-%H%M%S")
    if is_main_process:
        log_name = f"main_{timestamp}.log"
    else:
        log_name = f"{process_name}_{timestamp}_{proc.pid}.log"

    # 添加日志处理器
    log_path = f"./logs/{log_name}"

    # 使用类型断言确保值不为None
    project_name_val = str(_log_config["project_name"])
    process_name_val = str(_log_config["process_trace"]["process_name"])  # type: ignore

    logger.add(
        log_path,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               f"Project:{project_name_val} | "
               f"Process:{process_name_val} | "
               "{message}"
    )

    _initialized = True
    logger.info(f"Logger initialized for process: {process_name}")


# 示例使用方式
if __name__ == "__main__":
    # 主进程配置
    configure_logger("MyProject", is_main_process=True)
    logger.info("Main process started")


    # 子进程示例
    def child_task():
        configure_logger("MyProject", process_name="worker")
        logger.info("Child process task executed")


    child_task()