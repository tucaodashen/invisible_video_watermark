import os.path

from PySide6.QtWidgets import QFrame,QApplication
from GUI.error import Ui_ErrorReport
from qfluentwidgets import setTheme, Theme
from modules.LogProcessor import LogProcessor
import sys

class ErrorReportDialog(QFrame,Ui_ErrorReport):
    def __init__(self, parent=None,error=None,dump_file=None):
        super().__init__(parent)
        self.setupUi(self)
        setTheme(Theme.DARK)
        self.Image_lab.scaledToHeight(64)
        if error is not None:
            self.L_ErrorType.setText(str(error[0]))
            self.TB_Stack.setText(error[1])
        if dump_file is not None:
            st = ""
            for i in dump_file:
                size = os.path.getsize(os.path.join("./dumps",i))
                if size != 0:
                    st += str(i) + f"({size} bytes)" + "\n"
            self.textBrowser_5.setText(st)
        with open("identify_session.txt","r") as f:
            session_id = f.readline()
        name = os.path.join("./logs","app_"+str(session_id)+".log")
        level = ["debug","info","error","warning","critical","success"]
        self.comboBox_6.addItems(level)
        self.comboBox_3.addItems(level)
        self.lp = LogProcessor(name)
        self.comboBox_5.currentIndexChanged.connect(self.get_target_extract_log)
        self.comboBox_6.currentIndexChanged.connect(self.get_target_extract_log)
        self.spinBox_2.valueChanged.connect(self.get_target_extract_log)

        self.comboBox_2.currentIndexChanged.connect(self.get_target_process_log)
        self.comboBox_3.currentIndexChanged.connect(self.get_target_process_log)
        self.spinBox.valueChanged.connect(self.get_target_process_log)

        self.set_main_log()
        self.set_extract_log()
        self.add_task_select_extract()
        self.add_task_select_process()
        self.set_process_log()
        self.set_main_log()
        self.set_extract_log()
        self.add_task_select_extract()
        self.add_task_select_process()
        self.set_process_log()


    def set_main_log(self):
        main_log = self.lp.output_main_process_logs(["debug","info","error","warning","critical","success"])
        for i in main_log:
            self.textBrowser_2.append(i)

    def set_extract_log(self,process = "0",level = ["debug","info","error","warning","critical","success"]):
        self.textBrowser_4.clear()
        for i in self.lp.get_all_extract_task():
            extract_log = self.lp.output_extract_unit_logs(i,level,process)
            for i in extract_log:
                self.textBrowser_4.append(i)

    def set_process_log(self,process = "0",level = ["debug","info","error","warning","critical","success"]):
        self.textBrowser_3.clear()
        for i in self.lp.get_all_embed_task():
            extract_log = self.lp.output_extract_unit_logs(i,level,process)
            for i in extract_log:
                self.textBrowser_3.append(i)

    def add_task_select_extract(self):
        self.comboBox_5.addItem("ALL")
        for i in self.lp.get_all_extract_task():
            self.comboBox_5.addItem(i)

    def add_task_select_process(self):
        for i in self.lp.get_all_embed_task():
            self.comboBox_2.addItem(i)

    def get_target_extract_log(self):
        level = self.comboBox_6.currentText()
        task = self.comboBox_5.currentText()
        process = str(int(self.spinBox_2.value()))
        print(level,task,process)
        if task == "ALL":
            self.set_extract_log(str(process),[level])
        else:
            extract_log = self.lp.output_extract_unit_logs(task,[level],str(process))
            self.textBrowser_4.clear()
            for i in extract_log:
                self.textBrowser_4.append(i)

    def get_target_process_log(self):
        level = self.comboBox_3.currentText()
        task = self.comboBox_2.currentText()
        process = str(int(self.spinBox.value()))
        print(level,task,process)
        if task == "ALL":
            self.set_process_log(str(process),[level])
        else:
            process_log = self.lp.output_process_unit_logs(task,[level],str(process))
            self.textBrowser_3.clear()
            for i in process_log:
                self.textBrowser_3.append(i)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ErrorReportDialog(dump_file=['coredumpy_test.mp4_7_d8247a3a-509e-45eb-bb0d-90c3b7e5ce8b.dump'])
    dialog.show()
    sys.exit(app.exec())