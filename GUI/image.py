# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'image.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QTableWidgetItem,
    QVBoxLayout, QWidget)

from CustomGUI import ImagePreviewWidget
from qfluentwidgets import (BodyLabel, ComboBox, LineEdit, PrimaryPushButton,
    PushButton, RadioButton, SubtitleLabel, TableWidget,
    TextBrowser, TransparentPushButton)

class Ui_ImageProcessWindow(object):
    def setupUi(self, ImageProcessWindow):
        if not ImageProcessWindow.objectName():
            ImageProcessWindow.setObjectName(u"ImageProcessWindow")
        ImageProcessWindow.resize(754, 758)
        self.gridLayout_4 = QGridLayout(ImageProcessWindow)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.ControlFrame = QFrame(ImageProcessWindow)
        self.ControlFrame.setObjectName(u"ControlFrame")
        self.ControlFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ControlFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.ControlFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = SubtitleLabel(self.ControlFrame)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 64))

        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(self.ControlFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 64))
        self.frame.setMaximumSize(QSize(16777215, 128))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.FileList = TableWidget(self.frame)
        self.FileList.setObjectName(u"FileList")
        self.FileList.setMaximumSize(QSize(16777215, 128))

        self.gridLayout_5.addWidget(self.FileList, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.AddImage = PushButton(self.ControlFrame)
        self.AddImage.setObjectName(u"AddImage")

        self.horizontalLayout.addWidget(self.AddImage)

        self.DeleteImage = PushButton(self.ControlFrame)
        self.DeleteImage.setObjectName(u"DeleteImage")

        self.horizontalLayout.addWidget(self.DeleteImage)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.label_2 = SubtitleLabel(self.ControlFrame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.scrollArea = QScrollArea(self.ControlFrame)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -131, 329, 513))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.radioButton = RadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_3.addWidget(self.radioButton)

        self.radioButton_2 = RadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_3.addWidget(self.radioButton_2)

        self.radioButton_3 = RadioButton(self.groupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_3.addWidget(self.radioButton_3)

        self.radioButton_4 = RadioButton(self.groupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout_3.addWidget(self.radioButton_4)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = BodyLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit = LineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = BodyLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineEdit_2 = LineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_3.addWidget(self.lineEdit_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = BodyLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.lineEdit_3 = LineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_4.addWidget(self.lineEdit_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = BodyLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.lineEdit_4 = LineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_5.addWidget(self.lineEdit_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = BodyLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.lineEdit_5 = LineEdit(self.groupBox_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_6.addWidget(self.lineEdit_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = BodyLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_9.addWidget(self.label_8)

        self.comboBox = ComboBox(self.groupBox_3)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_9.addWidget(self.comboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_11.addWidget(self.label_12)

        self.horizontalSlider = QSlider(self.groupBox_3)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(100)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.horizontalSlider)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_11 = BodyLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_8.addWidget(self.label_11)

        self.comboBox_2 = ComboBox(self.groupBox_3)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_8.addWidget(self.comboBox_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = BodyLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_7.addWidget(self.label_9)

        self.lineEdit_6 = LineEdit(self.groupBox_3)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_7.addWidget(self.lineEdit_6)

        self.pushButton_3 = TransparentPushButton(self.groupBox_3)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = BodyLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_10.addWidget(self.label_10)

        self.lineEdit_7 = LineEdit(self.groupBox_3)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.horizontalLayout_10.addWidget(self.lineEdit_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.StartButton = PrimaryPushButton(self.ControlFrame)
        self.StartButton.setObjectName(u"StartButton")

        self.gridLayout.addWidget(self.StartButton, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.ControlFrame, 0, 0, 2, 1)

        self.ImageView = ImagePreviewWidget(ImageProcessWindow)
        self.ImageView.setObjectName(u"ImageView")
        self.ImageView.setFrameShape(QFrame.Shape.StyledPanel)
        self.ImageView.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.ImageView, 0, 1, 1, 1)

        self.ProcessLog = TextBrowser(ImageProcessWindow)
        self.ProcessLog.setObjectName(u"ProcessLog")
        self.ProcessLog.setMaximumSize(QSize(16777215, 256))

        self.gridLayout_4.addWidget(self.ProcessLog, 1, 1, 1, 1)


        self.retranslateUi(ImageProcessWindow)

        QMetaObject.connectSlotsByName(ImageProcessWindow)
    # setupUi

    def retranslateUi(self, ImageProcessWindow):
        ImageProcessWindow.setWindowTitle(QCoreApplication.translate("ImageProcessWindow", u"Frame", None))
        self.label.setText(QCoreApplication.translate("ImageProcessWindow", u"\u6587\u4ef6\u5217\u8868", None))
        self.AddImage.setText(QCoreApplication.translate("ImageProcessWindow", u"PushButton", None))
        self.DeleteImage.setText(QCoreApplication.translate("ImageProcessWindow", u"PushButton", None))
        self.label_2.setText(QCoreApplication.translate("ImageProcessWindow", u"\u5904\u7406\u8bbe\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("ImageProcessWindow", u"\u6c34\u5370\u7b97\u6cd5", None))
        self.radioButton.setText(QCoreApplication.translate("ImageProcessWindow", u"GuoFei", None))
        self.radioButton_2.setText(QCoreApplication.translate("ImageProcessWindow", u"FireKeepers", None))
        self.radioButton_3.setText(QCoreApplication.translate("ImageProcessWindow", u"RivaGan", None))
        self.radioButton_4.setText(QCoreApplication.translate("ImageProcessWindow", u"FreqMethod", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ImageProcessWindow", u"  \u6c34\u5370\u53c2\u6570", None))
        self.label_3.setText(QCoreApplication.translate("ImageProcessWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("ImageProcessWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("ImageProcessWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("ImageProcessWindow", u"TextLabel", None))
        self.label_7.setText(QCoreApplication.translate("ImageProcessWindow", u"TextLabel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ImageProcessWindow", u"\u8f6c\u5316\u8bbe\u7f6e", None))
        self.label_8.setText(QCoreApplication.translate("ImageProcessWindow", u"\u8f93\u51fa\u683c\u5f0f", None))
        self.label_12.setText(QCoreApplication.translate("ImageProcessWindow", u"\u56fe\u7247\u8d28\u91cf", None))
        self.label_11.setText(QCoreApplication.translate("ImageProcessWindow", u"\u8f93\u51fa\u65b9\u5f0f", None))
        self.label_9.setText(QCoreApplication.translate("ImageProcessWindow", u"\u8f93\u51fa\u8def\u5f84", None))
        self.pushButton_3.setText(QCoreApplication.translate("ImageProcessWindow", u"PushButton", None))
        self.label_10.setText(QCoreApplication.translate("ImageProcessWindow", u"\u524d\u7f00", None))
        self.StartButton.setText(QCoreApplication.translate("ImageProcessWindow", u"PushButton", None))
    # retranslateUi

