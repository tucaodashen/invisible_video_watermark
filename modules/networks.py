import time

import requests
import socket
import cv2
import zmq
import numpy as np
import pickle
import zlib



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
                    break
            except OSError as e:
                print(f"Receiver error: {e}")
                break

def send_image(image):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)  # 发布者
    socket.bind("tcp://*:5555")
    for i in image:
        compressed = zlib.compress(pickle.dumps(i))
        socket.send(compressed)


def receive_image(timeout_seconds=5,cb=None):
    """
    接收图像，如果超过指定时间没有收到新图像则停止接收

    Args:
        timeout_seconds: 超时时间（秒），默认5秒

    Returns:
        list: 接收到的图像列表
    """
    img_list = []
    context = zmq.Context()
    socket = context.socket(zmq.SUB)  # 订阅者
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    # 设置非阻塞模式，以便检查超时
    socket.setsockopt(zmq.RCVTIMEO, 100)  # 100毫秒接收超时

    last_receive_time = time.time()

    while True:
        try:
            compressed = socket.recv()

            # 成功接收到数据，更新最后接收时间
            last_receive_time = time.time()

            # 解压和反序列化
            frame = pickle.loads(zlib.decompress(compressed))
            img_list.append(frame)

            print(f"成功接收第 {len(img_list)} 张图像")

        except zmq.Again:
            # 接收超时，检查是否总体超时
            current_time = time.time()
            if current_time - last_receive_time > timeout_seconds:
                print(f"超过 {timeout_seconds} 秒未收到新图像，停止接收")
                break
            # 否则继续等待
            continue

        except Exception as e:
            print(f"接收图像时发生错误: {e}")
            break

    # 清理资源
    socket.close()
    context.term()
    if cb is not None:
        cb(img_list)

    return img_list
