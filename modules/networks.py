import time
import socket
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="networks", enable_udp=True, enable_console=True)
logger = get_logger()



"""
IPC
"""
def ipc_send(message,host,port):
    """
        发送UDP消息到指定主机和端口

        参数:
            host (str): 目标主机地址
            port (int): 目标端口号
            message (bytes/str): 要发送的消息（字符串将自动编码为UTF-8）
        """
    # 创建UDP套接字
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # 如果消息是字符串，则编码为字节
        if isinstance(message, str):
            message = message.encode('utf-8')

        # 发送消息
        sock.sendto(message, (host, port))
        # print(f"Sent {len(message)} bytes to {host}:{port}")


def ipc_recv(host,port,callback,buffer_size=1024):
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
        # print(f"UDP receiver started on {host}:{port}")

        while True:
            try:
                data, addr = sock.recvfrom(buffer_size)
                callback(data.decode('utf-8'), addr)
                if data.decode('utf-8') == "exit":
                    logger.info("exit signal received",tags="networks:ipc_recv")
                    break
            except OSError as e:
                logger.error(f"Error: {e}",tags="networks:ipc_recv")
                break

