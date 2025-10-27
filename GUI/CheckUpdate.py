import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QListWidget,
                               QListWidgetItem, QWidget, QVBoxLayout,
                               QProgressBar, QHBoxLayout, QLabel)
from PySide6.QtCore import Qt


class ProgressListItem(QWidget):
    def __init__(self, text, progress_value=0, parent=None):
        super().__init__(parent)

        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # 添加标签
        self.label = QLabel(text)
        layout.addWidget(self.label)

        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(progress_value)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def get_progress(self):
        return self.progress_bar.value()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("List with Progress Bars")
        self.setGeometry(100, 100, 600, 400)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout(central_widget)

        # 创建列表部件
        self.list_widget = QListWidget()

        # 添加10个带有进度条的项
        for i in range(10):
            item_widget = ProgressListItem(f"Item {i + 1}", (i + 1) * 10)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

        layout.addWidget(self.list_widget)

        # 设置选择右击行的行为（如果您的自定义列表组件支持）
        # 注意：标准QListWidget没有这个功能，您可能需要自定义列表组件
        # self.list_widget.setSelectRightClickedRow(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())