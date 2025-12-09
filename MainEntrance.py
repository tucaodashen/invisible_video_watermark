import multiprocessing
import os
import socket

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
    multiprocessing.freeze_support()
    if not os.path.exists("assets"):
        raise RuntimeError("文件不完整，无法运行")
    if not is_port_available(1165):
        raise RuntimeError("端口1165已被占用，无法运行")
    if not is_port_available(9999):
        raise RuntimeError("端口9999已被占用，无法运行")
    from GUI import Startup_Splash
    Startup_Splash.start()
