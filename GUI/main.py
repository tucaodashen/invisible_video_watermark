"""
请伟大的早濑优香大人保佑这段代码吧！
"""
import copy
import os.path
import pickle
import random
import threading
import time
import uuid

import numpy as np

from modules.PyAv import extract_video_frames

import cv2
from PySide6.QtGui import QPixmap, QImage

from BasicSystem import const
from modules import ProcessUnit, PyAv
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QVBoxLayout, QTableWidgetItem, QProgressBar, \
    QHeaderView, QTableWidget, QFileDialog
from PySide6.QtCore import Qt, QTimer, Signal
from qfluentwidgets import FluentIcon as FIF, FlyoutViewBase, Flyout, InfoBarIcon, ImageLabel

from GUI.Splash import Ui_SplashDesu
from GUI.MainWindows import Ui_MainWindow
from GUI.Setting import Ui_Form as Ui_Setting
from GUI.SetUp import Ui_SetUpNewForm

import sys
from GUI import PrepareRequirements
import gettext
from PySide6.QtCore import Qt
from GUI import error_report
from modules.ThreadingScheduler import ThreadPoolManager
import os
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = 'TRUE'

_ = gettext.gettext
_devices = {'AMD Ryzen 9 9955HX 16-Core Processor': 'cpu', 'AMD Radeon(TM) 610M': 'amd', 'NVIDIA GeForce RTX 5070 Laptop GPU': 'nvidia'}
print(_devices)


from qfluentwidgets import Dialog, setTheme, Theme, PrimaryPushButton, MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel


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

    return canvas


