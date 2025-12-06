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
        name = str(session_id[0])+".txt"
        self.lp = LogProcessor(name)


    def set_main_log(self):
        main_log = self.lp.output_main_process_logs(["debug","info","error","warning","critical"])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ErrorReportDialog(dump_file=['coredumpy_test.mp4_7_d8247a3a-509e-45eb-bb0d-90c3b7e5ce8b.dump', 'coredumpy_test.mp4_8_d8247a3a-509e-45eb-bb0d-90c3b7e5ce8b.dump'])
    dialog.show()
    sys.exit(app.exec())