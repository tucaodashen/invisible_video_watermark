import pyaudio
import wave
import threading
import time
import os
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="audio", enable_udp=True, enable_console=True)
logger = get_logger()


class AudioPlayer:
    def __init__(self):
        self.chunk = 1024  # 每次读取的帧数
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.wf = None  # wave file object

        # 状态标志
        self._running = True  # 控制后台线程生命周期
        self._playing = False  # 控制是否正在播放
        self._paused = False  # 控制是否暂停

        # 线程锁，确保在更换音频或操作流时线程安全
        self.lock = threading.Lock()

        # 启动后台播放线程
        self.thread = threading.Thread(target=self._playback_loop)
        self.thread.daemon = True  # 设置为守护线程，主程序退出时它也会退出
        self.thread.start()

    def load(self, filepath):
        """
        加载或更换音频文件。
        如果当前正在播放，会自动停止并加载新文件。
        """
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}",tags="audio:load")
            raise FileNotFoundError(f"File not found: {filepath}")

        # 加载新文件前，先获取锁并清理旧资源
        with self.lock:
            # 停止当前播放状态
            self._playing = False
            self._paused = False

            # 关闭旧的 stream 和 file
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            if self.wf:
                self.wf.close()
                self.wf = None

            # 打开新文件
            self.wf = wave.open(filepath, 'rb')

            # 根据新文件的参数创建新的 stream
            self.stream = self.pa.open(
                format=self.pa.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True
            )
            logger.debug(f"Loaded audio file: {filepath}",tags="audio:load")

    def play(self):
        """开始或继续播放"""
        with self.lock:
            if self.wf is None:
                logger.error("No audio file loaded to play.",tags="audio:play")
                return
            self._playing = True
            self._paused = False

    def pause(self):
        """暂停播放"""
        with self.lock:
            if self._playing:
                self._playing = False
                self._paused = True
                logger.debug("Audio playback paused.",tags="audio:play")

    def stop(self):
        """停止播放并重置进度"""
        with self.lock:
            self._playing = False
            self._paused = False
            if self.wf:
                self.wf.rewind()  # 文件指针回到开头
            logger.debug("Audio playback stopped and reset.",tags="audio:play")

    def close(self):
        """释放所有资源，终止线程（通常在程序退出时调用）"""
        self._running = False  # 停止线程循环
        if self.thread.is_alive():
            self.thread.join()  # 等待线程结束

        with self.lock:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.wf:
                self.wf.close()
            self.pa.terminate()
        logger.debug("Audio resources released.",tags="audio:close")

    def _playback_loop(self):
        """后台播放线程的主循环"""
        while self._running:
            # 获取锁的粒度要小，只在读取数据时获取，
            # 写入音频流(stream.write)是耗时操作，不应持有锁，否则会阻塞主线程的控制指令

            data = None
            should_write = False

            # 1. 安全读取数据
            with self.lock:
                if self._playing and not self._paused and self.wf:
                    data = self.wf.readframes(self.chunk)
                    if len(data) > 0:
                        should_write = True
                    else:
                        # 数据读完，说明播放结束
                        self._playing = False
                        self.wf.rewind()
                        logger.debug("Audio playback finished.",tags="audio:play")

            # 2. 写入音频流 (耗时操作，放在锁外面)
            if should_write and self.stream:
                try:
                    self.stream.write(data)
                except OSError as e:
                    # 处理可能的音频设备错误
                    logger.error(f"Audio stream error: {e}",tags="audio:play")
                    self._playing = False

            # 3. 如果没有播放，稍微休眠以节省CPU
            if not should_write:
                time.sleep(0.01)

if __name__ == "__main__":
    audio_player = AudioPlayer()
    audio_player.load("allstar.wav")
    audio_player.play()
    time.sleep(5)
    audio_player.pause()
    time.sleep(2)
    audio_player.play()
    time.sleep(5)
    audio_player.stop()
    audio_player.close()
