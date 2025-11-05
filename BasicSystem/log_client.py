# log_client.py (增强版本)
import socket
import json
import os
import threading
from datetime import datetime
from loguru import logger
import sys


class UDPLogger:
    def __init__(self, host='localhost', port=9999, default_tags='', enable_console=True):
        self.host = host
        self.port = port
        self.default_tags = default_tags
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.enable_udp = True
        self.enable_console = enable_console

        # 配置本地控制台日志（作为备用）
        if enable_console and not logger._core.handlers:
            logger.remove()
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[tags]}</cyan> | <level>{message}</level>",
                level="DEBUG",
                colorize=True
            )

    def _send_udp(self, log_data):
        """通过UDP发送日志"""
        try:
            data = json.dumps(log_data).encode('utf-8')
            self.sock.sendto(data, (self.host, self.port))
            return True
        except Exception as e:
            return False

    def _log_console(self, level, message, tags, extra):
        """在控制台记录日志（备用）"""
        if self.enable_console:
            log_context = logger.bind(tags=tags)
            if level == 'debug':
                log_context.debug(message, **extra)
            elif level == 'info':
                log_context.info(message, **extra)
            elif level == 'warning':
                log_context.warning(message, **extra)
            elif level == 'error':
                log_context.error(message, **extra)
            elif level == 'critical':
                log_context.critical(message, **extra)

    def log(self, message, level='INFO', tags=None, **extra):
        """发送日志消息"""
        final_tags = tags or self.default_tags

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'tags': final_tags,
            'extra': extra,
            'process_id': os.getpid(),
            'thread_id': threading.current_thread().ident
        }

        # 尝试通过UDP发送，失败则使用控制台
        udp_success = self._send_udp(log_data) if self.enable_udp else False

        # 如果UDP发送失败或禁用了UDP，使用控制台输出
        if not udp_success or not self.enable_udp:
            self._log_console(level, message, final_tags, extra)

    def debug(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'DEBUG', tags, **extra)

    def info(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'INFO', tags, **extra)

    def warning(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'WARNING', tags, **extra)

    def error(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'ERROR', tags, **extra)

    def critical(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'CRITICAL', tags, **extra)

    def success(self, message, tags=None, **extra):
        if len(message) >= 3000:
            message = message[:2997] + '...'
        self.log(message, 'SUCCESS', tags, **extra)


# 全局日志客户端实例
_logger = None


def setup_logger(host='localhost', port=9999, default_tags='', enable_udp=True, enable_console=True):
    """设置全局日志器"""
    global _logger
    _logger = UDPLogger(host, port, default_tags, enable_console)
    _logger.enable_udp = enable_udp
    return _logger


def get_logger(tags=''):
    """获取日志器实例"""
    global _logger
    if _logger is None:
        # 如果没有初始化，创建一个本地日志器
        _logger = UDPLogger(enable_udp=False, enable_console=True)

    if tags:
        # 返回带有特定标签的新实例
        new_logger = UDPLogger(
            _logger.host,
            _logger.port,
            tags,
            _logger.enable_console
        )
        new_logger.enable_udp = _logger.enable_udp
        return new_logger
    return _logger