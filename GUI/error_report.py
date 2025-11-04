from PySide6.QtWidgets import QFrame,QApplication
from GUI.error import Ui_ErrorReport
from qfluentwidgets import setTheme, Theme
from modules.PlatformInformation import get_hardware_report
import threading
import sys

class ErrorReportDialog(QFrame,Ui_ErrorReport):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        setTheme(Theme.DARK)
        self.Image_lab.scaledToHeight(64)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ErrorReportDialog()
    dialog.show()
    sys.exit(app.exec())