import requests
import threading
import os
import time
from typing import List, Tuple
from PySide6.QtCore import QObject, Signal, Slot

# --- 配置 ---
DEFAULT_MAX_RETRIES = 3
DEFAULT_CHUNK_SIZE = 1024 * 512  # 512 KaB
DEFAULT_THREAD_COUNT = 16  # 默认下载线程数


class MultiThreadDownloader(QObject):
    """
    一个支持多线程分块下载（Range Request）的下载器类。
    """

    # 定义 PySide6 信号
    progress_updated = Signal(float)  # 发送：(current_progress_percentage: float)
    download_finished = Signal(bool, str, str)  # 发送：(is_success: bool, file_path: str, message: str)
    retry_attempted = Signal(int, int, str, int)  # 发送：(current_try, max_retries, message, thread_id)

    def __init__(self, url: str, target_filepath: str, thread_count: int = DEFAULT_THREAD_COUNT,
                 max_retries: int = DEFAULT_MAX_RETRIES, parent=None):
        super().__init__(parent)
        self.url = url
        self.target_filepath = target_filepath
        self.thread_count = thread_count
        self.max_retries = max_retries

        self.total_size = 0
        self.downloaded_size = 0
        self.threads: List[threading.Thread] = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()  # 锁用于保护共享资源 (downloaded_size)
        self.segment_statuses: List[bool] = []  # 记录每个分块是否下载成功
        self.temp_files: List[str] = []  # 存储临时分块文件名

    def _get_file_size(self) -> int:
        """获取文件总大小并检查是否支持 Range Request。"""
        try:
            # 发送 HEAD 请求以获取文件信息
            response = requests.head(self.url, allow_redirects=True, timeout=10)
            response.raise_for_status()

            # 检查 Content-Length
            if 'Content-Length' not in response.headers:
                raise Exception("服务器未提供文件大小信息。")

            # 检查是否支持 Range Request
            if 'Accept-Ranges' not in response.headers and 'bytes' not in response.headers.get('Accept-Ranges', ''):
                # 某些服务器可能不支持，此时应回退到单线程下载
                raise Exception("服务器不支持 Range Request，无法进行分块下载。")

            return int(response.headers['Content-Length'])
        except Exception as e:
            # 在这里直接触发下载失败，因为无法进行多线程分块
            self.download_finished.emit(False, self.target_filepath, f"预检失败：{e}")
            return 0

    def _split_file(self) -> List[Tuple[int, int]]:
        """将文件分成 N 个下载段，返回 (start_byte, end_byte) 列表。"""
        segment_size = self.total_size // self.thread_count
        segments: List[Tuple[int, int]] = []

        start = 0
        for i in range(self.thread_count):
            end = start + segment_size - 1
            if i == self.thread_count - 1:
                # 确保最后一个线程下载剩余的所有字节
                end = self.total_size - 1

            segments.append((start, end))
            start = end + 1

        return segments

    def _download_segment(self, segment_index: int, start_byte: int, end_byte: int):
        """单个线程下载特定文件分段，包含自动重试。"""

        # 临时文件命名：在目标文件名后添加 .partX
        temp_filepath = f"{self.target_filepath}.part{segment_index}"
        self.temp_files[segment_index] = temp_filepath

        retries = 0
        segment_success = False
        last_error = ""

        # 尝试断点续传
        current_start_byte = start_byte
        if os.path.exists(temp_filepath):
            try:
                # 获取已下载的大小，更新实际的起始字节
                downloaded_part_size = os.path.getsize(temp_filepath)
                current_start_byte = start_byte + downloaded_part_size

                # 更新全局下载进度 (使用锁保护)
                with self._lock:
                    self.downloaded_size += downloaded_part_size
                    print(f"线程 {segment_index}: 续传 - 已下载 {downloaded_part_size} 字节。")

            except Exception as e:
                # 如果文件有问题，则从头开始下载
                print(f"线程 {segment_index}: 临时文件读取失败，将从头开始下载。错误：{e}")
                # 重新设置 current_start_byte = start_byte

        # 如果整个分段已经下载完成，则直接标记成功并退出
        if current_start_byte > end_byte:
            print(f"线程 {segment_index}: 分段已完成。")
            self.segment_statuses[segment_index] = True
            return

        while retries < self.max_retries and not segment_success and not self._stop_event.is_set():
            try:
                # 设置 Range 头部，支持断点续传
                headers = {'Range': f'bytes={current_start_byte}-{end_byte}'}
                mode = 'ab'  # 始终使用追加模式，因为起始字节已调整

                response = requests.get(self.url, headers=headers, stream=True, timeout=30)
                response.raise_for_status()

                # 检查响应头是否确认了 Range 请求
                if response.status_code != 206 and current_start_byte != start_byte:
                    # 如果不是 206 状态码 (Partial Content)，且不是从 0 开始下载，说明续传可能失败
                    print(f"线程 {segment_index}: 服务器未返回 206 状态码，可能不支持续传。将重新从头开始下载此分段。")
                    # 清理临时文件，重新从分段的起始字节开始
                    if os.path.exists(temp_filepath):
                        os.remove(temp_filepath)
                    current_start_byte = start_byte
                    headers = {'Range': f'bytes={current_start_byte}-{end_byte}'}
                    mode = 'wb'  # 切换为写入模式
                    response = requests.get(self.url, headers=headers, stream=True, timeout=30)
                    response.raise_for_status()

                # 写入临时文件
                with open(temp_filepath, mode) as f:
                    for chunk in response.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                        if self._stop_event.is_set():
                            raise Exception("下载被用户停止")

                        if chunk:
                            f.write(chunk)
                            chunk_size = len(chunk)
                            current_start_byte += chunk_size

                            # 更新全局进度 (使用锁保护共享资源)
                            with self._lock:
                                self.downloaded_size += chunk_size
                                if self.total_size > 0:
                                    progress = (self.downloaded_size / self.total_size) * 100
                                    self.progress_updated.emit(min(progress, 100.0))
                                    print(min(progress, 100.0))

                segment_success = True
                self.segment_statuses[segment_index] = True  # 标记此分块成功

            except Exception as e:
                retries += 1
                last_error = str(e)
                # 只有 RequestException 或连接问题才重试
                if isinstance(e, requests.exceptions.RequestException):
                    self.retry_attempted.emit(retries, self.max_retries, last_error, segment_index)
                    print(f"线程 {segment_index} 下载失败 (尝试 {retries}/{self.max_retries}): {last_error}")
                    if self._stop_event.wait(5): break  # 重试前等待
                else:
                    print(f"线程 {segment_index} 遇到非重试错误: {last_error}")
                    break  # 遇到其他错误则退出循环

        if not segment_success and not self._stop_event.is_set():
            # 达到最大重试次数仍失败，标记此分块为失败
            self.segment_statuses[segment_index] = False
            print(f"线程 {segment_index}: 分块下载最终失败，已达最大重试次数。")

    def _combine_files(self, segments: List[Tuple[int, int]]) -> bool:
        """合并所有分块文件到最终目标文件。"""
        if any(not status for status in self.segment_statuses):
            return False  # 存在未完成的分块

        print("所有分块下载完成，开始合并文件...")
        try:
            with open(self.target_filepath, 'wb') as outfile:
                for i in range(self.thread_count):
                    temp_filepath = f"{self.target_filepath}.part{i}"

                    # 简单检查文件大小是否匹配预期
                    expected_size = segments[i][1] - segments[i][0] + 1
                    actual_size = os.path.getsize(temp_filepath)
                    if actual_size != expected_size:
                        raise Exception(f"分块 {i} 大小不匹配。预期: {expected_size}，实际: {actual_size}")

                    with open(temp_filepath, 'rb') as infile:
                        outfile.write(infile.read())

                    # 合并成功后删除临时文件
                    os.remove(temp_filepath)
            return True
        except Exception as e:
            print(f"文件合并失败：{e}")
            return False

    def _cleanup(self):
        """清理所有临时文件。"""
        print("正在清理临时文件...")
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"警告: 无法删除临时文件 {temp_file}。{e}")

    def _run_download(self):
        """多线程下载的协调主函数。"""

        # 1. 预检文件大小和 Range 支持
        self.total_size = self._get_file_size()
        if self.total_size == 0:
            return  # 预检失败，信号已发送

        # 2. 分配下载任务
        segments = self._split_file()
        self.segment_statuses = [False] * self.thread_count
        self.temp_files = [""] * self.thread_count  # 预分配列表

        # 3. 启动线程
        for i, (start, end) in enumerate(segments):
            thread = threading.Thread(target=self._download_segment, args=(i, start, end))
            self.threads.append(thread)
            thread.start()

        # 4. 等待所有线程完成
        for thread in self.threads:
            thread.join()

        final_success = False
        final_message = ""

        if self._stop_event.is_set():
            final_message = "下载被用户停止。"
            self._cleanup()
        elif all(self.segment_statuses):
            # 5. 合并文件
            if self._combine_files(segments):
                final_success = True
                final_message = "多线程分块下载成功。"
                self.downloaded_size = self.total_size  # 确保最终进度为 100%
            else:
                final_message = "所有分块下载成功，但文件合并失败。"
                self._cleanup()
        else:
            final_message = "多线程分块下载失败：部分分块未能完成或达到最大重试次数。"
            # 保留未完成的分块，以便下次启动时可以尝试续传

        # 6. 发送最终信号
        self.download_finished.emit(final_success, self.target_filepath, final_message)

    def start_download(self):
        """在新的主线程中启动下载。"""
        if self.threads and any(t.is_alive() for t in self.threads):
            print("下载已在进行中...")
            return

        self._stop_event.clear()
        self.downloaded_size = 0
        self.threads = []

        main_thread = threading.Thread(target=self._run_download)
        main_thread.start()

    def stop_download(self):
        """停止所有下载线程。"""
        self._stop_event.set()
        print("请求停止下载...")
        # 等待所有分块线程结束
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)

if __name__ == "__main__":
    downloader = MultiThreadDownloader(
        url="https://github.com/tucaodashen/invisible_video_watermark/releases/download/1.13/output-files.zip",
        target_filepath="large_file.zip",
        thread_count=4
    )
    downloader.start_download()
