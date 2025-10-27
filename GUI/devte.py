from GUI.SetUp import Ui_SetUpNewForm
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpinBox,
    QVBoxLayout, QWidget)
from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, SubtitleLabel,theme,setTheme,Theme,
    TitleLabel)


class SetUpNewForm(QWidget, Ui_SetUpNewForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        setTheme(Theme.DARK)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    SetUpNewForm = SetUpNewForm()
    SetUpNewForm.show()
    sys.exit(app.exec())