def cv2_to_qpixmap(cv_img):
    """将 OpenCV 图像转换为 QPixmap"""
    # OpenCV 使用 BGR 格式，Qt 使用 RGB，需要转换
    if len(cv_img.shape) == 3:  # 彩色图像
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    else:  # 灰度图像
        h, w = cv_img.shape
        q_img = QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)

    return QPixmap.fromImage(q_img)


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
    QueueProgressUpdater = QTimer()
    freq_detail = QTimer()
    def __init__(self):
        super().__init__()
        self.update_image_thread = None
        self.batch_setUp_form = None
        self.error_window = []
        self.setUp_form = None
        self.pu_thread = None
        self.pu = None
        self.setupUi(self)
        self.statusbar.showMessage(_("准备就绪"))
        self.set_text()
        self.set_slot()
        setTheme(Theme.DARK)
        self.action_9.triggered.connect(self.show_all)
        self.setButtons()
        self.temporary = None

        self.current_selected_task = None


        self.task_queue = []
        self.QueueProgressUpdater.timeout.connect(self.update_total_progress)
        self.QueueProgressUpdater.start(250)
        self.QueueList.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


    def set_slot(self):
        self.SingleInputSelector.receive_file.connect(self.create_single_task)
        self.MultipleProcessSelector.receive_file.connect(self.add_batch_process)
        self.SLBrowser.clicked.connect(self.browse_single_video_file)
        self.SLOpen.clicked.connect(self.create_single_task_via_button)
        self.QueueList.itemSelectionChanged.connect(self.set_first_selected)
        self.freq_update_status()


    def browse_single_video_file(self):
        file_path, wtf = QFileDialog.getOpenFileName(
            self,  # 父窗口
            _("选择视频文件"),  # 对话框标题
            "",  # 初始目录（空字符串表示当前目录）
            _("视频文件 (*.mp4 *.avi *.mkv *.mov)")  # 文件过滤器
        )
        if file_path:
            self.SLTL.setText(file_path)

    def create_single_task_via_button(self):
        if len(self.SLTL.text()) == 0:
            return
        self.create_single_task([self.SLTL.text()])

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


    def update_progress(self,index,progress):
        self.QueueList.setItem(index, 4, QTableWidgetItem(str(progress)))


    def set_status(self):
        for i in self.task_queue:
            for row in range(self.QueueList.rowCount()):
                if self.QueueList.item(row, 0).text() == str(i.index):
                    self.QueueList.setItem(row, 2, QTableWidgetItem(i.statue))

    def dummy_function(self,*args,**kwargs):
        pass

    def update_details(self):
        for i in self.task_queue:
            if i.index == self.current_selected_task+1:
                self.SourceLabel.setText(_("源文件:") + os.path.basename(i.file))
                self.progressBar.setValue(i.progress*100)
                self.FileNameLabel.setText(_("文件名:") + os.path.basename(i.file))
                self.FilePathLabel.setText(_("文件路径:") + i.file)
                self.FileFormatLabel.setText(_("格式:") + i.output_format)
                self.ProjectPresentLabel.setText(_("项目预设:"))
                self.VideoInfoLabel.setText(_("视频:"))
                self.BitRateLabel.setText(_("码率:") + "Maximum Bitrate:"+str(i.MaximumBitRate)+" Target Bitrate:"+str(i.MaximumBitRate))
                self.AudioLabel.setText(_("音频:"))

    def prepare_thumbnail(self,):
        index = range(1,101)
        # todo: 把更新缩略图改为缓存式的









    def handle_error(self, err, _id,dump_file):
        print(err)
        print(dump_file,"DDDDUUUUMMMPPPP")
        self.error_window.append(error_report.ErrorReportDialog(error=err,dump_file=dump_file))
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
                        print("OIIAI")

        for ai in self.task_queue:
            print(ai.statue)

    def receive_preset(self,preset,name):
        preset['file'] = None
        preset['output_path'] = None
        preset['watermark_content'] = None
        self.save_preset(preset,name)


    def save_preset(self,template,name):
        if os.path.exists("preset"):
            pass
        else:
            os.mkdir("preset")
        if not os.path.exists(f"preset/{name}.pickle"):
            with open(f"preset/{name}.pickle",'wb') as f:
                pickle.dump(template,f)





    def create_single_task(self, files):
        if len(files) > 1:
            showFlyout(self,self.SingleInputSelector,InfoBarIcon.WARNING,_("请勿拖入多个文件"),_("非法操作"))
        else:
            file = files[0]
            self.setUp_form = CreateNewProject(file,self)
            self.setUp_form.setWindowModality(Qt.ApplicationModal)
            self.setUp_form.show()
            self.setUp_form.complete.connect(self.save_profile)
            self.setUp_form.create_preset.connect(self.receive_preset)

    def add_batch_process(self, files):
        self.batch_setUp_form = CreateNewProject(files, self)
        self.batch_setUp_form.setWindowModality(Qt.ApplicationModal)
        self.batch_setUp_form.show()
        self.batch_setUp_form.complete.connect(self.set_batch_file)
        self.batch_setUp_form.create_preset.connect(self.receive_preset)


    def set_batch_file(self):
        args = self.batch_setUp_form.save_watermark_profile()
        origin = copy.deepcopy(args)
        for i in self.batch_setUp_form.file_path:
            args.update({'file': i})
            args.update({'output_path': os.path.join(origin['output_path'],os.path.basename(i).split(".")[0])})
            self.temporary = ProcessUnit.ProcessUnit(i)
            self.temporary.set_args(**args)
            self.temporary.index = len(self.task_queue)+1
            self.temporary.progress_identify = str(uuid.uuid4())
            self.temporary.dump_uuid = str(uuid.uuid4())
            self.task_queue.append(self.temporary)
        self.batch_setUp_form.close()
        self.sync_queue()

        
    def save_profile(self):
        templ = self.setUp_form.save_watermark_profile()
        self.temporary = ProcessUnit.ProcessUnit(templ['file'])
        self.temporary.set_args(**templ)
        self.temporary.index = len(self.task_queue)+1
        self.temporary.progress_identify = str(uuid.uuid4())
        self.temporary.dump_uuid = str(uuid.uuid4())
        self.task_queue.append(self.temporary)
        self.setUp_form.close()
        self.sync_queue()

    def setButtons(self):
        self.error_window = []
        self.StartButton.clicked.connect(self.start_all_task)
        self.StopButton.clicked.connect(self.queue_stop)


    def start_all_task(self):
        corre_ = threading.Thread(target=self.queue_start)
        corre_.start()


    def queue_start(self):
        start_list = []
        for task in self.task_queue:
            if not task.running and task.status != 0 and task.completed != True:
                task.running = True
                task.statue = _("运行中")
                task.update_progress.connect(self.update_queue_percentage)
                task.OccurError.connect(self.handle_error)
                start_list.append(task.run)
        if start_list != []:
            threading_pool = ThreadPoolManager(max_workers=2)
            threading_pool.submit_tasks(start_list)
            threading_pool.start()
            self.set_status()

    def queue_suspend(self):
        for task in self.task_queue:
            if task.running:
                task.suspend()
                task.running = False
                task.statue = _("已暂停")
        self.set_status()

    def queue_resume(self):
        for task in self.task_queue:
            if not task.running and task.completed != True:
                task.resume()
                task.running = True
                task.statue = _("运行中")
        self.set_status()

    def queue_stop(self):
        for task in self.task_queue:
            if task.running:
                task.stop()
                task.running = False
                task.completed = _("已终止")
        self.set_status()

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
                task.update_progress.connect(self.update_queue_percentage)
                task.OccurError.connect(self.handle_error)



    def start_render(self):
        # pu = ProcessUnit.ProcessUnit()
        # pu.update_progress.connect(self.set_progess_bar)
        # threading.Thread(target=pu.run).start()

        print(self.get_selected_rows())
        # self.temporary.update_progress.connect(self.update_queue_percentage)
        # self.temporary.OccurError.connect(self.handle_error)
        # threading.Thread(target=self.temporary.run).start()




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
    complete = Signal()
    create_preset = Signal(dict,str)
    def __init__(self, file_path,parent=None):
        super().__init__(parent, Qt.Window)
        self.setupUi(self)
        self.render_device = _devices
        self.set_text()
        self.set_connections()
        self.initial_CB()
        self.checker = QTimer()
        self.checker.timeout.connect(self.setup_correct_setting_item)
        self.checker.start(50)
        self.template = None
        self.file_path = file_path
        self.PB_Confirm.clicked.connect(self.completed)
        self.PB_saveaspreset.clicked.connect(self.generate_preset)



    def completed(self):
        self.complete.emit()
        self.hide()


    def save_watermark_profile(self):
        self.generate_profile()
        return self.template

    def generate_preset(self):
        self.generate_profile()
        self.create_preset.emit(self.template,self.LE_PresetName.text())

    def generate_profile(self):


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
                watermark_content = cv2.imread(self.LE_WatermarkContent.text())
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
            watermark_content = cv2.imread(self.LE_WatermarkContent.text())
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
        print(FFmpegEncoder)
        if int(self.CB_BitRateControl.currentIndex()) == 0:
            bitrate_control = const.BitRateControl.VBR
        elif int(self.CB_BitRateControl.currentIndex()) == 1:
            bitrate_control = const.BitRateControl.CBR

        MaximumBitRate = str(self.LE_MaxBitRate.text())
        TargetBitRate = str(self.LE_BitRate.text())

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

        if self.CB_Foreward.isChecked():
            FFmpegForeward = int(self.SB_Forward.value())
        else:
            FFmpegForeward = None

        if self.CB_AdjustiveNormalize.isChecked():
            FFmpegSelfAdaptive = int(self.SB_AN.value())
        else:
            FFmpegSelfAdaptive = None
        print(watermark_method)
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
            "output_format": "mov",
            "two_pass": two_pass,
        }
        self.template = process_unit_template







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


# 更简洁的版本（只返回布尔值）
def is_file_larger_than_1gb(file_path):
    """
    检测文件大小是否大于1GB（简化版）

    参数:
        file_path (str): 文件路径

    返回:
        bool: 如果文件大小大于1GB返回True，否则返回False
    """
    try:
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            return file_size > (1024 * 1024 * 1024)
        return False
    except:
        return False


# 支持自定义大小的通用版本
def is_file_larger_than(file_path, size_gb=1):
    try:
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            threshold = size_gb * 1024 * 1024 * 1024
            return file_size > threshold
        return False
    except:
        return False



if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    window = SplashScreen()
    window.show()
    sys.exit(app.exec())
