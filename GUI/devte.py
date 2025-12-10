import sys
import os
import re  # 导入正则表达式库
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QTextEdit
)
from PySide6.QtCore import QTimer, Qt


class ColorLogViewer(QMainWindow):
    # --- 1. 定义颜色映射 ---
    COLOR_MAP = {
        "CRITICAL": "#8B0000",  # 深红
        "ERROR": "#FF0000",  # 亮红
        "WARNING": "#FFA500",  # 橙色
        "INFO": "#0000FF",  # 蓝色
        "DEBUG": "#A9A9A9",  # 深灰
        "SUCCESS": "#008000"  # 绿色
    }

    # 匹配日志等级的正则表达式 (匹配方括号中的大写单词)
    # 例如：[INFO] 或 [ERROR]
    LOG_LEVEL_PATTERN = re.compile(r'\[(CRITICAL|ERROR|WARNING|INFO|DEBUG|SUCCESS)\]')

    def __init__(self, log_file_path):
        super().__init__()
        self.setWindowTitle("PySide6 实时日志浏览器 (彩色)")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 使用 QPlainTextEdit，但通过 QTextCursor/HTML 插入内容
        self.log_display = QPlainTextEdit()
        self.log_display.setReadOnly(True)
        from PySide6.QtGui import QTextOption
        self.log_display.setWordWrapMode(QTextOption.NoWrap)
        layout.addWidget(self.log_display)

        self.log_file_path = log_file_path
        self.file_handle = None
        self.current_position = 0

        if self._initialize_file_handle():
            self._setup_timer()
            # 加载历史日志时也使用颜色
            self.load_initial_log()
        else:
            self.log_display.setPlainText(f"错误: 无法打开日志文件: {log_file_path}")

    # --- 2. 颜色解析函数 ---
    def _get_log_color(self, log_line: str) -> str:
        """根据日志行内容，查找日志等级并返回对应的十六进制颜色代码"""
        match = self.LOG_LEVEL_PATTERN.search(log_line.upper())

        if match:
            level = match.group(1)  # 获取匹配到的等级，如 "INFO"
            return self.COLOR_MAP.get(level, "#000000")  # 默认黑色

        return "#000000"  # 找不到等级，返回黑色

    # --- 3. 修改加载函数，使用颜色 ---
    def load_initial_log(self):
        """加载已存在的全部历史日志，并着色"""
        if self.file_handle:
            self.file_handle.seek(0)
            log_content = self.file_handle.read()

            # 清空并重新着色插入全部日志
            self.log_display.clear()
            for line in log_content.splitlines():
                self._insert_colored_line(line)

            self.file_handle.seek(0, os.SEEK_END)
            self.current_position = self.file_handle.tell()
            self.log_display.verticalScrollBar().setValue(
                self.log_display.verticalScrollBar().maximum()
            )

    def _insert_colored_line(self, line: str):
        """将单行日志格式化为 HTML 并插入到 QTextEdit"""
        color = self._get_log_color(line)
        # 使用 HTML 格式包裹日志行，并添加换行符 <br>
        html_line = f'<span style="color:{color};">{line}</span><br>'

        # 移动光标到文档末尾
        cursor = self.log_display.textCursor()
        cursor.movePosition(cursor.End)
        self.log_display.setTextCursor(cursor)

        # 插入 HTML
        self.log_display.insertHtml(html_line)

    # --- 4. 修改实时检查函数 ---
    def check_for_new_logs(self):
        """检查日志文件是否有新内容，并使用颜色显示"""
        if not self.file_handle:
            return

        try:
            current_file_size = os.path.getsize(self.log_file_path)

            if current_file_size > self.current_position:
                self.file_handle.seek(self.current_position)
                new_logs = self.file_handle.read()

                # 按行处理新日志，并着色
                for line in new_logs.splitlines():
                    if line:  # 避免处理空行
                        self._insert_colored_line(line)

                self.current_position = self.file_handle.tell()

                # 自动滚动到最新日志（底部）
                self.log_display.verticalScrollBar().setValue(
                    self.log_display.verticalScrollBar().maximum()
                )

            elif current_file_size < self.current_position:
                # 处理文件重置
                print("日志文件已被重置，从头开始重新加载...")
                # 重新初始化文件句柄和加载
                self.file_handle.close()
                self._initialize_file_handle()
                self.load_initial_log()

        except Exception as e:
            print(f"读取日志文件时发生错误: {e}")

    # 保持其他辅助方法不变
    def _initialize_file_handle(self):
        # ... (保持不变) ...
        try:
            self.file_handle = open(self.log_file_path, 'r', encoding='utf-8')
            self.file_handle.seek(0, os.SEEK_END)
            self.current_position = self.file_handle.tell()
            return True
        except Exception as e:
            return False

    def _setup_timer(self):
        # ... (保持不变) ...
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_new_logs)
        self.timer.start(500)

    def closeEvent(self, event):
        # ... (保持不变) ...
        if self.file_handle:
            self.file_handle.close()
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()


if __name__ == "__main__":
    LOG_FILE = "color_app.log"

    if not os.path.exists(LOG_FILE):
        print(f"创建测试日志文件: {LOG_FILE}")
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("2025-12-09 23:00:00 [INFO] 日志浏览器启动\n")
            f.write("2025-12-09 23:00:01 [CRITICAL] 核心服务故障！\n")

    app = QApplication(sys.argv)
    viewer = ColorLogViewer(LOG_FILE)
    viewer.show()
    sys.exit(app.exec())