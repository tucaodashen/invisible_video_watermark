"""
环境依赖检查模块 (PyAV migrated).
此模块负责检查运行时依赖是否就绪。
"""
import sys
import os
import subprocess

import gettext

_ = gettext.gettext


def check_pyav_installed():
    """检查 PyAV 是否已安装。"""
    try:
        import av  # noqa: F401
        return True
    except ImportError:
        return False


def is_pyav_available():
    """检查 PyAV 是否可用 (环境入口函数)。"""
    return check_pyav_installed()


# ── 以下为向后兼容的旧接口，已不再需要但保留以确保其他模块不会崩溃 ──


def check_ffmpeg_installed():
    """(已弃用) 现在的核心用 PyAV，不再需要 FFmpeg CLI。"""
    try:
        import av  # noqa: F401
        return True
    except ImportError:
        return False


def is_ffmpeg_exist():
    """(已弃用) 现在的核心用 PyAV，检查 PyAV 是否可用。"""
    return check_pyav_installed()


# 保留一个空线程类，确保 Startup_Splash 中旧的 download_thread 引用不会崩溃
class FFmpegPrepare:
    """(已弃用) FFmpeg 下载线程，PyAV 迁移后不再需要。"""

    def __init__(self):
        self.progress = None
        self.progress_text = None
        self.success = self._FakeSignal()

    class _FakeSignal:
        def __init__(self):
            self._handlers = []

        def emit(self, value):
            for h in self._handlers:
                h(value)

        def connect(self, handler):
            self._handlers.append(handler)

    def run(self):
        """(已弃用) 下载 FFmpeg — 不再需要。"""
        print("FFmpeg 下载已弃用，请使用 pip install av 安装 PyAV。")
        self.success.emit(False)

    def download_ffmpeg(self):
        """(已弃用)"""
        self.run()
