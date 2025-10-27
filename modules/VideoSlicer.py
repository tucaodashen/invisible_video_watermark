import os
import cv2
from moviepy import VideoFileClip
from PIL import Image
from BasicSystem import LogSystem
import multiprocessing

def slicer(slice_list,file,dist):
    clip = VideoFileClip(file)
    for i in slice_list:
        pt = os.path.join(dist,f"{i[0]}-{i[1]}")
        os.makedirs(pt)
        for ia in range(i[0],i[1]):
            clip.save_frame(os.path.join(pt,f"{ia}.png"),int(ia))
    clip.close()

def extract_frames(video_path, start_frame, end_frame, output_dir):
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
        output_path = os.path.join(output_dir, f"frame_{frame_num:06d}.png")
        cv2.imwrite(output_path, frame)

        # 显示进度
        if frame_num % 50 == 0:
            LogSystem.logger.debug(f"Extracted frame {frame_num}/{end_frame}")

    # 释放资源
    cap.release()
    LogSystem.logger.info(f"\nOver! Extracted {end_frame - start_frame + 1} to {output_dir}")
