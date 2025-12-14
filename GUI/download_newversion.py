# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_newversion.ui'
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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, ProgressBar, PushButton)

class Ui_DownloadNew(object):
    def setupUi(self, DownloadNew):
        if not DownloadNew.objectName():
            DownloadNew.setObjectName(u"DownloadNew")
        DownloadNew.resize(749, 123)
        self.gridLayout = QGridLayout(DownloadNew)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(DownloadNew)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = BodyLabel(self.frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.progressBar = ProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton = PushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label_2 = BodyLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(DownloadNew)

        QMetaObject.connectSlotsByName(DownloadNew)
    # setupUi

    def retranslateUi(self, DownloadNew):
        DownloadNew.setWindowTitle(QCoreApplication.translate("DownloadNew", u"\u4e0b\u8f7d\u4e2d", None))
        self.label.setText(QCoreApplication.translate("DownloadNew", u"\u4e0b\u8f7d\u4e2d\uff0c\u8bf7\u7a0d\u5019\u2026\u2026", None))
        self.pushButton.setText(QCoreApplication.translate("DownloadNew", u"\u91cd\u8bd5", None))
        self.label_2.setText(QCoreApplication.translate("DownloadNew", u"TextLabel", None))
    # retranslateUi

