import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme

from GUI import ImageViewer
from GUI.ImageViewer import ImageProcessWindow

if __name__ == "__main__":
    setTheme(Theme.AUTO)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    lists = os.listdir(r"D:\mangatranslation\General\Alice\ORIGIN")
    w = ImageProcessWindow([os.path.join(r"D:\mangatranslation\General\Alice\ORIGIN", file) for file in lists])
    w.show()
    sys.exit(app.exec())