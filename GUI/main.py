"""
请伟大的早濑优香大人保佑这段代码吧！
"""
import copy
import json
import os.path
import pickle
import random
import shutil
import subprocess
import sys
import threading
import time
import traceback
import uuid
from functools import partial
from typing import Optional

import numpy as np
import psutil
import pyanime4k

from BasicSystem.log_client import setup_logger, get_logger
from GUI.NewVersionFround import Ui_NewVersion
from GUI.NonCW import Ui_NonCriticalError
from GUI.UpScale import Ui_UpScaleAni
from GUI.UserInterfaceErrorFeedback import ErrorFeedbackUi_L
from GUI.download_newversion import Ui_DownloadNew
from GUI.log_viewer import LogViewerWindow
from modules.PyAv import extract_video_frames
from modules.GenerateVideo import get_video_parameters_simple,get_audio_parameters_simple
import cv2
from PySide6.QtGui import QPixmap, QImage, QDesktopServices

from BasicSystem import const
from modules import ProcessUnit, PyAv, multithread_downloader, update_check
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QVBoxLayout, QTableWidgetItem, QProgressBar, \
    QHeaderView, QTableWidget, QFileDialog, QAbstractItemView, QLineEdit
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QUrl
from qfluentwidgets import FluentIcon as FIF, FlyoutViewBase, Flyout, InfoBarIcon, ImageLabel, RoundMenu, Action, \
    FluentIcon, InfoBar, InfoBarPosition, PushButton, LineEdit

from GUI.MainWindows import Ui_MainWindow
from GUI.Setting import Ui_Form as Ui_Setting
from GUI.SetUp import Ui_SetUpNewForm
from GUI.PresetApplyConfirm import Ui_AP_Form
from GUI.RecoverWindow import Ui_Recover_Form
import gettext
from PySide6.QtCore import Qt
from GUI import error_report
from GUI.credit import Ui_Credit
from modules.ThreadingScheduler import ThreadPoolManager
import os
from modules.audio import AudioPlayer
from modules.ExtractUnit import ExtracUnit
from modules.pltform import get_render_devices

error_list = []

setup_logger(default_tags="main", enable_udp=True, enable_console=True)
logger = get_logger()

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = 'TRUE'

_ = gettext.gettext
_devices = get_render_devices()
print(_devices)
preset_path = "./preset"





from qfluentwidgets import Dialog, setTheme, Theme, PrimaryPushButton, MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel
import qdarktheme

if os.path.exists("setting.json"):
    with open("setting.json", "r", encoding="utf-8") as f:
        json_data = f.read()
    preference_args = json.loads(json_data)
    if preference_args['Theme'] == "dark":
        setTheme(Theme.DARK)

    elif preference_args['Theme'] == "light":
        setTheme(Theme.LIGHT)
        qdarktheme.setup_theme("light")
    else:
        setTheme(Theme.AUTO)
        qdarktheme.setup_theme("auto")
else:
    setTheme(Theme.AUTO)
    qdarktheme.setup_theme("auto")

def non_critical_error_info_bar(self,error):
    content = _("主处理程序疑似发生错误，这一错误可能不会影响程序的运行，但有可能导致对编解码模块的配置异常。")
    w = InfoBar(
        icon=InfoBarIcon.ERROR,
        title=_(f'主程序发生错误:{error[0]}'),
        content=content,
        orient=Qt.Vertical,  # vertical layout
        isClosable=True,
        position=InfoBarPosition.BOTTOM_RIGHT,
        duration=4000,
        parent=self
    )
    def show_detail_window(error):
        detail_window = NonCriticalErrorDetail(error,parent=self)
        detail_window.pushButton.clicked.connect(self.show_error_feedback)
        detail_window.show()

    detail_button = PrimaryPushButton(_("了解详情"))
    detail_button.clicked.connect(lambda : show_detail_window(error))
    w.addWidget(detail_button)
    w.show()





def _get_duration_opencv(video_path: str) -> Optional[float]:
    """使用OpenCV获取视频时长"""
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            return None

        # 获取帧率和总帧数
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        cap.release()

        if fps > 0 and frame_count > 0:
            logger.debug(f"Video duration: {frame_count / fps} seconds",tags="main:_get_duration_opencv")
            return frame_count / fps
        else:
            return None

    except ImportError:
        print("OpenCV未安装，请运行: pip install opencv-python")
        return None
    except Exception as e:
        print(f"OpenCV错误: {e}")
        return None

def resize_image_to_fixed_height_simple(image, target_height=216):
    h, w = image.shape[:2]

    # 计算缩放比例和新宽度
    scale = target_height / h
    new_width = int(w * scale)

    # 缩放图像
    resized = cv2.resize(image, (new_width, target_height))

    # 创建目标画布
    canvas = np.zeros((target_height, 384, 3), dtype=np.uint8)

    # 计算放置位置
    if new_width < 384:
        x_offset = (384 - new_width) // 2
        canvas[:, x_offset:x_offset + new_width] = resized
    else:
        x_offset = (new_width - 384) // 2
        canvas = resized[:, x_offset:x_offset + 384]

    # logger.debug(f"Resized image shape: {canvas.shape}",tags="main:resize_image_to_fixed_height_simple")

    return canvas


def cv2_to_qpixmap(cv_img):
    """将 OpenCV 图像转换为 QPixmap"""
    # 确保图像是连续的内存块
    cv_img = np.ascontiguousarray(cv_img)

    # OpenCV 使用 BGR 格式，Qt 使用 RGB，需要转换
    if len(cv_img.shape) == 3:  # 彩色图像
        # 检查是否是3通道的BGR图像
        if cv_img.shape[2] == 3:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        else:
            # 处理4通道图像（如RGBA）
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2RGBA)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
    else:  # 灰度图像
        h, w = cv_img.shape
        # 使用正确的格式和字节对齐
        bytes_per_line = w
        q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8)

    # 复制数据以避免内存问题
    # logger.debug(f"QImage size: {q_img.size()}",tags="main:cv2_to_qpixmap")
    return QPixmap.fromImage(q_img.copy())


