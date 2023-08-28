# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)
import gui.res_rc


class Ui_splashfr(object):
    def setupUi(self, splashfr):
        if not splashfr.objectName():
            splashfr.setObjectName(u"splashfr")
        splashfr.resize(750, 500)
        splashfr.setMinimumSize(QSize(750, 500))
        splashfr.setMaximumSize(QSize(750, 500))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        splashfr.setWindowIcon(icon)
        self.label = QLabel(splashfr)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 751, 501))
        self.label.setPixmap(QPixmap(u":/img/C:/Users/27698/Desktop/splash.png"))
        self.label.setScaledContents(True)

        self.retranslateUi(splashfr)

        QMetaObject.connectSlotsByName(splashfr)
    # setupUi

    def retranslateUi(self, splashfr):
        splashfr.setWindowTitle(QCoreApplication.translate("splashfr", u"Form", None))
        self.label.setText("")
    # retranslateUi

