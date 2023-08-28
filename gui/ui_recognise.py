# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recognise.ui'
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
    QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout,
    QWidget)
import gui.res_rc

class Ui_recongise(object):
    def setupUi(self, recongise):
        if not recongise.objectName():
            recongise.setObjectName(u"recongise")
        recongise.setEnabled(True)
        recongise.resize(332, 283)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(recongise.sizePolicy().hasHeightForWidth())
        recongise.setSizePolicy(sizePolicy)
        recongise.setMinimumSize(QSize(332, 283))
        recongise.setMaximumSize(QSize(332, 283))
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        recongise.setWindowIcon(icon)
        self.label_2 = QLabel(recongise)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 200, 81, 16))
        self.label_3 = QLabel(recongise)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 210, 211, 51))
        self.textBrowser = QTextBrowser(recongise)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 140, 256, 51))
        self.layoutWidget = QWidget(recongise)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 296, 58))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)


        self.retranslateUi(recongise)

        QMetaObject.connectSlotsByName(recongise)
    # setupUi

    def retranslateUi(self, recongise):
        recongise.setWindowTitle(QCoreApplication.translate("recongise", u"\u8bc6\u522b\u4e8c\u7ef4\u7801", None))
        self.label_2.setText(QCoreApplication.translate("recongise", u"\u8bc6\u522b\u7ed3\u679c\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("recongise", u"\u7b49\u5f85\u4e2d...", None))
        self.textBrowser.setHtml(QCoreApplication.translate("recongise", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8bf7\u6ce8\u610f\uff01opencv\u8bc6\u522b\u7387\u8f83\u4f4e\uff0c\u5404\u4f4d\u53ef\u7528\u624b\u673a\u5fae\u4fe1\u8fdb\u884c\u626b\u63cf\uff0c\u4ee5\u63d0\u9ad8\u8bc6\u522b\u7387</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("recongise", u"\u9009\u62e9\u8bc6\u522b\u6587\u4ef6", None))
        self.pushButton.setText(QCoreApplication.translate("recongise", u"\u6d4f\u89c8", None))
        self.pushButton_2.setText(QCoreApplication.translate("recongise", u"\u8bc6\u522b", None))
    # retranslateUi

