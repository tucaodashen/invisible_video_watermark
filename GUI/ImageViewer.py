import os
import random
import sys
import threading

import cv2
import numpy as np
from PySide6.QtWidgets import (QApplication, QFrame, QAbstractItemView,
                               QHeaderView, QTableWidgetItem, QStyledItemDelegate,QFileDialog)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontMetrics, QFont

from BasicSystem import const
from GUI.image import Ui_ImageProcessWindow
from qfluentwidgets import Theme, setTheme, TransparentPushButton, InfoBarIcon, Flyout, qconfig
from gettext import gettext as _

from modules.ImageProcessUnit import ImageProcessUnit


def setGlobalFont(families):
    # 1. 修改核心配置中的字体列表
    qconfig.set(qconfig.fontFamilies, families)
    # 2. 强制应用并保存（确保下次启动生效）
    qconfig.save()



def showFlyout(self, target, title, icon, content):
    Flyout.create(
        icon=icon,
        title=title,
        content=content, # 确保这里接收的是字符串 "请检查图片路径是否正确"
        target=target,
        parent=self,
        isClosable=True
    )

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
        super().__init__(parent, Qt.Window)
        self.output_method = None
        self.unit = None
        self.quality = None
        self.ext = None
        self.prefix = None
        self.output_path = None
        self.attachment_data = None
        self.watermark_method = None
        self.worker_thread = None
        self.content = None
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
        self.brow = TransparentPushButton()
        self.horizontalLayout_2.addWidget(self.brow)
        self.error_report_call_back = None


        # 设置列宽
        self.setupTableColumns()

        # 设为不可编辑
        self.FileList.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 添加数据
        self.add_files_to_table()
        self.set_text()
        self.add_bind()
        self.set_correct_choice_for_different_agori()

    def set_text(self):
        self.label.setText(_("文件列表"))
        self.groupBox.setTitle(_("水印算法"))
        self.groupBox_2.setTitle(_("水印参数"))
        self.groupBox_3.setTitle(_("转化设置"))
        self.label_3.setText(_("水印内容"))
        self.label_8.setText(_("输出格式"))
        self.label_11.setText(_("输出方式"))
        self.label_9.setText(_("输出路径"))
        self.label_10.setText(_("文件前缀"))
        self.pushButton_3.setText(_("浏览"))
        self.StartButton.setText(_("开始处理"))
        self.brow.setText(_("浏览"))
        self.comboBox.addItem(_("PNG"),userData="png")
        self.comboBox.addItem(_("JPEG"),userData="jpeg")
        self.comboBox.addItem(_("WEBP"),userData="webp")
        self.comboBox.addItem(_("AVIF"),userData="avif")
        self.pushButton_3.setText(_("浏览"))
        self.comboBox_2.addItem(_("嵌入式EXIF"),userData="exif")
        self.comboBox_2.addItem(_("外部JSON"),userData="json")


    def add_bind(self):
        self.radioButton.toggled.connect(self.set_correct_choice_for_different_agori)
        self.radioButton_2.toggled.connect(self.set_correct_choice_for_different_agori)
        self.radioButton_3.toggled.connect(self.set_correct_choice_for_different_agori)
        self.radioButton_4.toggled.connect(self.set_correct_choice_for_different_agori)
        self.StartButton.clicked.connect(self.run)
        self.brow.clicked.connect(self.select_image)
        self.pushButton_3.clicked.connect(self.select_output_path)


    def select_output_path(self):
        output_path = QFileDialog.getExistingDirectory(self, _("选择输出路径"))
        if output_path:
            self.lineEdit_6.setText(output_path)





    def set_correct_choice_for_different_agori(self):
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.lineEdit_4.show()
        self.lineEdit_5.show()
        self.lineEdit_3.show()
        self.lineEdit_2.show()
        self.brow.hide()
        self.label_4.setToolTip(_("在水印提取时使用，建议为9999以下的数字"))
        self.label_5.setToolTip(_("在水印提取时使用，建议为9999以下的数字"))
        self.lineEdit_2.setToolTip(_("例如 “1,9999”即为在1到9999之间取随机数"))
        self.lineEdit_3.setToolTip(_("例如 “1,9999”即为在1到9999之间取随机数"))
        self.lineEdit_2.setPlaceholderText(_("输入以半角逗号分割的数字以在范围内取随机数"))
        self.lineEdit_3.setPlaceholderText(_("输入以半角逗号分割的数字以在范围内取随机数"))
        self.lineEdit.setPlaceholderText(_("请输入嵌入文本"))
        if self.radioButton.isChecked():
            self.label_4.setText(_("图片密码"))
            self.label_5.setText(_("水印密码"))
            self.label_6.hide()
            self.label_7.hide()
            self.lineEdit_4.hide()
            self.lineEdit_5.hide()
            self.brow.show()
            self.lineEdit.setPlaceholderText(_("输入图片路径以嵌入图片，输入文字以嵌入文字"))
        if self.radioButton_3.isChecked():
            self.label_4.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.label_7.hide()
            self.lineEdit_4.hide()
            self.lineEdit_5.hide()
            self.lineEdit_3.hide()
            self.lineEdit_2.hide()
        if self.radioButton_4.isChecked():
            self.label_4.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.label_7.hide()
            self.lineEdit_4.hide()
            self.lineEdit_5.hide()
            self.lineEdit_3.hide()
            self.lineEdit_2.hide()
        if self.radioButton_2.isChecked():
            self.brow.show()
            self.lineEdit.setPlaceholderText(_("输入图片路径以嵌入图片，输入文字以嵌入文字"))
            self.label_4.setText(_("种子1"))
            self.label_5.setText(_("种子2"))
            self.label_6.setText(_("除数1"))
            self.label_7.setText(_("除数2"))
            self.lineEdit_4.setPlaceholderText(_("输入以半角逗号分割的数字以在范围内取随机数"))
            self.lineEdit_5.setPlaceholderText(_("输入以半角逗号分割的数字以在范围内取随机数"))


    def generate_profile(self):
        self.watermark_method = None
        if self.content is None:
            if os.path.exists(self.lineEdit.text()):
                self.content = cv2.imread(self.lineEdit.text())
            else:
                self.content = self.lineEdit.text()
        if self.content is None:
            raise ValueError(_("空内容错误 水印嵌入内容为空"))
        if self.radioButton.isChecked():
            self.attachment_data = {
                "img_password": auto_rand(self.lineEdit_2.text()),
                "wm_password": auto_rand(self.lineEdit_3.text())
            }
            if os.path.exists(self.lineEdit.text()):
                self.watermark_method = const.WatermarkAlgorithm.IMAGE_GUOFEI
            else:
                self.watermark_method = const.WatermarkAlgorithm.TEXT_GOUFEI
        elif self.radioButton_2.isChecked():
            self.watermark_method = const.WatermarkAlgorithm.IMAGE_FIREKEEPER
            self.attachment_data = {
                "seed1": auto_rand(self.lineEdit_2.text()),
                "seed2": auto_rand(self.lineEdit_3.text()),
                "mod1": auto_rand(self.lineEdit_4.text()),
                "mod2": auto_rand(self.lineEdit_5.text()),
            }
            if not os.path.exists(self.lineEdit.text()):
                raise ValueError(_("输入路径不存在"))
        elif self.radioButton_3.isChecked():
            self.watermark_method = const.WatermarkAlgorithm.TEXT_FREQM
            self.attachment_data = {
                'method': 'dwtDct',
                'wmType': 'bytes'
            }
        elif self.radioButton_4.isChecked():
            self.watermark_method = const.WatermarkAlgorithm.TEXT_RIVAGAN
            self.attachment_data = {
                'method':'rivaGan',
                'wmType':'bytes'
            }

        self.quality = int(self.horizontalSlider.value())
        if self.comboBox.currentData() == "png":
            self.ext = const.IMAGE_TYPE.PNG
        elif self.comboBox.currentData() == "jpg":
            self.ext = const.IMAGE_TYPE.JPG
        elif self.comboBox.currentData() == "jpeg":
            self.ext = const.IMAGE_TYPE.JPEG
        elif self.comboBox.currentData() == "avif":
            self.ext = const.IMAGE_TYPE.AVIF
        elif self.comboBox.currentData() == "webp":
            self.ext = const.IMAGE_TYPE.WEBP

        self.output_path = self.lineEdit_6.text()
        self.prefix = self.lineEdit_7.text()
        self.output_method = self.comboBox_2.currentData()

    def select_image(self):
        file_path = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg)")[0]
        if file_path:
            content = img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if content is not None:
                self.content = content
            else:
                showFlyout(self,self.lineEdit,_("图片读取失败"),InfoBarIcon.ERROR,_("请检查图片路径是否正确"))
            self.lineEdit.setText(file_path)











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

    def run(self):
        self.ProcessLog.show()
        self.generate_profile()
        print(self.watermark_method,self.content,self.attachment_data)
        if self.worker_thread is not None and self.worker_thread.is_alive():
            return
        self.unit = ImageProcessUnit(
            self.files,
            self.watermark_method,
            self.attachment_data,
            self.output_path,
            self.prefix,
            self.ext,
            self.quality,
            output_method=self.output_method,
            content=self.content
        )
        self.unit.log_emit.connect(self.update_log)
        self.unit.switch_image.connect(self.switch_correct_image)
        self.unit.error_occur.connect(self.display_error_window)
        self.unit.process_over.connect(self.after_process)
        self.worker_thread = threading.Thread(target=self.unit.run)
        self.worker_thread.start()
        self.StartButton.setEnabled(False)

    def update_log(self,log):
        self.ProcessLog.append(log)
    def display_error_window(self,error_frame):
        if self.error_report_call_back:
            ret = [error_frame['error_type']+":"+error_frame['error_message'],error_frame['stack_trace'],[os.path.basename(error_frame['core_dump'])]]
            self.error_report_call_back(ret)

    def after_process(self):
        self.StartButton.setEnabled(True)
        # 清理线程变量（虽然用 is_alive 判断了，但置空是个好习惯）
        self.worker_thread = None
        # 可以在这里弹窗提示“处理完成”
        print("处理完成")

    def switch_correct_image(self, path):
        # 1. 规范化路径以增强匹配的健壮性 (解决斜杠和大小写问题)
        target_path = os.path.normpath(path).lower()

        for i in range(self.FileList.rowCount()):
            item = self.FileList.item(i, 1)
            if not item:
                continue

            # 获取表格中的路径并规范化
            current_path = os.path.normpath(item.text()).lower()

            if current_path == target_path:
                # 2. 选中单元格
                # 注意：这一步会自动触发 currentItemChanged 信号，
                # 进而自动调用 connected 的 self.set_correct_image()
                self.FileList.setCurrentCell(i, 0)

                # 3. 确保选中的行滚动到可视区域 (提升体验)
                self.FileList.scrollToItem(item, QAbstractItemView.PositionAtCenter)

                # 4. 删除手动调用的 self.set_correct_image()，避免重复执行
                return

        print(f"警告: 在列表中未找到路径 {path}")


def auto_rand(input_num : str):
    inp = input_num.replace(" ","").replace("\n","").replace("\r","").replace("，",",")
    try:
        num1 = inp.split(",")[0]
        num2 = inp.split(",")[1]
        return random.randint(int(num1),int(num2))
    except:
        try:
            return int(input_num)
        except:
            raise ValueError(f"无法解析随机数范围: {input_num}")

if __name__ == "__main__":
    setTheme(Theme.AUTO)
    setGlobalFont(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    lists = os.listdir(r"D:\mangatranslation\General\Alice\ORIGIN")
    w = ImageProcessWindow([os.path.join(r"D:\mangatranslation\General\Alice\ORIGIN", file) for file in lists])
    w.show()
    sys.exit(app.exec())