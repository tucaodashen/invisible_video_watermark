# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'genqrcode.ui'
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
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)
import gui.res_rc

class Ui_genqrcode(object):
    def setupUi(self, genqrcode):
        if not genqrcode.objectName():
            genqrcode.setObjectName(u"genqrcode")
        genqrcode.resize(240, 108)
        genqrcode.setMinimumSize(QSize(240, 108))
        genqrcode.setMaximumSize(QSize(240, 108))
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        genqrcode.setWindowIcon(icon)
        self.layoutWidget = QWidget(genqrcode)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 215, 54))
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


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.layoutWidget1 = QWidget(genqrcode)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(40, 70, 140, 22))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.layoutWidget1)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setValue(3)

        self.horizontalLayout_2.addWidget(self.spinBox)


        self.retranslateUi(genqrcode)

        QMetaObject.connectSlotsByName(genqrcode)
    # setupUi

    def retranslateUi(self, genqrcode):
        genqrcode.setWindowTitle(QCoreApplication.translate("genqrcode", u"\u751f\u6210\u4e8c\u7ef4\u7801", None))
        self.label.setText(QCoreApplication.translate("genqrcode", u"\u8f93\u5165\u751f\u6210\u6587\u5b57", None))
        self.pushButton.setText(QCoreApplication.translate("genqrcode", u"\u751f\u6210", None))
        self.label_2.setText(QCoreApplication.translate("genqrcode", u"\u5355\u4e2a\u8272\u5757\u6240\u5360\u50cf\u7d20", None))
    # retranslateUi

