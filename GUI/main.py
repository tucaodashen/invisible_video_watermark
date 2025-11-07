import os.path
import random
import cv2
from BasicSystem import const
from modules import ProcessUnit
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QVBoxLayout
from PySide6.QtCore import Qt,QTimer
from qfluentwidgets import FluentIcon as FIF, FlyoutViewBase, Flyout, InfoBarIcon

from GUI.Splash import Ui_SplashDesu
from GUI.MainWindows import Ui_MainWindow
from GUI.Setting import Ui_Form as Ui_Setting
from GUI.SetUp import Ui_SetUpNewForm

import sys
import threading
from GUI import PrepareRequirements
import gettext
from PySide6.QtCore import Qt
from modules import pltform



_ = gettext.gettext


from qfluentwidgets import Dialog, setTheme, Theme, PrimaryPushButton, MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel




class SettingUi_L(QFrame,Ui_Setting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_text()

    def set_text(self):
        self.setWindowTitle(_("设置"))
        self.SettingTitleLabel.setText(_("设置"))
        self.General_label.setText(_("通用设置"))
        self.LanguageLabel.setText(_("语言/Language/言語"))
        self.LanguagecomboBox.addItem(_("中文(简体)"),"zh_CN")
        self.LanguagecomboBox.addItem(_("中文(繁體)"),"zh_TW")
        self.LanguagecomboBox.addItem(_("English"),"en_US")
        self.LanguagecomboBox.addItem(_("日本語"),"ja_JP")
        self.StartPageLabel.setText(_("开始页"))
        self.StartPageCombo.addItem(_("视频水印主页面"))
        self.StartPageCombo.addItem(_("图片水印主页面"))
        self.StartPageCombo.addItem(_("解码主页面"))
        self.CompleteDing.setText(_("完成时声音提醒"))
        self.FileRelatedLabel.setText(_("文件相关设置"))
        self.DefaultSaveDictTextEdit.setPlaceholderText(_("默认保存路径"))
        self.DefaultSaveDictLabel.setText(_("默认保存路径"))
        self.DefaultSaveDictBrowserButton.setText(_("浏览"))
        self.CacheDirLabel.setText(_("缓存目录"))
        self.CacheDirTL.setPlaceholderText(_("缓存目录"))
        self.CacheBrowButton.setText(_("浏览"))
        self.OutputStructureLabel.setText(_("输出结构"))
        self.OutputStructureComboBox.addItem(_("目录"),"dir")
        self.OutputStructureComboBox.addItem(_("压缩文件(ZIP)"),"zip-file")
        self.SoftwareVersionDetial.setText(_("InvisibleWatermarkToolboxNEXT ParySoftware © 2020-2025 All rights reserved.\nThis software is licensed under the MIT license.\nVersion:{version}").format(version=_("0.1 Alpha_α")))
        self.VideoSetting.setText(_("视频设置"))
        self.DefaultEncoderLabel.setText(_("默认编码器"))
        self.DefaultEncoder_comboBox_4.addItem(_("CPU编码器"),"CPU")
        self.DefaultEncoder_comboBox_4.addItem(_("GPU编码器"),"GPU")
        self.DefaultQualityControl.addItem(_("CRF"),"CRF")
        self.DefaultQualityControl.addItem(_("CBR"),"CBR")
        self.DefaultQualityControl.addItem(_("VBR"),"VBR")
        self.DefaultQualityControl.addItem(_("CVBR"),"CVBR")
        self.QualityControl.setText(_("质量控制"))
        self.MaximumBitRateLabel.setText(_("最大码率"))
        self.TargetBitrateLabel.setText(_("目标码率"))
        self.DefaultTargetLabel.setText(_("默认目标格式"))
        self.TargetFormatDefaultComboBox.addItem(_("MP4"),"mp4")
        self.TargetFormatDefaultComboBox.addItem(_("MKV"),"mkv")
        self.TargetFormatDefaultComboBox.addItem(_("AVI"),"avi")
        self.ProcessSettingLabel.setText(_("处理设置"))
        self.DefaultWatermarkMethod.setText(_("默认水印方法"))
        self.DefaultMethodComboBox.addItem(_("图片水印(FireKeeper)"),"FK_Image")
        self.DefaultMethodComboBox.addItem(_("图片水印(GuoFei)"),"GF_Image")
        self.DefaultMethodComboBox.addItem(_("文字水印(GuoFei)"),"GF_Text")
        self.DefaultMethodComboBox.addItem(_("文字水印(ShieldMint)"),"SM_Text")
        self.PerTaskPararllelCountLabel.setText(_("任务并行数"))
        self.PerProjMaxProcessLabel.setText(_("单任务最大进程数"))
        self.DisplayLogLabel.setText(_("显示日志"))
        self.DisplayLogButton.setText(_("显示"))
        self.DumpCoreDataWhenExceptionOccuredLabel.setText(_("发生异常时转储核心数据"))
        self.DumpCoreDataWhenExceptionOccuredCheckBox.setText(_("重启后生效"))
        self.ManualCoreDump.setText(_("手动转储核心数据"))
        self.ManualCoreDumpCheckBox.setText(_("重启后生效"))
        self.ManualCoreDumpShortCutLabel.setText(_("手动转储快捷键"))
        self.BugReportLabel.setText(_("报告错误"))
        self.BugReportButton.setText(_("报告"))
        self.VersionLabel.setText(_("版本信息"))
        self.SoftwareVersionLabel.setText(_("软件版本"))
        self.SoftwareVersionCheckButton.setText(_("检查更新"))




class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.pu_thread = None
        self.pu = None
        self.setupUi(self)
        self.statusbar.showMessage(_("准备就绪"))
        self.set_text()
        self.set_slot()
        setTheme(Theme.DARK)
        self.action_9.triggered.connect(self.show_all)
        self.settingUI = CreateNewProject("1")
        self.settingUI.show()
        self.setButtons()

    def set_slot(self):
        pass

    def setButtons(self):
        self.StartButton.clicked.connect(self.start_render)

    def start_render(self):
        pu = ProcessUnit.ProcessUnit()
        pu.update_progress.connect(self.set_progess_bar)
        threading.Thread(target=pu.run).start()

    def set_progess_bar(self, value, message):
        self.QueueProgressBar.setValue(value*100)
        self.statusbar.showMessage(message)

    def set_text(self):
        self.QueueLabel.setText(_("渲染队列"))
        self.tabWidget.setTabText(0, _("快捷导入"))
        self.tabWidget.setTabText(1, _("媒体浏览器"))
        self.label_Present.setText(_("预设"))
        self.CreatePresentButton.setText(_("创建新模板"))
        self.EditPresentButton.setText(_("编辑模板"))
        self.DeletePresentButton.setText(_("删除模板"))
        self.MediaSelectorTips.setText(_("请选择媒体文件"))
        self.DeleteSelected.setText(_("删除选中"))
        self.UseSelected.setText(_("使用选中"))
        self.SourceLabel.setText(_("源文件:{path}").format(path=_("当前无任务")))
        self.StartTimeLabel.setText(_("开始时间:{time}").format(time=""))
        self.ComsumedTimeLabel.setText(_("已耗时:{time}").format(time=""))
        self.DetailInfomation.setText(_("详细信息："))
        self.FileNameLabel.setText(_("文件名:{name}").format(name=""))
        self.FilePathLabel.setText(_("文件路径:{path}").format(path=""))
        self.FileFormatLabel.setText(_("格式:{format}").format(format=""))
        self.ProjectPresentLabel.setText(_("预设:{name}").format(name=""))
        self.VideoInfoLabel.setText(_("视频:{info}").format(info=""))
        self.BitRateLabel.setText(_("码率:{rate}").format(rate=""))
        self.AudioLabel.setText(_("音频:{info}").format(info=""))
        self.PauseButton.setIcon(FIF.PAUSE)
        self.PauseButton.setText(_("暂停"))
        self.StartButton.setText(_("开始"))
        self.StopButton.setText(_("停止"))
        self.StopButton.setIcon(FIF.CLOSE)
        self.setWindowTitle(_("Invisible Watermark Toolbox NEXT"))
        self.QueueProgressBar.setValue(0)
        self.progressBar.setValue(10)
        self.progressBar.setTextVisible(True)
        self.SingleSelectLabel.setText(_("请选择文件"))
        self.SLBrowser.setText(_("浏览"))
        self.SLBrowser.setIcon(FIF.DOCUMENT)
        self.SLBrowser.setFlat(True)
        self.MLBrowser.setText(_("浏览"))
        self.MLBrowser.setIcon(FIF.FOLDER)
        self.MLLabel.setText(_("批量处理"))
        self.MFOpen.setText(_("打开"))
        self.SLOpen.setText(_("打开"))
        self.label_10.scaledToHeight(150)
        self.setGeometry(0,0,1280,720)
        self.label_10.setBorderRadius(8, 8, 8, 8)
        self.StatusDock.setWindowTitle(_("任务进度"))
        self.PresentBrowserDock.setWindowTitle(_("模板浏览器"))
        self.MediaBrowserDock.setWindowTitle(_("媒体浏览器"))
        self.action_9.setText(_("显示全部"))



    def show_all(self):
        self.StatusDock.show()
        self.PresentBrowserDock.show()
        self.MediaBrowserDock.show()









class SplashScreen(QWidget,Ui_SplashDesu):
    timers = QTimer()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setInvisible()
        self.Tips.setText("Loading...")
        self.progressBar.setValue(0)
        self.MainWindow = MainWindow()
        self.timers.timeout.connect(self.prepare)
        self.timers.start(3000)


    def setInvisible(self): 
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def adjust_size_based_on_resolution(self):
        pass

    def prepare(self):
        self.timers.stop()
        self.Tips.setText(_("检查FFmpeg中..."))
        if not PrepareRequirements.is_ffmpeg_exist():
            self.Tips.setText(_("安装FFMpeg"))
            self.display_dialog()
        self.Tips.setText(_("清理松散文件中..."))

        self.Tips.setText(_("加载主页面..."))
        self.MainWindow.showMaximized()
        self.close()



    def display_dialog(self):
        title = _("FFmpeg未安装")
        content = _("FFmpeg是此程序和依赖库MoviePy的核心组件。如果你想自行安装FFmpeg并添加到环境变量中，请点击否。点击是将自动下载并安装FFmpeg。(不会添加到环境变量中)")
        w = Dialog(title, content, self)
        if w.exec():
            w = FFmpegDownloadPage(self)
            if w.exec():
                # print(w.urlLineEdit.text())
                pass
        else:
            print('Cancel button is pressed')

    def download_dialog(self):
        pass

class FFmpegDownloadPage(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(_('FFmpeg正在下载'), self)
        self.progressBar = ProgressBar(self)
        self.labels = BodyLabel(_('请耐心等待下载完成'), self)


        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progressBar)
        self.viewLayout.addWidget(self.labels)

        # change the text of button
        self.yesButton.hide()
        self.cancelButton.hide()

        self.widget.setMinimumWidth(350)

        # self.hideYesButton()
        self.download_thread = PrepareRequirements.FFmpegPrepare()
        self.download_thread.progress.connect(self.set_progress)
        self.download_thread.progress_text.connect(self.set_progress_text)
        self.download_thread.success.connect(self.is_success)
        try:
            self.download_thread.start()
        except Exception as e:
            self.labels.setText(str(e))

    def set_progress(self, value):
        self.progressBar.setVal(value)
    def set_progress_text(self, text):
        self.labels.setText(text)

    def is_success(self, value):
        if value:
            self.close()

class CreateNewProject(QFrame,Ui_SetUpNewForm):
    def __init__(self,file_path):
        super().__init__()
        self.setupUi(self)
        self.render_device = pltform.get_render_devices()
        self.set_text()
        self.set_connections()
        self.initial_CB()
        self.checker = QTimer()
        self.checker.timeout.connect(self.setup_correct_setting_item)
        self.checker.start(50)
        self.processUnit = None
        self.file_path = file_path

    def generate_profile(self):
        self.processUnit = ProcessUnit.ProcessUnit()
        self.processUnit.file = self.file_path
        if int(self.CB_WatermarkAgori.currentIndex()) == 0:
            if int(self.CB_WatermarkType.currentIndex()) == 0:
                self.processUnit.watermark_method = const.WatermarkAlgorithm.IMAGE_GUOFEI
                if "," in str(self.LE_wmpara1):
                    num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),int(self.LE_wmpara1.text().split(",")[1]))
                else:
                    num1 = int(self.LE_wmpara1.text())

                if "," in str(self.LE_wmpara2):
                    num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),int(self.LE_wmpara2.text().split(",")[1]))
                else:
                    num2 = int(self.LE_wmpara2.text())
                attachment_data = {
                    "img_password":num1,
                    "wm_password":num2
                }
                self.processUnit.attachment_data = attachment_data
                self.processUnit.watermark_content = cv2.imread(self.LE_WatermarkContent.text())
            elif int(self.CB_WatermarkType.currentIndex()) == 1:
                self.processUnit.watermark_method = const.WatermarkAlgorithm.TEXT_GOUFEI
                if "," in str(self.LE_wmpara1):
                    num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),int(self.LE_wmpara1.text().split(",")[1]))
                else:
                    num1 = int(self.LE_wmpara1.text())

                if "," in str(self.LE_wmpara2):
                    num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),int(self.LE_wmpara2.text().split(",")[1]))
                else:
                    num2 = int(self.LE_wmpara2.text())
                attachment_data = {
                    "img_password": num1,
                    "wm_password": num2
                }
                self.processUnit.attachment_data = attachment_data
                self.processUnit.watermark_content = str(self.LE_WatermarkContent.text())
        elif int(self.CB_WatermarkAgori.currentIndex()) == 1:
            self.processUnit.watermark_method = const.WatermarkAlgorithm.IMAGE_FIREKEEPER
            if "," in str(self.LE_wmpara1):
                num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),
                                      int(self.LE_wmpara1.text().split(",")[1]))
            else:
                num1 = int(self.LE_wmpara1.text())

            if "," in str(self.LE_wmpara2):
                num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),
                                      int(self.LE_wmpara2.text().split(",")[1]))
            else:
                num2 = int(self.LE_wmpara2.text())
            if "," in str(self.LE_wmpara3):
                num3 = random.randint(int(self.LE_wmpara3.text().split(",")[0]),
                                      int(self.LE_wmpara3.text().split(",")[1]))
            else:
                num3 = int(self.LE_wmpara3.text())

            if "," in str(self.LE_wmpara4):
                num4 = random.randint(int(self.LE_wmpara4.text().split(",")[0]),
                                      int(self.LE_wmpara4.text().split(",")[1]))
            else:
                num4 = int(self.LE_wmpara4.text())
            attachment_data = {
                "seed1": num1,
                "seed2": num2,
                "mod1": num3,
                "mod2": num4,
            }
            self.processUnit.watermark_content = cv2.imread(self.LE_WatermarkContent.text())
            self.processUnit.attachment_data = attachment_data
        elif int(self.CB_WatermarkAgori.currentIndex()) == 2:
            self.processUnit.watermark_method = const.WatermarkAlgorithm.TEXT_FREQM
            attachment_data = {
                'method':'dwtDct',
                'wmType':'bytes'
            }
            self.processUnit.attachment_data = attachment_data
            self.processUnit.watermark_content = str(self.LE_WatermarkContent.text())
        elif int(self.CB_WatermarkAgori.currentIndex()) == 3:
            self.processUnit.watermark_method = const.WatermarkAlgorithm.TEXT_RIVAGAN
            attachment_data = {
                'method':'rivaGan',
                'wmType':'bytes'
            }
            self.processUnit.watermark_content = str(self.LE_WatermarkContent.text())
            self.processUnit.attachment_data = attachment_data
        self.processUnit.output_name = "embedded"
        self.processUnit.output_path = str(self.LE_VideoExportPath.text())
        self.processUnit.slice_length = int(self.SB_Slicelength.value())
        self.processUnit.sample_times = int(self.SB_SamplerTimes.value())
        self.processUnit.sample_extend = int(self.SB_FrameExtend.value())
        if self.CB_MultiProcess.isChecked():
            if int(self.SB_MultiProcess.value()) <= 61:
                self.processUnit.multi_process = int(self.SB_MultiProcess.value())
            else:
                self.processUnit.multi_process = 61
        else:
            self.processUnit.multi_process = 1
        if int(self.CB_Sampler.currentIndex()) == 0:
            self.processUnit.sample_type = const.SamplerType.RANDOM
        elif int(self.CB_Sampler.currentIndex()) == 1:
            self.processUnit.sample_type = const.SamplerType.AVERAGE
        elif int(self.CB_Sampler.currentIndex()) == 2:
            self.processUnit.sample_type = const.SamplerType.MANUAL
            self.processUnit.manual_sample_sheet = str(self.LE_SamplerSheet.text())
        elif int(self.CB_Sampler.currentIndex()) == 3:
            self.processUnit.sample_type = const.SamplerType.FULL

        current_device = self.CB_RenderDevices.currentText()
        if self.render_device[current_device] == "cpu":
            if "DXV" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.Resolume_DXV
            else:
                self.processUnit.encoder = const.Encoder.X264
        elif self.render_device[current_device] == "nvidia":
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.NVIDIA_H264
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.NVIDIA_HEVC
            elif "AV1" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.NVIDIA_AV1
        elif self.render_device[current_device] == "amd":
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.AMD_H264
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                self.processUnit.encoder = const.Encoder.AMD_HEVC

        if int(self.CB_BitRateControl.currentIndex()) == 0:
            self.processUnit.bitrate_control = const.BitRateControl.VBR
        elif int(self.CB_BitRateControl.currentIndex()) == 1:
            self.processUnit.bitrate_control = const.BitRateControl.CBR

        self.processUnit.MaximumBitRate = str(self.LE_MaxBitRate.text())
        self.processUnit.TargetBitRate = str(self.LE_BitRate.text())

        if self.render_device[current_device] == "cpu":
            if str(self.CB_FFmpegPresent.text()) == "PLACEBO":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_PLACEBO
            elif str(self.CB_FFmpegPresent.text()) == "VERYSLOW":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_VERYSLOW
            elif str(self.CB_FFmpegPresent.text()) == "SLOWER":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_SLOWER
            elif str(self.CB_FFmpegPresent.text()) == "SLOW":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_SLOW
            elif str(self.CB_FFmpegPresent.text()) == "MEDIUM":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_MEDIUM
            elif str(self.CB_FFmpegPresent.text()) == "FAST":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_FAST
            elif str(self.CB_FFmpegPresent.text()) == "FASTER":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_FASTER
            elif str(self.CB_FFmpegPresent.text()) == "VERYFAST":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_VERYFAST
            elif str(self.CB_FFmpegPresent.text()) == "SUPERFAST":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_SUPERFAST
            elif str(self.CB_FFmpegPresent.text()) == "ULTRAFAST":
                self.processUnit.FFmpegPresent = const.FFmpegPreset.X264_UlTRAFAST
            elif str(self.CB_Tune.text()) == "FILM":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_FILM
            elif str(self.CB_Tune.text()) == "ANIMATION":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_ANIMATION
            elif str(self.CB_Tune.text()) == "GRAIN":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_GRAIN
            elif str(self.CB_Tune.text()) == "STILLIMAGE":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_STILLIMAGE
            elif str(self.CB_Tune.text()) == "PSNR":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_PSNR
            elif str(self.CB_Tune.text()) == "SSIM":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_SSIM

            if str(self.CB_Tune.text()) == "FILM":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_FILM
            elif str(self.CB_Tune.text()) == "ANIMATION":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_ANIMATION
            elif str(self.CB_Tune.text()) == "GRAIN":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_GRAIN
            elif str(self.CB_Tune.text()) == "STILLIMAGE":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_STILLIMAGE
            elif str(self.CB_Tune.text()) == "PSNR":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_PSNR
            elif str(self.CB_Tune.text()) == "SSIM":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_SSIM
            elif str(self.CB_Tune.text()) == "FASTDECODE":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_FASTDECODE
            elif str(self.CB_Tune.text()) == "ZEROLANTENCY":
                self.processUnit.FFmpegTune = const.FFmpegTune.X264_ZEROLANTENCY
        elif self.render_device[current_device] == "nvidia":
            if int(self.CB_EncodePattern.currentIndex()) == 0:
                self.processUnit.two_pass = False
            else:
                self.processUnit.two_pass = True
            if str(self.CB_FFmpegPresent.currentText()) == "P1":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P1
            elif str(self.CB_FFmpegPresent.currentText()) == "P2":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P2
            elif str(self.CB_FFmpegPresent.currentText()) == "P3":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P3
            elif str(self.CB_FFmpegPresent.currentText()) == "P4":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P4
            elif str(self.CB_FFmpegPresent.currentText()) == "P5":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P5
            elif str(self.CB_FFmpegPresent.currentText()) == "P6":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P6
            elif str(self.CB_FFmpegPresent.currentText()) == "P7":
                self.processUnit.FFmpegTune = const.FFmpegPreset.NVIDIA_P7
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "High Quality":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H264_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H264_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H264_SLL
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "Super High Quality":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H265_SHQ
                elif str(self.CB_Tune.text()) == "High Quality":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H265_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H265_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_H265_SLL
            elif "AV1" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "Super High Quality":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_AV1_SHQ
                elif str(self.CB_Tune.text()) == "High Quality":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_AV1_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_AV1_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    self.processUnit.FFmpegTune = const.FFmpegTune.NV_AV1_SLL

        if self.CB_Foreward.isChecked():
            self.processUnit.FFmpegForeward = int(self.SB_Forward.value())
        else:
            self.processUnit.FFmpegForeward = None

        if self.CB_AdjustiveNormalize.isChecked():
            self.processUnit.FFmpegSelfAdaptive = int(self.SB_AN.value())
        else:
            self.processUnit.FFmpegSelfAdaptive = None







    def set_text(self):
        self.L_CreateProject.setText(_("创建新项目"))
        self.CB_ProjectType.addItem(_("视频水印"))
        self.CB_ProjectType.addItem(_("图片水印"))
        for device in list(self.render_device.keys()):
            self.CB_RenderDevices.addItem(device)
        self.CB_BitRateControl.addItem(_("VBR"))
        self.CB_BitRateControl.addItem(_("CBR"))
        self.CB_VideoExportFormat.addItem(_("MP4"))
        self.CB_VideoExportFormat.addItem(_("MKV"))
        self.CB_VideoExportFormat.addItem(_("MOV"))
        self.CB_EncodePattern.addItem(_("单次编码"))
        self.CB_EncodePattern.addItem(_("二次编码(全分辨率)"))
        self.CB_WatermarkAgori.addItems([_("GuoFei"),_("FireKeeper"),_("ShieldMint_DCT"),_("ShieldMint_RivaGan")])
        self.CB_Sampler.addItems([_("随机采样器"),_("平均采样器"),_("固定值"),_("全部采样")])

    def set_connections(self):
        self.CB_RenderDevices.currentIndexChanged.connect(self.set_encoders)
        self.CB_VideoEncoder.currentIndexChanged.connect(self.DXV_OPT)
        self.CB_BitRateControl.currentIndexChanged.connect(self.bitrate_control_changed)
        self.CB_VideoEncoder.currentIndexChanged.connect(self.set_tune_options)
        self.CB_WatermarkAgori.currentIndexChanged.connect(self.set_watermark_method)
        self.HS_FrameExtend.valueChanged.connect(self.sync_frame_set_HS)
        self.SB_FrameExtend.valueChanged.connect(self.sync_frame_set_SB)
        self.CB_Sampler.currentIndexChanged.connect(self.sample_set)
        self.CB_WatermarkAgori.currentIndexChanged.connect(self.set_watermark_params)
        self.PB_Confirm.clicked.connect(self.check_validity)

    def sync_frame_set_HS(self):
        self.SB_FrameExtend.setValue(int(self.HS_FrameExtend.value()))
    def sync_frame_set_SB(self):
        self.HS_FrameExtend.setValue(int(self.SB_FrameExtend.value()))

    def initial_CB(self):
        self.set_encoders()

    def check_validity(self):
        if int(self.CB_BitRateControl.currentIndex()) == 1 and len(self.LE_BitRate.text()) == 1:
            showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率?！"),_("比特率不合规！"))
            return False
        elif int(self.CB_BitRateControl.currentIndex()) == 0:
            if len(self.LE_BitRate.text()) == 1 or len(self.LE_MaxBitRate.text()) == 1:
                showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率！"),_("比特率不合规！"))
                return False

        if int(self.CB_BitRateControl.currentIndex()) == 1 and len(self.LE_BitRate.text()) == 0:
            showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率！"),_("比特率不能为空！"))
            return False
        elif int(self.CB_BitRateControl.currentIndex()) == 0:
            if len(self.LE_BitRate.text()) == 0 or len(self.LE_MaxBitRate.text()) == 0:
                showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率！"),_("比特率不能为空！"))
                return False



        if int(self.CB_BitRateControl.currentIndex()) == 1:
            try:
                int(str(self.LE_BitRate.text()).replace("k","").replace("K","").replace("M","").replace("m","").replace(" ",""))
            except ValueError:
                    showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率?！"),_("比特率不合规！"))
                    return False
            except Exception as e:
                print(e)
                return False
        else:
            try:
                int(str(self.LE_BitRate.text()).replace("k","").replace("K","").replace("M","").replace("m","").replace(" ",""))
                int(str(self.LE_MaxBitRate.text()).replace("k", "").replace("K", "").replace("M", "").replace("m",
                                                                                                           "").replace(
                    " ", ""))
            except ValueError:
                    showFlyout(self,self.CB_BitRateControl,InfoBarIcon.ERROR,_("请重新输入比特率！"),_("比特率不合规！"))
                    return False
            except Exception as e:
                print(e)
                return False

        if self.CB_Sampler.currentIndex() == 2 and len(self.LE_SamplerSheet.text().replace("\n","")) == 0:
            showFlyout(self,self.CB_Sampler,InfoBarIcon.ERROR,_("请输入采样器工作表"),_("采样表不能为空！"))
            return False
        elif not os.path.exists(self.LE_VideoExportPath.text()):
            showFlyout(self,self.LE_VideoExportPath,InfoBarIcon.ERROR,_("导出路径不存在！请选择其他路径！"),_("导出路径不存在！"))
            return False
        return True



    def set_watermark_params(self):
        current_wm_method = self.CB_WatermarkAgori.currentText()
        self.L_wmpara1.show()
        self.LE_wmpara1.show()
        self.L_wmpara2.show()
        self.LE_wmpara2.show()
        self.L_wmpara3.show()
        self.LE_wmpara3.show()
        self.L_wmpara4.show()
        self.LE_wmpara4.show()
        if current_wm_method == _("GuoFei"):
            self.L_wmpara1.setText(_("图片密码"))
            self.LE_wmpara1.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara2.setText(_("水印密码"))
            self.LE_wmpara2.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara3.hide()
            self.LE_wmpara3.hide()
            self.L_wmpara4.hide()
            self.LE_wmpara4.hide()
        elif current_wm_method == _("FireKeeper"):
            self.L_wmpara1.setText(_("种子1"))
            self.LE_wmpara1.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara2.setText(_("种子2"))
            self.LE_wmpara2.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara3.setText(_("除数1"))
            self.LE_wmpara3.setPlaceholderText(_("除数越大鲁棒性越强，但图片失真越严重。输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara4.setText(_("除数2"))
            self.LE_wmpara4.setPlaceholderText(_("除数越大鲁棒性越强，但图片失真越严重。输入两个以半角逗号分割的数字以在选定范围内随机"))
        elif "DCT" in current_wm_method or "RivaGan" in current_wm_method:
            self.L_wmpara1.hide()
            self.LE_wmpara1.hide()
            self.L_wmpara2.hide()
            self.LE_wmpara2.hide()
            self.L_wmpara3.hide()
            self.LE_wmpara3.hide()
            self.L_wmpara4.hide()
            self.LE_wmpara4.hide()
            pass


    def sample_set(self):
        current_sampler = self.CB_Sampler.currentText()
        self.L_SamplerTimes.show()
        self.SB_SamplerTimes.show()
        self.LE_SamplerSheet.show()
        self.L_SamplerSheet.show()
        self.L_FrameExtend.show()
        self.HS_FrameExtend.show()
        self.SB_FrameExtend.show()
        if current_sampler == _("固定值"):
            self.LE_SamplerSheet.show()
            self.L_SamplerSheet.show()
            self.L_SamplerTimes.hide()
            self.SB_SamplerTimes.hide()

        elif current_sampler != _("全部采样"):
            self.LE_SamplerSheet.hide()
            self.L_SamplerSheet.hide()
            self.L_SamplerTimes.show()
            self.SB_SamplerTimes.show()
        else:
            self.L_SamplerSheet.hide()
            self.LE_SamplerSheet.hide()
            self.L_SamplerTimes.hide()
            self.SB_SamplerTimes.hide()
            self.L_FrameExtend.hide()
            self.HS_FrameExtend.hide()
            self.SB_FrameExtend.hide()


    def set_encoders(self):
        current_device = self.CB_RenderDevices.currentText()

        if self.render_device[current_device] == "cpu":
            self.CB_VideoEncoder.clear()
            self.CB_VideoEncoder.addItem(_("x264"))
            self.CB_VideoEncoder.addItem(_("Resolume DXV1"))
        if self.render_device[current_device] == "nvidia":
            self.CB_VideoEncoder.clear()
            self.CB_VideoEncoder.addItem(_("Nvidia NVENC H.264"))
            self.CB_VideoEncoder.addItem(_("Nvidia NVENC HEVC"))
            self.CB_VideoEncoder.addItem(_("Nvidia NVENC AV1"))
        if self.render_device[current_device] == "amd":
            self.CB_VideoEncoder.clear()
            self.CB_VideoEncoder.addItem(_("AMD HW H.264"))
            self.CB_VideoEncoder.addItem(_("AMD HW HEVC"))
        self.set_encoder_options()
        self.DXV_OPT()
        self.sample_set()
        self.set_watermark_params()

    def bitrate_control_changed(self):
        current_bitrate_control = self.CB_BitRateControl.currentText()
        if current_bitrate_control == "CBR":
            self.L_MaxBitRate.hide()
            self.LE_MaxBitRate.hide()
        else:
            self.L_MaxBitRate.show()
            self.LE_MaxBitRate.show()

    def DXV_OPT(self):
        current_encoder = self.CB_VideoEncoder.currentText()
        if "DXV" in current_encoder:
            self.F_VideoEncoder.hide()
        else:
            self.F_VideoEncoder.show()
        if "AMD" in current_encoder:
            self.CB_Foreward.hide()
            self.CB_AdjustiveNormalize.hide()
            self.SB_Forward.hide()
            self.SB_AN.hide()
        else:
            self.CB_Foreward.show()
            self.CB_AdjustiveNormalize.show()
            self.SB_Forward.show()
            self.SB_AN.show()
        if not "NVENC" in current_encoder:
            self.L_EncodePattern.hide()
            self.CB_EncodePattern.hide()
        else:
            self.L_EncodePattern.show()
            self.CB_EncodePattern.show()
        self.set_tune_options()
        self.set_watermark_method()

    def set_tune_options(self):
        current_encoder = self.CB_VideoEncoder.currentText()
        if "AMD" in current_encoder:
            self.CB_Tune.hide()
            self.L_Tune.hide()
        else:
            self.CB_Tune.show()
            self.L_Tune.show()
        self.CB_Tune.clear()
        if "H.264" in current_encoder:
            self.CB_Tune.addItem(_("High Quality"))
            self.CB_Tune.addItem(_("Low Latency"))
            self.CB_Tune.addItem(_("Super Low Latency"))
        elif "HEVC" in current_encoder:
            self.CB_Tune.addItem(_("Super High Quality"))
            self.CB_Tune.addItem(_("High Quality"))
            self.CB_Tune.addItem(_("Low Latency"))
            self.CB_Tune.addItem(_("Super Low Latency"))
        elif "AV1" in current_encoder:
            self.CB_Tune.addItem(_("Super High Quality"))
            self.CB_Tune.addItem(_("High Quality"))
            self.CB_Tune.addItem(_("Low Latency"))
            self.CB_Tune.addItem(_("Super Low Latency"))
        elif "x264" in current_encoder:
            self.CB_Tune.addItem(_("FILM"))
            self.CB_Tune.addItem(_("ANIMATION"))
            self.CB_Tune.addItem(_("GRAIN"))
            self.CB_Tune.addItem(_("STILLPICTURE"))
            self.CB_Tune.addItem(_("PSNR"))
            self.CB_Tune.addItem(_("SSIM"))
            self.CB_Tune.addItem(_("ZEROLATENCY"))
            self.CB_Tune.addItem(_("FASTDECODE"))
            self.CB_Tune.addItem(_("None"))

    def set_watermark_method(self):
        current_wm_method = self.CB_WatermarkAgori.currentText()
        if "Shield" in current_wm_method:
            self.CB_WatermarkType.clear()
            self.CB_WatermarkType.addItem(_("文字水印"))
        elif "GuoFei" in current_wm_method:
            self.CB_WatermarkType.clear()
            self.CB_WatermarkType.addItem(_("图片水印"))
            self.CB_WatermarkType.addItem(_("文字水印"))
        else:
            self.CB_WatermarkType.clear()
            self.CB_WatermarkType.addItem(_("图片水印"))



    def set_encoder_options(self):
        current_encoder = self.CB_VideoEncoder.currentText()
        current_bitrate_control = self.CB_BitRateControl.currentText()


        if "AMD" in current_encoder:
            self.CB_FFmpegPresent.clear()
            self.CB_FFmpegPresent.addItem(_("质量"))
            self.CB_FFmpegPresent.addItem(_("均衡"))
            self.CB_FFmpegPresent.addItem(_("速度"))
            self.CB_Tune.hide()

        if "NVENC" in current_encoder:
            self.CB_FFmpegPresent.clear()
            self.CB_FFmpegPresent.addItem(_("P1"))
            self.CB_FFmpegPresent.addItem(_("P2"))
            self.CB_FFmpegPresent.addItem(_("P3"))
            self.CB_FFmpegPresent.addItem(_("P4"))
            self.CB_FFmpegPresent.addItem(_("P5"))
            self.CB_FFmpegPresent.addItem(_("P6"))
            self.CB_FFmpegPresent.addItem(_("P7"))

        if "x264" in current_encoder:
            self.CB_FFmpegPresent.clear()
            self.CB_FFmpegPresent.addItem(_("PLACEBO"))
            self.CB_FFmpegPresent.addItem(_("VERYSLOW"))
            self.CB_FFmpegPresent.addItem(_("SLOWER"))
            self.CB_FFmpegPresent.addItem(_("SLOW"))
            self.CB_FFmpegPresent.addItem(_("MEDIUM"))
            self.CB_FFmpegPresent.addItem(_("FAST"))
            self.CB_FFmpegPresent.addItem(_("FASTER"))
            self.CB_FFmpegPresent.addItem(_("VERYFAST"))
            self.CB_FFmpegPresent.addItem(_("SUPERFAST"))
            self.CB_FFmpegPresent.addItem(_("ULTRAFAST"))




    def setup_correct_setting_item(self):
        if self.CB_ProjectType.currentIndex() == 0:
            self.F_Video.show()
        else:
            self.F_Video.hide()


def start():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    window = SplashScreen()
    window.show()
    sys.exit(app.exec())

def showFlyout(self,target,icon,content,title):
    Flyout.create(
        icon=icon,
        title=title,
        content=content,
        target=target,
        parent=self,
        isClosable=True
    )




if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    window = SplashScreen()
    window.show()
    sys.exit(app.exec())
