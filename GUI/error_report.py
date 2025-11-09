from PySide6.QtWidgets import QFrame,QApplication
from GUI.error import Ui_ErrorReport
from qfluentwidgets import setTheme, Theme
import sys

class ErrorReportDialog(QFrame,Ui_ErrorReport):
    def __init__(self, parent=None,error=None):
        super().__init__(parent)
        self.setupUi(self)
        setTheme(Theme.DARK)
        self.Image_lab.scaledToHeight(64)
        if error is not None:
            self.L_ErrorType.setText(str(error[0]))
            self.TB_Stack.setText(error[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ErrorReportDialog()
    dialog.show()
    sys.exit(app.exec())