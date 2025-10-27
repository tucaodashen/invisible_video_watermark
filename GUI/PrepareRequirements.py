import sys
import os
import zipfile
import requests
from PySide6.QtCore import QThread, Signal ,QObject
import gettext
import shutil
import subprocess

_ = gettext.gettext


def check_ffmpeg_installed():
    """检查FFmpeg是否已安装并在PATH中"""
    # 方法1.1：使用shutil.which（推荐）
    if shutil.which("ffmpeg") is not None:
        return True

    # 方法1.2：使用subprocess尝试运行ffmpeg命令
    try:
        subprocess.run(["ffmpeg", "-version"],
                       capture_output=True,
                       check=True,
                       timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def is_ffmpeg_exist():
    # 判断ffmpeg是否存在
    if sys.platform == "win32":
        if os.path.exists("./ffmpeg"):
            for root, dirs, files in os.walk("./ffmpeg"):
                if "ffmpeg.exe" in files:
                    ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                    # 添加到当前进程的PATH
                    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
                    return True
            return False
        elif check_ffmpeg_installed():
            return True
        else:
            return False









class FFmpegPrepare(QThread):
    progress = Signal(float)
    progress_text = Signal(str)
    success = Signal(bool)
    def __init__(self):
        super().__init__()

    def run(self):
        self.download_ffmpeg()



    def download_with_progress(self,url, filename):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r下载进度: {percent:.2f}% ({downloaded}/{total_size} bytes)", end="")
                        self.progress_text.emit(_("下载进度: {percent:.2f}% ({downloaded}/{total_size} bytes".format(percent=percent, downloaded=downloaded,total_size=total_size)))
                        self.progress.emit(percent)
                    else:
                        print(f"\r已下载: {downloaded} bytes", end="")
                        self.progress_text.emit(_("已下载: {downloaded} bytes".format(downloaded=downloaded)))
                        self.progress.emit(0)  # 进度条显示MB
        print()  # 换行

    def download_ffmpeg(self):
        print("FFmpeg未找到，尝试自动下载...")

        # 确定平台
        if sys.platform == "win32":
            # Windows平台
            ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            ffmpeg_zip = "ffmpeg.zip"
            ffmpeg_dir = "ffmpeg"

            if not os.path.exists("ffmpeg.zip"):
                self.download_with_progress(ffmpeg_url, ffmpeg_zip)

            # 解压
            with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)

            # 查找ffmpeg.exe
            for root, dirs, files in os.walk(ffmpeg_dir):
                if "ffmpeg.exe" in files:
                    ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                    # 添加到当前进程的PATH
                    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
                    print(f"FFmpeg已安装到: {ffmpeg_path}")
                    self.success.emit(True)
                    return True

            print("无法找到ffmpeg.exe")
            self.success.emit(False)
            return False

if __name__ == "__main__":
    dw = FFmpegPrepare()
    dw.download_ffmpeg()