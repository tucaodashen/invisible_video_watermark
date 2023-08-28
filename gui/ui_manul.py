# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manul.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
import gui.res_rc

class Ui_manul(object):
    def setupUi(self, manul):
        if not manul.objectName():
            manul.setObjectName(u"manul")
        manul.resize(400, 254)
        icon = QIcon()
        icon.addFile(u":/icon/C:/Users/27698/Downloads/reico.ico", QSize(), QIcon.Normal, QIcon.Off)
        manul.setWindowIcon(icon)
        self.widget = QWidget(manul)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 20, 275, 196))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_4.addWidget(self.lineEdit_4)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_5 = QLineEdit(self.widget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_5.addWidget(self.lineEdit_5)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit_6 = QLineEdit(self.widget)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_6.addWidget(self.lineEdit_6)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)


        self.retranslateUi(manul)

        QMetaObject.connectSlotsByName(manul)
    # setupUi

    def retranslateUi(self, manul):
        manul.setWindowTitle(QCoreApplication.translate("manul", u"\u624b\u52a8\u6062\u590d\u6c34\u5370", None))
        self.label.setText(QCoreApplication.translate("manul", u"\u8bf7\u8f93\u5165\u56fe\u7247\u8def\u5f84", None))
        self.label_2.setText(QCoreApplication.translate("manul", u"\u8bf7\u8f93\u5165\u7b2c\u4e00\u4f4d\u968f\u673a\u79cd\u5b50", None))
        self.label_3.setText(QCoreApplication.translate("manul", u"\u8bf7\u8f93\u5165\u7b2c\u4e8c\u4f4d\u968f\u673a\u79cd\u5b50", None))
        self.label_4.setText(QCoreApplication.translate("manul", u"\u8bf7\u8f93\u5165\u6c34\u5370\u8d28\u91cf", None))
        self.label_5.setText(QCoreApplication.translate("manul", u"\u8f93\u5165\u6c34\u5370\u56fe\u7247\u6a2a\u5411\u5206\u8fa8\u7387", None))
        self.label_6.setText(QCoreApplication.translate("manul", u"\u8f93\u5165\u6c34\u5370\u56fe\u7247\u7ad6\u5411\u5206\u8fa8\u7387", None))
        self.pushButton.setText(QCoreApplication.translate("manul", u"\u89e3\u6c34\u5370", None))
    # retranslateUi

