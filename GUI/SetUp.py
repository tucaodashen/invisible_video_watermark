# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetUp.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CaptionLabel, CheckBox, ComboBox,
    ImageLabel, LineEdit, PushButton, Slider,
    SpinBox, SubtitleLabel, TextBrowser, TitleLabel)

class Ui_SetUpNewForm(object):
    def setupUi(self, SetUpNewForm):
        if not SetUpNewForm.objectName():
            SetUpNewForm.setObjectName(u"SetUpNewForm")
        SetUpNewForm.resize(805, 669)
        self.horizontalLayout_22 = QHBoxLayout(SetUpNewForm)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.scrollArea = QScrollArea(SetUpNewForm)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -453, 377, 1102))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.L_CreateProject = TitleLabel(self.scrollAreaWidgetContents)
        self.L_CreateProject.setObjectName(u"L_CreateProject")

        self.verticalLayout_7.addWidget(self.L_CreateProject)

        self.F_Present = QFrame(self.scrollAreaWidgetContents)
        self.F_Present.setObjectName(u"F_Present")
        self.F_Present.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_Present.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.F_Present)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.L_UsePresent = BodyLabel(self.F_Present)
        self.L_UsePresent.setObjectName(u"L_UsePresent")

        self.horizontalLayout_2.addWidget(self.L_UsePresent)

        self.C_UsePresent = CheckBox(self.F_Present)
        self.C_UsePresent.setObjectName(u"C_UsePresent")

        self.horizontalLayout_2.addWidget(self.C_UsePresent)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.L_SelectPresent = BodyLabel(self.F_Present)
        self.L_SelectPresent.setObjectName(u"L_SelectPresent")

        self.horizontalLayout.addWidget(self.L_SelectPresent)

        self.CB_SelectPresent = ComboBox(self.F_Present)
        self.CB_SelectPresent.setObjectName(u"CB_SelectPresent")

        self.horizontalLayout.addWidget(self.CB_SelectPresent)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_7.addWidget(self.F_Present)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.L_ProjectType = SubtitleLabel(self.scrollAreaWidgetContents)
        self.L_ProjectType.setObjectName(u"L_ProjectType")

        self.horizontalLayout_10.addWidget(self.L_ProjectType)

        self.CB_ProjectType = ComboBox(self.scrollAreaWidgetContents)
        self.CB_ProjectType.setObjectName(u"CB_ProjectType")

        self.horizontalLayout_10.addWidget(self.CB_ProjectType)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.F_Watermark = QFrame(self.scrollAreaWidgetContents)
        self.F_Watermark.setObjectName(u"F_Watermark")
        self.F_Watermark.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_Watermark.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.F_Watermark)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.L_WatermarkSetting = SubtitleLabel(self.F_Watermark)
        self.L_WatermarkSetting.setObjectName(u"L_WatermarkSetting")

        self.verticalLayout_10.addWidget(self.L_WatermarkSetting)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.L_WatermarkAgori = BodyLabel(self.F_Watermark)
        self.L_WatermarkAgori.setObjectName(u"L_WatermarkAgori")

        self.horizontalLayout_11.addWidget(self.L_WatermarkAgori)

        self.CB_WatermarkAgori = ComboBox(self.F_Watermark)
        self.CB_WatermarkAgori.setObjectName(u"CB_WatermarkAgori")

        self.horizontalLayout_11.addWidget(self.CB_WatermarkAgori)


        self.verticalLayout_10.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.L_WatermarkType = BodyLabel(self.F_Watermark)
        self.L_WatermarkType.setObjectName(u"L_WatermarkType")

        self.horizontalLayout_12.addWidget(self.L_WatermarkType)

        self.CB_WatermarkType = ComboBox(self.F_Watermark)
        self.CB_WatermarkType.setObjectName(u"CB_WatermarkType")

        self.horizontalLayout_12.addWidget(self.CB_WatermarkType)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.L_WatermarkContent = BodyLabel(self.F_Watermark)
        self.L_WatermarkContent.setObjectName(u"L_WatermarkContent")

        self.horizontalLayout_13.addWidget(self.L_WatermarkContent)

        self.LE_WatermarkContent = LineEdit(self.F_Watermark)
        self.LE_WatermarkContent.setObjectName(u"LE_WatermarkContent")

        self.horizontalLayout_13.addWidget(self.LE_WatermarkContent)


        self.verticalLayout_10.addLayout(self.horizontalLayout_13)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.L_wmpara1 = CaptionLabel(self.F_Watermark)
        self.L_wmpara1.setObjectName(u"L_wmpara1")

        self.horizontalLayout_26.addWidget(self.L_wmpara1)

        self.LE_wmpara1 = LineEdit(self.F_Watermark)
        self.LE_wmpara1.setObjectName(u"LE_wmpara1")

        self.horizontalLayout_26.addWidget(self.LE_wmpara1)


        self.verticalLayout_5.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.L_wmpara2 = CaptionLabel(self.F_Watermark)
        self.L_wmpara2.setObjectName(u"L_wmpara2")

        self.horizontalLayout_25.addWidget(self.L_wmpara2)

        self.LE_wmpara2 = LineEdit(self.F_Watermark)
        self.LE_wmpara2.setObjectName(u"LE_wmpara2")

        self.horizontalLayout_25.addWidget(self.LE_wmpara2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.L_wmpara3 = CaptionLabel(self.F_Watermark)
        self.L_wmpara3.setObjectName(u"L_wmpara3")

        self.horizontalLayout_24.addWidget(self.L_wmpara3)

        self.LE_wmpara3 = LineEdit(self.F_Watermark)
        self.LE_wmpara3.setObjectName(u"LE_wmpara3")

        self.horizontalLayout_24.addWidget(self.LE_wmpara3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.L_wmpara4 = CaptionLabel(self.F_Watermark)
        self.L_wmpara4.setObjectName(u"L_wmpara4")

        self.horizontalLayout_23.addWidget(self.L_wmpara4)

        self.LE_wmpara4 = LineEdit(self.F_Watermark)
        self.LE_wmpara4.setObjectName(u"LE_wmpara4")

        self.horizontalLayout_23.addWidget(self.LE_wmpara4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_23)


        self.verticalLayout_10.addLayout(self.verticalLayout_5)


        self.verticalLayout_7.addWidget(self.F_Watermark)

        self.F_Video = QFrame(self.scrollAreaWidgetContents)
        self.F_Video.setObjectName(u"F_Video")
        self.F_Video.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_Video.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.F_Video)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.L_VideoProcess = SubtitleLabel(self.F_Video)
        self.L_VideoProcess.setObjectName(u"L_VideoProcess")

        self.verticalLayout_4.addWidget(self.L_VideoProcess)

        self.F_Sampler = QFrame(self.F_Video)
        self.F_Sampler.setObjectName(u"F_Sampler")
        self.F_Sampler.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_Sampler.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.F_Sampler)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.L_Samper = SubtitleLabel(self.F_Sampler)
        self.L_Samper.setObjectName(u"L_Samper")

        self.verticalLayout_2.addWidget(self.L_Samper)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.L_SamplerType = BodyLabel(self.F_Sampler)
        self.L_SamplerType.setObjectName(u"L_SamplerType")

        self.horizontalLayout_6.addWidget(self.L_SamplerType)

        self.CB_Sampler = ComboBox(self.F_Sampler)
        self.CB_Sampler.setObjectName(u"CB_Sampler")

        self.horizontalLayout_6.addWidget(self.CB_Sampler)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.L_SamplerSheet = BodyLabel(self.F_Sampler)
        self.L_SamplerSheet.setObjectName(u"L_SamplerSheet")

        self.horizontalLayout_5.addWidget(self.L_SamplerSheet)

        self.LE_SamplerSheet = LineEdit(self.F_Sampler)
        self.LE_SamplerSheet.setObjectName(u"LE_SamplerSheet")

        self.horizontalLayout_5.addWidget(self.LE_SamplerSheet)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.L_SamplerTimes = BodyLabel(self.F_Sampler)
        self.L_SamplerTimes.setObjectName(u"L_SamplerTimes")

        self.horizontalLayout_4.addWidget(self.L_SamplerTimes)

        self.SB_SamplerTimes = SpinBox(self.F_Sampler)
        self.SB_SamplerTimes.setObjectName(u"SB_SamplerTimes")

        self.horizontalLayout_4.addWidget(self.SB_SamplerTimes)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.L_FrameExtend = BodyLabel(self.F_Sampler)
        self.L_FrameExtend.setObjectName(u"L_FrameExtend")

        self.horizontalLayout_3.addWidget(self.L_FrameExtend)

        self.HS_FrameExtend = Slider(self.F_Sampler)
        self.HS_FrameExtend.setObjectName(u"HS_FrameExtend")
        self.HS_FrameExtend.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.HS_FrameExtend)

        self.SB_FrameExtend = SpinBox(self.F_Sampler)
        self.SB_FrameExtend.setObjectName(u"SB_FrameExtend")

        self.horizontalLayout_3.addWidget(self.SB_FrameExtend)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.F_Sampler)

        self.F_VideoExport = QFrame(self.F_Video)
        self.F_VideoExport.setObjectName(u"F_VideoExport")
        self.F_VideoExport.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_VideoExport.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.F_VideoExport)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.L_VideoExportSetting = SubtitleLabel(self.F_VideoExport)
        self.L_VideoExportSetting.setObjectName(u"L_VideoExportSetting")

        self.verticalLayout_3.addWidget(self.L_VideoExportSetting)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.L_VideoExportPath = BodyLabel(self.F_VideoExport)
        self.L_VideoExportPath.setObjectName(u"L_VideoExportPath")

        self.horizontalLayout_7.addWidget(self.L_VideoExportPath)

        self.LE_VideoExportPath = LineEdit(self.F_VideoExport)
        self.LE_VideoExportPath.setObjectName(u"LE_VideoExportPath")

        self.horizontalLayout_7.addWidget(self.LE_VideoExportPath)

        self.PB_VideoExportPath = PushButton(self.F_VideoExport)
        self.PB_VideoExportPath.setObjectName(u"PB_VideoExportPath")

        self.horizontalLayout_7.addWidget(self.PB_VideoExportPath)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.L_VideoExportFormat = BodyLabel(self.F_VideoExport)
        self.L_VideoExportFormat.setObjectName(u"L_VideoExportFormat")

        self.horizontalLayout_8.addWidget(self.L_VideoExportFormat)

        self.CB_VideoExportFormat = ComboBox(self.F_VideoExport)
        self.CB_VideoExportFormat.setObjectName(u"CB_VideoExportFormat")

        self.horizontalLayout_8.addWidget(self.CB_VideoExportFormat)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.L_RenderDevices = BodyLabel(self.F_VideoExport)
        self.L_RenderDevices.setObjectName(u"L_RenderDevices")

        self.horizontalLayout_27.addWidget(self.L_RenderDevices)

        self.CB_RenderDevices = ComboBox(self.F_VideoExport)
        self.CB_RenderDevices.setObjectName(u"CB_RenderDevices")

        self.horizontalLayout_27.addWidget(self.CB_RenderDevices)


        self.verticalLayout_3.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.L_VideoEncoder = BodyLabel(self.F_VideoExport)
        self.L_VideoEncoder.setObjectName(u"L_VideoEncoder")

        self.horizontalLayout_9.addWidget(self.L_VideoEncoder)

        self.CB_VideoEncoder = ComboBox(self.F_VideoExport)
        self.CB_VideoEncoder.setObjectName(u"CB_VideoEncoder")

        self.horizontalLayout_9.addWidget(self.CB_VideoEncoder)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)


        self.verticalLayout_4.addWidget(self.F_VideoExport)

        self.F_VideoEncoder = QFrame(self.F_Video)
        self.F_VideoEncoder.setObjectName(u"F_VideoEncoder")
        self.F_VideoEncoder.setFrameShape(QFrame.Shape.StyledPanel)
        self.F_VideoEncoder.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.F_VideoEncoder)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.L_VideoEncoderSetting = SubtitleLabel(self.F_VideoEncoder)
        self.L_VideoEncoderSetting.setObjectName(u"L_VideoEncoderSetting")

        self.verticalLayout_6.addWidget(self.L_VideoEncoderSetting)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.L_BitRateControl = BodyLabel(self.F_VideoEncoder)
        self.L_BitRateControl.setObjectName(u"L_BitRateControl")

        self.horizontalLayout_14.addWidget(self.L_BitRateControl)

        self.CB_BitRateControl = ComboBox(self.F_VideoEncoder)
        self.CB_BitRateControl.setObjectName(u"CB_BitRateControl")

        self.horizontalLayout_14.addWidget(self.CB_BitRateControl)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.L_BitRate = BodyLabel(self.F_VideoEncoder)
        self.L_BitRate.setObjectName(u"L_BitRate")

        self.horizontalLayout_15.addWidget(self.L_BitRate)

        self.LE_BitRate = LineEdit(self.F_VideoEncoder)
        self.LE_BitRate.setObjectName(u"LE_BitRate")

        self.horizontalLayout_15.addWidget(self.LE_BitRate)


        self.verticalLayout_6.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.L_MaxBitRate = BodyLabel(self.F_VideoEncoder)
        self.L_MaxBitRate.setObjectName(u"L_MaxBitRate")

        self.horizontalLayout_16.addWidget(self.L_MaxBitRate)

        self.LE_MaxBitRate = LineEdit(self.F_VideoEncoder)
        self.LE_MaxBitRate.setObjectName(u"LE_MaxBitRate")

        self.horizontalLayout_16.addWidget(self.LE_MaxBitRate)


        self.verticalLayout_6.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.L_FFmpegPresent = BodyLabel(self.F_VideoEncoder)
        self.L_FFmpegPresent.setObjectName(u"L_FFmpegPresent")

        self.horizontalLayout_17.addWidget(self.L_FFmpegPresent)

        self.CB_FFmpegPresent = ComboBox(self.F_VideoEncoder)
        self.CB_FFmpegPresent.setObjectName(u"CB_FFmpegPresent")

        self.horizontalLayout_17.addWidget(self.CB_FFmpegPresent)


        self.verticalLayout_6.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.L_Tune = BodyLabel(self.F_VideoEncoder)
        self.L_Tune.setObjectName(u"L_Tune")

        self.horizontalLayout_18.addWidget(self.L_Tune)

        self.CB_Tune = ComboBox(self.F_VideoEncoder)
        self.CB_Tune.setObjectName(u"CB_Tune")

        self.horizontalLayout_18.addWidget(self.CB_Tune)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.L_EncodePattern = BodyLabel(self.F_VideoEncoder)
        self.L_EncodePattern.setObjectName(u"L_EncodePattern")

        self.horizontalLayout_19.addWidget(self.L_EncodePattern)

        self.CB_EncodePattern = ComboBox(self.F_VideoEncoder)
        self.CB_EncodePattern.setObjectName(u"CB_EncodePattern")

        self.horizontalLayout_19.addWidget(self.CB_EncodePattern)


        self.verticalLayout_6.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.CB_Foreward = CheckBox(self.F_VideoEncoder)
        self.CB_Foreward.setObjectName(u"CB_Foreward")

        self.horizontalLayout_28.addWidget(self.CB_Foreward)

        self.SB_Forward = SpinBox(self.F_VideoEncoder)
        self.SB_Forward.setObjectName(u"SB_Forward")

        self.horizontalLayout_28.addWidget(self.SB_Forward)


        self.verticalLayout_6.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.CB_AdjustiveNormalize = CheckBox(self.F_VideoEncoder)
        self.CB_AdjustiveNormalize.setObjectName(u"CB_AdjustiveNormalize")

        self.horizontalLayout_29.addWidget(self.CB_AdjustiveNormalize)

        self.SB_AN = SpinBox(self.F_VideoEncoder)
        self.SB_AN.setObjectName(u"SB_AN")

        self.horizontalLayout_29.addWidget(self.SB_AN)


        self.verticalLayout_6.addLayout(self.horizontalLayout_29)


        self.verticalLayout_4.addWidget(self.F_VideoEncoder)

        self.L_OutputFormat = SubtitleLabel(self.F_Video)
        self.L_OutputFormat.setObjectName(u"L_OutputFormat")

        self.verticalLayout_4.addWidget(self.L_OutputFormat)

        self.CB_OutputFormat = ComboBox(self.F_Video)
        self.CB_OutputFormat.setObjectName(u"CB_OutputFormat")

        self.verticalLayout_4.addWidget(self.CB_OutputFormat)


        self.verticalLayout_7.addWidget(self.F_Video)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_22.addWidget(self.scrollArea)

        self.frame_7 = QFrame(SetUpNewForm)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.L_PreviewImage = ImageLabel(self.frame_7)
        self.L_PreviewImage.setObjectName(u"L_PreviewImage")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.L_PreviewImage.sizePolicy().hasHeightForWidth())
        self.L_PreviewImage.setSizePolicy(sizePolicy)
        self.L_PreviewImage.setMinimumSize(QSize(128, 128))

        self.verticalLayout_9.addWidget(self.L_PreviewImage)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.L_S_OutputPath = BodyLabel(self.frame_7)
        self.L_S_OutputPath.setObjectName(u"L_S_OutputPath")

        self.horizontalLayout_21.addWidget(self.L_S_OutputPath)

        self.L_D_OutputPath = BodyLabel(self.frame_7)
        self.L_D_OutputPath.setObjectName(u"L_D_OutputPath")

        self.horizontalLayout_21.addWidget(self.L_D_OutputPath)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.L_S_CalculateOccupation = BodyLabel(self.frame_7)
        self.L_S_CalculateOccupation.setObjectName(u"L_S_CalculateOccupation")

        self.horizontalLayout_20.addWidget(self.L_S_CalculateOccupation)

        self.L_D_CalculateOccupation = BodyLabel(self.frame_7)
        self.L_D_CalculateOccupation.setObjectName(u"L_D_CalculateOccupation")

        self.horizontalLayout_20.addWidget(self.L_D_CalculateOccupation)


        self.verticalLayout_9.addLayout(self.horizontalLayout_20)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.L_S_DetailArgs = BodyLabel(self.frame_7)
        self.L_S_DetailArgs.setObjectName(u"L_S_DetailArgs")

        self.verticalLayout_8.addWidget(self.L_S_DetailArgs)

        self.TB_S_Detail = TextBrowser(self.frame_7)
        self.TB_S_Detail.setObjectName(u"TB_S_Detail")

        self.verticalLayout_8.addWidget(self.TB_S_Detail)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)


        self.horizontalLayout_22.addWidget(self.frame_7)


        self.retranslateUi(SetUpNewForm)

        QMetaObject.connectSlotsByName(SetUpNewForm)
    # setupUi

    def retranslateUi(self, SetUpNewForm):
        SetUpNewForm.setWindowTitle(QCoreApplication.translate("SetUpNewForm", u"CreateNewProject", None))
        self.L_CreateProject.setText(QCoreApplication.translate("SetUpNewForm", u"\u65b0\u5efa\u5de5\u7a0b", None))
        self.L_UsePresent.setText(QCoreApplication.translate("SetUpNewForm", u"\u4f7f\u7528\u9884\u8bbe", None))
        self.C_UsePresent.setText("")
        self.L_SelectPresent.setText(QCoreApplication.translate("SetUpNewForm", u"\u9009\u62e9\u9884\u8bbe", None))
        self.L_ProjectType.setText(QCoreApplication.translate("SetUpNewForm", u"\u5de5\u7a0b\u7c7b\u578b", None))
        self.L_WatermarkSetting.setText(QCoreApplication.translate("SetUpNewForm", u"\u6c34\u5370\u8bbe\u7f6e", None))
        self.L_WatermarkAgori.setText(QCoreApplication.translate("SetUpNewForm", u"\u6c34\u5370\u7b97\u6cd5", None))
        self.L_WatermarkType.setText(QCoreApplication.translate("SetUpNewForm", u"\u6c34\u5370\u7c7b\u578b", None))
        self.L_WatermarkContent.setText(QCoreApplication.translate("SetUpNewForm", u"\u6c34\u5370\u5185\u5bb9", None))
        self.L_wmpara1.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_wmpara2.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_wmpara3.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_wmpara4.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_VideoProcess.setText(QCoreApplication.translate("SetUpNewForm", u"\u89c6\u9891\u5904\u7406", None))
        self.L_Samper.setText(QCoreApplication.translate("SetUpNewForm", u"\u91c7\u6837\u5668", None))
        self.L_SamplerType.setText(QCoreApplication.translate("SetUpNewForm", u"\u91c7\u6837\u5668\u9009\u62e9", None))
        self.L_SamplerSheet.setText(QCoreApplication.translate("SetUpNewForm", u"\u91c7\u6837\u8868", None))
        self.L_SamplerTimes.setText(QCoreApplication.translate("SetUpNewForm", u"\u91c7\u6837\u6570", None))
        self.L_FrameExtend.setText(QCoreApplication.translate("SetUpNewForm", u"\u5ef6\u7eed\u5904\u7406\u5e27", None))
        self.L_VideoExportSetting.setText(QCoreApplication.translate("SetUpNewForm", u"\u89c6\u9891\u8f93\u51fa\u8bbe\u7f6e", None))
        self.L_VideoExportPath.setText(QCoreApplication.translate("SetUpNewForm", u"\u8f93\u51fa\u8def\u5f84", None))
        self.PB_VideoExportPath.setText(QCoreApplication.translate("SetUpNewForm", u"PushButton", None))
        self.L_VideoExportFormat.setText(QCoreApplication.translate("SetUpNewForm", u"\u8f93\u51fa\u683c\u5f0f", None))
        self.L_RenderDevices.setText(QCoreApplication.translate("SetUpNewForm", u"\u6e32\u67d3\u8bbe\u5907", None))
        self.L_VideoEncoder.setText(QCoreApplication.translate("SetUpNewForm", u"\u89c6\u9891\u7f16\u7801\u5668", None))
        self.L_VideoEncoderSetting.setText(QCoreApplication.translate("SetUpNewForm", u"\u89c6\u9891\u7f16\u7801\u5668\u8bbe\u7f6e", None))
        self.L_BitRateControl.setText(QCoreApplication.translate("SetUpNewForm", u"\u6bd4\u7279\u7387\u63a7\u5236", None))
        self.L_BitRate.setText(QCoreApplication.translate("SetUpNewForm", u"\u6bd4\u7279\u7387", None))
        self.L_MaxBitRate.setText(QCoreApplication.translate("SetUpNewForm", u"\u6700\u5927\u6bd4\u7279\u7387", None))
        self.L_FFmpegPresent.setText(QCoreApplication.translate("SetUpNewForm", u"\u9884\u8bbe", None))
        self.L_Tune.setText(QCoreApplication.translate("SetUpNewForm", u"\u8c03\u8282", None))
        self.L_EncodePattern.setText(QCoreApplication.translate("SetUpNewForm", u"\u7f16\u7801\u6a21\u5f0f", None))
        self.CB_Foreward.setText(QCoreApplication.translate("SetUpNewForm", u"\u524d\u5411\u8003\u8651", None))
        self.CB_AdjustiveNormalize.setText(QCoreApplication.translate("SetUpNewForm", u"\u81ea\u9002\u5e94\u91cf\u5316", None))
        self.L_OutputFormat.setText(QCoreApplication.translate("SetUpNewForm", u"\u8f93\u51fa\u683c\u5f0f", None))
        self.L_PreviewImage.setText("")
        self.L_S_OutputPath.setText(QCoreApplication.translate("SetUpNewForm", u"\u8f93\u51fa\u8def\u5f84", None))
        self.L_D_OutputPath.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_S_CalculateOccupation.setText(QCoreApplication.translate("SetUpNewForm", u"\u9884\u8ba1\u5927\u5c0f", None))
        self.L_D_CalculateOccupation.setText(QCoreApplication.translate("SetUpNewForm", u"TextLabel", None))
        self.L_S_DetailArgs.setText(QCoreApplication.translate("SetUpNewForm", u"\u8be6\u7ec6\u53c2\u6570", None))
    # retranslateUi

