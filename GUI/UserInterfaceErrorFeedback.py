import sys
from copy import deepcopy

import wmi
from PySide6.QtCore import Qt

from GUI.ErrorFeedback import Ui_ErrorFeedback
from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QFrame, QHeaderView, QTableWidgetItem, QCheckBox, \
    QFileDialog
from qfluentwidgets import theme, setTheme, Theme, CheckBox

from modules.error_feedback_related import pack_error
import platform
import psutil
import socket
import datetime
from pprint import pprint


def _(text):
    return text

class ErrorFeedbackUi_L(QFrame,Ui_ErrorFeedback):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.checkBox_5.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_4.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_3.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_2.checkStateChanged.connect(self.set_correct_button)
        self.checkBox.checkStateChanged.connect(self.set_correct_button)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(
            [_("错误"), _("级别"), _("报告"),_("索引")])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # 所有列自适应内容
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 名称列拉伸填充剩余空间
        self.comboBox.addItem(_("手动报告"))
        self.textBrowser.setText(_("此报告方式会输出一个压缩包文件，请将此压缩包上传到Github的Issue附件中或者直接通过网盘等方式发送给开发人员。"))
        self.error_list = []
        self.display_error()
        self.set_correct_button()
        self.pushButton.clicked.connect(self.packup)


    def set_correct_button(self):
        if self.checkBox.isChecked():
            if True not in [self.checkBox_5.isChecked(), self.checkBox_4.isChecked(), self.checkBox_3.isChecked(), self.checkBox_2.isChecked()]:
                self.pushButton.setEnabled(False)
            else:
                self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)


    def add_error(self,error,level,stack,dump,log):
        error_item = [error,level,stack,dump,log]
        if error_item not in self.error_list:
            self.error_list.append(error_item)
        self.display_error()



    def display_error(self):
        self.tableWidget.setRowCount(0)
        if self.error_list:
            for i in self.error_list:
                self._add_to_table(i)

    def _add_to_table(self,frame):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        index_item = QTableWidgetItem(str(frame[0]))
        index_item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 0, index_item)

        name_item = QTableWidgetItem(str(frame[1]))
        self.tableWidget.setItem(row, 1, name_item)

        ccb = QCheckBox()
        ccb.setStyleSheet("""
            QCheckBox {
                margin-left: 5%;
                margin-right: 5%;
            }
        """)
        self.tableWidget.setCellWidget(row, 2, ccb)

        index_item = QTableWidgetItem(str(row))
        index_item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(row, 3, index_item)

    def packup(self):
        is_device_info = self.checkBox_3.isChecked()
        pass_fault = []
        all = []
        for i in range(self.tableWidget.rowCount()):
            is_checked = self.tableWidget.cellWidget(i, 2).isChecked()
            print(i,is_checked,self.error_list[i])
            cur = deepcopy(self.error_list[i])
            if not self.checkBox_4.isChecked():
                cur[3] = []
            if not self.checkBox_2.isChecked():
                cur[2] = ""
            if not self.checkBox_5.isChecked():
                cur[4] = ""
            if is_checked:
                pass_fault.append(cur)
            all.append(is_checked)
        if True in all:
            output_path = QFileDialog.getSaveFileName(self, _("保存错误报告"), "error_packup.zst", _("压缩包文件 (*.zst)"))[0]
            if not output_path:
                return
            pack_error(pass_fault,is_device_info,output_path)
        












if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorFeedbackUi_L()
    window.show()
    window.add_error("RuntimeError(""视频文件不存在"")","CRITICAL","栈","转储","日志")
    sys.exit(app.exec())