class UpscaleWindow(QWidget,Ui_UpScaleAni):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(_("超分辨率"))
        self.lineEdit.setPlaceholderText(_("请输入图片路径，若输入目录则会批量处理"))
        self.lineEdit_2.setPlaceholderText(_("请输入输出目录"))
        self.pushButton.setText(_("浏览"))
        self.pushButton_3.setText(_("浏览"))
        self.pushButton_2.setText(_("启动"))
        self.pushButton.clicked.connect(lambda: self.browse_filename(self.lineEdit))
        self.pushButton_3.clicked.connect(lambda: self.browse_output_dir(self.lineEdit_2))
        self.pushButton_2.clicked.connect(self.process)

    def browse_filename(self, lineEdit:LineEdit):
        filename, a_ = QFileDialog.getOpenFileName(self, _("选择文件"), "", _("图片文件 (*.png *.jpg *.jpeg)"))
        if filename:
            lineEdit.setText(filename)

    def browse_output_dir(self, lineEdit:LineEdit):
        dirname = QFileDialog.getExistingDirectory(self, _("选择目录"))
        if dirname:
            lineEdit.setText(dirname)

    def process(self):
        self.pushButton_2.setText(_("处理中..."))
        self.pushButton_2.setEnabled(
                False
        )
        processor = pyanime4k.Processor(
            processor_type="opencl",
            device=0,
            model="acnet-hdn0"
        )
        if len(self.lineEdit.text()) == 0 or len(self.lineEdit_2.text()) == 0:
            InfoBar.error(
                title=_("错误"),
                content=_("请输入图片路径和输出目录"),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            self.pushButton_2.setEnabled(
                True
            )
            self.pushButton_2.setText(_("启动"))
            return
        if os.path.isfile(self.lineEdit.text()) and os.path.exists(self.lineEdit_2.text()):
            src = cv2.imread(self.lineEdit.text())
            dst = processor(src)
            cv2.imwrite(filename=os.path.join(self.lineEdit_2.text(), str(os.path.basename(self.lineEdit.text()))), img=dst)
            self.pushButton_2.setEnabled(
                True
            )
            self.pushButton_2.setText(_("启动"))
        if not os.path.isfile(self.lineEdit.text()) and os.path.exists(self.lineEdit_2.text()):
            for file in os.listdir(self.lineEdit.text()):
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    src = cv2.imread(os.path.join(self.lineEdit.text(), file))
                    dst = processor(src)
                    cv2.imwrite(filename=os.path.join(self.lineEdit_2.text(), file), img=dst)
            self.pushButton_2.setEnabled(
                True
            )
            self.pushButton_2.setText(_("启动"))
        InfoBar.success(
            title=_("处理完成"),
            content=_("Yay!"),
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )


class SettingUi_L(QFrame,Ui_Setting):
    reload_settings = Signal()
    def __init__(self):
        super().__init__()
        self.log_process = None
        self.viewer = None
        self.setupUi(self)
        self.set_text()
        self.credit_window = None
        self.set_slot()
        self.AboutButton.clicked.connect(self.display_credit)
        self.setting_list = {
            "language":"ZH_CN",
            "CompleteNotice":True,
            "DefaultSavePath":"./",
            "OutputStructure":"dir",
            "EnableCoreDump":True,
            "AutoCheckUpdate":True,
            "Theme":"dark"
        }
        if not os.path.exists("setting.json"):
            self.initial()
        self.load_and_set_correct_optiton()

    def display_credit(self):
        if self.credit_window is None:
            self.credit_window = CreditWindow()
        self.credit_window.show()

    def display_log_window(self):
        if self.log_process is None:
            self.log_process = LogViewerWindow()
            with open("identify_session.txt", "r") as f:
                session_id = f.readline()
            name = os.path.join("./logs", "app_" + str(session_id) + ".log")
            self.log_process._load_file(name)
            self.log_process.show()
        else:
            self.log_process.raise_()
            self.log_process.activateWindow()
            self.log_process.show()


    def set_text(self):
        self.setWindowTitle(_("设置"))
        self.SettingTitleLabel.setText(_("设置"))
        self.General_label.setText(_("通用设置"))
        self.LanguageLabel.setText(_("语言/Language/言語"))
        self.LanguagecomboBox.addItem(_("中文(简体)"),userData="zh_CN")
        self.LanguagecomboBox.addItem(_("中文(繁體)"),userData="zh_TW")
        self.LanguagecomboBox.addItem(_("English"),userData="en_US")
        self.LanguagecomboBox.addItem(_("日本語"),userData="ja_JP")
        self.CompleteDing.setText(_("完成时声音提醒"))
        self.FileRelatedLabel.setText(_("文件相关设置"))
        self.DefaultSaveDictTextEdit.setPlaceholderText(_("默认保存路径"))
        self.DefaultSaveDictLabel.setText(_("默认保存路径"))
        self.DefaultSaveDictBrowserButton.setText(_("浏览"))
        self.OutputStructureLabel.setText(_("输出结构"))
        self.OutputStructureComboBox.addItem(_("目录"),userData="dir")
        self.OutputStructureComboBox.addItem(_("压缩文件(ZIP)"),userData="zip-file")
        self.SoftwareVersionDetial.setText(_("InvisibleWatermarkToolboxNEXT ParySoftware © 2020-2025 All rights reserved.\nThis software is licensed under the MIT license.\nVersion:{version}").format(version=_(const.__version__)))
        self.DisplayLogLabel.setText(_("显示日志"))
        self.DisplayLogButton.setText(_("显示"))
        self.DumpCoreDataWhenExceptionOccuredLabel.setText(_("发生异常时转储核心数据"))
        self.DumpCoreDataWhenExceptionOccuredCheckBox.setText(_("重启后生效"))
        self.BugReportLabel.setText(_("报告错误"))
        self.BugReportButton.setText(_("报告"))
        self.VersionLabel.setText(_("版本信息"))
        self.SoftwareVersionLabel.setText(_("软件版本"))
        self.SoftwareVersionCheckButton.setText(_("检查更新"))
        self.CB_Theme.clear()
        self.CB_Theme.addItem(_("深色"),userData="dark")
        self.CB_Theme.addItem(_("浅色"),userData="light")
        self.CB_Theme.addItem(_("系统默认"),userData="system")



    def set_slot(self):
        self.DisplayLogButton.clicked.connect(self.display_log_window)
        self.DefaultSaveDictBrowserButton.clicked.connect(self.set_default_save_path)

    def set_default_save_path(self):
        path = QFileDialog.getExistingDirectory(self, _("选择默认保存路径"))
        if path:
            self.DefaultSaveDictTextEdit.setText(path)

    def load_and_set_correct_optiton(self):
        with open("setting.json", "r", encoding="utf-8") as f:
            self.setting_list = json.load(f)
        self.LanguagecomboBox.setCurrentIndex(self.LanguagecomboBox.findData(self.setting_list["language"]))
        self.CompleteDingCheck.setChecked(self.setting_list["CompleteNotice"])
        self.DefaultSaveDictTextEdit.setText(self.setting_list["DefaultSavePath"])
        self.OutputStructureComboBox.setCurrentIndex(self.OutputStructureComboBox.findData(self.setting_list["OutputStructure"]))
        self.DumpCoreDataWhenExceptionOccuredCheckBox.setChecked(self.setting_list["EnableCoreDump"])
        self.CB_autocheck.setChecked(self.setting_list["AutoCheckUpdate"])
        self.CB_Theme.setCurrentIndex(self.CB_Theme.findData(self.setting_list["Theme"]))

    def initial(self):
        self.setting_list["language"] = self.LanguagecomboBox.currentData()
        if self.CompleteDingCheck.isChecked():
            self.setting_list["CompleteNotice"] = True
        else:
            self.setting_list["CompleteNotice"] = False
        self.setting_list["DefaultSavePath"] = self.DefaultSaveDictTextEdit.text()
        self.setting_list["OutputStructure"] = self.OutputStructureComboBox.currentData()
        if self.DumpCoreDataWhenExceptionOccuredCheckBox.isChecked():
            self.setting_list["EnableCoreDump"] = True
        else:
            self.setting_list["EnableCoreDump"] = False
        if self.CB_autocheck.isChecked():
            self.setting_list["AutoCheckUpdate"] = True
        else:
            self.setting_list["AutoCheckUpdate"] = False
        self.setting_list["Theme"] = self.CB_Theme.currentData()
        json_data = json.dumps(self.setting_list, ensure_ascii=False, indent=4)
        with open("setting.json", "w", encoding="utf-8") as f:
            f.write(json_data)
        self.reload_settings.emit()

    def closeEvent(self, event):
        self.setting_list["language"] = self.LanguagecomboBox.currentData()
        if self.CompleteDingCheck.isChecked():
            self.setting_list["CompleteNotice"] = True
        else:
            self.setting_list["CompleteNotice"] = False
        self.setting_list["DefaultSavePath"] = self.DefaultSaveDictTextEdit.text()
        self.setting_list["OutputStructure"] = self.OutputStructureComboBox.currentData()
        if self.DumpCoreDataWhenExceptionOccuredCheckBox.isChecked():
            self.setting_list["EnableCoreDump"] = True
        else:
            self.setting_list["EnableCoreDump"] = False
        if self.CB_autocheck.isChecked():
            self.setting_list["AutoCheckUpdate"] = True
        else:
            self.setting_list["AutoCheckUpdate"] = False
        self.setting_list["Theme"] = self.CB_Theme.currentData()
        json_data = json.dumps(self.setting_list, ensure_ascii=False, indent=4)
        with open("setting.json", "w", encoding="utf-8") as f:
            f.write(json_data)
        self.reload_settings.emit()
        event.accept()


class CreditWindow(QWidget,Ui_Credit):
    def __init__(self):
        # raise Exception(_("CreditWindow is not implemented"))
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label_22.setImage("./assets/image/slogan.png")
        self.label_22.scaledToHeight(64)
        self.label_2.setImage("./assets/image/Tucaodashen.png")
        self.label_2.setRadius(50)
        self.label_3.setImage("./assets/image/Chengshi.jpg")
        self.label_3.setRadius(50)
        self.label_4.setText(_("雨泽."))
        self.label_4.setRadius(50)
        self.label_11.setText(("雨泽."))
        self.label_13.setText(const.__version__)
        self.pushButton.clicked.connect(self.jump_to_url)

    def jump_to_url(self):
        QDesktopServices.openUrl(QUrl("https://afdian.com/a/AnkhTheOtherSphere"))



class Preset_Confirm(QFrame,Ui_AP_Form):
    save = Signal(dict)
    save_batch = Signal(list)
    def __init__(self,preset_name,file,parent = None):
        super().__init__(parent,Qt.Window)
        self.setupUi(self)
        self.L_title.setText(_("预设应用确认"))
        self.L_outputPath.setText(_("输出路径"))
        self.L_WatermarkContent.setText(_("水印内容"))
        self.setWindowTitle(_("预设应用确认"))
        self.PB_OP.setText(_("浏览"))
        self.PB_WC.setText(_("浏览"))
        self.preset_name = preset_name
        self.file = file
        self.Confirm.clicked.connect(self.generate_template)
        self.Cancel.clicked.connect(self.close)

    def generate_template(self):
        with open(os.path.join(preset_path, f"{self.preset_name}.pickle"), "rb") as f:
            template = pickle.load(f)
        if template['watermark_method'] in [const.WatermarkAlgorithm.IMAGE_GUOFEI, const.WatermarkAlgorithm.IMAGE_FIREKEEPER]:
            template.update({"output_path": self.LE_OP.text(), "watermark_content": cv2.imread(self.LE_WC.text())})
        else:
            template.update({"output_path": self.LE_OP.text(), "watermark_content": str(self.LE_WC.text())})
        if len(self.file) == 1 or type(self.file) == str:
            template.update({"file": self.file})
            logger.debug(f"Single preset template: {template}",tags="main:Preset_Confirm:generate_template")
            self.save.emit(template)
        else:
            logger.debug(f"Batch preset template: {template}",tags="main:Preset_Confirm:generate_template")
            self.save_batch.emit([template,self.file])


def get_log():
    with open("identify_session.txt","r") as f:
        session_id = f.readline()
    name = os.path.join("./logs","app_"+str(session_id)+".log")
    return name


def run_updater():
    command = 'start AobaUpdater.exe'

    subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


class MainWindow(QMainWindow, Ui_MainWindow):
    QueueProgressUpdater = QTimer()
    freq_detail = QTimer()
    update_detail = QTimer()
    thumbnail_status_signal = Signal(str)
    update_button_signal = Signal(bool)
    snw = Signal(list)
    anv = Signal()
    check_update_timer = QTimer()
    def __init__(self):
        super().__init__()
        self.check_thread = None
        self.update_close = False
        self.new_version_window = None
        self.credit_window = None
        self.error_feedback_ui = None
        self.preference_window = None
        self.upscale_window = None
        self.log_process = None
        self.recover_window = None
        self.played = False
        self.preference_window = SettingUi_L()
        self.audio_player = AudioPlayer()
        self.confirm_preset_form = None
        self.update_image_thread = None
        self.batch_setUp_form = None
        self.error_window = []
        self.setUp_form = None
        self.pu_thread = None
        self.pu = None
        self.preset_list = []
        self.setupUi(self)
        self.statusbar.showMessage(_("准备就绪"))
        self.set_text()
        self.set_slot()

        self.action_9.triggered.connect(self.show_all)
        self.setButtons()
        self.temporary = None
        self.thumbnail_status_signal.connect(self.update_status_message)



        self.current_selected_task = None


        self.task_queue = []
        self.QueueProgressUpdater.timeout.connect(self.update_total_progress)
        self.QueueProgressUpdater.start(250)
        self.QueueList.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.thumbnail_cache = {}

        self.thumbnail_thread = None
        self.thumbnail_lock = threading.Lock()  # 防止竞态条件
        self.default_detail_show = None
        self.started = False
        self.browser.setDisabled(True)
        self.preference_args = {}
        self.load_setting()
        self.update_button_signal.connect(self.set_button_status)

        self.snw.connect(self.show_new_version_window)
        self.anv.connect(self.already_latese)
        if self.preference_args['AutoCheckUpdate']:
            self.check_update_timer.timeout.connect(self.check_update_from_github)
            self.check_update_timer.start(3000)



    def load_setting(self):
        if os.path.exists("setting.json"):
            with open("setting.json", "r", encoding="utf-8") as f:
                json_data = f.read()
            self.preference_args = json.loads(json_data)
            print(self.preference_args)




    def update_status_message(self, message):
        logger.debug(f"Status message: {message}",tags="main:update_status_message")
        self.statusbar.showMessage(message)


    def set_slot(self):
        self.SingleInputSelector.receive_file.connect(self.create_single_task)
        self.MultipleProcessSelector.receive_file.connect(self.add_batch_process)
        self.SLBrowser.clicked.connect(self.browse_single_video_file)
        self.SLOpen.clicked.connect(self.create_single_task_via_button)
        self.QueueList.itemSelectionChanged.connect(self.set_first_selected)
        self.freq_detail.timeout.connect(self.clear_useless_cache)
        self.freq_detail.timeout.connect(self.prepare_thumbnail)
        self.freq_detail.timeout.connect(self.scan_preset)
        self.freq_detail.timeout.connect(self.is_task_over)
        self.freq_detail.start(2500)
        self.update_detail.timeout.connect(self.update_details)
        self.update_detail.start(500)
        self.QueueList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.QueueList.customContextMenuRequested.connect(self.show_context_menu)
        self.SLOpen.rightClicked.connect(self.apply_preset)
        self.MFOpen.rightClicked.connect(self.apply_preset_multi)
        self.MFOpen.clicked.connect(self.create_batch_via_button)
        self.PresentList.receive_file.connect(self.receive_preset_drag)
        self.action_14.triggered.connect(self.show_recover_window)
        self.action_12.triggered.connect(lambda : self.jump_to_website("https://opensource.org/license/mit"))
        self.action_7.triggered.connect(self.display_upscale_window)
        self.action_4.triggered.connect(self.display_preference)
        self.action_13.triggered.connect(self.display_credit)
        self.action_15.triggered.connect(self.show_error_feedback)

    def show_NCW(self,err):
        error_list.append([err[0],"WARNING",err[1],[],get_log()])
        non_critical_error_info_bar(self,err)
        
        
    def display_credit(self):
        if self.credit_window is None:
            self.credit_window = CreditWindow()
        self.credit_window.show()





    def display_preference(self):
        if self.preference_window is None:
            self.preference_window = SettingUi_L()
            self.preference_window.show()
        else:
            self.preference_window.raise_()
            self.preference_window.activateWindow()
            self.preference_window.show()
        self.preference_window.BugReportButton.clicked.connect(self.show_error_feedback)
        self.preference_window.reload_settings.connect(self.load_setting)
        self.preference_window.SoftwareVersionCheckButton.clicked.connect(self.check_update_from_github)



    def is_task_over(self):
        if int(self.QueueProgressBar.value()) == 100 and self.started and not self.played:
            if self.preference_args["CompleteNotice"]:
                self.audio_player.load(r"assets\sound\complete.wav")
                self.audio_player.play()
                self.played = True
            logger.debug(f"Task completed",tags="main:is_task_over")
            
    def show_recover_window(self):
        self.recover_window = RecoverWindow(self)
        self.recover_window.show()
        logger.debug(f"Recover window shown",tags="main:show_recover_window")


    def create_batch_via_button(self):
        if os.path.exists(self.MLTL.text()):
            list_files = os.listdir(self.MLTL.text())
            if len(list_files) == 0:
                showFlyout(self,target = self.MLTL,icon = InfoBarIcon.WARNING, title = _("目录为空"), content = _("请先放入视频文件"))
                logger.warning(f"Batch process directory is empty",tags="main:create_batch_via_button")
            else:
                res = []
                for i in list_files:
                    if i.split(".")[-1] in ["mp4","mkv","mov","avi"]:
                        res.append(os.path.join(self.MLTL.text(),i))
                logger.debug(f"Batch process files: {res}",tags="main:create_batch_via_button")
                self.add_batch_process(res)
        else:
            showFlyout(self,target = self.MLTL,icon = InfoBarIcon.WARNING, title = _("目录不存在"), content = _("请先创建目录"))
            logger.warning(f"Batch process directory is empty",tags="main:create_batch_via_button")

    def display_upscale_window(self):
        self.upscale_window = UpscaleWindow()
        self.upscale_window.show()
        logger.debug(f"Upscale window shown",tags="main:display_upscale_window")


    def show_context_menu(self, pos):
        row = self.QueueList.rowAt(pos.y())
        col = self.QueueList.columnAt(pos.x())
        has_selection = row >= 0 and col >= 0

        menu = RoundMenu(parent=self)

        delete_action = Action(FluentIcon.DELETE, _("删除"), self)
        start_action = Action(FluentIcon.PLAY, _("开始"), self)
        pause_action = Action(FluentIcon.PAUSE, _("暂停"), self)
        resum_action = Action(FluentIcon.PLAY, _("继续"), self)
        stop_action = Action(FluentIcon.REMOVE_FROM, _("停止"), self)

        # 设置动作状态
        if not has_selection:

            start_action.setEnabled(False)
            pause_action.setEnabled(False)
            stop_action.setEnabled(False)
            delete_action.setEnabled(False)


        # 添加动作到菜单
        if has_selection:
            index = int(self.QueueList.item(row, 0).text())
            print(row,index)
            for i in self.task_queue:
                if int(i.index) == index:
                    start_action.setEnabled(False)
                    stop_action.setEnabled(False)
                    pause_action.setEnabled(False)
                    delete_action.setEnabled(False)
                    if i.running:
                        start_action.setEnabled(False)
                        stop_action.setEnabled(True)
                        pause_action.setEnabled(True)
                        delete_action.setEnabled(False)
                    else:
                        start_action.setEnabled(True)
                        delete_action.setEnabled(True)
                    if i.completed:
                        pause_action.setEnabled(False)
                        stop_action.setEnabled(False)
                        start_action.setEnabled(False)
                        delete_action.setEnabled(True)
                    if i.paused:
                        start_action.setEnabled(True)
                        stop_action.setEnabled(False)
                        pause_action.setEnabled(False)
                        delete_action.setEnabled(False)
                    if i.error_occured:
                        start_action.setEnabled(False)
                        stop_action.setEnabled(False)
                        pause_action.setEnabled(False)
                        delete_action.setEnabled(True)


            menu.addAction(start_action)
            menu.addAction(pause_action)
            menu.addAction(stop_action)
            menu.addAction(delete_action)

        # 连接信号
        actions = {
            start_action: partial(self.launch_selected_task, row),
            pause_action: partial(self.suspend_selected_task, row),
            stop_action: partial(self.terminate_selected_task, row),
            delete_action: partial(self.delete_selected_task,row),
        }

        for action, slot in actions.items():
            action.triggered.connect(slot)

        menu.exec_(self.QueueList.mapToGlobal(pos))

    def delete_selected_task(self,row_index,checked=False):
        index = int(self.QueueList.item(row_index, 0).text())
        for i in self.task_queue:
            if i.index == index:
                self.task_queue.remove(i)
                self.sync_queue()
                logger.debug(f"Task {index} deleted",tags="main:delete_selected_task")
    def suspend_selected_task(self,row_index,checked=False):
        has_single = False
        print(row_index)
        index = int(self.QueueList.item(row_index, 0).text())
        for task in self.task_queue:
            if int(task.index) == index:
                if task.process_limit == 1:
                    has_single = True
                if task.running and task.process_limit != 1:
                    task.suspend()
                    task.running = False
                    task.statue = _("已暂停")
            logger.debug(f"Task {index} suspended",tags="main:suspend_selected_task")
            self.set_status()

        if has_single:
            logger.warning(f"Single process task {index} cannot be suspended",tags="main:suspend_selected_task")
            showFlyout(self, self.QueueList, InfoBarIcon.WARNING, _("此任务无法暂停"),
                       _("单进程任务暂时无法暂停"))
    def launch_selected_task(self,row_index, checked=False):
        self.started = True
        self.played = False
        index = int(self.QueueList.item(row_index, 0).text())
        sl = None
        for task in self.task_queue:
            if task.index == index:
                if not task.paused:
                    if not task.running and task.status != 0 and task.completed != True and task.stopped != True:
                        task.running = True
                        task.consumed_timer = time.time()
                        task.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        task.statue = _("运行中")
                        task.update_progress.connect(self.update_queue_percentage)
                        task.OccurError.connect(self.handle_error)
                        sl = task.run
                        logger.debug(f"Task {index} launched",tags="main:launch_selected_task")
                    else:
                        sl = None

            if not task.paused:
                if sl is not None:
                    threading_pool = ThreadPoolManager(max_workers=1)
                    threading_pool.submit_tasks([sl])
                    threading_pool.start()
                    self.set_status()
                    return 0
            else:
                task.resume()
                task.running = True
                task.statue = _("运行中")
                self.set_status()
                logger.debug(f"Task {index} resumed",tags="main:launch_selected_task")
                return 0

    def terminate_selected_task(self,row_index,checked=False):
        index = int(self.QueueList.item(row_index, 0).text())
        for i in self.task_queue:
            if i.index == index:
                i.stop()
                i.running = False
                i.stopped = True
                i.statue = _("已终止")
                self.set_status()
                logger.debug(f"Task {index} terminated",tags="main:terminate_selected_task")



    def browse_single_video_file(self):
        file_path, wtf = QFileDialog.getOpenFileName(
            self,  # 父窗口
            _("选择视频文件"),  # 对话框标题
            "",  # 初始目录（空字符串表示当前目录）
            _("视频文件 (*.mp4 *.avi *.mkv *.mov)")  # 文件过滤器
        )
        if file_path:
            self.SLTL.setText(file_path)
            logger.debug(f"Single video file {file_path} selected",tags="main:browse_single_video_file")



    def create_single_task_via_button(self):
        if len(self.SLTL.text()) == 0:
            return
        self.create_single_task([self.SLTL.text()])
        logger.debug(f"Single task {self.SLTL.text()} created",tags="main:create_single_task_via_button")

    def scan_preset(self):
        plo = []
        preset_list = os.listdir(preset_path)
        if preset_list:
            for i in preset_list:
                plo.append(i.split(".")[0])
            if self.preset_list != plo:
                self.PresentList.clear()
                self.PresentList.addItems(plo)
            self.preset_list = plo
        else:
            self.PresentList.clear()


    def create_new_preset(self):
        self.create_single_task(["Dummy"],True)
        logger.debug(f"New preset created",tags="main:create_new_preset")

    def sync_queue(self):
        self.QueueList.setRowCount(0)
        self.QueueList.clearContents()
        for i in self.task_queue:
            index = i.index
            name = os.path.basename(i.file).split(".")[0]
            statue = i.status
            output_path = i.output_path
            metadata = {'index': index, 'name': name, 'status': statue, 'output_path': output_path, 'progress': 0,
                        "thumbnail": extract_video_frames(i.file,[0])[0]}
            self.add_to_queue(metadata)
            logger.debug(f"Task {index} added to queue",tags="main:sync_queue")


    def update_progress(self,index,progress):
        self.QueueList.setItem(index, 4, QTableWidgetItem(str(progress)))


    def set_status(self):
        for i in self.task_queue:
            for row in range(self.QueueList.rowCount()):
                if self.QueueList.item(row, 0).text() == str(i.index):
                    self.QueueList.setItem(row, 2, QTableWidgetItem(i.statue))

    def dummy_function(self,*args,**kwargs):
        pass

    def update_default(self):
        if self.current_selected_task is None:
            status_list = []
            for i in self.task_queue:
                status_list.append(i.completed)
            if False in status_list:
                for i in self.task_queue:
                    if not i.completed:
                        self.default_detail_show = i
                        return

    def update_details(self):
        if self.task_queue:
            if self.current_selected_task is None:
                self.update_default()
                self.SourceLabel.setText(_("源文件:") + os.path.basename(self.default_detail_show.file))
                self.progressBar.setValue(self.default_detail_show.progress*100)
                self.FileNameLabel.setText(_("文件名:") + os.path.basename(self.default_detail_show.file))
                self.FilePathLabel.setText(_("文件路径:") + self.default_detail_show.file)
                self.FileFormatLabel.setText(_("格式:") + self.default_detail_show.output_format)
                self.ProjectPresentLabel.setText(_("项目预设:"))
                self.VideoInfoLabel.setText(_(f"视频:{get_video_parameters_simple(self.default_detail_show.file)}"))
                self.BitRateLabel.setText(_("码率:") + "Maximum Bitrate:"+str(self.default_detail_show.MaximumBitRate)+" Target Bitrate:"+str(self.default_detail_show.TargetBitRate))
                self.AudioLabel.setText(_(f"音频:{get_audio_parameters_simple(self.default_detail_show.file)}"))
                self.label_10.setImage(cv2_to_qpixmap(self.get_thumbnail(self.default_detail_show)))
                self.label_10.scaledToHeight(216)
                if self.default_detail_show.start_time is not None:
                    self.StartTimeLabel.setText(_("开始时间:") + self.default_detail_show.start_time)
                else:
                    self.StartTimeLabel.setText(_("开始时间:未开始"))
                if self.default_detail_show.consumed_timer is not None and self.default_detail_show.running:
                    self.ComsumedTimeLabel.setText(_("消耗时间:") + str(round(time.time() - self.default_detail_show.consumed_timer, 2)) + "s")

            else:
                for i in self.task_queue:
                    if i.index == self.current_selected_task+1:
                        self.SourceLabel.setText(_("源文件:") + os.path.basename(i.file))
                        self.progressBar.setValue(i.progress*100)
                        self.FileNameLabel.setText(_("文件名:") + os.path.basename(i.file))
                        self.FilePathLabel.setText(_("文件路径:") + i.file)
                        self.FileFormatLabel.setText(_("格式:") + i.output_format)
                        self.ProjectPresentLabel.setText(_("项目预设:"))
                        self.VideoInfoLabel.setText(_(f"视频:{get_video_parameters_simple(i.file)}"))
                        self.BitRateLabel.setText(_("码率:") + "Maximum Bitrate:"+str(i.MaximumBitRate)+" Target Bitrate:"+str(i.TargetBitRate))
                        self.AudioLabel.setText(_(f"音频:{get_audio_parameters_simple(i.file)}"))
                        self.label_10.setImage(cv2_to_qpixmap(self.get_thumbnail(i)))
                        self.label_10.scaledToHeight(216)
                        if i.start_time is not None:
                            self.StartTimeLabel.setText(_("开始时间:") + i.start_time)
                        else:
                            self.StartTimeLabel.setText(_("开始时间:未开始"))
                        if i.consumed_timer is not None and i.running:
                            self.ComsumedTimeLabel.setText(_("消耗时间:") + str(
                                round(time.time() - i.consumed_timer, 2)) + "s")
        else:
            self.label_10.setImage("assets/image/reisa.jpg")
            self.label_10.scaledToHeight(216)

    def prepare_thumbnail(self):
        with self.thumbnail_lock:
            if self.thumbnail_thread is not None and self.thumbnail_thread.is_alive():
                return  # 线程已在运行

            self.thumbnail_thread = threading.Thread(target=self._prepare_thumbnail)
            self.thumbnail_thread.start()


    def _prepare_thumbnail(self):

        index = range(1, 102)
        if self.task_queue:
            for i in self.task_queue:
                if str(i.progress_identify) not in list(self.thumbnail_cache.keys()):
                    logger.debug(f"Thumbnail cache for task not found, preparing...", tags="main:prepare_thumbnail")
                    self.thumbnail_status_signal.emit(_("正在生成缩略图..."))
                    spf_list = []
                    for ind in index:
                        # 确保帧号不超过视频总帧数-1（0-based索引）
                        frame_index = min(int(i.frame_count * (ind / 101)), i.frame_count - 1)
                        spf_list.append(frame_index)

                    frames = PyAv.extract_video_frames(i.file, spf_list)
                    thu = []
                    for idx, fra in enumerate(frames):
                        if fra is not None:
                            try:
                                resized_frame = resize_image_to_fixed_height_simple(fra)
                                if resized_frame is not None:
                                    thu.append(resized_frame)
                                else:
                                    print(
                                        f"Warning: resize_image_to_fixed_height_simple returned None for frame {spf_list[idx]}")
                            except Exception as e:
                                print(f"Error resizing frame {spf_list[idx]}: {e}")
                        else:
                            print(f"Warning: Frame {spf_list[idx]} extraction failed")

                    if thu:
                        self.thumbnail_cache.update({str(i.progress_identify): thu})
                        self.thumbnail_status_signal.emit(_("准备就绪"))
                        logger.success(f"Thumbnail cache for task {i.progress_identify} prepared successfully", tags="main:prepare_thumbnail")
                    else:
                        print(f"Error: No thumbnails generated for {i.progress_identify}")

    def clear_useless_cache(self):
        if self.task_queue:
            for i in self.task_queue:
                if str(i.progress_identify) in list(self.thumbnail_cache.keys()) and i.completed:
                    cache = self.thumbnail_cache[str(i.progress_identify)][-1]
                    self.thumbnail_cache[str(i.progress_identify)] = [cache]
        # print(self.task_queue)
        if not self.task_queue:
            self.thumbnail_cache = {}
            # logger.info(f"Thumbnail cache cleared successfully", tags="main:clear_useless_cache")




    def get_thumbnail(self,task):
        if self.task_queue:
            if str(task.progress_identify) in list(self.thumbnail_cache.keys()):
                if len(self.thumbnail_cache[str(task.progress_identify)]) <= 2:
                    return self.thumbnail_cache[str(task.progress_identify)][0]
                return (self.thumbnail_cache[str(task.progress_identify)])[int(task.progress*100)]
            else:
                return cv2.imread(r"assets\image\reisa.jpg")
        if task is None:
            return cv2.imread(r"assets\image\reisa.jpg")

    def jump_to_website(self,url):
        QDesktopServices.openUrl(QUrl(url))

    def show_error_feedback(self):
        if self.error_feedback_ui is None:
            self.error_feedback_ui = ErrorFeedbackUi_L()
        if error_list:
            for i in error_list:
                self.error_feedback_ui.add_error(i[0],i[1],i[2],i[3],i[4])
        self.error_feedback_ui.show()

    def handle_error(self, err, _id,dump_file):
        print(err)
        print(dump_file)
        window = error_report.ErrorReportDialog(error=err,dump_file=dump_file)
        window.error_signal.connect(self.show_error_feedback)
        self.error_window.append(window)
        error_list.append([err[0],"CRITICAL",err[1],dump_file,get_log()])
        self.error_window[-1].show()
        for i in self.task_queue:
            if i.progress_identify == _id:
                i.statue = _("错误")
                i.completed = True
                i.update_progress.disconnect(self.update_queue_percentage)
                i.stop()
                for row in range(self.QueueList.rowCount()):
                    if self.QueueList.item(row, 0).text() == str(i.index):
                        progressbar = self.QueueList.cellWidget(row, 4)
                        progressbar.setValue(100)
                        self.QueueList.setItem(row, 2, QTableWidgetItem(i.statue))

        for ai in self.task_queue:
            logger.debug(f"Task {ai.progress_identify} status updated to {ai.statue}", tags="main:handle_error")



    def receive_preset(self,preset,name):
        preset['file'] = None
        preset['output_path'] = None
        preset['watermark_content'] = None
        self.save_preset(preset,name)
        logger.info(f"Preset {name} saved successfully", tags="main:save_preset")


    def save_preset(self,template,name):
        if os.path.exists("preset"):
            pass
        else:
            os.mkdir("preset")
        if not os.path.exists(f"preset/{name}.pickle"):
            with open(f"preset/{name}.pickle",'wb') as f:
                pickle.dump(template,f)





    def create_single_task(self, files,preset=False):
        if len(files) > 1:
            showFlyout(self,self.SingleInputSelector,InfoBarIcon.WARNING,_("请勿拖入多个文件"),_("非法操作"))
        else:
            if not preset:
                file = files[0]
                self.setUp_form = CreateNewProject(file,self)
                self.setUp_form.setWindowModality(Qt.ApplicationModal)
                self.setUp_form.show()
                self.setUp_form.complete.connect(self.save_profile)
                self.setUp_form.create_preset.connect(self.receive_preset)
            else:
                file = files[0]
                self.setUp_form = CreateNewProject(file, self)
                self.setUp_form.setWindowModality(Qt.ApplicationModal)
                self.setUp_form.PB_Confirm.hide()
                self.setUp_form.PB_Cancel.hide()
                self.setUp_form.L_CreateProject.setText(_("新建预设"))
                self.setUp_form.setWindowTitle(_("创建预设"))
                self.setUp_form.show()
                self.setUp_form.create_preset.connect(self.receive_preset)

    def add_batch_process(self, files):
        self.batch_setUp_form = CreateNewProject(files, self)
        self.batch_setUp_form.setWindowModality(Qt.ApplicationModal)
        self.batch_setUp_form.show()
        self.batch_setUp_form.complete.connect(self.set_batch_file)
        self.batch_setUp_form.create_preset.connect(self.receive_preset)

    #处理批量模板任务的函数，但是以前的名字和qt内部函数冲突。WTF？？？
    def idkwant_but_the_function_name_have_conflict_with_qt(self,arg):
        self.set_batch_file([arg[0],arg[1]])
        self.confirm_preset_form.close()
        logger.info(f"Batch preset {arg[1]} created successfully", tags="main:idkwant_but_the_function_name_have_conflict_with_qt")

    def rec_pre(self,args):
        self.save_profile(args)
        self.confirm_preset_form.close()
        logger.info(f"Batch preset {args['name']} saved successfully", tags="main:rec_pre")


    def set_batch_file(self,preset_data = None):
        if not preset_data:
            args = self.batch_setUp_form.save_watermark_profile()
        else:
            args = preset_data[0]
        origin = copy.deepcopy(args)
        if not preset_data:
            meiji_obj = self.batch_setUp_form.file_path
        else:
            meiji_obj = copy.deepcopy(preset_data[1])
        for i in meiji_obj:
            args.update({'file': i})
            args.update({'output_path': os.path.join(origin['output_path'],os.path.basename(i).split(".")[0])})
            self.temporary = ProcessUnit.ProcessUnit(i)
            self.temporary.set_args(**args)
            self.temporary.index = len(self.task_queue)+1
            self.temporary.progress_identify = str(uuid.uuid4())
            self.temporary.dump_uuid = str(uuid.uuid4())

            self.task_queue.append(self.temporary)
        if not preset_data:
            self.batch_setUp_form.close()
        self.sync_queue()
        logger.info(f"Batch preset {args['name']} processed successfully", tags="main:set_batch_file")



        
    def save_profile(self,preset = None):
        if not preset:
            templ = self.setUp_form.save_watermark_profile()
        else:
            templ = preset
        self.temporary = ProcessUnit.ProcessUnit(templ['file'])
        self.temporary.set_args(**templ)
        self.temporary.index = len(self.task_queue)+1
        self.temporary.progress_identify = str(uuid.uuid4())
        self.temporary.dump_uuid = str(uuid.uuid4())
        self.task_queue.append(self.temporary)
        if not preset:
            self.setUp_form.close()
        self.sync_queue()



    def setButtons(self):
        self.error_window = []
        self.StartButton.clicked.connect(self.start_all_task)
        self.StopButton.clicked.connect(self.queue_stop)
        self.PauseButton.clicked.connect(self.queue_suspend)
        self.CreatePresentButton.clicked.connect(self.create_new_preset)
        self.DeletePresentButton.clicked.connect(self.remove_selected_preset)



    def start_all_task(self):
        self.started = True
        self.played = False
        corre_ = threading.Thread(target=self.queue_start)
        corre_.start()


    def queue_start(self,resume_task=False):
        start_list = []
        for task in self.task_queue:
            if not task.running and task.status != 0 and task.completed != True and task.stopped != True:
                if not task.paused:
                    task.running = True
                    task.statue = _("运行中")
                    task.consumed_timer = time.time()
                    task.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    task.update_progress.connect(self.update_queue_percentage)
                    task.OccurError.connect(self.handle_error)
                    start_list.append(task.run)
            if not task.running and task.status != 0 and task.completed != True and task.stopped != True and task.paused == True:
                task.running = True
                task.statue = _("运行中")
                task.update_progress.connect(self.update_queue_percentage)
                task.OccurError.connect(self.handle_error)
                task.resume()
        if start_list != []:
            threading_pool = ThreadPoolManager(max_workers=1)
            threading_pool.submit_tasks(start_list)
            threading_pool.start()
        logger.debug(f"Started {len(start_list)} tasks", tags="main:queue_start")
        self.set_status()

    def queue_suspend(self):
        has_single = False
        for task in self.task_queue:
            if task.process_limit == 1:
                has_single = True
            if task.running and task.process_limit != 1:
                task.suspend()
                task.running = False
                task.paused = True
                task.statue = _("已暂停")
        self.set_status()
        if has_single:
            showFlyout(self, self.QueueList, InfoBarIcon.WARNING, _("已暂停所有可暂停任务"), _("单进程任务暂时无法暂停"))
        logger.debug(f"Paused {len(self.task_queue)} tasks", tags="main:queue_suspend")


    def queue_stop(self):
        for task in self.task_queue:
            if task.running:
                task.stop()
                task.running = False
                task.completed = _("已终止")
        self.set_status()
        logger.info(f"Stopped {len(self.task_queue)} tasks", tags="main:queue_stop")



    def set_first_selected(self):
        all = self.get_selected_rows()
        if all:
            self.current_selected_task = all[0]
            self.update_details()
        else:
            self.current_selected_task = None

    def get_selected_rows(self):
        """获取所有选中的行号"""
        selected_ranges = self.QueueList.selectedRanges()
        selected_rows = set()  # 使用集合避免重复

        for range_ in selected_ranges:
            selected_rows.update(range(range_.topRow(), range_.bottomRow() + 1))

        return sorted(selected_rows)  # 返回排序后的列表


    def start_selected_task(self):
        for task in self.task_queue:
            if task.running:
                task.start()
                task.running = True
                self.temporary.consumed_timer = time.time()

                task.update_progress.connect(self.update_queue_percentage)
                task.OccurError.connect(self.handle_error)

    def apply_preset(self,drag_trigger=False):
        if self.get_current_selection() is not None:
            if drag_trigger or len(self.SLTL.text()) > 0:
                if not drag_trigger:
                    self.confirm_preset_form = Preset_Confirm(parent=self, file=self.SLTL.text(), preset_name=self.get_current_selection())
                else:
                    self.confirm_preset_form = Preset_Confirm(parent=self, file=drag_trigger,
                                                              preset_name=self.get_current_selection())
                self.confirm_preset_form.setWindowModality(Qt.ApplicationModal)
                self.confirm_preset_form.show()
                self.confirm_preset_form.save.connect(self.rec_pre)
                logger.info(f"Preset {self.get_current_selection()} applied successfully", tags="main:apply_preset")



    def apply_preset_multi(self,drag_trigger=False):
        if self.get_current_selection() is not None:
            if drag_trigger != False or len(self.MLTL.text()) > 0:
                if not drag_trigger:
                    if os.path.exists(self.MLTL.text()):
                        file_list = os.listdir(self.MLTL.text())
                        path_list = []
                        for i in file_list:
                            path_list.append(os.path.join(self.MLTL.text(),i))
                else:
                    path_list = drag_trigger
                    self.confirm_preset_form = Preset_Confirm(parent=self,file=path_list,preset_name=self.get_current_selection())
                    self.confirm_preset_form.setWindowModality(Qt.ApplicationModal)
                    self.confirm_preset_form.show()
                    self.confirm_preset_form.save_batch.connect(self.idkwant_but_the_function_name_have_conflict_with_qt)
                    logger.info(f"Batch preset {self.get_current_selection()} applied successfully", tags="main:apply_preset_multi")

    def receive_preset_drag(self,file):
        if self.get_current_selection() is None:
            showFlyout(self, self.PresentList, InfoBarIcon.ERROR, _("请先选择一个预设"),_("错误"))
            return
        for i in file:
            if str(i).split(".")[-1] not in ["mp4","avi","mov","mkv"]:
                showFlyout(self, self.PresentList, InfoBarIcon.ERROR, _("仅支持视频文件"), _("错误"))
                return
        if len(file) == 1:
            self.apply_preset(drag_trigger=file)
        elif len(file) > 1:
            self.apply_preset_multi(drag_trigger=file)


    def get_current_selection(self):
        """获取列表组件的当前选择"""
        current_item = self.PresentList.currentItem()
        if current_item:
            return current_item.text()
        return None






    def update_queue_percentage(self,value,msg,id_uuid):
        index = None
        for task in self.task_queue:
            if task.progress_identify == id_uuid:
                index = task.index
                break
        for row in range(self.QueueList.rowCount()):
            if self.QueueList.item(row, 0).text() == str(index):
                progress_bar = self.QueueList.cellWidget(row, 4)
                progress_bar.setValue(value*100)
                break

    def remove_selected_preset(self):
        if os.path.exists(os.path.join(preset_path,f"{self.get_current_selection()}.pickle")):
            os.remove(os.path.join(preset_path,f"{self.get_current_selection()}.pickle"))
            logger.info(f"Preset {self.get_current_selection()} removed successfully", tags="main:remove_preset")


    def set_is_completed(self):
        for task in self.task_queue:
            if task.completed and task.status == 1:
                for row in range(self.QueueList.rowCount()):
                    if self.QueueList.item(row, 0).text() == str(task.index):
                        self.QueueList.setItem(row, 2, QTableWidgetItem(_("已完成")))
                        progress_bar = self.QueueList.cellWidget(row, 4)
                        progress_bar.setValue(100)
                        break
            elif task.status == 0:
                for row in range(self.QueueList.rowCount()):
                    if self.QueueList.item(row, 0).text() == str(task.index):
                        if task.stopped:
                            self.QueueList.setItem(row, 2, QTableWidgetItem(_("已终止")))
                        else:
                            self.QueueList.setItem(row, 2, QTableWidgetItem(_("错误")))
                        progress_bar = self.QueueList.cellWidget(row, 4)
                        progress_bar.setValue(100)
                        break

    def update_total_progress(self):
        total_progress = 0
        tpb = 0
        if self.QueueList.rowCount() != 0:
            for task in self.task_queue:
                total_progress += 1
            for pb in range(self.QueueList.rowCount()):
                progress_bar = self.QueueList.cellWidget(pb, 4)
                tpb += progress_bar.value()
            if total_progress != 0:
                self.QueueProgressBar.setValue(tpb/total_progress)
            self.set_is_completed()


    def terminal_all_task(self):
        self.temporary.stop()

    def set_progess_bar(self, value, message,id_uuid):
        self.QueueProgressBar.setValue(value*100)
        self.statusbar.showMessage(message)

    def add_to_queue(self,metadata):
        row = self.QueueList.rowCount()
        self.QueueList.insertRow(row)

        index_item = QTableWidgetItem(str(metadata['index']))
        index_item.setTextAlignment(Qt.AlignCenter)
        self.QueueList.setItem(row, 0, index_item)

        name_item = QTableWidgetItem(str(metadata['name']))
        self.QueueList.setItem(row, 1, name_item)

        status_item = QTableWidgetItem(str(metadata['status']))
        status_item.setTextAlignment(Qt.AlignCenter)
        self.QueueList.setItem(row, 2, status_item)

        thumbnail_label = ImageLabel()
        pixmap = cv2_to_qpixmap(metadata['thumbnail'])
        if not pixmap.isNull():
            # 缩放缩略图到合适大小
            thumbnail_label.setPixmap(pixmap.scaled(60, 40, Qt.KeepAspectRatio))
        else:
            thumbnail_label.setText("无图片")
        thumbnail_label.setAlignment(Qt.AlignCenter)
        self.QueueList.setCellWidget(row, 3, thumbnail_label)

        progress_bar = QProgressBar()
        progress_bar.setValue(metadata['progress'])
        progress_bar.setAlignment(Qt.AlignCenter)
        self.QueueList.setCellWidget(row, 4, progress_bar)

        output_path_item = QTableWidgetItem(str(metadata['output_path']))
        self.QueueList.setItem(row, 5, output_path_item)
        logger.debug(f"Added task {metadata['index']} to queue", tags="main:add_to_queue")


    def set_text(self):
        self.QueueList.setColumnCount(6)
        self.QueueList.setHorizontalHeaderLabels([_("索引"), _("名称"), _("状态"), _("缩略图"), _("进度条"),_("输出路径")])
        header = self.QueueList.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # 所有列自适应内容
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # 名称列拉伸填充剩余空间
        self.QueueLabel.setText(_("渲染队列"))
        self.tabWidget.setTabText(0, _("快捷导入"))
        self.tabWidget.setTabText(1, _("媒体浏览器"))
        self.label_Present.setText(_("预设"))
        self.CreatePresentButton.setText(_("创建新模板"))
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

    def closeEvent(self, event):
        print("TryToClose",self.update_close)
        try:
            if self.credit_window is not None:
                self.credit_window.close()
            if self.new_version_window is not None:
                self.new_version_window.close()
            if self.error_feedback_ui is not None:
                self.error_feedback_ui.close()
            if self.preference_window is not None:
                self.preference_window.close()
            if self.upscale_window is not None:
                self.upscale_window.close()
            if self.recover_window is not None:
                self.recover_window.close()
            if self.confirm_preset_form is not None:
                self.confirm_preset_form.close()
            if not self.error_window:
                for i in self.error_window:
                    i.close()
            if self.setUp_form is not None:
                self.setUp_form.close()
        finally:
            if self.log_process:
                self.log_process.terminate()
            if is_running_simple("ffmpeg.exe"):
                if kill_process_by_name("ffmpeg"):
                    if self.update_close:
                        run_updater()
                    event.accept()
                else:
                    event.ignore()
            else:
                if self.update_close:
                    run_updater()
                event.accept()
                
                
    def set_button_status(self,status):
        self.preference_window.SoftwareVersionCheckButton.setEnabled(status)

    def show_new_version_window(self,data):
        self.new_version_window = check_update(data[0], data[1], data[2])
        self.new_version_window.update_signal.connect(self.close_for_update)
        self.new_version_window.show()
        
    def check_update_from_github(self):
        if self.check_thread is None:
            self.check_thread = threading.Thread(target=self._check_update_from_github)
            self.check_thread.start()
        self.check_update_timer.stop()

    def already_latese(self):
        showFlyout(self, self.preference_window.SoftwareVersionCheckButton, InfoBarIcon.SUCCESS, _("已检查最新版本"),
                   _("当前版本为最新版本"))

    def _check_update_from_github(self):
        try:
            self.update_button_signal.emit(False)
            _version , _log = update_check.get_latest_github_release_info(const.owner,const.name)
            ignorance = ""
            if os.path.exists("ignore_version.txt"):
                with open("ignore_version.txt","r") as f:
                    ignorance = f.read()
            if _version not in ignorance and _version != const.__version__:
                data = update_check.get_latest_release_assets(const.owner, const.name)
                self.snw.emit([_version,_log,data])
            else:
                self.anv.emit()
                self.update_button_signal.emit(True)
        finally:
            self.update_button_signal.emit(True)
            self.check_thread = None



    def close_for_update(self):
        self.update_close = True
        self.close()







class CreateNewProject(QFrame,Ui_SetUpNewForm):
    complete = Signal()
    create_preset = Signal(dict,str)
    detail_timer = QTimer()
    def __init__(self, file_path,parent=None):
        super().__init__(parent, Qt.Window)
        self.video_length = None
        self.setupUi(self)
        self.render_device = _devices
        self.set_text()
        self.set_connections()
        self.initial_CB()
        self.prev_review = None
        self._prev_temp = None
        self.size = None
        self.checker = QTimer()
        self.checker.timeout.connect(self.setup_correct_setting_item)
        self.checker.start(50)
        self.template = None
        self.file_path = file_path
        self.PB_Confirm.clicked.connect(self.completed)
        self.PB_saveaspreset.clicked.connect(self.generate_preset)
        self.detail_timer.timeout.connect(self.display_detail)
        self.detail_timer.start(100)
        self.CB_MultiProcess.setChecked(True)
        self.CB_MultiProcess.setEnabled(False)
        self.CB_ProjectType.setEnabled(False)
        self.L_D_OutputPath.setText("")
        self.L_D_CalculateOccupation.setText("")
        self.PB_wmcontent.clicked.connect(self.select_image)
        if os.path.exists("setting.json"):
            with open("setting.json","r") as f:
                self.preference_args = json.load(f)
        self.LE_VideoExportPath.setText(self.preference_args["DefaultSavePath"])
        self.PB_VideoExportPath.clicked.connect(self.set_out_path)




    def completed(self):
        if self.check_validity():
            self.complete.emit()
            self.hide()

    def get_length(self):
        if type(self.file_path) == str:
            if os.path.exists(self.file_path):
                self.video_length = float(_get_duration_opencv(self.file_path) / 60)
        else:
            if os.path.exists(self.file_path[0]):
                self.video_length = float(_get_duration_opencv(self.file_path[0]) / 60)

    def select_image(self):
        path = QFileDialog.getOpenFileName(self, _("选择水印图片"), os.path.expanduser("~"), "图片文件 (*.png *.jpg *.jpeg)")
        if path[0]:
            self.LE_WatermarkContent.setText(path[0])



    def calculate_file_size(self):
        """
        计算VBR编码的视频文件大小

        参数:
        target_bitrate: 目标比特率 (Mbps)
        max_bitrate: 最大比特率 (Mbps)
        encoding: 编码方式 ('AV1', 'DXV', 'H264', 'HEVC')
        duration_minutes: 视频时长 (分钟)

        返回:
        file_size_mb: 文件大小 (MB)
        file_size_gb: 文件大小 (GB)
        """

        # 验证编码方式

        if self.video_length is None:
            self.get_length()
        if self.video_length is None:
            return None
        if self._prev_temp is None:
            return None
        if self._prev_temp['FFmpegEncoder'] == const.Encoder.NVIDIA_AV1:
            encoding = "AV1"
        elif self._prev_temp['FFmpegEncoder'] == const.Encoder.NVIDIA_HEVC or self._prev_temp['FFmpegEncoder'] == const.Encoder.AMD_HEVC:
            encoding = "HEVC"
        elif self._prev_temp['FFmpegEncoder'] == const.Encoder.NVIDIA_H264 or self._prev_temp['FFmpegEncoder'] == const.Encoder.X264 or self._prev_temp['FFmpegEncoder'] == const.Encoder.AMD_H264:
            encoding = "H264"
        elif self._prev_temp['FFmpegEncoder'] == const.Encoder.Resolume_DXV:
            encoding = "DXV"


        valid_encodings = ['AV1', 'DXV', 'H264', 'HEVC']
        if encoding.upper() not in valid_encodings:
            raise ValueError(f"不支持的编码方式。支持的编码方式: {valid_encodings}")
        if str(self._prev_temp['TargetBitRate'])[-1].upper() != "K" and str(self._prev_temp['TargetBitRate'])[-1].upper() != "M":
            return None
        if str(self._prev_temp['MaximumBitRate'])[-1].upper() != "K" and str(self._prev_temp['MaximumBitRate'])[-1].upper() != "M":
            return None
        if str(self._prev_temp['TargetBitRate'])[-1].upper() == "K":
            target_bitrate = int(int(self._prev_temp['TargetBitRate'][:-1]) / 1000)
        else:
            target_bitrate = self._prev_temp['TargetBitRate'][:-1]
        if str(self._prev_temp['MaximumBitRate'])[-1].upper() == "K":
            max_bitrate = int(int(self._prev_temp['MaximumBitRate'][:-1]) / 1000)
        else:
            max_bitrate = self._prev_temp['MaximumBitRate'][:-1]
        duration_minutes = self.video_length
        target_bitrate = int(target_bitrate)
        max_bitrate = int(max_bitrate)
        # 验证比特率合理性
        if target_bitrate <= 0 or max_bitrate <= 0:
            return None

        if target_bitrate > max_bitrate:
            return None

        # 不同编码方式的效率系数（基于实际压缩效率）
        efficiency_factors = {
            'AV1': 1.4,  # AV1效率最高
            'HEVC': 1.2,  # HEVC次之
            'H264': 1.0,  # H264作为基准
            'DXV': 0.8  # DXV通常用于无损或高质量压缩，效率较低
        }

        # 计算VBR平均比特率（目标比特率和最大比特率的加权平均）
        # 对于VBR编码，我们使用目标比特率作为主要参考，但考虑最大比特率的影响
        vbr_average_bitrate = (target_bitrate * 0.7 + max_bitrate * 0.3)

        # 应用编码效率系数
        efficiency_factor = efficiency_factors[encoding.upper()]
        effective_bitrate = vbr_average_bitrate * efficiency_factor

        # 计算文件大小（比特 -> 字节转换）
        # 公式: (比特率 × 时长) / 8 = 文件大小(字节)
        duration_seconds = duration_minutes * 60
        file_size_bits = effective_bitrate * 1e6 * duration_seconds  # 转换为比特
        file_size_bytes = file_size_bits / 8  # 转换为字节
        file_size_mb = file_size_bytes / (1024 * 1024)  # 转换为MB
        file_size_gb = file_size_mb / 1024  # 转换为GB

        return {
            'encoding': encoding.upper(),
            'duration_minutes': duration_minutes,
            'target_bitrate_mbps': target_bitrate,
            'max_bitrate_mbps': max_bitrate,
            'calculated_average_bitrate_mbps': vbr_average_bitrate,
            'file_size_mb': round(file_size_mb, 2),
            'file_size_gb': round(file_size_gb, 2)
        }

    def display_detail(self):
        try:
            preview_content = self.generate_profile(True)
        except ValueError:
            return
        except:
            raise
        stt = ""
        stt += "参数   参数值\n"
        stt += "----------\n"
        for key, value in preview_content.items():

            stt += f"{key}:{value}\n"
        if stt == self.prev_review:
            pass
        else:
            self.TB_S_Detail.setText(stt)
        self.prev_review = stt
        self.L_D_OutputPath.setText(f"{self.LE_VideoExportPath.text()}")
        size = self.calculate_file_size()
        if size is not None:
            self.L_D_CalculateOccupation.setText(f"预计占用空间:{size['file_size_mb']} MB")








    def save_watermark_profile(self):
        self.generate_profile()
        return self.template

    def generate_preset(self):
        if self.check_validity():
            self.generate_profile()
            self.create_preset.emit(self.template,self.LE_PresetName.text())


    def generate_profile(self,previews=False):


        watermark_method = None

        file = None
        watermark_method = None
        attachment_data = None
        output_name = None
        output_path = None
        slice_length = None
        sample_times = None
        sample_extend = None
        multi_process = None
        sample_type = None
        manual_sample_sheet = None
        watermark_content = None
        bitrate_control = None
        MaximumBitRate = None
        TargetBitRate = None
        FFmpegEncoder = None
        FFmpegTune = None
        FFmpegPresent = None
        FFmpegForeward = None
        FFmpegSelfAdaptive = None
        two_pass = None
        output_format = None
        file = self.file_path
        if int(self.CB_WatermarkAgori.currentIndex()) == 0:
            if self.CB_IW.isChecked():
                watermark_method = const.WatermarkAlgorithm.IMAGE_GUOFEI
                if "," in str(self.LE_wmpara1.text()):
                    num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),int(self.LE_wmpara1.text().split(",")[1]))
                else:
                    num1 = int(self.LE_wmpara1.text())

                if "," in str(self.LE_wmpara2.text()):
                    num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),int(self.LE_wmpara2.text().split(",")[1]))
                else:
                    num2 = int(self.LE_wmpara2.text())
                attachment_data = {
                    "img_password":num1,
                    "wm_password":num2
                }
                if not previews:
                    watermark_content = cv2.imread(self.LE_WatermarkContent.text())
                else:
                    watermark_content = self.LE_WatermarkContent.text()
            else:
                watermark_method = const.WatermarkAlgorithm.TEXT_GOUFEI
                if "," in str(self.LE_wmpara1.text()):
                    num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),int(self.LE_wmpara1.text().split(",")[1]))
                else:
                    num1 = int(self.LE_wmpara1.text())

                if "," in str(self.LE_wmpara2.text()):
                    num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),int(self.LE_wmpara2.text().split(",")[1]))
                else:
                    num2 = int(self.LE_wmpara2.text())
                attachment_data = {
                    "img_password": num1,
                    "wm_password": num2
                }
                watermark_content = str(self.LE_WatermarkContent.text())
        elif int(self.CB_WatermarkAgori.currentIndex()) == 1:
            watermark_method = const.WatermarkAlgorithm.IMAGE_FIREKEEPER
            if "," in str(self.LE_wmpara1.text()):
                num1 = random.randint(int(self.LE_wmpara1.text().split(",")[0]),
                                      int(self.LE_wmpara1.text().split(",")[1]))
            else:
                num1 = int(self.LE_wmpara1.text())

            if "," in str(self.LE_wmpara2.text()):
                num2 = random.randint(int(self.LE_wmpara2.text().split(",")[0]),
                                      int(self.LE_wmpara2.text().split(",")[1]))
            else:
                num2 = int(self.LE_wmpara2.text())
            if "," in str(self.LE_wmpara3.text()):
                num3 = random.randint(int(self.LE_wmpara3.text().split(",")[0]),
                                      int(self.LE_wmpara3.text().split(",")[1]))
            else:
                num3 = int(self.LE_wmpara3.text())

            if "," in str(self.LE_wmpara4.text()):
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
            if not previews:
                watermark_content = cv2.imread(self.LE_WatermarkContent.text())
            else:
                watermark_content = self.LE_WatermarkContent.text()
        elif int(self.CB_WatermarkAgori.currentIndex()) == 2:
            watermark_method = const.WatermarkAlgorithm.TEXT_FREQM
            attachment_data = {
                'method':'dwtDct',
                'wmType':'bytes'
            }
            watermark_content = str(self.LE_WatermarkContent.text())
        elif int(self.CB_WatermarkAgori.currentIndex()) == 3:
            watermark_method = const.WatermarkAlgorithm.TEXT_RIVAGAN
            attachment_data = {
                'method':'rivaGan',
                'wmType':'bytes'
            }
            watermark_content = str(self.LE_WatermarkContent.text())
        output_name = "embedded"
        output_path = str(self.LE_VideoExportPath.text())
        slice_length = int(self.SB_Slicelength.value())
        sample_times = int(self.SB_SamplerTimes.value())
        sample_extend = int(self.SB_FrameExtend.value())
        if self.CB_MultiProcess.isChecked():
            if int(self.SB_MultiProcess.value()) <= 61:
                multi_process = int(self.SB_MultiProcess.value())
            else:
                multi_process = 61
        else:
            multi_process = 1
        if int(self.CB_Sampler.currentIndex()) == 0:
            sample_type = const.SamplerType.RANDOM
        elif int(self.CB_Sampler.currentIndex()) == 1:
            sample_type = const.SamplerType.AVERAGE
        elif int(self.CB_Sampler.currentIndex()) == 2:
            sample_type = const.SamplerType.MANUAL
            manual_sample_sheet = str(self.LE_SamplerSheet.text())
        elif int(self.CB_Sampler.currentIndex()) == 3:
            sample_type = const.SamplerType.FULL

        current_device = self.CB_RenderDevices.currentText()
        if self.render_device[current_device] == "cpu":
            if "DXV" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.Resolume_DXV
            else:
                FFmpegEncoder = const.Encoder.X264

        elif self.render_device[current_device] == "nvidia":
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.NVIDIA_H264
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.NVIDIA_HEVC
            elif "AV1" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.NVIDIA_AV1
        elif self.render_device[current_device] == "amd":
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.AMD_H264
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                FFmpegEncoder = const.Encoder.AMD_HEVC
        if int(self.CB_BitRateControl.currentIndex()) == 0:
            bitrate_control = const.BitRateControl.VBR
        elif int(self.CB_BitRateControl.currentIndex()) == 1:
            bitrate_control = const.BitRateControl.CBR

        MaximumBitRate = str(self.LE_MaxBitRate.text())
        TargetBitRate = str(self.LE_BitRate.text())
        if self.CB_VideoExportFormat.text() == "MP4":
            output_format = "mp4"
        elif self.CB_VideoExportFormat == "MKV":
            output_format = "mkv"
        elif self.CB_VideoExportFormat.text() == "MOV":
            output_format = "mov"
        if self.render_device[current_device] == "cpu":
            if str(self.CB_FFmpegPresent.text()) == "PLACEBO":
                FFmpegPresent = const.FFmpegPreset.X264_PLACEBO
            elif str(self.CB_FFmpegPresent.text()) == "VERYSLOW":
                FFmpegPresent = const.FFmpegPreset.X264_VERYSLOW
            elif str(self.CB_FFmpegPresent.text()) == "SLOWER":
                FFmpegPresent = const.FFmpegPreset.X264_SLOWER
            elif str(self.CB_FFmpegPresent.text()) == "SLOW":
                FFmpegPresent = const.FFmpegPreset.X264_SLOW
            elif str(self.CB_FFmpegPresent.text()) == "MEDIUM":
                FFmpegPresent = const.FFmpegPreset.X264_MEDIUM
            elif str(self.CB_FFmpegPresent.text()) == "FAST":
                FFmpegPresent = const.FFmpegPreset.X264_FAST
            elif str(self.CB_FFmpegPresent.text()) == "FASTER":
                FFmpegPresent = const.FFmpegPreset.X264_FASTER
            elif str(self.CB_FFmpegPresent.text()) == "VERYFAST":
                FFmpegPresent = const.FFmpegPreset.X264_VERYFAST
            elif str(self.CB_FFmpegPresent.text()) == "SUPERFAST":
                FFmpegPresent = const.FFmpegPreset.X264_SUPERFAST
            elif str(self.CB_FFmpegPresent.text()) == "ULTRAFAST":
                FFmpegPresent = const.FFmpegPreset.X264_UlTRAFAST
            elif str(self.CB_Tune.text()) == "FILM":
                FFmpegTune = const.FFmpegTune.X264_FILM
            elif str(self.CB_Tune.text()) == "ANIMATION":
                FFmpegTune = const.FFmpegTune.X264_ANIMATION
            elif str(self.CB_Tune.text()) == "GRAIN":
                FFmpegTune = const.FFmpegTune.X264_GRAIN
            elif str(self.CB_Tune.text()) == "STILLIMAGE":
                FFmpegTune = const.FFmpegTune.X264_STILLIMAGE
            elif str(self.CB_Tune.text()) == "PSNR":
                FFmpegTune = const.FFmpegTune.X264_PSNR
            elif str(self.CB_Tune.text()) == "SSIM":
                FFmpegTune = const.FFmpegTune.X264_SSIM

            if str(self.CB_Tune.text()) == "FILM":
                FFmpegTune = const.FFmpegTune.X264_FILM
            elif str(self.CB_Tune.text()) == "ANIMATION":
                FFmpegTune = const.FFmpegTune.X264_ANIMATION
            elif str(self.CB_Tune.text()) == "GRAIN":
                FFmpegTune = const.FFmpegTune.X264_GRAIN
            elif str(self.CB_Tune.text()) == "STILLIMAGE":
                FFmpegTune = const.FFmpegTune.X264_STILLIMAGE
            elif str(self.CB_Tune.text()) == "PSNR":
                FFmpegTune = const.FFmpegTune.X264_PSNR
            elif str(self.CB_Tune.text()) == "SSIM":
                FFmpegTune = const.FFmpegTune.X264_SSIM
            elif str(self.CB_Tune.text()) == "FASTDECODE":
                FFmpegTune = const.FFmpegTune.X264_FASTDECODE
            elif str(self.CB_Tune.text()) == "ZEROLANTENCY":
                FFmpegTune = const.FFmpegTune.X264_ZEROLANTENCY
        elif self.render_device[current_device] == "nvidia":
            if int(self.CB_EncodePattern.currentIndex()) == 0:
                two_pass = False
            else:
                two_pass = True
            if str(self.CB_FFmpegPresent.currentText()) == "P1":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P1
            elif str(self.CB_FFmpegPresent.currentText()) == "P2":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P2
            elif str(self.CB_FFmpegPresent.currentText()) == "P3":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P3
            elif str(self.CB_FFmpegPresent.currentText()) == "P4":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P4
            elif str(self.CB_FFmpegPresent.currentText()) == "P5":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P5
            elif str(self.CB_FFmpegPresent.currentText()) == "P6":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P6
            elif str(self.CB_FFmpegPresent.currentText()) == "P7":
                FFmpegPresent = const.FFmpegPreset.NVIDIA_P7
            if "H.264" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "High Quality":
                    FFmpegTune = const.FFmpegTune.NV_H264_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_H264_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_H264_SLL
            elif "HEVC" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "Super High Quality":
                    FFmpegTune = const.FFmpegTune.NV_H265_SHQ
                elif str(self.CB_Tune.text()) == "High Quality":
                    FFmpegTune = const.FFmpegTune.NV_H265_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_H265_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_H265_SLL
            elif "AV1" in str(self.CB_VideoEncoder.currentText()):
                if str(self.CB_Tune.text()) == "Super High Quality":
                    FFmpegTune = const.FFmpegTune.NV_AV1_SHQ
                elif str(self.CB_Tune.text()) == "High Quality":
                    FFmpegTune = const.FFmpegTune.NV_AV1_HQ
                elif str(self.CB_Tune.text()) == "Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_AV1_LL
                elif str(self.CB_Tune.text()) == "Super Low Latency":
                    FFmpegTune = const.FFmpegTune.NV_AV1_SLL
        elif self.render_device[current_device] == "amd":
            if self.CB_FFmpegPresent.currentData() == "quality":
                FFmpegPresent = const.FFmpegPreset.AMD_QUALITY
            elif self.CB_FFmpegPresent.currentData() == "balance":
                FFmpegPresent = const.FFmpegPreset.AMD_BALANCE
            elif self.CB_FFmpegPresent.currentData() == "speed":
                FFmpegPresent = const.FFmpegPreset.AMD_SPEED

        if self.CB_Foreward.isChecked():
            FFmpegForeward = int(self.SB_Forward.value())
        else:
            FFmpegForeward = None

        if self.CB_AdjustiveNormalize.isChecked():
            FFmpegSelfAdaptive = int(self.SB_AN.value())
        else:
            FFmpegSelfAdaptive = None
        process_unit_template = {
            "version": const.__version__,
            "file": file,
            "watermark_method": watermark_method,
            "attachment_data": attachment_data,
            "output_name": output_name,
            "output_path": output_path,
            "slice_length": slice_length,
            "sample_times": sample_times,
            "sample_extend": sample_extend,
            "process_limit": multi_process,
            "sample_type": sample_type,
            "manual_sample_sheet": manual_sample_sheet,
            "watermark_content": watermark_content,
            "BitRateControl": bitrate_control,
            "MaximumBitRate": MaximumBitRate,
            "TargetBitRate": TargetBitRate,
            "FFmpegEncoder": FFmpegEncoder,
            "FFmpegTune": FFmpegTune,
            "FFmpegPresent": FFmpegPresent,
            "FFmpegForeward": FFmpegForeward,
            "FFmpegSelfAdaptive": FFmpegSelfAdaptive,
            "output_format": output_format,
            "two_pass": two_pass,
        }
        if not previews:
            self.template = process_unit_template
        else:
            process_unit_template.update({"attachment_data":"To be added"})
            self._prev_temp = process_unit_template
            return process_unit_template


    def set_out_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.LE_VideoExportPath.setText(path)




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
        self.HS_FrameExtend.valueChanged.connect(self.sync_frame_set_HS)
        self.SB_FrameExtend.valueChanged.connect(self.sync_frame_set_SB)
        self.CB_Sampler.currentIndexChanged.connect(self.sample_set)
        self.CB_WatermarkAgori.currentIndexChanged.connect(self.set_watermark_params)

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
        if int(self.CB_WatermarkAgori.currentIndex()) == 3:
            if len(str(self.LE_WatermarkContent.text()).encode('utf-8')) != 4:
                showFlyout(self,self.LE_WatermarkContent,InfoBarIcon.ERROR,_("RivaGan算法目前并不支持四字节以外长度！"),_("水印长度不匹配！"))
                return False
        if len(self.LE_WatermarkContent.text()) >= 500:
            showFlyout(self, self.LE_WatermarkContent, InfoBarIcon.ERROR, _("其实这个并不是很能藏的......"),
                       _("水印长度过长！"))
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
        if len(self.LE_VideoExportPath.text()) == 0:
            showFlyout(self,self.LE_VideoExportPath,InfoBarIcon.ERROR,_("请输入导出路径！"),_("导出路径不能为空！"))
            return False
        if "AV1" in self.CB_VideoEncoder.text() and self.CB_VideoExportFormat == "MOV":
            showFlyout(self,self.CB_VideoEncoder,InfoBarIcon.ERROR,_("AV1编码不支持MOV格式！"),_("请选择其他格式进行编码"))
            return False
        if self.CB_Sampler.currentIndex() in [0,1] and self.SB_SamplerTimes.value() == 0:
            showFlyout(self,self.SB_SamplerTimes,InfoBarIcon.ERROR,_("请输入采样次数！"),_("采样次数不能为0！"))
            return False
        if self.SB_Slicelength.value() == 0:
            showFlyout(self,self.SB_Slicelength,InfoBarIcon.ERROR,_("请输入切片长度！"),_("切片长度不能为0！"))
            return False
        if len(self.LE_WatermarkContent.text()) == 0:
            showFlyout(self,self.LE_WatermarkContent,InfoBarIcon.ERROR,_("请输入水印内容！"),_("水印内容不能为空！"))
            return False
        if self.LE_wmpara1.isVisible() and len(self.LE_wmpara1.text()) == 0:
            showFlyout(self,self.LE_wmpara1,InfoBarIcon.ERROR,_("请输入参数1！"),_("参数1不能为空！"))
            return False
        if self.LE_wmpara2.isVisible() and len(self.LE_wmpara2.text()) == 0:
            showFlyout(self,self.LE_wmpara2,InfoBarIcon.ERROR,_("请输入参数2！"),_("参数2不能为空！"))
            return False
        if self.LE_wmpara3.isVisible() and len(self.LE_wmpara3.text()) == 0:
            showFlyout(self,self.LE_wmpara3,InfoBarIcon.ERROR,_("请输入参数3！"),_("参数3不能为空！"))
            return False
        if self.LE_wmpara4.isVisible() and len(self.LE_wmpara4.text()) == 0:
            showFlyout(self,self.LE_wmpara4,InfoBarIcon.ERROR,_("请输入参数4！"),_("参数4不能为空！"))
            return False
        if self.LE_wmpara1.isVisible():
            try:
                content = self.LE_wmpara1.text()
                res = content.replace(",","")
                int(res)
            except ValueError:
                showFlyout(self,self.LE_wmpara1,InfoBarIcon.ERROR,_("请输入参数1！"),_("参数1不合规！"))
                return False
        if self.LE_wmpara2.isVisible():
            try:
                content = self.LE_wmpara2.text()
                res = content.replace(",","")
                int(res)
            except ValueError:
                showFlyout(self,self.LE_wmpara2,InfoBarIcon.ERROR,_("请输入参数2！"),_("参数2不合规！"))
                return False
        if self.LE_wmpara3.isVisible():
            try:
                content = self.LE_wmpara3.text()
                res = content.replace(",","")
                int(res)
            except ValueError:
                showFlyout(self,self.LE_wmpara3,InfoBarIcon.ERROR,_("请输入参数3！"),_("参数3不合规！"))
                return False
        if self.LE_wmpara4.isVisible():
            try:
                content = self.LE_wmpara4.text()
                res = content.replace(",","")
                int(res)
            except ValueError:
                showFlyout(self,self.LE_wmpara4,InfoBarIcon.ERROR,_("请输入参数4！"),_("参数4不合规！"))
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
        self.CB_IW.show()
        if current_wm_method == _("GuoFei"):
            self.L_wmpara1.setText(_("图片密码"))
            self.LE_wmpara1.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara2.setText(_("水印密码"))
            self.LE_wmpara2.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara3.hide()
            self.LE_wmpara3.hide()
            self.L_wmpara4.hide()
            self.LE_wmpara4.hide()
            self.CB_IW.setEnabled(True)
        elif current_wm_method == _("FireKeeper"):
            self.L_wmpara1.setText(_("种子1"))
            self.LE_wmpara1.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara2.setText(_("种子2"))
            self.LE_wmpara2.setPlaceholderText(_("输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara3.setText(_("除数1"))
            self.LE_wmpara3.setPlaceholderText(_("除数越大鲁棒性越强，但图片失真越严重。输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.L_wmpara4.setText(_("除数2"))
            self.LE_wmpara4.setPlaceholderText(_("除数越大鲁棒性越强，但图片失真越严重。输入两个以半角逗号分割的数字以在选定范围内随机"))
            self.CB_IW.setEnabled(True)
            self.CB_IW.setChecked(True)
            self.CB_IW.setEnabled(False)
        elif "DCT" in current_wm_method or "RivaGan" in current_wm_method:
            self.CB_IW.setEnabled(False)
            self.CB_IW.hide()
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




    def set_encoder_options(self):
        current_encoder = self.CB_VideoEncoder.currentText()
        current_bitrate_control = self.CB_BitRateControl.currentText()


        if "AMD" in current_encoder:
            self.CB_FFmpegPresent.clear()
            self.CB_FFmpegPresent.addItem(_("质量"),userData="quality")
            self.CB_FFmpegPresent.addItem(_("均衡"),userData="balance")
            self.CB_FFmpegPresent.addItem(_("速度"),userData="speed")
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




def showFlyout(self,target,icon,content,title):
    Flyout.create(
        icon=icon,
        title=title,
        content=content,
        target=target,
        parent=self,
        isClosable=True
    )


import os


def is_larger_than_1gb(file_path):
    """
    检测文件大小是否大于1GB

    参数:
        file_path (str): 文件路径

    返回:
        bool: 如果文件大小大于1GB返回True，否则返回False
        str: 如果文件不存在或路径错误，返回错误信息
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False, f"文件不存在: {file_path}"

        # 检查是否为文件（不是目录）
        if not os.path.isfile(file_path):
            return False, f"路径不是文件: {file_path}"

        # 获取文件大小（字节）
        file_size = os.path.getsize(file_path)

        # 1GB = 1024 * 1024 * 1024 字节
        gb_size = 1024 * 1024 * 1024

        # 返回比较结果
        return file_size > gb_size, f"文件大小: {file_size} 字节 ({file_size / gb_size:.2f} GB)"

    except Exception as e:
        return False, f"检测文件大小时出错: {str(e)}"

def createSuccessInfoBar(self,title,content):
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        # position='Custom',   # NOTE: use custom info bar manager
        duration=2000,
        parent=self
    )



class RecoverWindow(QFrame,Ui_Recover_Form):
    def __init__(self, parent=None):
        super().__init__(parent,Qt.Window)
        self.plk_data = None
        self.watermark_file = None
        self.video_file = None
        self._inst = None
        self.setupUi(self)
        self.set_up()
        self.recover_process = None
        self.frame.receive_file.connect(self.check_and_start)
        self.result = None
        self.image_index = 1
        self.pushButton_2.clicked.connect(self.prev_image)
        self.pushButton_3.clicked.connect(self.next_image)
        self.progressBar.setValue(0)
        self.label_8.setScaledContents(True)
        self.label_8.setFixedSize(256,256)
        self.pushButton_4.clicked.connect(self.save_selected_image)
        self.pushButton_5.clicked.connect(self.save_all_image)
        self.pushButton.clicked.connect(self.save_text_to_file)
        self.tabWidget.setTabText(0,_("恢复设置"))
        self.tabWidget.setTabText(1,_("恢复结果"))
        self.soundplayer = AudioPlayer()
        self.soundplayer.load("assets/sound/complete.wav")
        self.pushButton_4.setText(_("保存当前图片"))
        self.pushButton_5.setText(_("保存所有图片"))
        self.setWindowTitle(_("恢复水印"))
        self.error_window = []


    def show_error_window(self,err,dump_file):
        print(err)
        print(dump_file)
        if len(self.error_window) <= 10:
            self.error_window.append(error_report.ErrorReportDialog(error=err, dump_file=dump_file))
            self.error_window[-1].show()




    def set_up(self):
        self.F_TextResult.hide()
        self.F_ImageResult.hide()
        self.label_5.setText(_("请先启动分析"))
        logger.debug("RecoverWindow initialized", tags="main:recover_init")

    def check_and_start(self,files):
        if len(files) != 2:
            showFlyout(self,self.L_title,InfoBarIcon.ERROR,_("请选择视频文件和水印文件"),_("错误"))
            return False
        if len(files) == 2:
            have_video = False
            have_pkl = False
            for i in files:
                if str(i).split(".")[-1] in ["mp4","mkv","avi","mov"]:
                    have_video = True
                    self.video_file = str(i)
                if str(i).split(".")[-1] == "pkl":
                    have_pkl = True
                    self.watermark_file = str(i)
            if have_pkl and have_video:
                self.plk_data = pickle.load(open(self.watermark_file, 'rb'))
                self.run_recover(self.video_file,self.watermark_file)
                self.label_5.setText(_("正在分析中，请稍候"))
                self.frame.hide()
                self.label_2.setText(_("分析中，请稍等"))
            else:
                showFlyout(self,self.L_title,InfoBarIcon.ERROR,_("请确定您的输入只含有视频文件和水印文件"),_("错误"))
                return False
        return True

    def pre_process_result(self,*args):
        self.process_result(self._inst.result)

    def process_result(self,result):
        ind = 1
        self.label_5.hide()
        self.result = result
        if self.plk_data['watermark_method'] == const.WatermarkAlgorithm.IMAGE_GUOFEI or self.plk_data[
            'watermark_method'] == const.WatermarkAlgorithm.IMAGE_FIREKEEPER:
            self.label_7.setText(_(f"分析完成，超过可识别阈值的图片有{len(result)}张"))
            self.F_ImageResult.show()
            self.F_TextResult.hide()
            self.L_CurIndex.setText(f"{self.image_index}/{len(self.result)}")
            self.progressBar_2.setValue(0)
            if len(self.result) > 0:
                self.set_correct_image()
        else:
            self.label_6.setText(_(f"分析完成，超过可识别阈值的文字{len(result)}组"))
            self.F_TextResult.show()
            self.F_ImageResult.hide()
            st = ""

            for i in result:
                st += _(f"组{ind}\n")
                for ite in i:
                    st += f"{ite}\n"
                ind = + 1
            self.textBrowser.setText(st)
        createSuccessInfoBar(self,_("分析完成"),_(f"请查看分析结果"))

        self.soundplayer.play()

    def save_text_to_file(self):
        if self.result:
            self._save_text_to_file(str(self.result))

    def _save_text_to_file(self,context):
        path = QFileDialog.getSaveFileName(self,_("保存文件"),f"recover_{self.image_index}.txt",_("文本文件 (*.txt)"))[0]
        if path:
            with open(path,"w",encoding="utf-8") as f:
                f.write(context)

    def save_selected_image(self):
        if self.result:
            path = QFileDialog.getSaveFileName(self,_("保存文件"),f"recover_{self.image_index}.png",_("图像文件 (*.png)"))[0]
            if path:
                cv2.imwrite(path, self.result[self.image_index-1])

    def save_all_image(self):
        if self.result:
            path = QFileDialog.getSaveFileName(self,_("保存文件"),f"recover_{self.image_index}.png",_("图像文件 (*.png)"))[0]
            if path:
                for i in range(len(self.result)):
                    cv2.imwrite(f"{path.split('.')[0]}_{i}.png", self.result[i])


    def set_correct_image(self):
        if self.image_index <= len(self.result):
            cur_img = self.result[self.image_index-1]
            img_path = f"recover_{self.image_index}_{uuid.uuid4()}.png"
            cv2.imwrite(img_path, cur_img)
            self.label_8.setImage(img_path)
            os.remove(img_path)





    def next_image(self):
        if 0 < self.image_index <= len(self.result):
            self.image_index += 1
            self.set_correct_image()
            self.L_CurIndex.setText(f"{self.image_index}/{len(self.result)}")
            self.progressBar_2.setValue(self.image_index*100//len(self.result))

    def prev_image(self):
        if 0 < self.image_index <= len(self.result):
            self.image_index -= 1
            self.set_correct_image()
            self.L_CurIndex.setText(f"{self.image_index}/{len(self.result)}")
            self.progressBar_2.setValue(self.image_index * 100 // len(self.result))


    def warpper_error(self,*args):
        self.show_error_window(args[0][0][0],args[0][1])




    def run_recover(self,file,recover_file):
        self._inst = ExtracUnit(file,recover_file,int(self.SB_MaxWorker.value()))
        self._inst.update_progress.connect(self.set_progress)
        self._inst.receive_result.connect(self.pre_process_result)
        self._inst.error_occured.connect(self.warpper_error)
        self.recover_process = threading.Thread(target=self._inst.run)
        self.recover_process.start()


    def set_progress(self,progress):
        if type(progress) == float:
            self.progressBar.setValue(progress*100)


class NonCriticalErrorDetail(QWidget,Ui_NonCriticalError):
    def __init__(self,error,parent=None):
        super().__init__(parent,Qt.Window)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(_("啊哈哈...发生非致命性错误"))
        self.label_2.setImage("./assets/image/NCW.png")
        self.label_2.scaledToHeight(64)
        self.label_2.setBorderRadius(8, 8, 8, 8)
        self.pushButton_2.setText(_("忽略"))
        self.pushButton.setText(_("报告错误"))
        self.label.setText(error[0])
        self.textBrowser.setText(error[1])
        self.pushButton_2.clicked.connect(self.close)


class check_update(QWidget,Ui_NewVersion):
    update_signal = Signal()
    def __init__(self,version,change_log,data):
        super().__init__()
        self.setupUi(self)
        # 设置为无边框透明窗口
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.version = version
        self.change_log = change_log
        for i in data:
            print(i)
            if i["name"] == "Windows_amd64.zip":
                self.download_url = i["download_url"]
                self.download_name = i["name"]
            if i["name"] == "AobaUpdater.exe":
                self.updater_url = i["download_url"]
                self.updater_name = i["name"]
        self.label_2.setText(self.version)
        self.textBrowser.setText(self.change_log)
        self.signal()
        self.download_window = None

    def signal(self):
        self.pushButton.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.update)
        self.pushButton_2.clicked.connect(self.ignore_version)

    def ignore_version(self):
        if os.path.exists("ignore_version.txt"):
            os.remove("ignore_version.txt")
        with open("ignore_version.txt","w") as f:
            f.write(self.version)
        self.close()

    def update(self):
        if self.download_window is None:
            self.download_window = DownloadWindow(self.download_url, self.download_name,self.updater_name,self.updater_url)
        self.download_window.show()
        self.download_window.rea.connect(self.ready)

    def ready(self):
        self.update_signal.emit()


class DownloadWindow(QWidget,Ui_DownloadNew):
    download_over_signal = Signal()
    rea = Signal()
    def __init__(self,download_url,download_name,updater_name,updater_url):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._downloader = None
        self.updater_name = updater_name
        self.updater_url = updater_url
        self.setupUi(self)
        self.download_url = download_url
        self.download_name = download_name
        print(self.download_url,self.download_name)
        self.pushButton.hide()
        self.label_2.setText(self.download_name)
        name = "archive."+str(self.download_name.split(".")[-1])
        self.downloader = multithread_downloader.MultiThreadDownloader(self.download_url,os.path.join("./download",name))
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.download_finished.connect(self.download_over)
        self.signal()
        self.download_updater()


    def signal(self):
        self.pushButton.clicked.connect(self.download)

    def download_updater(self):
        self._downloader = multithread_downloader.MultiThreadDownloader(self.updater_url,os.path.join("./download",self.updater_name),thread_count=4)
        self._downloader.progress_updated.connect(self.update_progress)
        self._downloader.download_finished.connect(self.download)
        self._downloader.start_download()

    def update_progress(self, progress):
        self.progressBar.setValue(progress)
        self.label_2.setText(f"{progress:.2f}%")

    def download_over(self):
        self.post_download()
        self.download_over_signal.emit()



    def download(self):
        self.downloader.start_download()

    def post_download(self):
        os.remove("AobaUpdater.exe")
        shutil.copy2("./download/AobaUpdater.exe","./")
        self.rea.emit()
        self.close()








def kill_process_by_name(process_name):
    """
    根据进程名称关闭程序

    Args:
        process_name (str): 要关闭的进程名称

    Returns:
        int: 成功关闭的进程数量
    """
    killed_count = 0

    for proc in psutil.process_iter(['name']):
        try:
            # 检查进程名称是否匹配（不区分大小写）
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                proc.kill()
                print(f"已关闭进程: {proc.info['name']} (PID: {proc.pid})")
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 处理异常情况
            pass

    if killed_count == 0:
        return False
    else:
        return True

def is_running_simple(process_name):
    """简单的单行检查函数"""
    return any(process_name.lower() in proc.info['name'].lower()
               for proc in psutil.process_iter(['name'])
               if proc.info['name'])


if __name__ == "__main__":
    print("Hello World!")
