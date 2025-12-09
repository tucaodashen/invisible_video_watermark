# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UpScale.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (LineEdit, PrimaryPushButton, PushButton, TitleLabel)

class Ui_UpScaleAni(object):
    def setupUi(self, UpScaleAni):
        if not UpScaleAni.objectName():
            UpScaleAni.setObjectName(u"UpScaleAni")
        UpScaleAni.resize(804, 128)
        self.verticalLayout = QVBoxLayout(UpScaleAni)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = TitleLabel(UpScaleAni)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = LineEdit(UpScaleAni)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = PushButton(UpScaleAni)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_2 = LineEdit(UpScaleAni)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.pushButton_3 = PushButton(UpScaleAni)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_2 = PrimaryPushButton(UpScaleAni)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)


        self.retranslateUi(UpScaleAni)

        QMetaObject.connectSlotsByName(UpScaleAni)
    # setupUi

    def retranslateUi(self, UpScaleAni):
        UpScaleAni.setWindowTitle(QCoreApplication.translate("UpScaleAni", u"Form", None))
        self.label.setText(QCoreApplication.translate("UpScaleAni", u"\u8d85\u5206\u8fa8\u7387", None))
        self.pushButton.setText(QCoreApplication.translate("UpScaleAni", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("UpScaleAni", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("UpScaleAni", u"PushButton", None))
    # retranslateUi

