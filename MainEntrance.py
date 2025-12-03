import multiprocessing
import os
import socket

def is_port_in_use(port: int, host: str = 'localhost') -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # 设置连接超时时间
        try:
            # 尝试连接指定端口
            result = s.connect_ex((host, port))
            # 如果连接成功（返回0），则端口被占用
            return result == 0
        except socket.gaierror:
            # 主机名解析失败
            return False
        except Exception:
            # 其他异常情况
            return False

if __name__ == "__main__":
    multiprocessing.freeze_support()
    if not os.path.exists("assets"):
        raise RuntimeError("文件不完整，无法运行")
    if is_port_in_use(1165):
        raise RuntimeError("端口1165已被占用，无法运行")
    if is_port_in_use(9999):
        raise RuntimeError("端口9999已被占用，无法运行")
    from GUI import main
    main.start()