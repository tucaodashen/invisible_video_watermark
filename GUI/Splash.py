# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Splash.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (ImageLabel, ProgressBar)
from . import allin_rc

class Ui_SplashDesu(object):
    def setupUi(self, SplashDesu):
        if not SplashDesu.objectName():
            SplashDesu.setObjectName(u"SplashDesu")
        SplashDesu.resize(725, 500)
        self.Pic = ImageLabel(SplashDesu)
        self.Pic.setObjectName(u"Pic")
        self.Pic.setGeometry(QRect(0, 0, 725, 500))
        self.Pic.setPixmap(QPixmap(u":/splash/BandiView_Splash.png"))
        self.Pic.setScaledContents(True)
        self.layoutWidget = QWidget(SplashDesu)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 410, 351, 51))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.progressBar = ProgressBar(self.layoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.Tips = QLabel(self.layoutWidget)
        self.Tips.setObjectName(u"Tips")
        font = QFont()
        font.setFamilies([u"\u6c49\u4eea\u6674\u7a7a\u4f53W"])
        font.setPointSize(12)
        self.Tips.setFont(font)

        self.verticalLayout.addWidget(self.Tips)

        self.version_info = QLabel(SplashDesu)
        self.version_info.setObjectName(u"version_info")
        self.version_info.setGeometry(QRect(40, 10, 181, 16))

        self.retranslateUi(SplashDesu)

        QMetaObject.connectSlotsByName(SplashDesu)
    # setupUi

    def retranslateUi(self, SplashDesu):
        SplashDesu.setWindowTitle(QCoreApplication.translate("SplashDesu", u"Form", None))
        self.Pic.setText("")
        self.Tips.setText(QCoreApplication.translate("SplashDesu", u"Loading\u2026\u2026", None))
        self.version_info.setText(QCoreApplication.translate("SplashDesu", u"TextLabel", None))
    # retranslateUi

