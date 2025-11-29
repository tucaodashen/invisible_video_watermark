# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'credit.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

from qfluentwidgets import (AvatarWidget, CaptionLabel, ImageLabel, SubtitleLabel,
    TitleLabel)
from . import allin_rc

class Ui_Credit(object):
    def setupUi(self, Credit):
        if not Credit.objectName():
            Credit.setObjectName(u"Credit")
        Credit.resize(673, 397)
        self.gridLayout = QGridLayout(Credit)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(Credit)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_6 = QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = TitleLabel(self.page)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.label_13 = CaptionLabel(self.page)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_4.addWidget(self.label_13)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(128, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_5 = ImageLabel(self.page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u"../GUI/slogan.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = AvatarWidget(self.page)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_9 = CaptionLabel(self.page)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout.addWidget(self.label_9)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.label_8 = SubtitleLabel(self.page)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_2.addWidget(self.label_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = AvatarWidget(self.page)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_10 = CaptionLabel(self.page)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_2.addWidget(self.label_10)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.label_7 = SubtitleLabel(self.page)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_3.addWidget(self.label_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = AvatarWidget(self.page)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_11 = CaptionLabel(self.page)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_3.addWidget(self.label_11)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.label_6 = SubtitleLabel(self.page)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_6.addLayout(self.verticalLayout_5)

        self.horizontalSpacer = QSpacerItem(160, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 46, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.label_12 = QLabel(self.page)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_5.addWidget(self.label_12)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(Credit)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Credit)
    # setupUi

    def retranslateUi(self, Credit):
        Credit.setWindowTitle(QCoreApplication.translate("Credit", u"Form", None))
        self.label.setText(QCoreApplication.translate("Credit", u"InvisibleVideoWatermark-NEXT", None))
        self.label_13.setText(QCoreApplication.translate("Credit", u"0.1_Omicron CE", None))
        self.label_5.setText("")
        self.label_2.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("Credit", u"\u5f7c\u5cb8\u4e4b\u5b89\u5361", None))
        self.label_8.setText(QCoreApplication.translate("Credit", u"\u540e\u7aef\u5f00\u53d1 \u6838\u5fc3\u529f\u80fd\u5b9e\u73b0", None))
        self.label_3.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("Credit", u"\u57ce\u5e02Chengshi", None))
        self.label_7.setText(QCoreApplication.translate("Credit", u"CI/CD QC \u524d\u7aef\u5f00\u53d1", None))
        self.label_4.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("Credit", u"\u7b2c\u4e00\u6279\u6d4b\u8bd5\u4eba\u5458", None))
        self.label_12.setText(QCoreApplication.translate("Credit", u"PraySoftware2019-2025\u00a9 All Rights Reserved OpenCore_Edition", None))
    # retranslateUi

