import gettext
import os
import shutil
import socket
import subprocess
import sys
import traceback

# 假设这些模块和类已经存在于您的项目中
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import Dialog, MessageBoxBase, SubtitleLabel, ProgressBar, BodyLabel

from GUI import PrepareRequirements
from GUI.Splash import Ui_SplashDesu
from PySide6.QtCore import QTimer, Qt, Signal, QThread  # 导入 QThread 和 Signal

# -----------------------------------------------------------
# ⚠️ 注意: 由于我无法访问您的 GUI.PrepareRequirements 模块，
# 我假设 FFmpegPrepare 是 QThread 的子类，并包含必要的信号。
# -----------------------------------------------------------

_ = gettext.gettext


def run_process_and_get_pid(command):
    """
    运行命令并返回进程对象和PID
    """
    # 如果command是字符串，需要设置shell=True
    if isinstance(command, str):
        process = subprocess.Popen(command, shell=True)
    else:
        process = subprocess.Popen(command)

    pid = process.pid
    return process, pid


class SplashScreen(QWidget, Ui_SplashDesu):
    timers = QTimer()
    # 增加一个成员变量用于保存下载窗口的引用
    ffmpeg_download_window = None

    def __init__(self):
        super().__init__()
        self.process = None
        self.timer_st_oneshot = QTimer()
        self.timer_st_oneshot.timeout.connect(self.start_now)
        self.setupUi(self)
        self.setInvisible()
        self.Tips.setText("Loading...")
        self.progressBar.setValue(0)

        self.prepare()  # 从这里开始检查环境

    def setInvisible(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def adjust_size_based_on_resolution(self):
        pass

    def prepare(self):
        """
        检查环境的起始方法。如果需要下载FFmpeg，则暂停流程并进入下载异步等待。
        """
        self.timers.stop()
        self.Tips.setText(_("检查FFmpeg中..."))

        if not PrepareRequirements.is_ffmpeg_exist():
            self.Tips.setText(_("安装FFMpeg"))
            self.display_dialog()
            # 关键：如果需要下载，在此处返回，后续流程将在 handle_ffmpeg_download_result 中启动
            return

            # --- FFmpeg 检查通过或下载成功的后续流程 ---
        self.continue_after_ffmpeg_check()

    def continue_after_ffmpeg_check(self):
        """
        FFmpeg 检查通过或下载成功后继续执行的流程。
        """
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
        self.process, pid = run_process_and_get_pid(["LogServer.exe"])

    def custom_exception_hook(self, exc_type, exc_value, exc_traceback):
        """
        这是一个自定义的异常钩子函数，用于捕获所有未处理的异常。
        """

        # --- 1. 记录/处理异常信息 ---
        print("=" * 60)
        print("🚨 捕获到一个未处理的异常！")
        print(f"异常类型: {exc_type.__name__}")
        print(f"异常信息: {exc_value}")

        formatted_traceback_lines = traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )

        print("\n--- 完整追溯信息 (格式化为字符串) ---")
        # 将列表中的行连接成一个完整的字符串
        full_traceback_string = "".join(formatted_traceback_lines)
        print(full_traceback_string)

        print("=" * 60)
        self.MainWindow.show_NCW([str(exc_value), full_traceback_string])

    def start_now(self):
        from GUI.main import MainWindow
        self.MainWindow = MainWindow()
        self.MainWindow.log_process = self.process
        self.MainWindow.showMaximized()
        sys.excepthook = self.custom_exception_hook
        self.close()
        self.timer_st_oneshot.stop()

    def display_dialog(self):
        """
        显示是否下载 FFmpeg 的对话框，并连接信号。
        """
        title = _("FFmpeg未安装")
        content = _(
            "FFmpeg是此程序和依赖库MoviePy的核心组件。如果你想自行安装FFmpeg并添加到环境变量中，请点击否。点击是将自动下载并安装FFmpeg。(不会添加到环境变量中)")

        w = Dialog(title, content, self)

        # 移除 w.exec()
        # 连接用户点击“是”（Accepted）和“否”（Rejected）的信号
        w.accepted.connect(self.start_ffmpeg_download)
        w.rejected.connect(lambda: sys.exit(0))

        w.show()  # 非模态显示，等待用户选择

    def start_ffmpeg_download(self):
        """
        用户点击“是”后，开始 FFmpeg 下载并显示进度条窗口。
        """
        # 实例化下载窗口，并保存为成员变量防止被垃圾回收
        self.ffmpeg_download_window = FFmpegDownloadPage(self)

        # 连接下载线程的 success 信号到处理结果的方法
        self.ffmpeg_download_window.download_thread.success.connect(self.handle_ffmpeg_download_result)

        # 非模态显示下载窗口。这是关键，让主线程不阻塞，可以处理绘制和进度信号。
        self.ffmpeg_download_window.show()

    def handle_ffmpeg_download_result(self, is_success):
        """
        处理 FFmpeg 下载线程的结果。
        """
        if self.ffmpeg_download_window:
            # 无论成功失败，都关闭下载进度窗口
            self.ffmpeg_download_window.close()
            # 清理引用
            self.ffmpeg_download_window = None

        if is_success:
            print("FFmpeg下载成功，继续启动流程。")
            self.continue_after_ffmpeg_check()
        else:
            print("FFmpeg下载失败，请手动安装或重试。")
            # 可以在这里显示一个错误对话框，并让用户决定是退出还是继续。
            error_msg = MessageBoxBase(_("下载失败"), _("FFmpeg下载失败，应用可能无法正常工作。是否退出？"), self)
            if error_msg.exec():
                sys.exit(1)
            else:
                self.continue_after_ffmpeg_check()  # 允许用户忽略并继续


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

        # 实例化 QThread 子类 (假设 PrepareRequirements.FFmpegPrepare 是)
        self.download_thread = PrepareRequirements.FFmpegPrepare()
        self.download_thread.progress.connect(self.set_progress)
        self.download_thread.progress_text.connect(self.set_progress_text)
        self.download_thread.success.connect(self.is_success)

        try:
            # 启动线程，下载在后台进行，不阻塞主 GUI 线程
            self.download_thread.start()
        except Exception as e:
            self.labels.setText(str(e))
            # 立即发送失败信号，通知 SplashScreen
            self.download_thread.success.emit(False)

    def set_progress(self, value):
        self.progressBar.setVal(value)

    def set_progress_text(self, text):
        self.labels.setText(text)

    def is_success(self, value):
        # 这里的关闭只是关闭进度条窗口本身，后续流程由 SplashScreen 的 signal/slot 机制处理
        if value:
            # self.close() # 在 handle_ffmpeg_download_result 中关闭，以确保流程控制统一
            pass  # 仅接收信号，不立即关闭窗口
        else:
            self.labels.setText(_("下载失败，请检查网络或日志。"))


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