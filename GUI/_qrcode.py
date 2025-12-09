# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qrcode.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QVBoxLayout, QWidget)

from qfluentwidgets import (CaptionLabel, ImageLabel, LineEdit, PushButton,
    SpinBox, SubtitleLabel, TitleLabel)

class Ui_GenerateQRCODE(object):
    def setupUi(self, GenerateQRCODE):
        if not GenerateQRCODE.objectName():
            GenerateQRCODE.setObjectName(u"GenerateQRCODE")
        GenerateQRCODE.resize(851, 430)
        self.verticalLayout_3 = QVBoxLayout(GenerateQRCODE)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = TitleLabel(GenerateQRCODE)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame = QFrame(GenerateQRCODE)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = CaptionLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_2 = SpinBox(self.frame)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.horizontalLayout.addWidget(self.spinBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = CaptionLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.spinBox = SpinBox(self.frame)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_2.addWidget(self.spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = CaptionLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.lineEdit = LineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.pushButton = PushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout_4.addWidget(self.frame)

        self.frame_2 = QFrame(GenerateQRCODE)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = SubtitleLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.label = ImageLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)


        self.horizontalLayout_4.addWidget(self.frame_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.retranslateUi(GenerateQRCODE)

        QMetaObject.connectSlotsByName(GenerateQRCODE)
    # setupUi

    def retranslateUi(self, GenerateQRCODE):
        GenerateQRCODE.setWindowTitle(QCoreApplication.translate("GenerateQRCODE", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("GenerateQRCODE", u"\u751f\u6210\u4e8c\u7ef4\u7801", None))
        self.label_3.setText(QCoreApplication.translate("GenerateQRCODE", u"\u5c0f\u65b9\u683c\u50cf\u7d20\u5927\u5c0f", None))
        self.label_4.setText(QCoreApplication.translate("GenerateQRCODE", u"\u8fb9\u6846\u50cf\u7d20\u5927\u5c0f", None))
        self.label_5.setText(QCoreApplication.translate("GenerateQRCODE", u"\u4e8c\u7ef4\u7801\u5185\u5bb9", None))
        self.pushButton.setText(QCoreApplication.translate("GenerateQRCODE", u"\u4fdd\u5b58", None))
        self.label_6.setText(QCoreApplication.translate("GenerateQRCODE", u"\u9884\u89c8", None))
        self.label.setText(QCoreApplication.translate("GenerateQRCODE", u"TextLabel", None))
    # retranslateUi

