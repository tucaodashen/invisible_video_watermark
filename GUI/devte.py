import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QEvent, Qt


class ClickToCloseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("点击任意位置关闭窗口")
        self.resize(400, 300)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 设置布局
        layout = QVBoxLayout(central_widget)

        # 添加标签
        label = QLabel("点击窗口任意位置即可关闭")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # 添加一个按钮作为示例
        button = QPushButton("这个按钮不会关闭窗口")
        layout.addWidget(button)

        # 为中央部件安装事件过滤器
        central_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        # 过滤鼠标按下事件
        if event.type() == QEvent.MouseButtonPress:
            self.close()
            return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickToCloseWindow()
    window.show()
    sys.exit(app.exec())