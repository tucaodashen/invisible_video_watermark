import gettext
import os
import shutil
import socket
import subprocess
import sys
import traceback
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import Dialog
from BasicSystem import const
from GUI import PrepareRequirements
from GUI.Splash import Ui_SplashDesu
from PySide6.QtCore import QTimer, Qt, Signal
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

    def __init__(self):
        super().__init__()
        self.process = None
        self.timer_st_oneshot = QTimer()
        self.timer_st_oneshot.timeout.connect(self.start_now)
        self.setupUi(self)
        self.setInvisible()
        self.Tips.setText(_("检查环境设置..."))
        self.progressBar.setValue(0)
        self.Pic.setImage("./assets/image/Splash_Nano.png")
        self.Pic.scaledToWidth(self.width())
        self.version_info.setText(const.__version__)

        self.prepare()  # 从这里开始检查环境

    def setInvisible(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def adjust_size_based_on_resolution(self):
        pass

    def prepare(self):
        """
        检查 PyAV 环境。如未安装则提示安装后退出。
        """
        self.timers.stop()
        self.Tips.setText(_("检查PyAV中..."))

        if not PrepareRequirements.check_pyav_installed():
            self.Tips.setText(_("依赖缺失"))
            self.show_pyav_missing_dialog()
            return

        self.continue_after_pyav_check()

    def show_pyav_missing_dialog(self):
        """
        PyAV 未安装时显示错误对话框并退出。
        """
        title = _("PyAV 未安装")
        content = _(
            "PyAV (av) 是本程序的核心视频处理依赖。\n"
            "请运行: pip install av\n"
            "或: uv pip install av\n"
            "安装后重新启动程序。"
        )
        w = Dialog(title, content, self)
        w.accepted.connect(lambda: sys.exit(1))
        w.rejected.connect(lambda: sys.exit(1))
        w.show()

    def continue_after_pyav_check(self):
        """
        PyAV 检查通过后继续执行的流程。
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
        formatted_traceback_lines = traceback.format_exception(
            exc_type, exc_value, exc_traceback
        )
        # 将列表中的行连接成一个完整的字符串
        full_traceback_string = "".join(formatted_traceback_lines)
        if "scroll_bar.py" in full_traceback_string:
            return
        self.MainWindow.show_NCW([str(exc_value), full_traceback_string])
        print("=" * 60)
        print("🚨 捕获到一个未处理的异常！")
        print(f"异常类型: {exc_type.__name__}")
        print(f"异常信息: {exc_value}")
        print("\n--- 完整追溯信息 (格式化为字符串) ---")
        print(full_traceback_string)
        print("=" * 60)

    def start_now(self):
        from GUI.main import MainWindow
        self.MainWindow = MainWindow()
        self.MainWindow.log_process = self.process
        self.MainWindow.showMaximized()
        sys.excepthook = self.custom_exception_hook
        self.close()
        self.timer_st_oneshot.stop()

    def custom_exception_hook(self, exc_type, exc_value, exc_traceback):
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