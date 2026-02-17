import multiprocessing
import os
import socket
import sys

import psutil


def check_process_running(process_name):
    """
    检查是否有匹配名称的进程在运行
    """
    # 遍历当前所有运行的进程
    for proc in psutil.process_iter(['name']):
        try:
            # 检查进程名是否匹配（忽略大小写）
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 忽略在遍历过程中可能已经消失或无权访问的进程
            pass
    return False


def is_port_available(port: int, host: str = '0.0.0.0') -> bool:
    """检查端口是否可用（未被占用）"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False
        except Exception:
            return False

if __name__ == "__main__":
    process_images = []
    for i in sys.argv:
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith(".webp"):
            process_images.append(i)
    if len(process_images) != 0:
        if check_process_running("LogServer.exe") or check_process_running("IVW_Nano.exe"):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if not is_port_available(10492):
                raise RuntimeError("端口10492已被占用，无法运行")
            target_addr = ('127.0.0.1', 10492)
            for message in process_images:
                for aaa in range(5): # 防止因未启动导致的丢失
                    client_socket.sendto(message.encode('utf-8'), target_addr)
            exit()
        else:
            pass # 启动图片处理窗口
    else:
        if check_process_running("LogServer.exe") or check_process_running("IVW_Nano.exe"):
            print("已在运行，无法重复启动")
            exit()
        multiprocessing.freeze_support()
        if not os.path.exists("assets"):
            raise RuntimeError("文件不完整，无法运行")
        if not is_port_available(1165):
            raise RuntimeError("端口1165已被占用，无法运行")
        if not is_port_available(9999):
            raise RuntimeError("端口9999已被占用，无法运行")
        from GUI import Startup_Splash
        Startup_Splash.start()
