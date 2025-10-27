import cv2
import random
import os
import ffmpeg
from PySide6.QtCore import QObject,Signal
import multiprocessing
import psutil
from BasicSystem import LogSystem
from BasicSystem.VirtualFileSystem import FileSystem
from BasicSystem.const import *











def add_audio_to_video(video_path, audio_path, output_path):
    """
    为无声视频添加音频，不重新编码视频流

    参数:
        video_path: 输入视频文件路径
        audio_path: 输入音频文件路径
        output_path: 输出文件路径
    """
    try:
        # 加载视频和音频流
        video_stream = ffmpeg.input(video_path)
        audio_stream = ffmpeg.input(audio_path)

        # 合并视频和音频，仅复制视频流，编码音频流（如果需要）
        # 使用-shortest确保输出长度与最短的输入流相同
        output = ffmpeg.output(
            video_stream.video,
            audio_stream.audio,
            output_path,
            vcodec='copy',  # 直接复制视频流，不重新编码
            acodec='aac',  # 使用AAC编码音频（可根据需要更改）
            shortest=None  # 以最短的流为准
        )

        # 执行转换
        ffmpeg.run(output, overwrite_output=True)
        print(f"成功生成输出文件: {output_path}")

    except ffmpeg.Error as e:
        print(f"FFmpeg错误: {e.stderr.decode()}")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def slice_list(target_list, per_len):
    """
    slice list into per_len parts
    :param target_list:
    :param per_len:
    :return:
    """
    sl_inde = []
    liust_len = len(target_list)
    full_times = liust_len // per_len
    remain_len = liust_len % per_len
    if remain_len == 0:
        for i in range(full_times):
            sl_inde.append(target_list[i * per_len:(i + 1) * per_len])
        return sl_inde
    else:
        for i in range(full_times):
            sl_inde.append(target_list[i * per_len:(i + 1) * per_len])
        sl_inde.append(target_list[full_times * per_len:])
        return sl_inde


def get_frame_count(path):
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

