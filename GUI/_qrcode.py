import psutil

def find_process_using_port(port):
    """查找使用指定端口的进程"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                process = psutil.Process(conn.pid)
                return {
                    'pid': conn.pid,
                    'name': process.name(),
                    'status': process.status(),
                    'port': port
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    return None

# 使用示例
port = 1165  # 替换为你想检查的端口
result = find_process_using_port(port)
if result:
    print(f"端口 {port} 被以下进程占用：")
    print(f"PID: {result['pid']}")
    print(f"进程名: {result['name']}")
    print(f"状态: {result['status']}")
else:
    print(f"端口 {port} 未被占用")