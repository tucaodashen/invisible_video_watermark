import cv2
import random
import os
import ffmpeg
from BasicSystem import const
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="VideoProcessor", enable_udp=True, enable_console=True)
logger = get_logger()










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
        logger.success(f"Add audio to video success: {output_path}",tags="VideoProcessor:add_audio_to_video")

    except ffmpeg.Error as e:
        logger.error(f"Add audio to video error: {e.stderr.decode()}",tags="VideoProcessor:add_audio_to_video")
    except Exception as e:
        logger.error(f"Add audio to video error: {str(e)}",tags="VideoProcessor:add_audio_to_video")

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


def video_sampler(source_path,sampler_times,sampler_extension,sampler_type,manual=None):

    logger.info(f"Start sampling video: {source_path}",tags="VideoProcessor:video_sampler")
    cap = cv2.VideoCapture(source_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    logger.info(f"Total frames: {total_frames}",tags="VideoProcessor:video_sampler")
    if sampler_type == const.SamplerType.RANDOM:
        primary_sampler_point = []
        for i in range(sampler_times):
            primary_sampler_point.append(random.randint(0,total_frames-1))
        logger.info(f"Primary sampler point: {primary_sampler_point}",tags="VideoProcessor:video_sampler")
        secondary_sampler_point = []
        for i in primary_sampler_point:
            for ti in range(sampler_extension):
                secondary_sampler_point.append(i+ti)
        logger.info(f"Secondary sampler point: {secondary_sampler_point}",tags="VideoProcessor:video_sampler")
        final_sampler_point = primary_sampler_point + secondary_sampler_point
        final_sampler_point.sort()
        final_sampler_point = list(set(final_sampler_point))
        logger.debug(f"Final sampler point: {final_sampler_point}",tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.FULL:
        final_sampler_point = list(range(total_frames))
        logger.debug(f"Final sampler point: {final_sampler_point}",tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.AVERAGE:
        primary_sampler_point = []
        period = total_frames // sampler_times
        for i in range(sampler_times):
            primary_sampler_point.append(i*period)
        logger.debug(f"Primary sampler point: {primary_sampler_point}",tags="VideoProcessor:video_sampler")
        secondary_sampler_point = []
        for i in primary_sampler_point:
            for ti in range(sampler_extension):
                secondary_sampler_point.append(i+ti)
        logger.debug(f"Secondary sampler point: {secondary_sampler_point}",tags="VideoProcessor:video_sampler")
        final_sampler_point = primary_sampler_point + secondary_sampler_point
        final_sampler_point.sort()
        final_sampler_point = list(set(final_sampler_point))
        logger.info(f"Final sampler point: {final_sampler_point}",tags="VideoProcessor:video_sampler")
        return final_sampler_point
    elif sampler_type == const.SamplerType.PSY:
        pass
    else:
        sampler_list = str(manual).split(",")
        final_sampler_point = []
        for i in sampler_list:
            final_sampler_point.append(int(i))
        logger.debug(f"Final sampler point: {final_sampler_point}",tags="VideoProcessor:video_sampler")
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
        logger.critical(f"Failed to open video file: {video_path}",tags="VideoProcessor:extract_frame_by_index")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")
        return

    # 设置目标帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    # 读取帧
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(output_path, frame)
        logger.debug(f"Extracted frame {frame_index} to {output_path}",tags="VideoProcessor:extract_frame_by_index")
    else:
        logger.error(f"Failed to extract frame {frame_index} from {video_path}",tags="VideoProcessor:extract_frame_by_index")

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
        logger.error(f"Failed to open video file: {video_path}",tags="VideoProcessor:extract_frames")
        raise FileNotFoundError(f"Failed to open video file: {video_path}")
        return

    # 获取视频总帧数和帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    logger.info(f"total_frames: {total_frames}",tags="VideoProcessor:extract_frames")
    logger.info(f"fps: {fps:.2f}",tags="VideoProcessor:extract_frames")

    # 验证帧范围有效性
    if start_frame < 0 or end_frame >= total_frames or start_frame > end_frame:
        logger.warning(f"Invalid frame range: {start_frame} to {end_frame}",tags="VideoProcessor:extract_frames")
        cap.release()
        return

    # 设置起始帧位置
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 逐帧处理
    for frame_num in range(start_frame, end_frame + 1):
        ret, frame = cap.read()

        if not ret:
            logger.critical(f"Failed to read {frame_num}",tags="VideoProcessor:extract_frames")
            raise RuntimeError(f"Failed to read frame {frame_num} from {video_path}")
            break

        # 保存帧为图像文件
        output_path = os.path.join(output_dir, f"frame_{frame_num:06d}.{formate}")
        cv2.imwrite(output_path, frame)

        # 显示进度
        if frame_num % 1 == 0:
            logger.debug(f"Extracted frame {frame_num}/{end_frame}",tags=f"VideoProcessor:extract_frames:{os.path.basename(video_path)}")
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
    logger.info(f"\nOver! Extracted {end_frame - start_frame + 1} to {output_dir}",tags=f"VideoProcessor:extract_frames:{os.path.basename(video_path)}")

def spitter(total_frame_count,split_size):
    logger.info(f"Executing spitter with total_frame_count: {total_frame_count} and split_size: {split_size}",tags="VideoProcessor:spitter")
    result = []
    start_index = 0
    while start_index < total_frame_count-1:
        s_start_index = start_index
        start_index = start_index + split_size
        end_index = min(start_index, total_frame_count)
        result.append((s_start_index, end_index-1))
    logger.debug(f"Spitter result: {result}",tags="VideoProcessor:spitter")
    return result


if __name__ == '__main__':
    print(spitter(100,10))








