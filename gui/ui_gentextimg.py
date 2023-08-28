# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gentextimg.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QWidget)
import gui.res_rc

class Ui_gentextimg(object):
    def setupUi(self, gentextimg):
        if not gentextimg.objectName():
            gentextimg.setObjectName(u"gentextimg")
        gentextimg.resize(235, 86)
        gentextimg.setMinimumSize(QSize(235, 86))
        gentextimg.setMaximumSize(QSize(235, 86))
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        gentextimg.setWindowIcon(icon)
        self.spinBox = QSpinBox(gentextimg)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(80, 50, 42, 22))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(99999)
        self.spinBox.setValue(640)
        self.spinBox_2 = QSpinBox(gentextimg)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(160, 50, 42, 22))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(99999)
        self.spinBox_2.setValue(480)
        self.label = QLabel(gentextimg)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(13, 50, 61, 20))
        self.layoutWidget = QWidget(gentextimg)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 216, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.retranslateUi(gentextimg)

        QMetaObject.connectSlotsByName(gentextimg)
    # setupUi

    def retranslateUi(self, gentextimg):
        gentextimg.setWindowTitle(QCoreApplication.translate("gentextimg", u"\u751f\u6210\u6587\u5b57\u56fe", None))
        self.label.setText(QCoreApplication.translate("gentextimg", u"\u751f\u6210\u5206\u8fa8\u7387", None))
        self.pushButton.setText(QCoreApplication.translate("gentextimg", u"\u751f\u6210", None))
    # retranslateUi