def get_count(path):
    cap = cv2.VideoCapture(path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return int(total_frames)


def video_sampler(source_path,sampler_times,sampler_extension):
    LogSystem.logger.info(f"Start sampling video: {source_path}")
    cap = cv2.VideoCapture(source_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    LogSystem.logger.info(f"Total frames: {total_frames}")
    primary_sampler_point = []
    for i in range(sampler_times):
        primary_sampler_point.append(random.randint(0,total_frames-1))
    LogSystem.logger.info(f"Primary sampler point: {primary_sampler_point}")
    secondary_sampler_point = []
    for i in primary_sampler_point:
        for ti in range(sampler_extension):
            secondary_sampler_point.append(i+ti)
    LogSystem.logger.info(f"Secondary sampler point: {secondary_sampler_point}")
    final_sampler_point = primary_sampler_point + secondary_sampler_point
    final_sampler_point.sort()
    final_sampler_point = list(set(final_sampler_point))
    LogSystem.logger.debug(f"Final sampler point: {final_sampler_point}")
    return final_sampler_point


def extract_frame_by_index(video_path, frame_index, output_path):
    """
    按帧序号提取特定帧
    :param video_path: 视频文件路径
    :param frame_index: 目标帧序号（从0开始）
    :param output_path: 保存图像的路径
    """
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 设置目标帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    # 读取帧
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(output_path, frame)
        print(f"已保存第 {frame_index} 帧到 {output_path}")
    else:
        print("读取帧失败")

    cap.release()

def extract_frames(video_path, start_frame, end_frame, output_dir,formate="png",callback=None):
    """
    提取视频中指定帧范围的所有帧

    参数:
    video_path: 视频文件路径
    start_frame: 起始帧号(包含)
    end_frame: 结束帧号(包含)
    output_dir: 输出目录路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        LogSystem.logger.error(f"Failed to open video file: {video_path}")
        return

    # 获取视频总帧数和帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    LogSystem.logger.info(f"total_frames: {total_frames}")
    print(f"FPS:{fps:.2f}")

    # 验证帧范围有效性
    if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
        LogSystem.logger.error(f"Invalid frame range: {start_frame} to {end_frame}")
        cap.release()
        return

    # 设置起始帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 逐帧处理
    for frame_num in range(start_frame, end_frame + 1):
        ret, frame = cap.read()

        if not ret:
            LogSystem.logger.error(f"Failed to read {frame_num}")
            break

        # 保存帧为图像文件
        output_path = os.path.join(output_dir, f"frame_{frame_num:06d}.{formate}")
        cv2.imwrite(output_path, frame)

        # 显示进度
        if frame_num % 1 == 0:
            LogSystem.logger.debug(f"Extracted frame {frame_num}/{end_frame}")
            total = ((end_frame-start_frame+1)*1.0)
            cur = ((frame_num-start_frame)*1.0)
            if callback is not None and type(callback) is not float:
                try:
                    if cur/total <= 0.98:
                        callback(cur/total)
                    else:
                        callback(1)
                except TypeError:
                    callback(1)
                #这是个奇妙Bug，如果进度逼近1，就会出现TypeError，但是不影响程序运行，所以暂时这样用着吧。

    # 释放资源
    cap.release()
    LogSystem.logger.info(f"\nOver! Extracted {end_frame - start_frame + 1} to {output_dir}")

def spitter(total_frame_count,split_size):
    LogSystem.logger.info(f"Executing spitter with total_frame_count: {total_frame_count} and split_size: {split_size}")
    result = []
    start_index = 0
    while start_index < total_frame_count-1:
        s_start_index = start_index
        start_index = start_index + split_size
        end_index = min(start_index, total_frame_count)
        result.append((s_start_index, end_index-1))
    LogSystem.logger.debug(f"Spitter result: {result}")
    return result

def multiprocess_video_extractor(source_path,spitter_result,process=0):
    if process == 0:
        process = psutil.cpu_count(logical=True)
    args_list = []
    index = 0
    for i in spitter_result:
        index += 1
        args_list.append([source_path,i[0],i[1],"./output"])
    if len(args_list) <= process:
        process = len(args_list)
    else:
        process = process

def video_fusion():
    pass
def video_output():
    pass

def concatenate_with_ffmpeg_python(video_paths, output_path):
    """
    使用ffmpeg-python库拼接视频

    参数:
    video_paths: 视频文件路径列表
    output_path: 输出文件路径
    """
    # 创建临时文件列表
    list_file = "video_list.txt"
    with open(list_file, "w") as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    try:
        # 使用ffmpeg-python构建命令
        (
            ffmpeg
            .input(list_file,format='concat', safe=0)
            .output(output_path, c='copy')
            .overwrite_output()
            .run()
        )
        print(f"视频拼接完成: {output_path}")
    except ffmpeg.Error as e:
        print(f"拼接过程中出错: {e}")
    finally:
        # 清理临时文件
        if os.path.exists(list_file):
            os.remove(list_file)

class ProcessUnit(QObject):
    """
    最小处理单元
    """
    def __init__(self,
                 input_file,
                 output,
                 thread=0):
        super().__init__()
        self.attachment_data = []
        self.basic_args(thread,output,input_file)

    def basic_args(self,thread,output,input_file):
        # input and process setings
        self.source_file_type = SourceType.VIDEO
        self.watermark_content = "Defa"
        self.encode_type = BitRateControl.CBR
        self.encoder = Encoder.CPU
        self.bit_rate = 10000
        self.output_format = OutputFormat.MP4

        # process device settings
        self.thread = thread
        self.output_dir = output
        self.input_file = input_file

        # de_space settings
        self.slice_length = 1800


    def run_task(self):
        pass

    def slice_indexer(self):
        self.frame_count = get_frame_count(self.input_file)
        self.split_index = spitter(self.frame_count,self.slice_length)

    def slicer(self):
        pass

    def runner(self):
        args_list = []
        sliced_frame_list = slice_list(spitter(get_frame_count(self.input_file),self.slice_length),self.thread)



if __name__ == '__main__':
    print(spitter(100,10))








