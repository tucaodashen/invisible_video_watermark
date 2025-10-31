import socket
import loguru
import threading
import json
from loguru import logger
import sys




def setup_logger_simple(default_tags=None, log_file="app.json.log"):
    """使用Loguru内置的序列化功能"""

    # 移除默认配置
    logger.remove()

    # 控制台处理器 - 文本格式
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level> | {extra}",
        level="DEBUG",
        colorize=True
    )

    # 文件处理器 - 使用serialize=True让Loguru自动处理JSON序列化
    logger.add(
        log_file,
        format="{extra} {message}",
        level="DEBUG",
        serialize=True,  # 关键：让Loguru自动序列化为JSON
        rotation="10 MB",
        encoding="utf-8"
    )

    # 如果有默认标签，绑定到logger
    if default_tags:
        logger.configure(extra=default_tags)

    return logger

class NetworkLogSystem:
    def __init__(self, port, path):
        self._thread = None
        self._runed = None
        self.port = port
        self.path = path
        self._running = True
        self._logger = None


        log_template = {
            "level": "INFO",
            "content":"",
            "tags":[]
        }

    def set_logger(self, path,default_tags=None):
        self._logger = setup_logger_simple(
            default_tags=default_tags,
            log_file=path
        )

    def log_callback(self, message, addr):
        cur_data = json.loads(message)
        if cur_data['level'] == 'CRITICAL':
            self._logger.critical(cur_data['content'], extra=cur_data['tags'])
        elif cur_data['level'] == 'ERROR':
            self._logger.error(cur_data['content'], extra=cur_data['tags'])
        elif cur_data['level'] == 'WARNING':
            self._logger.warning(cur_data['content'], extra=cur_data['tags'])
        elif cur_data['level'] == 'INFO':
            self._logger.info(cur_data['content'], extra=cur_data['tags'])
        elif cur_data['level'] == 'DEBUG':
            self._logger.debug(cur_data['content'], extra=cur_data['tags'])

    def stop(self):
        self._running = False



    def start(self):
        self._thread = threading.Thread(target=self.ipc_recv, args=("0.0.0.0", self.port, self.log_callback))
        if not self._runed:
            self._thread.start()
            self._thread.join()



    def ipc_recv(self,host,port,callback, buffer_size=81920):
        """
            启动UDP接收服务，持续接收消息并传递给回调函数

            参数:
                host (str): 绑定主机地址（如"0.0.0.0"）
                port (int): 绑定端口号
                callback (function): 消息处理回调函数，格式应为 callback(data, addr)
                buffer_size (int): 接收缓冲区大小（字节）
            """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((host, port))
            print(f"UDP receiver started on {host}:{port}")

            while self._running:
                try:
                    self._runed = True
                    data, addr = sock.recvfrom(buffer_size)
                    callback(data.decode('utf-8'), addr)
                except OSError as e:
                    print(f"Receiver error: {e}")
                    break
                if not self._running:
                    break









