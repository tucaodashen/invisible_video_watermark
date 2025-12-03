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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (AvatarWidget, BodyLabel, CaptionLabel, ImageLabel,
    SubtitleLabel, TitleLabel, TransparentPushButton)
from . import allin_rc

class Ui_Credit(object):
    def setupUi(self, Credit):
        if not Credit.objectName():
            Credit.setObjectName(u"Credit")
        Credit.resize(796, 469)
        self.gridLayout = QGridLayout(Credit)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Credit)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = TitleLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.label_13 = CaptionLabel(self.frame)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_4.addWidget(self.label_13)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(128, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_5 = ImageLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setPixmap(QPixmap(u"C:/Users/ASUS/.designer/GUI/slogan.png"))
        self.label_5.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_5)

        self.label_22 = ImageLabel(self.frame)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout.addWidget(self.label_22)


        self.verticalLayout_14.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = AvatarWidget(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_9 = CaptionLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(77, 0))

        self.verticalLayout_2.addWidget(self.label_9)


        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = AvatarWidget(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_10 = CaptionLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = AvatarWidget(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.label_11 = CaptionLabel(self.frame)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout.addWidget(self.label_11)


        self.verticalLayout_5.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_8 = SubtitleLabel(self.frame)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_6.addWidget(self.label_8)

        self.label_7 = SubtitleLabel(self.frame)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_6.addWidget(self.label_7)

        self.label_6 = SubtitleLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_6.addWidget(self.label_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(160, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_15 = BodyLabel(self.frame)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_7.addWidget(self.label_15)

        self.label_16 = BodyLabel(self.frame)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_7.addWidget(self.label_16)

        self.label_17 = BodyLabel(self.frame)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_7.addWidget(self.label_17)

        self.label_18 = BodyLabel(self.frame)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_7.addWidget(self.label_18)

        self.label_19 = BodyLabel(self.frame)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_7.addWidget(self.label_19)

        self.label_20 = BodyLabel(self.frame)
        self.label_20.setObjectName(u"label_20")

        self.verticalLayout_7.addWidget(self.label_20)

        self.label_21 = BodyLabel(self.frame)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_7.addWidget(self.label_21)

        self.label_23 = BodyLabel(self.frame)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_7.addWidget(self.label_23)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_7)


        self.verticalLayout_14.addLayout(self.horizontalLayout_4)

        self.pushButton = TransparentPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_14.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(17, 64, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_14.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_5.addWidget(self.label_12)


        self.verticalLayout_14.addLayout(self.horizontalLayout_5)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Credit)

        QMetaObject.connectSlotsByName(Credit)
    # setupUi

    def retranslateUi(self, Credit):
        Credit.setWindowTitle(QCoreApplication.translate("Credit", u"Form", None))
        self.label.setText(QCoreApplication.translate("Credit", u"InvisibleVideoWatermark-NEXT", None))
        self.label_13.setText(QCoreApplication.translate("Credit", u"0.1_Omicron CE", None))
        self.label_5.setText("")
        self.label_22.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_9.setText(QCoreApplication.translate("Credit", u"\u5f7c\u5cb8\u4e4b\u5b89\u5361", None))
        self.label_3.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_10.setText(QCoreApplication.translate("Credit", u"\u63d0\u98ce_City", None))
        self.label_4.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_11.setText(QCoreApplication.translate("Credit", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("Credit", u"\u540e\u7aef\u5f00\u53d1 \u6838\u5fc3\u529f\u80fd\u5b9e\u73b0", None))
        self.label_7.setText(QCoreApplication.translate("Credit", u"CI/CD QC \u524d\u7aef\u5f00\u53d1", None))
        self.label_6.setText(QCoreApplication.translate("Credit", u"\u7b2c\u4e00\u6279\u6d4b\u8bd5\u4eba\u5458", None))
        self.label_15.setText(QCoreApplication.translate("Credit", u"Credit:", None))
        self.label_16.setText(QCoreApplication.translate("Credit", u"- FireKeeper", None))
        self.label_17.setText(QCoreApplication.translate("Credit", u"- GuoFei", None))
        self.label_18.setText(QCoreApplication.translate("Credit", u"- ShieldMint", None))
        self.label_19.setText(QCoreApplication.translate("Credit", u"- Nuitka", None))
        self.label_20.setText(QCoreApplication.translate("Credit", u"- FFmpeg", None))
        self.label_21.setText(QCoreApplication.translate("Credit", u"\u542f\u52a8\u56fe\u50cf\u827a\u672f\u5bb6\uff1a\u305b\u3093\u3061\u3083 \n"
"pid113793108", None))
        self.label_23.setText(QCoreApplication.translate("Credit", u"\u7f29\u7565\u56fe\u5360\u4f4d\u7b26\u827a\u672f\u5bb6\uff1aRiok_hh\n"
"pid134732976", None))
        self.pushButton.setText(QCoreApplication.translate("Credit", u"\u652f\u6301\u6211\u4eec", None))
        self.label_12.setText(QCoreApplication.translate("Credit", u"PraySoftware2019-2025\u00a9 All Rights Reserved OpenCore_Edition", None))
    # retranslateUi

