import os.path
import socket
import json
import sys
from datetime import datetime
from threading import Thread
from loguru import logger
from pathlib import Path


class LogServer:
    def __init__(self, host='localhost', port=9999, log_dir='logs'):
        self.host = host
        self.port = port
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # 为每次运行创建唯一的日志文件
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"app_{self.session_id}.log"

        self.setup_logger()
        self.running = False

    def setup_logger(self):
        """配置loguru日志器"""
        logger.remove()  # 移除默认配置

        # 添加控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[tags]}</cyan> | <level>{message}</level>",
            level="DEBUG",
            enqueue=True,
            colorize=True
        )

        # 添加文件处理器
        logger.add(
            self.log_file,
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[tags]} | {message}",
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

    def handle_log_message(self, data, addr):
        """处理接收到的日志消息"""
        try:
            log_data = json.loads(data.decode('utf-8'))

            # 提取日志信息
            level = log_data.get('level', 'INFO').lower()
            message = log_data.get('message', '')
            tags = log_data.get('tags', '')
            extra_data = log_data.get('extra', {})

            # 创建带有标签的日志上下文
            log_context = logger.bind(tags=tags)

            # 根据日志级别记录
            if level == 'debug':
                log_context.debug(message, **extra_data)
            elif level == 'info':
                log_context.info(message, **extra_data)
            elif level == 'warning':
                log_context.warning(message, **extra_data)
            elif level == 'error':
                log_context.error(message, **extra_data)
            elif level == 'critical':
                log_context.critical(message, **extra_data)
            elif level == 'success':
                log_context.success(message, **extra_data)
            else:
                log_context.info(message, **extra_data)

        except Exception as e:
            print(f"日志处理错误: {e}")
            print(f"原始数据: {data}")

    def start_server(self):
        """启动日志服务器"""
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))

        print(f"日志服务器启动在 {self.host}:{self.port}")
        print(f"日志文件: {self.log_file}")

        try:
            while self.running:
                data, addr = sock.recvfrom(10240)
                Thread(target=self.handle_log_message, args=(data, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\n正在停止日志服务器...")
        finally:
            sock.close()

    def stop_server(self):
        self.running = False


if __name__ == "__main__":
    server = LogServer()
    if not os.path.exists("identify_session.txt"):
        with open("identify_session.txt", "w") as f:
            f.write(server.session_id)
    else:
        os.remove("identify_session.txt")
        with open("identify_session.txt", "w") as f:
            f.write(server.session_id)
    server.start_server()