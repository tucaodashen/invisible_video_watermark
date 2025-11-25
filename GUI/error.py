# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'error.ui'
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
    QSpacerItem, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)

from qfluentwidgets import (BodyLabel, CaptionLabel, ComboBox, ImageLabel,
    PrimaryPushButton, PushButton, TextBrowser, TitleLabel)
from . import allin_rc

class Ui_ErrorReport(object):
    def setupUi(self, ErrorReport):
        if not ErrorReport.objectName():
            ErrorReport.setObjectName(u"ErrorReport")
        ErrorReport.resize(720, 532)
        self.verticalLayout_4 = QVBoxLayout(ErrorReport)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.Image_lab = ImageLabel(ErrorReport)
        self.Image_lab.setObjectName(u"Image_lab")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Image_lab.sizePolicy().hasHeightForWidth())
        self.Image_lab.setSizePolicy(sizePolicy)
        self.Image_lab.setMinimumSize(QSize(64, 64))
        self.Image_lab.setMaximumSize(QSize(128, 128))
        self.Image_lab.setPixmap(QPixmap(u":/MainWindow/\u545c\u54c7.png"))
        self.Image_lab.setScaledContents(True)

        self.horizontalLayout_12.addWidget(self.Image_lab)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = TitleLabel(ErrorReport)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.L_ErrorType = BodyLabel(ErrorReport)
        self.L_ErrorType.setObjectName(u"L_ErrorType")

        self.verticalLayout_3.addWidget(self.L_ErrorType)


        self.horizontalLayout_12.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.LogBrowser = QTabWidget(ErrorReport)
        self.LogBrowser.setObjectName(u"LogBrowser")
        self.LogBrowser.setMinimumSize(QSize(700, 350))
        self.LogBrowser.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_6 = QGridLayout(self.tab_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.TB_Stack = TextBrowser(self.tab_4)
        self.TB_Stack.setObjectName(u"TB_Stack")

        self.gridLayout_6.addWidget(self.TB_Stack, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.tab_4, "")
        self.PlatformInfoTab = QWidget()
        self.PlatformInfoTab.setObjectName(u"PlatformInfoTab")
        self.gridLayout = QGridLayout(self.PlatformInfoTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser = TextBrowser(self.PlatformInfoTab)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.PlatformInfoTab, "")
        self.MainProgressLog = QWidget()
        self.MainProgressLog.setObjectName(u"MainProgressLog")
        self.verticalLayout_5 = QVBoxLayout(self.MainProgressLog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = BodyLabel(self.MainProgressLog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.comboBox = ComboBox(self.MainProgressLog)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.textBrowser_2 = QTextBrowser(self.MainProgressLog)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.verticalLayout_5.addWidget(self.textBrowser_2)

        self.LogBrowser.addTab(self.MainProgressLog, "")
        self.EncodeProcessorLog = QWidget()
        self.EncodeProcessorLog.setObjectName(u"EncodeProcessorLog")
        self.gridLayout_2 = QGridLayout(self.EncodeProcessorLog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = BodyLabel(self.EncodeProcessorLog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.comboBox_2 = ComboBox(self.EncodeProcessorLog)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_2.addWidget(self.comboBox_2)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = BodyLabel(self.EncodeProcessorLog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.comboBox_3 = ComboBox(self.EncodeProcessorLog)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_3.addWidget(self.comboBox_3)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = BodyLabel(self.EncodeProcessorLog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.comboBox_4 = ComboBox(self.EncodeProcessorLog)
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.horizontalLayout_4.addWidget(self.comboBox_4)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.textBrowser_3 = QTextBrowser(self.EncodeProcessorLog)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.verticalLayout.addWidget(self.textBrowser_3)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.EncodeProcessorLog, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = BodyLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_9.addWidget(self.label_7)

        self.comboBox_5 = ComboBox(self.tab)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.horizontalLayout_9.addWidget(self.comboBox_5)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_9)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = BodyLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.comboBox_6 = ComboBox(self.tab)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.horizontalLayout_10.addWidget(self.comboBox_6)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = BodyLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.comboBox_7 = ComboBox(self.tab)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.horizontalLayout_11.addWidget(self.comboBox_7)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.textBrowser_4 = QTextBrowser(self.tab)
        self.textBrowser_4.setObjectName(u"textBrowser_4")

        self.verticalLayout_2.addWidget(self.textBrowser_4)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_4 = QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.textBrowser_5 = QTextBrowser(self.tab_2)
        self.textBrowser_5.setObjectName(u"textBrowser_5")

        self.gridLayout_4.addWidget(self.textBrowser_5, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.textBrowser_6 = QTextBrowser(self.tab_3)
        self.textBrowser_6.setObjectName(u"textBrowser_6")

        self.gridLayout_5.addWidget(self.textBrowser_6, 0, 0, 1, 1)

        self.LogBrowser.addTab(self.tab_3, "")

        self.verticalLayout_4.addWidget(self.LogBrowser)

        self.label_10 = CaptionLabel(ErrorReport)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_4.addWidget(self.label_10)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.pushButton = PushButton(ErrorReport)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_13.addWidget(self.pushButton)

        self.pushButton_2 = PushButton(ErrorReport)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_13.addWidget(self.pushButton_2)

        self.pushButton_3 = PrimaryPushButton(ErrorReport)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_13.addWidget(self.pushButton_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)


        self.retranslateUi(ErrorReport)

        self.LogBrowser.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ErrorReport)
    # setupUi

    def retranslateUi(self, ErrorReport):
        ErrorReport.setWindowTitle(QCoreApplication.translate("ErrorReport", u"Form", None))
        self.Image_lab.setText("")
        self.label.setText(QCoreApplication.translate("ErrorReport", u"\u53d1\u751f\u81f4\u547d\u9519\u8bef\uff01", None))
        self.L_ErrorType.setText(QCoreApplication.translate("ErrorReport", u"TextLabel", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.tab_4), QCoreApplication.translate("ErrorReport", u"\u5806\u6808\u62a5\u544a", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.PlatformInfoTab), QCoreApplication.translate("ErrorReport", u"\u5e73\u53f0\u4fe1\u606f", None))
        self.label_3.setText(QCoreApplication.translate("ErrorReport", u"\u7ea7\u522b", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.MainProgressLog), QCoreApplication.translate("ErrorReport", u"\u4e3b\u7a0b\u5e8f\u65e5\u5fd7", None))
        self.label_4.setText(QCoreApplication.translate("ErrorReport", u"\u4efb\u52a1", None))
        self.label_5.setText(QCoreApplication.translate("ErrorReport", u"\u7ea7\u522b", None))
        self.label_6.setText(QCoreApplication.translate("ErrorReport", u"\u8fdb\u7a0b", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.EncodeProcessorLog), QCoreApplication.translate("ErrorReport", u"\u7f16\u7801\u5355\u5143\u65e5\u5fd7", None))
        self.label_7.setText(QCoreApplication.translate("ErrorReport", u"\u4efb\u52a1", None))
        self.label_8.setText(QCoreApplication.translate("ErrorReport", u"\u7ea7\u522b", None))
        self.label_9.setText(QCoreApplication.translate("ErrorReport", u"\u8fdb\u7a0b", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.tab), QCoreApplication.translate("ErrorReport", u"\u89e3\u7801\u5355\u5143\u65e5\u5fd7", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.tab_2), QCoreApplication.translate("ErrorReport", u"\u6838\u5fc3\u8f6c\u50a8\u4fe1\u606f", None))
        self.LogBrowser.setTabText(self.LogBrowser.indexOf(self.tab_3), QCoreApplication.translate("ErrorReport", u"VizTracer\u4fe1\u606f", None))
        self.label_10.setText(QCoreApplication.translate("ErrorReport", u"\u4e0d\u8981\u4ec5\u4ec5\u53ea\u662f\u622a\u56fe\u6b64\u754c\u9762\uff0c\u8bf7\u5c06\u9519\u8bef\u65e5\u5fd7\u4e00\u540c\u63d0\u4ea4\u7ed9\u5f00\u53d1\u4eba\u5458\uff01", None))
        self.pushButton.setText(QCoreApplication.translate("ErrorReport", u"\u5173\u95ed(\u7ed3\u675f\u7a0b\u5e8f)", None))
        self.pushButton_2.setText(QCoreApplication.translate("ErrorReport", u"\u63d0\u4ea4\u9519\u8bef", None))
        self.pushButton_3.setText(QCoreApplication.translate("ErrorReport", u"\u5bfc\u51fa\u9519\u8bef\u62a5\u544a", None))
    # retranslateUi

