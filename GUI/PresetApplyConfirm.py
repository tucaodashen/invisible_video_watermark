# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PresetApplyConfirm.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, LineEdit, PrimaryPushButton, PushButton,
    TitleLabel)

class Ui_AP_Form(object):
    def setupUi(self, AP_Form):
        if not AP_Form.objectName():
            AP_Form.setObjectName(u"AP_Form")
        AP_Form.resize(400, 136)
        self.verticalLayout = QVBoxLayout(AP_Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.L_title = TitleLabel(AP_Form)
        self.L_title.setObjectName(u"L_title")

        self.horizontalLayout_3.addWidget(self.L_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.L_outputPath = BodyLabel(AP_Form)
        self.L_outputPath.setObjectName(u"L_outputPath")

        self.horizontalLayout_2.addWidget(self.L_outputPath)

        self.LE_OP = LineEdit(AP_Form)
        self.LE_OP.setObjectName(u"LE_OP")

        self.horizontalLayout_2.addWidget(self.LE_OP)

        self.PB_OP = PushButton(AP_Form)
        self.PB_OP.setObjectName(u"PB_OP")

        self.horizontalLayout_2.addWidget(self.PB_OP)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.L_WatermarkContent = BodyLabel(AP_Form)
        self.L_WatermarkContent.setObjectName(u"L_WatermarkContent")

        self.horizontalLayout.addWidget(self.L_WatermarkContent)

        self.LE_WC = LineEdit(AP_Form)
        self.LE_WC.setObjectName(u"LE_WC")

        self.horizontalLayout.addWidget(self.LE_WC)

        self.PB_WC = PushButton(AP_Form)
        self.PB_WC.setObjectName(u"PB_WC")

        self.horizontalLayout.addWidget(self.PB_WC)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Confirm = PrimaryPushButton(AP_Form)
        self.Confirm.setObjectName(u"Confirm")

        self.horizontalLayout_4.addWidget(self.Confirm)

        self.Cancel = PushButton(AP_Form)
        self.Cancel.setObjectName(u"Cancel")

        self.horizontalLayout_4.addWidget(self.Cancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(AP_Form)

        QMetaObject.connectSlotsByName(AP_Form)
    # setupUi

    def retranslateUi(self, AP_Form):
        AP_Form.setWindowTitle(QCoreApplication.translate("AP_Form", u"ApplyPreset", None))
        self.L_title.setText(QCoreApplication.translate("AP_Form", u"TextLabel", None))
        self.L_outputPath.setText(QCoreApplication.translate("AP_Form", u"TextLabel", None))
        self.PB_OP.setText(QCoreApplication.translate("AP_Form", u"PushButton", None))
        self.L_WatermarkContent.setText(QCoreApplication.translate("AP_Form", u"TextLabel", None))
        self.PB_WC.setText(QCoreApplication.translate("AP_Form", u"PushButton", None))
        self.Confirm.setText(QCoreApplication.translate("AP_Form", u"PushButton", None))
        self.Cancel.setText(QCoreApplication.translate("AP_Form", u"PushButton", None))
    # retranslateUi

