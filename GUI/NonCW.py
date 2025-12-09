# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NonCW.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CaptionLabel, ImageLabel, PushButton, TextBrowser,
    TitleLabel, TransparentPushButton)

class Ui_NonCriticalError(object):
    def setupUi(self, NonCriticalError):
        if not NonCriticalError.objectName():
            NonCriticalError.setObjectName(u"NonCriticalError")
        NonCriticalError.resize(545, 324)
        self.gridLayout_3 = QGridLayout(NonCriticalError)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = ImageLabel(NonCriticalError)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.label = TitleLabel(NonCriticalError)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textBrowser = TextBrowser(NonCriticalError)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = CaptionLabel(NonCriticalError)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_2 = PushButton(NonCriticalError)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = TransparentPushButton(NonCriticalError)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(NonCriticalError)

        QMetaObject.connectSlotsByName(NonCriticalError)
    # setupUi

    def retranslateUi(self, NonCriticalError):
        NonCriticalError.setWindowTitle(QCoreApplication.translate("NonCriticalError", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("NonCriticalError", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("NonCriticalError", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("NonCriticalError", u"\u8bf7\u4e0d\u8981\u53ea\u662f\u622a\u56fe\u6b64\u9875\u9762\uff01\u8bf7\u5c06\u9519\u8bef\u62a5\u544a\u4e00\u8d77\u63d0\u4ea4", None))
        self.pushButton_2.setText(QCoreApplication.translate("NonCriticalError", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("NonCriticalError", u"PushButton", None))
    # retranslateUi

