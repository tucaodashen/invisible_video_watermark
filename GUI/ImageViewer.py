import os
import sys
from PySide6.QtWidgets import (QApplication, QFrame, QAbstractItemView,
                               QHeaderView, QTableWidgetItem, QStyledItemDelegate,QFileDialog)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontMetrics
from GUI.image import Ui_ImageProcessWindow
from qfluentwidgets import Theme, setTheme
from gettext import gettext as _


def display_image_file_select_window():
    """
    显示图像文件选择窗口。
    """
    # 显示文件选择对话框
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFiles)
    file_dialog.setNameFilter(_("图像文件 (*.png *.jpg *.jpeg)"))
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        return selected_files
    return None


class ElideDelegate(QStyledItemDelegate):
    """自定义委托，用于显示省略号"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 获取文本
        text = index.data(Qt.DisplayRole)
        if not text:
            return

        # 计算省略后的文本
        fm = QFontMetrics(option.font)
        elided_text = fm.elidedText(text, Qt.ElideRight, option.rect.width() - 10)

        # 绘制文本
        option.text = elided_text
        super().paint(painter, option, index)


class ImageProcessWindow(QFrame, Ui_ImageProcessWindow):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.files = files
        self.ControlFrame.setMaximumWidth(612)
        self.frame.setMinimumHeight(200)
        self.ProcessLog.hide()
        self.FileList.setColumnCount(2)
        self.FileList.setHorizontalHeaderLabels([_("文件名"), _("路径")])
        self.FileList.currentItemChanged.connect(self.set_correct_image)
        self.radioButton.setChecked(True)
        self.AddImage.setText("+")
        self.DeleteImage.setText("-")
        self.AddImage.clicked.connect(self.select_new)
        self.DeleteImage.clicked.connect(self.delete_select)


        # 设置列宽
        self.setupTableColumns()

        # 设为不可编辑
        self.FileList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 添加数据
        self.add_files_to_table()


    def select_new(self):
        selected_files = display_image_file_select_window()
        if selected_files:
            for file in selected_files:
                self.add_new_files_to_table(file)
                self.files.append(file)

    def delete_select(self):
        # 1. 获取所有选中单元格对应的行索引
        # 使用 set 去重，防止一行中有多个单元格被选中导致重复计算
        selected_indices = {item.row() for item in self.FileList.selectedItems()}

        if not selected_indices:
            #默认选择第一行
            self.FileList.setCurrentCell(0, 0)
            selected_indices = {item.row() for item in self.FileList.selectedItems()}


        # 2. 关键：将行索引按从大到小排序
        # 必须先删后面的行，这样前面行的索引才不会变
        rows_to_delete = sorted(list(selected_indices), reverse=True)

        for row in rows_to_delete:
            # 3. 先删 UI 界面上的行
            self.FileList.removeRow(row)

            # 4. 再删数据列表中的对应项
            # 因为是倒序删除，所以这里的 row 依然对应 self.files 的正确位置
            if 0 <= row < len(self.files):
                del self.files[row]



    def add_new_files_to_table(self,path):
        filename = os.path.basename(path)
        row_position = self.FileList.rowCount()
        self.FileList.insertRow(row_position)
        filename_item = QTableWidgetItem(filename)
        filename_item.setToolTip(filename)  # 鼠标悬停显示完整文件名
        self.FileList.setItem(row_position, 0, filename_item)
        path_item = QTableWidgetItem(path)
        path_item.setToolTip(path)  # 鼠标悬停显示完整路径
        path_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.FileList.setItem(row_position, 1, path_item)
        self.adjust_column_widths()
        self.FileList.resizeRowsToContents()


    def set_correct_image(self):
        cur_image = self.FileList.currentRow()
        if cur_image >= 0:
            self.ImageView.setImage(self.files[cur_image])
            print(self.files[cur_image])


    def setupTableColumns(self):
        """设置表格列宽策略"""
        header = self.FileList.horizontalHeader()

        # 设置列宽模式
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 文件名列
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # 路径列可交互

        # 设置初始列宽
        self.FileList.setColumnWidth(0, 200)  # 文件名列初始宽度
        self.FileList.setColumnWidth(1, 400)  # 路径列初始宽度

        # 设置最小列宽
        header.setMinimumSectionSize(100)

        # 设置表头可排序
        self.FileList.setSortingEnabled(True)

        # 设置行高
        self.FileList.verticalHeader().setDefaultSectionSize(30)

    def add_files_to_table(self):
        """添加文件到表格"""
        for file in self.files:
            # 获取文件名
            filename = file.split("\\")[-1]

            # 添加行
            row_position = self.FileList.rowCount()
            self.FileList.insertRow(row_position)

            # 设置文件名
            filename_item = QTableWidgetItem(filename)
            filename_item.setToolTip(filename)  # 鼠标悬停显示完整文件名
            self.FileList.setItem(row_position, 0, filename_item)

            # 设置路径
            path_item = QTableWidgetItem(file)
            path_item.setToolTip(file)  # 鼠标悬停显示完整路径
            path_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.FileList.setItem(row_position, 1, path_item)

        # 调整列宽
        self.adjust_column_widths()

        # 调整行高
        self.FileList.resizeRowsToContents()

    def adjust_column_widths(self):
        """根据内容调整列宽"""
        # 先调整文件名列
        self.FileList.resizeColumnToContents(0)

        # 确保文件名列有合理的最小和最大宽度
        filename_width = self.FileList.columnWidth(0)
        if filename_width < 150:
            self.FileList.setColumnWidth(0, 150)
        elif filename_width > 300:
            self.FileList.setColumnWidth(0, 300)

        # 计算表格可用宽度
        table_width = self.FileList.width()

        # 计算路径列的宽度（表格宽度减去文件名列宽度减去边框等）
        path_width = table_width - self.FileList.columnWidth(0) - 25

        # 确保路径列有最小宽度
        if path_width < 200:
            path_width = 200

        self.FileList.setColumnWidth(1, path_width)

    def resizeEvent(self, event):
        """窗口大小变化时调整列宽"""
        super().resizeEvent(event)
        self.adjust_column_widths()


if __name__ == "__main__":
    setTheme(Theme.AUTO)
    app = QApplication(sys.argv)
    lists = os.listdir(r"D:\mangatranslation\General\Alice\ORIGIN")
    w = ImageProcessWindow([os.path.join(r"D:\mangatranslation\General\Alice\ORIGIN", file) for file in lists])
    w.show()
    sys.exit(app.exec())