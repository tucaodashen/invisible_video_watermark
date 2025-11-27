# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindows.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

from CustomGUI import (DropFrame, DropList, RightClickButton)
from qfluentwidgets import (BodyLabel, CaptionLabel, ImageLabel, LineEdit,
    PrimaryPushButton, ProgressBar, PushButton, SubtitleLabel,
    TableWidget, TitleLabel, TransparentPushButton)
from . import allin_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 1105)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_3 = QAction(MainWindow)
        self.action_3.setObjectName(u"action_3")
        self.action_4 = QAction(MainWindow)
        self.action_4.setObjectName(u"action_4")
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_6 = QAction(MainWindow)
        self.action_6.setObjectName(u"action_6")
        self.action_7 = QAction(MainWindow)
        self.action_7.setObjectName(u"action_7")
        self.actionBug = QAction(MainWindow)
        self.actionBug.setObjectName(u"actionBug")
        self.action_8 = QAction(MainWindow)
        self.action_8.setObjectName(u"action_8")
        self.actionVizTracer = QAction(MainWindow)
        self.actionVizTracer.setObjectName(u"actionVizTracer")
        self.action_9 = QAction(MainWindow)
        self.action_9.setObjectName(u"action_9")
        self.action_10 = QAction(MainWindow)
        self.action_10.setObjectName(u"action_10")
        self.action_11 = QAction(MainWindow)
        self.action_11.setObjectName(u"action_11")
        self.action_12 = QAction(MainWindow)
        self.action_12.setObjectName(u"action_12")
        self.action_13 = QAction(MainWindow)
        self.action_13.setObjectName(u"action_13")
        self.action_14 = QAction(MainWindow)
        self.action_14.setObjectName(u"action_14")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.QueueLabel = SubtitleLabel(self.centralwidget)
        self.QueueLabel.setObjectName(u"QueueLabel")

        self.horizontalLayout_9.addWidget(self.QueueLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.StartButton = PrimaryPushButton(self.centralwidget)
        self.StartButton.setObjectName(u"StartButton")

        self.horizontalLayout_9.addWidget(self.StartButton)

        self.PauseButton = TransparentPushButton(self.centralwidget)
        self.PauseButton.setObjectName(u"PauseButton")

        self.horizontalLayout_9.addWidget(self.PauseButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.QueueList = TableWidget(self.frame_2)
        self.QueueList.setObjectName(u"QueueList")

        self.gridLayout_2.addWidget(self.QueueList, 0, 0, 1, 1)


        self.verticalLayout_7.addWidget(self.frame_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.QueueProgressBar = ProgressBar(self.centralwidget)
        self.QueueProgressBar.setObjectName(u"QueueProgressBar")
        self.QueueProgressBar.setValue(24)

        self.horizontalLayout_10.addWidget(self.QueueProgressBar)

        self.L_TotalProgress = BodyLabel(self.centralwidget)
        self.L_TotalProgress.setObjectName(u"L_TotalProgress")

        self.horizontalLayout_10.addWidget(self.L_TotalProgress)

        self.StopButton = TransparentPushButton(self.centralwidget)
        self.StopButton.setObjectName(u"StopButton")

        self.horizontalLayout_10.addWidget(self.StopButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        self.menu_6 = QMenu(self.menubar)
        self.menu_6.setObjectName(u"menu_6")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MediaBrowserDock = QDockWidget(MainWindow)
        self.MediaBrowserDock.setObjectName(u"MediaBrowserDock")
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.gridLayout = QGridLayout(self.dockWidgetContents_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.dockWidgetContents_4)
        self.tabWidget.setObjectName(u"tabWidget")
        self.quickaction = QWidget()
        self.quickaction.setObjectName(u"quickaction")
        self.gridLayout_4 = QGridLayout(self.quickaction)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.SingleInputSelector = DropFrame(self.quickaction)
        self.SingleInputSelector.setObjectName(u"SingleInputSelector")
        self.SingleInputSelector.setFrameShape(QFrame.Shape.StyledPanel)
        self.SingleInputSelector.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.SingleInputSelector)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.SingleSelectLabel = BodyLabel(self.SingleInputSelector)
        self.SingleSelectLabel.setObjectName(u"SingleSelectLabel")

        self.verticalLayout_5.addWidget(self.SingleSelectLabel)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.SLTL = LineEdit(self.SingleInputSelector)
        self.SLTL.setObjectName(u"SLTL")

        self.horizontalLayout_7.addWidget(self.SLTL)

        self.SLBrowser = TransparentPushButton(self.SingleInputSelector)
        self.SLBrowser.setObjectName(u"SLBrowser")

        self.horizontalLayout_7.addWidget(self.SLBrowser)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.SLOpen = RightClickButton(self.SingleInputSelector)
        self.SLOpen.setObjectName(u"SLOpen")

        self.verticalLayout_5.addWidget(self.SLOpen)


        self.gridLayout_4.addWidget(self.SingleInputSelector, 0, 0, 1, 1)

        self.MultipleProcessSelector = DropFrame(self.quickaction)
        self.MultipleProcessSelector.setObjectName(u"MultipleProcessSelector")
        self.MultipleProcessSelector.setFrameShape(QFrame.Shape.StyledPanel)
        self.MultipleProcessSelector.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.MultipleProcessSelector)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.MLLabel = BodyLabel(self.MultipleProcessSelector)
        self.MLLabel.setObjectName(u"MLLabel")

        self.verticalLayout_6.addWidget(self.MLLabel)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.MLTL = LineEdit(self.MultipleProcessSelector)
        self.MLTL.setObjectName(u"MLTL")

        self.horizontalLayout_8.addWidget(self.MLTL)

        self.MLBrowser = TransparentPushButton(self.MultipleProcessSelector)
        self.MLBrowser.setObjectName(u"MLBrowser")

        self.horizontalLayout_8.addWidget(self.MLBrowser)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.MFOpen = RightClickButton(self.MultipleProcessSelector)
        self.MFOpen.setObjectName(u"MFOpen")

        self.verticalLayout_6.addWidget(self.MFOpen)


        self.gridLayout_4.addWidget(self.MultipleProcessSelector, 1, 0, 1, 1)

        self.tabWidget.addTab(self.quickaction, "")
        self.browser = QWidget()
        self.browser.setObjectName(u"browser")
        self.gridLayout_5 = QGridLayout(self.browser)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.MediaSelectorTips = BodyLabel(self.browser)
        self.MediaSelectorTips.setObjectName(u"MediaSelectorTips")

        self.horizontalLayout_4.addWidget(self.MediaSelectorTips)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.MediaSelector = TableWidget(self.browser)
        self.MediaSelector.setObjectName(u"MediaSelector")

        self.verticalLayout_3.addWidget(self.MediaSelector)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.DeleteSelected = PushButton(self.browser)
        self.DeleteSelected.setObjectName(u"DeleteSelected")

        self.horizontalLayout_5.addWidget(self.DeleteSelected)

        self.UseSelected = PrimaryPushButton(self.browser)
        self.UseSelected.setObjectName(u"UseSelected")

        self.horizontalLayout_5.addWidget(self.UseSelected)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.gridLayout_5.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.browser, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.MediaBrowserDock.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.MediaBrowserDock)
        self.PresentBrowserDock = QDockWidget(MainWindow)
        self.PresentBrowserDock.setObjectName(u"PresentBrowserDock")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.gridLayout_3 = QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_Present = SubtitleLabel(self.dockWidgetContents_3)
        self.label_Present.setObjectName(u"label_Present")

        self.gridLayout_3.addWidget(self.label_Present, 0, 0, 1, 1)

        self.PresentList = DropList(self.dockWidgetContents_3)
        self.PresentList.setObjectName(u"PresentList")

        self.gridLayout_3.addWidget(self.PresentList, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.CreatePresentButton = PrimaryPushButton(self.dockWidgetContents_3)
        self.CreatePresentButton.setObjectName(u"CreatePresentButton")

        self.horizontalLayout_6.addWidget(self.CreatePresentButton)

        self.DeletePresentButton = PushButton(self.dockWidgetContents_3)
        self.DeletePresentButton.setObjectName(u"DeletePresentButton")

        self.horizontalLayout_6.addWidget(self.DeletePresentButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.PresentBrowserDock.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.PresentBrowserDock)
        self.StatusDock = QDockWidget(MainWindow)
        self.StatusDock.setObjectName(u"StatusDock")
        self.StatusDock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable|QDockWidget.DockWidgetFeature.DockWidgetFloatable|QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.StatusDock.setDockLocation(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.SourceLabel = TitleLabel(self.dockWidgetContents_5)
        self.SourceLabel.setObjectName(u"SourceLabel")

        self.horizontalLayout_2.addWidget(self.SourceLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.progressBar = ProgressBar(self.dockWidgetContents_5)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.StartTimeLabel = BodyLabel(self.dockWidgetContents_5)
        self.StartTimeLabel.setObjectName(u"StartTimeLabel")

        self.horizontalLayout.addWidget(self.StartTimeLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.ComsumedTimeLabel = BodyLabel(self.dockWidgetContents_5)
        self.ComsumedTimeLabel.setObjectName(u"ComsumedTimeLabel")

        self.horizontalLayout.addWidget(self.ComsumedTimeLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.frame = QFrame(self.dockWidgetContents_5)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.DetailInfomation = SubtitleLabel(self.frame)
        self.DetailInfomation.setObjectName(u"DetailInfomation")

        self.horizontalLayout_3.addWidget(self.DetailInfomation)

        self.horizontalSpacer_4 = QSpacerItem(1556, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.gridLayout_6.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)

        self.label_10 = ImageLabel(self.frame)
        self.label_10.setObjectName(u"label_10")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(192, 108))
        self.label_10.setMaximumSize(QSize(192, 108))
        self.label_10.setPixmap(QPixmap(u":/MainWindow/C:/Users/ASUS/Desktop/G0DtOFdaQAEjRZC.jpg"))
        self.label_10.setScaledContents(True)
        self.label_10.setWordWrap(False)
        self.label_10.setOpenExternalLinks(False)

        self.gridLayout_6.addWidget(self.label_10, 1, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.FileNameLabel = CaptionLabel(self.frame)
        self.FileNameLabel.setObjectName(u"FileNameLabel")

        self.verticalLayout_2.addWidget(self.FileNameLabel)

        self.FilePathLabel = CaptionLabel(self.frame)
        self.FilePathLabel.setObjectName(u"FilePathLabel")

        self.verticalLayout_2.addWidget(self.FilePathLabel)

        self.FileFormatLabel = CaptionLabel(self.frame)
        self.FileFormatLabel.setObjectName(u"FileFormatLabel")

        self.verticalLayout_2.addWidget(self.FileFormatLabel)

        self.ProjectPresentLabel = CaptionLabel(self.frame)
        self.ProjectPresentLabel.setObjectName(u"ProjectPresentLabel")

        self.verticalLayout_2.addWidget(self.ProjectPresentLabel)

        self.VideoInfoLabel = CaptionLabel(self.frame)
        self.VideoInfoLabel.setObjectName(u"VideoInfoLabel")

        self.verticalLayout_2.addWidget(self.VideoInfoLabel)

        self.BitRateLabel = CaptionLabel(self.frame)
        self.BitRateLabel.setObjectName(u"BitRateLabel")

        self.verticalLayout_2.addWidget(self.BitRateLabel)

        self.AudioLabel = CaptionLabel(self.frame)
        self.AudioLabel.setObjectName(u"AudioLabel")

        self.verticalLayout_2.addWidget(self.AudioLabel)


        self.gridLayout_6.addLayout(self.verticalLayout_2, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.frame)

        self.StatusDock.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.StatusDock)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_10)
        self.menu_2.addAction(self.action_4)
        self.menu_3.addAction(self.action_9)
        self.menu_4.addAction(self.action_5)
        self.menu_4.addAction(self.action_6)
        self.menu_4.addAction(self.action_7)
        self.menu_4.addAction(self.action_14)
        self.menu_6.addAction(self.action_11)
        self.menu_6.addAction(self.action_12)
        self.menu_6.addAction(self.action_13)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.action_3.setText(QCoreApplication.translate("MainWindow", u"\u53e6\u5b58\u4e3a", None))
        self.action_4.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9009\u9879", None))
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u5de5\u5177", None))
        self.action_6.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u8bc6\u522b", None))
        self.action_7.setText(QCoreApplication.translate("MainWindow", u"\u8d85\u5206\u8fa8\u7387", None))
        self.actionBug.setText(QCoreApplication.translate("MainWindow", u"Bug\u6c47\u62a5", None))
        self.action_8.setText(QCoreApplication.translate("MainWindow", u"\u6838\u5fc3\u8f6c\u50a8", None))
        self.actionVizTracer.setText(QCoreApplication.translate("MainWindow", u"VizTracer", None))
        self.action_9.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u6240\u6709", None))
        self.action_10.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u8bc1\u4e66", None))
        self.action_11.setText(QCoreApplication.translate("MainWindow", u"\u6587\u6863", None))
        self.action_12.setText(QCoreApplication.translate("MainWindow", u"\u8bb8\u53ef\u8bc1", None))
        self.action_13.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.action_14.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d\u6c34\u5370\u5185\u5bb9", None))
        self.QueueLabel.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u52a1\u961f\u5217", None))
        self.StartButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.PauseButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.L_TotalProgress.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.StopButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.menu_6.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.SingleSelectLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.SLBrowser.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.SLOpen.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.MLLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.MLBrowser.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.MFOpen.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.quickaction), QCoreApplication.translate("MainWindow", u"\u5feb\u6377\u5bfc\u5165", None))
        self.MediaSelectorTips.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.DeleteSelected.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u6240\u9009", None))
        self.UseSelected.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u6240\u9009", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.browser), QCoreApplication.translate("MainWindow", u"\u5a92\u4f53\u6d4f\u89c8\u5668", None))
        self.label_Present.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.CreatePresentButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.DeletePresentButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.SourceLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.StartTimeLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ComsumedTimeLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.DetailInfomation.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_10.setText("")
        self.FileNameLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.FilePathLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.FileFormatLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ProjectPresentLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.VideoInfoLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.BitRateLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.AudioLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

