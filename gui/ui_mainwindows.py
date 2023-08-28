# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindows.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)
import gui.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(612, 409)
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.genimg = QAction(MainWindow)
        self.genimg.setObjectName(u"genimg")
        self.recqrcode = QAction(MainWindow)
        self.recqrcode.setObjectName(u"recqrcode")
        self.genqrcode = QAction(MainWindow)
        self.genqrcode.setObjectName(u"genqrcode")
        self.initialflodar = QAction(MainWindow)
        self.initialflodar.setObjectName(u"initialflodar")
        self.recover = QAction(MainWindow)
        self.recover.setObjectName(u"recover")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.manr = QAction(MainWindow)
        self.manr.setObjectName(u"manr")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 583, 356))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Source Han Sans Bold"])
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.videofile = QLineEdit(self.layoutWidget)
        self.videofile.setObjectName(u"videofile")
        self.videofile.setFont(font)

        self.verticalLayout.addWidget(self.videofile)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.imagefile = QLineEdit(self.layoutWidget)
        self.imagefile.setObjectName(u"imagefile")
        self.imagefile.setFont(font)

        self.verticalLayout.addWidget(self.imagefile)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.browservideo = QPushButton(self.layoutWidget)
        self.browservideo.setObjectName(u"browservideo")
        self.browservideo.setFont(font)

        self.verticalLayout_2.addWidget(self.browservideo)

        self.browserimage = QPushButton(self.layoutWidget)
        self.browserimage.setObjectName(u"browserimage")
        self.browserimage.setFont(font)

        self.verticalLayout_2.addWidget(self.browserimage)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.imagewm = QRadioButton(self.layoutWidget)
        self.imagewm.setObjectName(u"imagewm")
        self.imagewm.setFont(font)
        self.imagewm.setTabletTracking(False)
        self.imagewm.setChecked(True)

        self.horizontalLayout_2.addWidget(self.imagewm)

        self.textwm = QRadioButton(self.layoutWidget)
        self.textwm.setObjectName(u"textwm")
        self.textwm.setFont(font)

        self.horizontalLayout_2.addWidget(self.textwm)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.wm_quality = QSpinBox(self.layoutWidget)
        self.wm_quality.setObjectName(u"wm_quality")
        self.wm_quality.setFont(font)
        self.wm_quality.setFrame(False)
        self.wm_quality.setMinimum(1)
        self.wm_quality.setMaximum(200)
        self.wm_quality.setSingleStep(1)
        self.wm_quality.setValue(35)

        self.horizontalLayout_3.addWidget(self.wm_quality)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.filttype = QComboBox(self.layoutWidget)
        self.filttype.addItem("")
        self.filttype.addItem("")
        self.filttype.addItem("")
        self.filttype.addItem("")
        self.filttype.setObjectName(u"filttype")
        self.filttype.setFont(font)

        self.horizontalLayout_5.addWidget(self.filttype)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.layoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_13)

        self.sampletime = QSpinBox(self.layoutWidget)
        self.sampletime.setObjectName(u"sampletime")
        self.sampletime.setFont(font)
        self.sampletime.setMinimum(1)
        self.sampletime.setMaximum(9999)
        self.sampletime.setValue(10)

        self.horizontalLayout_11.addWidget(self.sampletime)


        self.verticalLayout_7.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_14 = QLabel(self.layoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_14)

        self.peroid = QSpinBox(self.layoutWidget)
        self.peroid.setObjectName(u"peroid")
        self.peroid.setFont(font)
        self.peroid.setMinimum(1)
        self.peroid.setMaximum(9999)
        self.peroid.setValue(1)

        self.horizontalLayout_10.addWidget(self.peroid)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)


        self.verticalLayout_3.addLayout(self.verticalLayout_7)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 1, 0, 1, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_5.addWidget(self.label_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_4.addWidget(self.comboBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_8)

        self.vtype = QComboBox(self.layoutWidget)
        self.vtype.addItem("")
        self.vtype.addItem("")
        self.vtype.addItem("")
        self.vtype.addItem("")
        self.vtype.setObjectName(u"vtype")
        self.vtype.setFont(font)

        self.horizontalLayout_6.addWidget(self.vtype)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_9)

        self.output = QLineEdit(self.layoutWidget)
        self.output.setObjectName(u"output")
        self.output.setFont(font)

        self.horizontalLayout_7.addWidget(self.output)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.verticalLayout_5.addWidget(self.label_10)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_11)

        self.dkbps = QLineEdit(self.layoutWidget)
        self.dkbps.setObjectName(u"dkbps")
        self.dkbps.setFont(font)

        self.horizontalLayout_8.addWidget(self.dkbps)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_12)

        self.maxkbps = QLineEdit(self.layoutWidget)
        self.maxkbps.setObjectName(u"maxkbps")
        self.maxkbps.setFont(font)

        self.horizontalLayout_9.addWidget(self.maxkbps)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.gridLayout_2.addLayout(self.verticalLayout_5, 1, 1, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.processbar_bo = QProgressBar(self.layoutWidget)
        self.processbar_bo.setObjectName(u"processbar_bo")
        self.processbar_bo.setFont(font)
        self.processbar_bo.setValue(0)

        self.horizontalLayout_12.addWidget(self.processbar_bo)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.buton_start = QPushButton(self.layoutWidget)
        self.buton_start.setObjectName(u"buton_start")
        self.buton_start.setFont(font)

        self.verticalLayout_6.addWidget(self.buton_start)

        self.stopbutton = QPushButton(self.layoutWidget)
        self.stopbutton.setObjectName(u"stopbutton")

        self.verticalLayout_6.addWidget(self.stopbutton)


        self.horizontalLayout_12.addLayout(self.verticalLayout_6)


        self.verticalLayout_8.addLayout(self.horizontalLayout_12)

        self.operation_label = QLabel(self.layoutWidget)
        self.operation_label.setObjectName(u"operation_label")
        self.operation_label.setFont(font)

        self.verticalLayout_8.addWidget(self.operation_label)


        self.gridLayout_2.addLayout(self.verticalLayout_8, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 612, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.about = QMenu(self.menubar)
        self.about.setObjectName(u"about")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.about.menuAction())
        self.menu.addAction(self.genimg)
        self.menu.addAction(self.recqrcode)
        self.menu.addAction(self.genqrcode)
        self.menu.addAction(self.manr)
        self.menu.addAction(self.recover)
        self.about.addAction(self.actionabout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e0d\u53ef\u89c1\u6c34\u5370\u5de5\u5177  codeby\uff1a\u5410\u69fd\u5927\u795e_Official", None))
        self.genimg.setText(QCoreApplication.translate("MainWindow", u"\u6587\u5b57\u751f\u6210\u56fe\u7247", None))
        self.recqrcode.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u8bc6\u522b", None))
        self.genqrcode.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u751f\u6210", None))
        self.initialflodar.setText(QCoreApplication.translate("MainWindow", u"\u521d\u59cb\u5316\u6587\u4ef6\u5939", None))
        self.recover.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u6c34\u5370", None))
        self.actionabout.setText(QCoreApplication.translate("MainWindow", u"about", None))
        self.manr.setText(QCoreApplication.translate("MainWindow", u"\u624b\u52a8\u8bfb\u53d6\u6c34\u5370", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5370\uff08\u5982\u679c\u4e3a\u56fe\u7247\u6c34\u5370\u5219\u4e3a\u56fe\u7247\u8def\u5f84\uff0c\u6587\u5b57\u6c34\u5370\u4e3a\u5185\u5bb9\uff09", None))
        self.browservideo.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.browserimage.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5370\u8bbe\u7f6e", None))
        self.imagewm.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u6c34\u5370", None))
        self.textwm.setText(QCoreApplication.translate("MainWindow", u"\u6587\u5b57\u6c34\u5370", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6c34\u5370\u6297\u5e72\u6270\u6027   \u6570\u503c\u8d8a\u5927\u8d8a\u6297\u5e72\u6270\uff0c\u4f46\u753b\u8d28\u4f1a\u964d\u4f4e", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u6b64\u9009\u9879\u5728\u6587\u5b57\u6c34\u5370\u4e0b\u65e0\u6548", None))
        self.filttype.setItemText(0, QCoreApplication.translate("MainWindow", u".png", None))
        self.filttype.setItemText(1, QCoreApplication.translate("MainWindow", u".jpg", None))
        self.filttype.setItemText(2, QCoreApplication.translate("MainWindow", u".jpeg", None))
        self.filttype.setItemText(3, QCoreApplication.translate("MainWindow", u".bmp", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u683c\u5f0f(\u7a0b\u5e8f\u5904\u7406\u65f6\u6240\u7528\u7684\u683c\u5f0f\uff0c\u5efa\u8bae\u9009\u62e9png)", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u6837\u6570", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u91c7\u6837\u5e27\u5ef6\u7eed", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u8bbe\u7f6e", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u89c6\u9891", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None))

        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u683c\u5f0f", None))
        self.vtype.setItemText(0, QCoreApplication.translate("MainWindow", u".mp4", None))
        self.vtype.setItemText(1, QCoreApplication.translate("MainWindow", u".avi", None))
        self.vtype.setItemText(2, QCoreApplication.translate("MainWindow", u".mkv", None))
        self.vtype.setItemText(3, QCoreApplication.translate("MainWindow", u".flv", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u540d", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u7801\u8bbe\u7f6e", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u7801\u7387(kbps)", None))
        self.dkbps.setText(QCoreApplication.translate("MainWindow", u"10000", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u6700\u9ad8\u7801\u7387(kbps)", None))
        self.maxkbps.setText(QCoreApplication.translate("MainWindow", u"15000", None))
        self.buton_start.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb", None))
        self.stopbutton.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62", None))
        self.operation_label.setText(QCoreApplication.translate("MainWindow", u"\u7b49\u5f85\u4e2d....", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.about.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi

