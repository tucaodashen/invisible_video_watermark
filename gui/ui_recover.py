# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recover.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import gui.res_rc

class Ui_readwm(object):
    def setupUi(self, readwm):
        if not readwm.objectName():
            readwm.setObjectName(u"readwm")
        readwm.resize(301, 180)
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        readwm.setWindowIcon(icon)
        self.layoutWidget = QWidget(readwm)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 276, 125))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.label_4 = QLabel(readwm)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 150, 54, 16))
        self.label_5 = QLabel(readwm)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(70, 150, 211, 16))

        self.retranslateUi(readwm)

        QMetaObject.connectSlotsByName(readwm)
    # setupUi

    def retranslateUi(self, readwm):
        readwm.setWindowTitle(QCoreApplication.translate("readwm", u"\u8bfb\u53d6\u6c34\u5370", None))
        self.label.setText(QCoreApplication.translate("readwm", u"\u5904\u7406\u7c7b\u578b", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("readwm", u"\u56fe\u7247", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("readwm", u"\u6587\u5b57", None))

        self.label_2.setText(QCoreApplication.translate("readwm", u"json\u6587\u4ef6", None))
        self.pushButton.setText(QCoreApplication.translate("readwm", u"\u6d4f\u89c8", None))
        self.label_3.setText(QCoreApplication.translate("readwm", u"\u89c6\u9891\u6587\u4ef6", None))
        self.pushButton_2.setText(QCoreApplication.translate("readwm", u"\u6d4f\u89c8", None))
        self.pushButton_3.setText(QCoreApplication.translate("readwm", u"\u63d0\u53d6", None))
        self.label_4.setText(QCoreApplication.translate("readwm", u"\u6587\u5b57\u7ed3\u679c\uff1a", None))
        self.label_5.setText("")
    # retranslateUi

