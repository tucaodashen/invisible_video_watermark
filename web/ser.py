import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse, unquote


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器，添加简单的路由功能"""

    def do_GET(self):
        """处理GET请求"""
        # 解析URL路径
        parsed_path = urlparse(self.path)
        path = unquote(parsed_path.path)

        # 默认首页
        if path == '/':
            path = '/index.html'

        # 获取文件绝对路径
        file_path = os.path.join(os.getcwd(), 'www', path.lstrip('/'))

        # 检查文件是否存在且可访问
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # 设置响应头
            self.send_response(200)

            # 根据文件扩展名设置Content-Type
            ext = os.path.splitext(file_path)[1]
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.gif': 'image/gif',
                '.ico': 'image/x-icon',
                '.txt': 'text/plain',
                '.json': 'application/json'
            }

            content_type = content_types.get(ext, 'application/octet-stream')
            self.send_header('Content-Type', content_type)
            self.end_headers()

            # 读取并发送文件内容
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            # 文件不存在，返回404错误
            self.send_error(404, "File not found")


def run_server(port=8000, directory='www'):
    """运行Web服务器"""

    # 创建www目录（如果不存在）
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建了 {directory} 目录")

    # 创建默认首页（如果不存在）
    index_file = os.path.join(directory, 'index.html')
    if not os.path.exists(index_file):
        html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>简单Python Web服务器</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>简单Python Web服务器</h1>
    <p>恭喜！你的Python Web服务器正在运行。</p>
    <div class="info">
        <p><strong>服务器信息：</strong></p>
        <p>端口：{port}</p>
        <p>根目录：{directory}</p>
        <p>当前时间：<span id="datetime"></span></p>
    </div>
    <script>
        document.getElementById('datetime').textContent = new Date().toLocaleString();
    </script>
</body>
</html>""".format(port=port, directory=directory)

        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"创建了默认首页 {index_file}")

    # 启动服务器
    with socketserver.TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
        print(f"服务器运行在 http://localhost:{port}")
        print(f"根目录: {os.path.abspath(directory)}")
        print("按 Ctrl+C 停止服务器")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")


if __name__ == "__main__":
    # 获取命令行参数
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("端口号必须是整数，使用默认端口8000")

    # 运行服务器
    run_server(port=port)