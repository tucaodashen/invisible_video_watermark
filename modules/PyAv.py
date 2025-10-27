import av
import numpy as np
from typing import List
import cv2
from collections import defaultdict


def extract_video_frames(video_path: str, frame_indices: List[int]) -> List[np.ndarray]:
    """
    从视频中提取指定帧号的帧

    参数:
        video_path: 视频文件路径
        frame_indices: 需要提取的帧号列表 (0-based索引)

    返回:
        包含指定帧的列表 (OpenCV BGR格式的numpy数组)
    """
    # 确保帧号列表是升序排列且去重
    sorted_indices = sorted(set(frame_indices))
    frame_dict = {idx: None for idx in sorted_indices}

    frames = []
    container = av.open(video_path)

    try:
        # 获取视频流 (通常取第一个视频流)
        stream = container.streams.video[0]
        stream.thread_type = 'AUTO'  # 自动选择线程类型提高解码速度

        # 设置起始位置到第一个关键帧
        if sorted_indices:
            container.seek(sorted_indices[0], stream=stream)

        # 遍历解码的视频帧
        frame_count = 0
        for frame in container.decode(stream):
            # 如果当前帧号在目标列表中
            if frame_count in frame_dict:
                # 转换为OpenCV格式 (BGR排列)
                img = frame.to_ndarray(format='bgr24')
                frame_dict[frame_count] = img

            # 当收集完所有需要的帧时提前退出
            if frame_count >= sorted_indices[-1]:
                break

            frame_count += 1

    finally:
        container.close()

    # 按原始请求顺序返回结果
    return [frame_dict[idx] for idx in frame_indices]


def group_similar_images(images, hash_threshold=5, size=(8, 8)):
    """
    根据图像相似度对输入图片进行分组，支持单通道和彩色图像

    参数:
        images: list of np.array, 输入图像列表 (灰度或BGR格式)
        hash_threshold: int, 哈希距离阈值 (默认5)
        size: tuple, 哈希计算时的缩放尺寸 (默认8x8)

    返回:
        list of lists of np.array, 相似图片的分组（每组包含原始图片数组）
    """

    # 计算图像的感知哈希值
    def calc_phash(img):
        # 处理不同通道数的图像
        if img.ndim == 3 and img.shape[2] == 3:  # BGR彩色图像
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.ndim == 3 and img.shape[2] == 4:  # BGRA图像
            gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        elif img.ndim == 2:  # 灰度图像
            gray = img
        else:
            # 其他格式的图像，尝试转换为灰度
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except:
                # 如果转换失败，取第一个通道
                gray = img[:, :, 0] if img.ndim == 3 else img

        # 缩放到指定尺寸
        resized = cv2.resize(gray, size)
        # 计算DCT变换
        dct = cv2.dct(np.float32(resized))
        # 取左上角8x8区域
        roi = dct[:8, :8]
        # 计算中值并生成哈希
        median = np.median(roi)
        hash_val = 0
        for i in range(8):
            for j in range(8):
                hash_val = (hash_val << 1) | (1 if roi[i, j] > median else 0)
        return hash_val

    # 计算汉明距离
    def hamming_distance(hash1, hash2):
        xor_val = hash1 ^ hash2
        distance = 0
        while xor_val:
            distance += 1
            xor_val &= xor_val - 1
        return distance

    # 计算所有图片的哈希值
    hashes = [calc_phash(img) for img in images]

    # 使用并查集进行分组
    parent = list(range(len(images)))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    # 比较所有图片对
    for i in range(len(images)):
        for j in range(i + 1, len(images)):
            if hamming_distance(hashes[i], hashes[j]) <= hash_threshold:
                union(i, j)

    # 收集分组结果（直接存储图片数组）
    groups = defaultdict(list)
    for i in range(len(images)):
        groups[find(i)].append(images[i])

    return list(groups.values())



