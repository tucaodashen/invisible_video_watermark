# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting.ui'
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
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    PushButton, ScrollArea, TextBrowser, TitleLabel)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 580)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SettingTitleLabel = TitleLabel(Form)
        self.SettingTitleLabel.setObjectName(u"SettingTitleLabel")

        self.verticalLayout.addWidget(self.SettingTitleLabel)

        self.scrollArea = ScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 768, 571))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.General_label = TitleLabel(self.frame)
        self.General_label.setObjectName(u"General_label")

        self.verticalLayout_2.addWidget(self.General_label)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.LanguageLabel = QLabel(self.frame)
        self.LanguageLabel.setObjectName(u"LanguageLabel")

        self.horizontalLayout_21.addWidget(self.LanguageLabel)

        self.LanguagecomboBox = ComboBox(self.frame)
        self.LanguagecomboBox.setObjectName(u"LanguagecomboBox")

        self.horizontalLayout_21.addWidget(self.LanguagecomboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.CompleteDing = BodyLabel(self.frame)
        self.CompleteDing.setObjectName(u"CompleteDing")

        self.horizontalLayout_2.addWidget(self.CompleteDing)

        self.CompleteDingCheck = CheckBox(self.frame)
        self.CompleteDingCheck.setObjectName(u"CompleteDingCheck")

        self.horizontalLayout_2.addWidget(self.CompleteDingCheck)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_8.addWidget(self.frame)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.FileRelatedLabel = TitleLabel(self.frame_2)
        self.FileRelatedLabel.setObjectName(u"FileRelatedLabel")

        self.verticalLayout_3.addWidget(self.FileRelatedLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.DefaultSaveDictLabel = BodyLabel(self.frame_2)
        self.DefaultSaveDictLabel.setObjectName(u"DefaultSaveDictLabel")

        self.horizontalLayout_3.addWidget(self.DefaultSaveDictLabel)

        self.DefaultSaveDictTextEdit = LineEdit(self.frame_2)
        self.DefaultSaveDictTextEdit.setObjectName(u"DefaultSaveDictTextEdit")

        self.horizontalLayout_3.addWidget(self.DefaultSaveDictTextEdit)

        self.DefaultSaveDictBrowserButton = PushButton(self.frame_2)
        self.DefaultSaveDictBrowserButton.setObjectName(u"DefaultSaveDictBrowserButton")

        self.horizontalLayout_3.addWidget(self.DefaultSaveDictBrowserButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.OutputStructureLabel = BodyLabel(self.frame_2)
        self.OutputStructureLabel.setObjectName(u"OutputStructureLabel")

        self.horizontalLayout_5.addWidget(self.OutputStructureLabel)

        self.OutputStructureComboBox = ComboBox(self.frame_2)
        self.OutputStructureComboBox.setObjectName(u"OutputStructureComboBox")

        self.horizontalLayout_5.addWidget(self.OutputStructureComboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.verticalLayout_8.addWidget(self.frame_2)

        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.DebugLabel = TitleLabel(self.frame_5)
        self.DebugLabel.setObjectName(u"DebugLabel")

        self.verticalLayout_6.addWidget(self.DebugLabel)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.DisplayLogLabel = BodyLabel(self.frame_5)
        self.DisplayLogLabel.setObjectName(u"DisplayLogLabel")

        self.horizontalLayout_14.addWidget(self.DisplayLogLabel)

        self.DisplayLogButton = PushButton(self.frame_5)
        self.DisplayLogButton.setObjectName(u"DisplayLogButton")

        self.horizontalLayout_14.addWidget(self.DisplayLogButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.DumpCoreDataWhenExceptionOccuredLabel = BodyLabel(self.frame_5)
        self.DumpCoreDataWhenExceptionOccuredLabel.setObjectName(u"DumpCoreDataWhenExceptionOccuredLabel")

        self.horizontalLayout_15.addWidget(self.DumpCoreDataWhenExceptionOccuredLabel)

        self.DumpCoreDataWhenExceptionOccuredCheckBox = CheckBox(self.frame_5)
        self.DumpCoreDataWhenExceptionOccuredCheckBox.setObjectName(u"DumpCoreDataWhenExceptionOccuredCheckBox")

        self.horizontalLayout_15.addWidget(self.DumpCoreDataWhenExceptionOccuredCheckBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.BugReportLabel = BodyLabel(self.frame_5)
        self.BugReportLabel.setObjectName(u"BugReportLabel")

        self.horizontalLayout_18.addWidget(self.BugReportLabel)

        self.BugReportButton = PushButton(self.frame_5)
        self.BugReportButton.setObjectName(u"BugReportButton")

        self.horizontalLayout_18.addWidget(self.BugReportButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)


        self.verticalLayout_8.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.VersionLabel = TitleLabel(self.frame_6)
        self.VersionLabel.setObjectName(u"VersionLabel")

        self.gridLayout_2.addWidget(self.VersionLabel, 0, 0, 1, 1)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_7)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.SoftwareVersionLabel = BodyLabel(self.frame_7)
        self.SoftwareVersionLabel.setObjectName(u"SoftwareVersionLabel")
        font = QFont()
        font.setPointSize(20)
        self.SoftwareVersionLabel.setFont(font)

        self.verticalLayout_7.addWidget(self.SoftwareVersionLabel)

        self.SoftwareVersionDetial = TextBrowser(self.frame_7)
        self.SoftwareVersionDetial.setObjectName(u"SoftwareVersionDetial")

        self.verticalLayout_7.addWidget(self.SoftwareVersionDetial)


        self.horizontalLayout_19.addLayout(self.verticalLayout_7)

        self.SoftwareVersionCheckButton = PushButton(self.frame_7)
        self.SoftwareVersionCheckButton.setObjectName(u"SoftwareVersionCheckButton")

        self.horizontalLayout_19.addWidget(self.SoftwareVersionCheckButton)


        self.gridLayout.addLayout(self.horizontalLayout_19, 0, 0, 1, 1)

        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_8)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.AboutLabel = BodyLabel(self.frame_8)
        self.AboutLabel.setObjectName(u"AboutLabel")

        self.horizontalLayout_20.addWidget(self.AboutLabel)

        self.AboutButton = PushButton(self.frame_8)
        self.AboutButton.setObjectName(u"AboutButton")

        self.horizontalLayout_20.addWidget(self.AboutButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_20, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_8, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame_7, 1, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.frame_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.SettingTitleLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.General_label.setText(QCoreApplication.translate("Form", u"\u901a\u7528", None))
        self.LanguageLabel.setText(QCoreApplication.translate("Form", u"\u8bed\u8a00", None))
        self.CompleteDing.setText(QCoreApplication.translate("Form", u"\u5b8c\u6210\u540e\u63d0\u793a\u97f3", None))
        self.CompleteDingCheck.setText("")
        self.FileRelatedLabel.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6", None))
        self.DefaultSaveDictLabel.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u4fdd\u5b58\u76ee\u5f55", None))
        self.DefaultSaveDictBrowserButton.setText(QCoreApplication.translate("Form", u"\u6d4f\u89c8", None))
        self.OutputStructureLabel.setText(QCoreApplication.translate("Form", u"\u8f93\u51fa\u683c\u5f0f", None))
        self.DebugLabel.setText(QCoreApplication.translate("Form", u"Debug", None))
        self.DisplayLogLabel.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u65e5\u5fd7", None))
        self.DisplayLogButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.DumpCoreDataWhenExceptionOccuredLabel.setText(QCoreApplication.translate("Form", u"\u9519\u8bef\u65f6\u6838\u5fc3\u8f6c\u50a8", None))
        self.DumpCoreDataWhenExceptionOccuredCheckBox.setText(QCoreApplication.translate("Form", u"\u91cd\u65b0\u542f\u52a8\u540e\u751f\u6548", None))
        self.BugReportLabel.setText(QCoreApplication.translate("Form", u"\u53cd\u9988Bug", None))
        self.BugReportButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.VersionLabel.setText(QCoreApplication.translate("Form", u"\u7248\u672c", None))
        self.SoftwareVersionLabel.setText(QCoreApplication.translate("Form", u"\u8f6f\u4ef6\u7248\u672c", None))
        self.SoftwareVersionCheckButton.setText(QCoreApplication.translate("Form", u"PushButton", None))
        self.AboutLabel.setText(QCoreApplication.translate("Form", u"\u5173\u4e8e", None))
        self.AboutButton.setText(QCoreApplication.translate("Form", u"\u6253\u5f00", None))
    # retranslateUi

