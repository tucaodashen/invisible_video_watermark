# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewVersionFround.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

from qfluentwidgets import (PrimaryPushButton, PushButton, SubtitleLabel, TitleLabel)

class Ui_NewVersion(object):
    def setupUi(self, NewVersion):
        if not NewVersion.objectName():
            NewVersion.setObjectName(u"NewVersion")
        NewVersion.resize(557, 333)
        self.gridLayout = QGridLayout(NewVersion)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(NewVersion)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = TitleLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = SubtitleLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.textBrowser = QTextBrowser(self.frame)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = PushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = PushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = PrimaryPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(NewVersion)

        QMetaObject.connectSlotsByName(NewVersion)
    # setupUi

    def retranslateUi(self, NewVersion):
        NewVersion.setWindowTitle(QCoreApplication.translate("NewVersion", u"\u53d1\u73b0\u65b0\u7248\u672c", None))
        self.label.setText(QCoreApplication.translate("NewVersion", u"\u53d1\u73b0\u65b0\u7248\u672c", None))
        self.label_2.setText(QCoreApplication.translate("NewVersion", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("NewVersion", u"\u5ffd\u7565", None))
        self.pushButton_2.setText(QCoreApplication.translate("NewVersion", u"\u8df3\u8fc7\u8fd9\u4e00\u7248\u672c", None))
        self.pushButton_3.setText(QCoreApplication.translate("NewVersion", u"\u66f4\u65b0", None))
    # retranslateUi

