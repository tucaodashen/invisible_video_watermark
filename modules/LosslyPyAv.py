import av
import numpy as np
from typing import List
from bisect import bisect_left


def extract_video_frames_optimized(video_path: str, frame_indices: List[int]) -> List[np.ndarray]:
    """
    优化版：从视频中提取指定帧号的帧，特别适合分散的帧提取

    参数:
        video_path: 视频文件路径
        frame_indices: 需要提取的帧号列表 (0-based索引)

    返回:
        包含指定帧的列表 (OpenCV BGR格式的numpy数组)
    """
    if not frame_indices:
        return []

    # 去重并排序
    sorted_indices = sorted(set(frame_indices))
    frame_dict = {idx: None for idx in sorted_indices}

    # 分组策略：将连续的帧分成一组，减少seek次数
    groups = []
    current_group = [sorted_indices[0]]

    for i in range(1, len(sorted_indices)):
        # 如果帧号连续或接近，放在同一组（阈值可调整）
        if sorted_indices[i] - sorted_indices[i - 1] <= 30:  # 30帧内的认为是连续的
            current_group.append(sorted_indices[i])
        else:
            groups.append(current_group)
            current_group = [sorted_indices[i]]
    groups.append(current_group)

    container = av.open(video_path)

    try:
        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'

        for group in groups:
            if not group:
                continue

            start_frame = group[0]
            end_frame = group[-1]

            # 跳转到组起始位置（向前多跳一些以确保包含关键帧）
            seek_target = max(0, start_frame - 30)  # 向前多跳30帧
            container.seek(seek_target, stream=stream)

            frame_count = 0
            decoded_since_seek = 0

            for frame in container.decode(stream):
                current_frame = frame.pts * stream.time_base * stream.average_rate
                frame_count = int(round(current_frame))

                # 如果已经超过当前组范围，提前退出
                if frame_count > end_frame:
                    break

                # 如果当前帧在目标组中
                if frame_count in frame_dict and frame_dict[frame_count] is None:
                    img = frame.to_ndarray(format='bgr24')
                    frame_dict[frame_count] = img

                decoded_since_seek += 1
                # 安全机制：如果解码太多帧还没找到目标，可能seek失败，跳出循环
                if decoded_since_seek > 1000:
                    break

    finally:
        container.close()

    # 按原始顺序返回结果
    return [frame_dict[idx] for idx in frame_indices]


def extract_video_frames_fastest(video_path: str, frame_indices: List[int]) -> List[np.ndarray]:
    """
    最快版本：对每个目标帧单独seek（适合非常分散的帧）

    参数:
        video_path: 视频文件路径
        frame_indices: 需要提取的帧号列表 (0-based索引)

    返回:
        包含指定帧的列表 (OpenCV BGR格式的numpy数组)
    """
    if not frame_indices:
        return []

    sorted_indices = sorted(set(frame_indices))
    frame_dict = {idx: None for idx in sorted_indices}

    container = av.open(video_path)

    try:
        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'

        for target_frame in sorted_indices:
            try:
                # 精确跳转到目标帧附近
                container.seek(target_frame, stream=stream)

                # 解码直到找到目标帧
                for frame in container.decode(stream):
                    current_frame = frame.pts * stream.time_base * stream.average_rate
                    current_frame_num = int(round(current_frame))

                    if current_frame_num >= target_frame:
                        if current_frame_num == target_frame:
                            img = frame.to_ndarray(format='bgr24')
                            frame_dict[target_frame] = img
                        break

            except Exception as e:
                print(f"Error extracting frame {target_frame}: {e}")
                continue

    finally:
        container.close()

    return [frame_dict[idx] for idx in frame_indices]


def extract_video_frames_adaptive(video_path: str, frame_indices: List[int], threshold: int = 10) -> List[np.ndarray]:
    """
    自适应版本：根据帧的分散程度自动选择最优策略

    参数:
        video_path: 视频文件路径
        frame_indices: 需要提取的帧号列表
        threshold: 判断分散程度的阈值（平均间隔大于此值时使用快速模式）

    返回:
        包含指定帧的列表
    """
    if not frame_indices:
        return []

    sorted_indices = sorted(set(frame_indices))

    # 计算帧的平均间隔来判断分散程度
    if len(sorted_indices) > 1:
        total_span = sorted_indices[-1] - sorted_indices[0]
        avg_interval = total_span / len(sorted_indices)

        if avg_interval > threshold:
            # 帧比较分散，使用快速模式
            return extract_video_frames_fastest(video_path, frame_indices)

    # 帧比较集中，使用优化模式
    return extract_video_frames_optimized(video_path, frame_indices)