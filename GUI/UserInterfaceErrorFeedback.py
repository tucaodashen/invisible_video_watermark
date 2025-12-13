import sys

from PySide6.QtCore import Qt

from GUI.ErrorFeedback import Ui_ErrorFeedback
from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QFrame, QHeaderView, QTableWidgetItem, QCheckBox
from qfluentwidgets import theme, setTheme, Theme, CheckBox


def _(text):
    return text

class ErrorFeedbackUi_L(QFrame,Ui_ErrorFeedback):
    def __init__(self):
        setTheme(Theme.DARK)
        super().__init__()
        self.setupUi(self)
        self.checkBox_5.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_4.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_3.checkStateChanged.connect(self.set_correct_button)
        self.checkBox_2.checkStateChanged.connect(self.set_correct_button)
        self.checkBox.checkStateChanged.connect(self.set_correct_button)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            [_("错误"), _("级别"), _("报告")])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # 所有列自适应内容
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 名称列拉伸填充剩余空间
        self.comboBox.addItem(_("手动报告"))
        self.textBrowser.setText(_("此报告方式会输出一个压缩包文件，请将此压缩包上传到Github的Issue附件中或者直接通过网盘等方式发送给开发人员。"))
        self.error_list = []
        self.display_error()
        self.set_correct_button()


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ErrorFeedbackUi_L()
    window.show()
    window.add_error("RuntimeError(""视频文件不存在"")","CRITICAL","栈","转储","日志")
    sys.exit(app.exec())
