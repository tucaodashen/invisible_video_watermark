# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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


class Ui_Formabout(object):
    def setupUi(self, Formabout):
        if not Formabout.objectName():
            Formabout.setObjectName(u"Formabout")
        Formabout.resize(480, 360)
        Formabout.setMinimumSize(QSize(480, 360))
        Formabout.setMaximumSize(QSize(480, 360))
        icon = QIcon()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        Formabout.setWindowIcon(icon)
        Formabout.setStyleSheet(u"")
        self.label = QLabel(Formabout)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 481, 361))
        self.label.setStyleSheet(u"")
        self.label.setPixmap(QPixmap(u":/img/C:/Users/27698/Desktop/about.png"))
        self.label.setScaledContents(True)

        self.retranslateUi(Formabout)

        QMetaObject.connectSlotsByName(Formabout)
    # setupUi

    def retranslateUi(self, Formabout):
        Formabout.setWindowTitle(QCoreApplication.translate("Formabout", u"Form", None))
        self.label.setText("")
    # retranslateUi

