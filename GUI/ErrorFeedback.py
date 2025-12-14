# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ErrorFeedback.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QSizePolicy, QTableWidgetItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, PrimaryPushButton,
    SubtitleLabel, TableWidget, TextBrowser)

class Ui_ErrorFeedback(object):
    def setupUi(self, ErrorFeedback):
        if not ErrorFeedback.objectName():
            ErrorFeedback.setObjectName(u"ErrorFeedback")
        ErrorFeedback.resize(842, 555)
        self.horizontalLayout_2 = QHBoxLayout(ErrorFeedback)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(ErrorFeedback)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = SubtitleLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tableWidget = TableWidget(self.frame)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)


        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(ErrorFeedback)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = BodyLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.comboBox = ComboBox(self.frame_2)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.textBrowser = TextBrowser(self.frame_2)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBox_4 = CheckBox(self.groupBox)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setTristate(False)

        self.verticalLayout_2.addWidget(self.checkBox_4)

        self.checkBox_3 = CheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_3)

        self.checkBox_2 = CheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_2)

        self.checkBox_5 = CheckBox(self.groupBox)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_5)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.checkBox = CheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_3.addWidget(self.checkBox)

        self.pushButton = PrimaryPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.retranslateUi(ErrorFeedback)

        QMetaObject.connectSlotsByName(ErrorFeedback)
    # setupUi

    def retranslateUi(self, ErrorFeedback):
        ErrorFeedback.setWindowTitle(QCoreApplication.translate("ErrorFeedback", u"\u62a5\u544a\u9519\u8bef", None))
        self.label.setText(QCoreApplication.translate("ErrorFeedback", u"\u6240\u6709\u9519\u8bef", None))
        self.label_2.setText(QCoreApplication.translate("ErrorFeedback", u"\u62a5\u544a\u65b9\u5f0f", None))
        self.groupBox.setTitle(QCoreApplication.translate("ErrorFeedback", u"\u4e0a\u4f20\u4fe1\u606f\u63a7\u5236", None))
        self.checkBox_4.setText(QCoreApplication.translate("ErrorFeedback", u"\u4e0a\u4f20\u6838\u5fc3\u8f6c\u50a8\u6587\u4ef6", None))
        self.checkBox_3.setText(QCoreApplication.translate("ErrorFeedback", u"\u4e0a\u4f20\u5f53\u524d\u8fd0\u884c\u8bbe\u5907\u4fe1\u606f", None))
        self.checkBox_2.setText(QCoreApplication.translate("ErrorFeedback", u"\u4e0a\u4f20\u5806\u6808\u62a5\u544a", None))
        self.checkBox_5.setText(QCoreApplication.translate("ErrorFeedback", u"\u4e0a\u4f20\u65e5\u5fd7", None))
        self.checkBox.setText(QCoreApplication.translate("ErrorFeedback", u"\u540c\u610f\u6211\u4eec\u7684EULA", None))
        self.pushButton.setText(QCoreApplication.translate("ErrorFeedback", u"\u62a5\u544a", None))
    # retranslateUi

