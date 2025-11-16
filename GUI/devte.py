import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QTableWidgetItem, QProgressBar, QLabel, QVBoxLayout, QWidget)
from qfluentwidgets import TableWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建表格
        self.table_widget = TableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["索引", "名称", "状态", "缩略图", "进度条", "开始时间"])

        # 添加示例数据
        self.add_table_row(1, "任务1", "运行中", "thumbnail1.png", 75)
        self.add_table_row(2, "任务2", "等待", "thumbnail2.png", 30)
        self.add_table_row(3, "任务3", "完成", "thumbnail3.png", 100)

        self.setCentralWidget(self.table_widget)
        self.resize(800, 400)

    def add_table_row(self, index, name, status, thumbnail_path, progress):
        # 获取当前行数并插入新行
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)

        # 1. 索引 (int)
        index_item = QTableWidgetItem(str(index))
        index_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 0, index_item)

        # 2. 名称 (str)
        name_item = QTableWidgetItem(name)
        self.table_widget.setItem(row, 1, name_item)

        # 3. 状态 (str)
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 2, status_item)

        # 4. 缩略图 (QLabel)
        thumbnail_label = QLabel()
        pixmap = QPixmap(thumbnail_path)
        if not pixmap.isNull():
            # 缩放缩略图到合适大小
            thumbnail_label.setPixmap(pixmap.scaled(60, 40, Qt.KeepAspectRatio))
        else:
            thumbnail_label.setText("无图片")
        thumbnail_label.setAlignment(Qt.AlignCenter)
        self.table_widget.setCellWidget(row, 3, thumbnail_label)

        # 5. 进度条 (QProgressBar)
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setAlignment(Qt.AlignCenter)
        self.table_widget.setCellWidget(row, 4, progress_bar)

        # 6. 开始时间 (str)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_item = QTableWidgetItem(time_str)
        self.table_widget.setItem(row, 5, time_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())