# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RecoverWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

from CustomGUI import DropFrame
from qfluentwidgets import (BodyLabel, ImageLabel, ProgressBar, SpinBox,
    TitleLabel)

class Ui_Recover_Form(object):
    def setupUi(self, Recover_Form):
        if not Recover_Form.objectName():
            Recover_Form.setObjectName(u"Recover_Form")
        Recover_Form.resize(730, 347)
        self.verticalLayout = QVBoxLayout(Recover_Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.L_title = TitleLabel(Recover_Form)
        self.L_title.setObjectName(u"L_title")

        self.verticalLayout.addWidget(self.L_title)

        self.tabWidget = QTabWidget(Recover_Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.frame = DropFrame(self.tab)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = BodyLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.SB_SliceLength = SpinBox(self.frame)
        self.SB_SliceLength.setObjectName(u"SB_SliceLength")
        self.SB_SliceLength.setMinimum(1)
        self.SB_SliceLength.setMaximum(100)
        self.SB_SliceLength.setValue(3)

        self.horizontalLayout.addWidget(self.SB_SliceLength)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = BodyLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.SB_MaxWorker = SpinBox(self.frame)
        self.SB_MaxWorker.setObjectName(u"SB_MaxWorker")
        self.SB_MaxWorker.setMinimum(1)
        self.SB_MaxWorker.setMaximum(61)
        self.SB_MaxWorker.setValue(8)

        self.horizontalLayout_2.addWidget(self.SB_MaxWorker)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_6.addWidget(self.frame)

        self.progressBar = ProgressBar(self.tab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout_6.addWidget(self.progressBar)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_5 = QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_5.addWidget(self.label_5)

        self.F_TextResult = QFrame(self.tab_2)
        self.F_TextResult.setObjectName(u"F_TextResult")
        self.F_TextResult.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_TextResult.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.F_TextResult)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_6 = QLabel(self.F_TextResult)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.textBrowser = QTextBrowser(self.F_TextResult)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton = QPushButton(self.F_TextResult)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addWidget(self.F_TextResult)

        self.F_ImageResult = QFrame(self.tab_2)
        self.F_ImageResult.setObjectName(u"F_ImageResult")
        self.F_ImageResult.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_ImageResult.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.F_ImageResult)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.F_ImageResult)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.label_8 = ImageLabel(self.F_ImageResult)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_4.addWidget(self.label_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_2 = QPushButton(self.F_ImageResult)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_5.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.F_ImageResult)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_5.addWidget(self.pushButton_3)

        self.progressBar_2 = ProgressBar(self.F_ImageResult)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressBar_2)

        self.L_CurIndex = QLabel(self.F_ImageResult)
        self.L_CurIndex.setObjectName(u"L_CurIndex")

        self.horizontalLayout_5.addWidget(self.L_CurIndex)

        self.pushButton_4 = QPushButton(self.F_ImageResult)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_5.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.F_ImageResult)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_5.addWidget(self.pushButton_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)


        self.verticalLayout_5.addWidget(self.F_ImageResult)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Recover_Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Recover_Form)
    # setupUi

    def retranslateUi(self, Recover_Form):
        Recover_Form.setWindowTitle(QCoreApplication.translate("Recover_Form", u"Form", None))
        self.L_title.setText(QCoreApplication.translate("Recover_Form", u"\u8bfb\u53d6\u6c34\u5370", None))
        self.label_2.setText(QCoreApplication.translate("Recover_Form", u"\u62d6\u5165\u89c6\u9891\u6587\u4ef6\u4e0e\u6062\u590d\u6587\u4ef6\u542f\u52a8\u8bfb\u53d6", None))
        self.label_3.setText(QCoreApplication.translate("Recover_Form", u"\u5207\u7247\u957f\u5ea6", None))
        self.label_4.setText(QCoreApplication.translate("Recover_Form", u"\u6700\u5927\u5e76\u884c\u6570", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Recover_Form", u"Tab 1", None))
        self.label_5.setText(QCoreApplication.translate("Recover_Form", u"\u5206\u6790\u7ed3\u679c", None))
        self.label_6.setText(QCoreApplication.translate("Recover_Form", u"detail", None))
        self.pushButton.setText(QCoreApplication.translate("Recover_Form", u"\u4fdd\u5b58\u5230\u6587\u4ef6", None))
        self.label_7.setText(QCoreApplication.translate("Recover_Form", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("Recover_Form", u"TextLabel", None))
        self.pushButton_2.setText(QCoreApplication.translate("Recover_Form", u"\u4e0a\u4e00\u5f20", None))
        self.pushButton_3.setText(QCoreApplication.translate("Recover_Form", u"\u4e0b\u4e00\u5f20", None))
        self.L_CurIndex.setText(QCoreApplication.translate("Recover_Form", u"TextLabel", None))
        self.pushButton_4.setText(QCoreApplication.translate("Recover_Form", u"PushButton", None))
        self.pushButton_5.setText(QCoreApplication.translate("Recover_Form", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Recover_Form", u"Tab 2", None))
    # retranslateUi

