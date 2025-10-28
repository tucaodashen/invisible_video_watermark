# structured_logger.py
import os
import time
import uuid
import multiprocessing
import sys
import inspect
from loguru import logger as global_logger

# 全局日志系统实例
_global_log_system = None


def init_global_log_system(log_system_instance):
    """初始化全局日志系统"""
    global _global_log_system
    _global_log_system = log_system_instance


def get_module_logger(module_name=None):
    """
    获取模块日志记录器（用于松散模块）

    :param module_name: 模块名称，如果为None则自动检测
    :return: 配置好的日志记录器
    """
    global _global_log_system

    if _global_log_system is None:
        # 如果全局日志系统未初始化，创建后备日志记录器
        from loguru import logger
        return logger

    if module_name is None:
        # 自动获取调用者模块名
        import inspect
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__ if module else "unknown"

    return _global_log_system.get_module_logger(module_name)


class StructuredLogger:
    def __init__(self, project_name, base_dir="./logs", console_level="INFO"):
        """
        初始化结构化日志系统

        :param project_name: 项目名称
        :param base_dir: 日志基础目录，默认为"./logs"
        :param console_level: 控制台日志级别，默认为"INFO"
        """
        self.project_name = project_name
        self.execution_id = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.base_path = os.path.join(base_dir, f"{project_name}_{self.execution_id}")
        self.subprocess_dir = os.path.join(self.base_path, "subprocess_logs")
        self.modules_dir = os.path.join(self.base_path, "module_logs")
        self.console_level = console_level

        # 创建目录结构
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.subprocess_dir, exist_ok=True)
        os.makedirs(self.modules_dir, exist_ok=True)

        # 配置主进程日志
        self.main_log_path = os.path.join(self.base_path, "main_process.log")
        self._configure_main_logger()

        # 存储日志信息
        self.log_info = {
            "project_name": project_name,
            "execution_id": self.execution_id,
            "base_path": self.base_path,
            "main_log": self.main_log_path,
            "subprocess_logs": {},
            "module_logs": {}
        }

        # 提供全局日志记录器
        self.logger = global_logger

        # 缓存模块日志记录器
        self.module_loggers = {}

        # 记录初始化信息
        self.logger.info(f"Structured logger initialized for project: {project_name}")
        self.logger.info(f"Execution ID: {self.execution_id}")
        self.logger.info(f"Log base path: {self.base_path}")

        # 设置全局日志系统
        init_global_log_system(self)

    def _configure_main_logger(self):
        """配置主进程日志记录器"""
        global_logger.remove()  # 移除默认配置

        # 主日志格式 - 使用Loguru内置的字段
        main_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        # 文件日志
        global_logger.add(
            self.main_log_path,
            level="DEBUG",
            format=main_format,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

        # 控制台输出
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        global_logger.add(
            sys.stdout,
            level=self.console_level,
            format=console_format
        )

    def get_subprocess_logger(self, process_name):
        """
        为子进程创建独立的日志记录器

        :param process_name: 子进程名称
        :return: 配置好的日志记录器
        """
        process_id = multiprocessing.current_process().name.split("-")[-1]
        log_filename = f"{process_name}_{process_id}.log"
        log_path = os.path.join(self.subprocess_dir, log_filename)

        # 创建全新的日志记录器实例
        sub_logger = global_logger.bind(process_name=process_name)

        # 移除可能存在的默认处理器
        sub_logger.remove()

        # 子进程日志格式 - 使用Loguru内置的字段
        sub_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<magenta>Process: {extra[process_name]}</magenta> | "
            "<level>{message}</level>"
        )

        # 文件日志
        sub_logger.add(
            log_path,
            level="DEBUG",
            format=sub_format,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

        # 控制台输出
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<magenta>Process: {extra[process_name]}</magenta> | "
            "<level>{message}</level>"
        )

        sub_logger.add(
            sys.stdout,
            level=self.console_level,
            format=console_format
        )

        # 存储日志信息
        self.log_info["subprocess_logs"][process_name] = log_path
        return sub_logger

    def get_module_logger(self, module_name):
        """
        为松散模块创建独立的日志记录器

        :param module_name: 模块名称
        :return: 配置好的日志记录器
        """
        # 如果已经创建过，直接返回缓存的记录器
        if module_name in self.module_loggers:
            return self.module_loggers[module_name]

        log_filename = f"{module_name}.log"
        log_path = os.path.join(self.modules_dir, log_filename)

        # 创建全新的日志记录器实例
        module_logger = global_logger.bind(module_name=module_name)

        # 移除可能存在的默认处理器
        module_logger.remove()

        # 模块日志格式 - 使用Loguru内置的字段
        module_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        # 文件日志
        module_logger.add(
            log_path,
            level="DEBUG",
            format=module_format,
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

        # 控制台输出
        console_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        module_logger.add(
            sys.stdout,
            level=self.console_level,
            format=console_format
        )

        # 存储日志信息
        self.log_info["module_logs"][module_name] = log_path
        self.module_loggers[module_name] = module_logger
        return module_logger

    def get_execution_info(self):
        """获取日志执行信息"""
        return self.log_info

    def __getstate__(self):
        """序列化时排除不可pickle的对象"""
        state = self.__dict__.copy()
        # 移除不可pickle的对象
        state.pop('logger', None)
        state.pop('module_loggers', None)
        return state

    def __setstate__(self, state):
        """反序列化时重新初始化"""
        self.__dict__.update(state)
        # 重新初始化必要的属性
        self.logger = global_logger
        self.module_loggers = {}