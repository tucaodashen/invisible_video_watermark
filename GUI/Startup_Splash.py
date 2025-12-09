import gettext
import os
import shutil
import socket
import subprocess
import sys

from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import Dialog, MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel

from GUI import PrepareRequirements
from GUI.Splash import Ui_SplashDesu
from PySide6.QtCore import QTimer, Qt


_ = gettext.gettext

def run_process_and_get_pid(command):
    """
    运行命令并返回进程对象和PID

    Args:
        command (str/list): 要执行的命令，可以是字符串或列表

    Returns:
        tuple: (process对象, PID)
    """
    # 如果command是字符串，需要设置shell=True
    if isinstance(command, str):
        process = subprocess.Popen(command, shell=True)
    else:
        process = subprocess.Popen(command)

    pid = process.pid
    return process, pid

class SplashScreen(QWidget,Ui_SplashDesu):
    timers = QTimer()
    def __init__(self):
        super().__init__()
        self.process = None
        self.timer_st_oneshot = QTimer()
        self.timer_st_oneshot.timeout.connect(self.start_now)
        self.timer_st_oneshot.setSingleShot(True)
        self.setupUi(self)
        self.setInvisible()
        self.Tips.setText("Loading...")
        self.progressBar.setValue(0)

        self.prepare()





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
        if os.path.exists("WorkPath"):
            shutil.rmtree("WorkPath")
        os.mkdir("WorkPath")
        self.Tips.setText(_("启动日志服务器..."))
        self.run_log()
        self.Tips.setText(_("加载主页面..."))
        self.timer_st_oneshot.start(3000)

    def run_log(self):
        print("当前工作目录:", os.getcwd())
        self.process,pid = run_process_and_get_pid(["ls/LogServer.exe"])

    def start_now(self):
        from GUI.main import MainWindow
        self.MainWindow = MainWindow()
        self.MainWindow.log_process = self.process
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

def is_port_in_use(port: int, host: str = 'localhost') -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # 设置连接超时时间
        try:
            # 尝试连接指定端口
            result = s.connect_ex((host, port))
            # 如果连接成功（返回0），则端口被占用
            return result == 0
        except socket.gaierror:
            # 主机名解析失败
            return False
        except Exception:
            # 其他异常情况
            return False

def start():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    window = SplashScreen()
    window.show()

    sys.exit(app.exec())