import cv2
import numpy as np
from typing import List, Tuple, Dict
import os


class AdvancedFrameSelector:
    def __init__(self, processing_size=(320, 240)):
        """
        高级帧选择器 - 避免大面积连续纯色区域

        参数:
            processing_size: 处理时使用的图像尺寸
        """
        self.processing_size = processing_size

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """快速预处理：缩放和转灰度"""
        small_frame = cv2.resize(frame, self.processing_size)
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        return gray, small_frame

    def detect_solid_color_areas(self, frame: np.ndarray,
                                 color_variance_threshold: float = 10.0,
                                 min_region_ratio: float = 0.05) -> Dict[str, float]:
        """
        检测大面积连续纯色区域

        参数:
            color_variance_threshold: 颜色方差阈值，低于此值视为纯色
            min_region_ratio: 最小区域占比阈值

        返回:
            纯色区域信息
        """
        # 转换为LAB颜色空间，更好的感知均匀性
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        # 计算局部颜色方差
        local_color_variance = self.calculate_local_color_variance(lab)

        # 检测低方差区域（纯色区域）
        solid_color_mask = local_color_variance < color_variance_threshold

        # 计算纯色区域总占比
        solid_ratio = np.sum(solid_color_mask) / solid_color_mask.size

        # 检测大面积连续纯色区域
        large_solid_regions = self.detect_large_solid_regions(
            solid_color_mask, min_region_ratio
        )

        # 检测特定颜色的纯色区域（白色、黑色等）
        white_regions = self.detect_specific_color_regions(frame, 'white')
        black_regions = self.detect_specific_color_regions(frame, 'black')

        return {
            'solid_ratio': solid_ratio,
            'has_large_solid_region': large_solid_regions,
            'white_ratio': white_regions['ratio'],
            'black_ratio': black_regions['ratio'],
            'has_large_white_region': white_regions['has_large_region'],
            'has_large_black_region': black_regions['has_large_region'],
            'solid_mask': solid_color_mask
        }

    def calculate_local_color_variance(self, lab: np.ndarray, kernel_size: int = 7) -> np.ndarray:
        """计算局部颜色方差"""
        l, a, b = cv2.split(lab.astype(np.float32))

        # 计算每个通道的局部方差
        l_var = self.calculate_local_variance(l, kernel_size)
        a_var = self.calculate_local_variance(a, kernel_size)
        b_var = self.calculate_local_variance(b, kernel_size)

        # 综合颜色方差
        color_variance = (l_var + a_var + b_var) / 3.0
        return color_variance

    def calculate_local_variance(self, channel: np.ndarray, kernel_size: int) -> np.ndarray:
        """计算单通道的局部方差"""
        mean_filter = cv2.boxFilter(channel, -1, (kernel_size, kernel_size))
        mean_square_filter = cv2.boxFilter(channel ** 2, -1, (kernel_size, kernel_size))
        local_var = mean_square_filter - mean_filter ** 2
        return local_var

    def detect_large_solid_regions(self, solid_mask: np.ndarray, min_region_ratio: float) -> bool:
        """检测大面积连续纯色区域"""
        # 寻找连通区域
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            solid_mask.astype(np.uint8), connectivity=8
        )

        # 计算每个区域的面积占比
        total_pixels = solid_mask.size
        for i in range(1, num_labels):  # 跳过背景(0)
            area_ratio = stats[i, cv2.CC_STAT_AREA] / total_pixels
            if area_ratio > min_region_ratio:
                return True

        return False

    def detect_specific_color_regions(self, frame: np.ndarray, color: str) -> Dict[str, float]:
        """检测特定颜色的区域（白色、黑色等）"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if color == 'white':
            # 白色检测：高亮度、低饱和度
            v_channel = hsv[:, :, 2]
            s_channel = hsv[:, :, 1]
            color_mask = (v_channel > 220) & (s_channel < 30)
        elif color == 'black':
            # 黑色检测：低亮度
            v_channel = hsv[:, :, 2]
            color_mask = v_channel < 30
        else:
            color_mask = np.zeros(frame.shape[:2], dtype=bool)

        color_ratio = np.sum(color_mask) / color_mask.size
        has_large_region = self.detect_large_solid_regions(color_mask, 0.05)

        return {
            'ratio': color_ratio,
            'has_large_region': has_large_region
        }

    def fast_brightness_analysis(self, gray: np.ndarray) -> Dict[str, float]:
        """快速亮度分析"""
        brightness = gray.astype(np.float32)

        mean_val = np.mean(brightness)
        std_val = np.std(brightness)
        min_val = np.min(brightness)
        max_val = np.max(brightness)

        contrast = self.fast_contrast_measure(gray)

        return {
            'mean': mean_val,
            'std': std_val,
            'range': max_val - min_val,
            'contrast': contrast,
            'variation_score': std_val * 0.7 + (max_val - min_val) * 0.3
        }

    def fast_contrast_measure(self, gray: np.ndarray, block_size: int = 8) -> float:
        """快速对比度测量"""
        h, w = gray.shape
        local_contrasts = []

        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = gray[i:i + block_size, j:j + block_size]
                block_std = np.std(block)
                local_contrasts.append(block_std)

        return np.mean(local_contrasts) if local_contrasts else 0

    def fast_texture_analysis(self, gray: np.ndarray) -> Dict[str, float]:
        """快速纹理分析"""
        # 梯度计算
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        gradient_var = np.var(gradient_magnitude)

        # 边缘密度
        edges_approx = (gradient_magnitude > 30).astype(np.uint8) * 255
        edge_density = np.mean(edges_approx > 0)

        # 局部方差
        local_var = self.fast_local_variance(gray)

        # 综合纹理分数
        texture_score = gradient_var * 0.5 + edge_density * 0.3 + local_var * 0.2

        return {
            'gradient_var': gradient_var,
            'edge_density': edge_density,
            'local_variance': local_var,
            'texture_score': texture_score
        }

    def fast_local_variance(self, gray: np.ndarray, kernel_size: int = 5) -> float:
        """快速局部方差计算"""
        mean_filter = cv2.boxFilter(gray.astype(np.float32), -1, (kernel_size, kernel_size))
        mean_square_filter = cv2.boxFilter((gray ** 2).astype(np.float32), -1, (kernel_size, kernel_size))
        local_var = mean_square_filter - mean_filter ** 2
        return np.mean(local_var)

    def calculate_solid_color_penalty(self, solid_info: Dict[str, float],
                                      max_solid_ratio: float = 0.3,
                                      max_white_ratio: float = 0.2,
                                      max_black_ratio: float = 0.3) -> float:
        """计算纯色区域惩罚分数"""
        solid_ratio = solid_info['solid_ratio']
        white_ratio = solid_info['white_ratio']
        black_ratio = solid_info['black_ratio']

        # 基础惩罚
        penalty = 1.0

        # 大面积连续纯色区域严重惩罚
        if solid_info['has_large_solid_region']:
            penalty *= 0.1

        # 大面积白色区域惩罚
        if solid_info['has_large_white_region']:
            penalty *= 0.2

        # 大面积黑色区域惩罚
        if solid_info['has_large_black_region']:
            penalty *= 0.3

        # 纯色区域比例惩罚
        if solid_ratio > max_solid_ratio:
            excess_ratio = (solid_ratio - max_solid_ratio) / (1.0 - max_solid_ratio)
            penalty *= max(0.1, 1.0 - excess_ratio)

        # 白色区域比例惩罚
        if white_ratio > max_white_ratio:
            excess_ratio = (white_ratio - max_white_ratio) / (1.0 - max_white_ratio)
            penalty *= max(0.2, 1.0 - excess_ratio)

        # 黑色区域比例惩罚
        if black_ratio > max_black_ratio:
            excess_ratio = (black_ratio - max_black_ratio) / (1.0 - max_black_ratio)
            penalty *= max(0.3, 1.0 - excess_ratio)

        return max(0.05, penalty)  # 确保最小惩罚不为0

    def calculate_frame_score_enhanced(self, frame: np.ndarray,
                                       max_solid_ratio: float = 0.3,
                                       max_white_ratio: float = 0.2,
                                       max_black_ratio: float = 0.3,
                                       color_variance_threshold: float = 10.0) -> Dict[str, float]:
        """
        增强版帧评分计算，避免大面积纯色区域
        """
        # 预处理
        gray, small_frame = self.preprocess_frame(frame)

        # 纯色区域检测
        solid_info = self.detect_solid_color_areas(
            small_frame, color_variance_threshold
        )

        # 计算纯色区域惩罚
        solid_penalty = self.calculate_solid_color_penalty(
            solid_info, max_solid_ratio, max_white_ratio, max_black_ratio
        )

        # 亮度和纹理分析
        brightness_features = self.fast_brightness_analysis(gray)
        texture_features = self.fast_texture_analysis(gray)

        # 亮度适宜度
        brightness_mean = brightness_features['mean']
        if 50 <= brightness_mean <= 200:
            brightness_optimal = 1.0 - abs(brightness_mean - 127) / 77
        else:
            brightness_optimal = 0.3

        # 综合评分（加入纯色区域惩罚）
        total_score = (
                brightness_features['variation_score'] * 0.35 +
                texture_features['texture_score'] * 0.45 +
                brightness_optimal * 0.1 +
                solid_penalty * 0.1  # 纯色区域影响
        )

        return {
            'total_score': total_score,
            'brightness_variation': brightness_features['variation_score'],
            'brightness_std': brightness_features['std'],
            'brightness_range': brightness_features['range'],
            'texture_complexity': texture_features['texture_score'],
            'brightness_optimal': brightness_optimal,
            'solid_ratio': solid_info['solid_ratio'],
            'white_ratio': solid_info['white_ratio'],
            'black_ratio': solid_info['black_ratio'],
            'has_large_solid_region': solid_info['has_large_solid_region'],
            'has_large_white_region': solid_info['has_large_white_region'],
            'has_large_black_region': solid_info['has_large_black_region'],
            'solid_penalty': solid_penalty
        }

    def select_frames_avoiding_solid_colors(self, video_path: str,
                                            num_frames: int = 10,
                                            sampling_interval: int = 10,
                                            min_brightness_std: float = 15.0,
                                            min_texture_score: float = 30.0,
                                            max_solid_ratio: float = 0.3,
                                            max_white_ratio: float = 0.2,
                                            max_black_ratio: float = 0.3,
                                            color_variance_threshold: float = 10.0) -> List[Tuple[int, Dict]]:
        """
        避免纯色区域的帧选择方法
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        print(f"视频信息: {total_frames} 帧, {fps:.1f} FPS")
        print("开始分析（避免纯色区域）...")

        frame_scores = []
        frame_count = 0
        processed_count = 0
        solid_rejected_count = 0  # 记录因纯色区域被拒绝的帧数

        last_progress = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % sampling_interval == 0:
                score_info = self.calculate_frame_score_enhanced(
                    frame, max_solid_ratio, max_white_ratio, max_black_ratio, color_variance_threshold
                )

                # 应用阈值过滤（包括纯色区域检查）
                solid_ok = (score_info['solid_ratio'] <= max_solid_ratio and
                            not score_info['has_large_solid_region'] and
                            score_info['white_ratio'] <= max_white_ratio and
                            score_info['black_ratio'] <= max_black_ratio)

                brightness_ok = score_info['brightness_std'] >= min_brightness_std
                texture_ok = score_info['texture_complexity'] >= min_texture_score

                if solid_ok and brightness_ok and texture_ok:
                    frame_scores.append((frame_count, score_info))
                elif not solid_ok:
                    solid_rejected_count += 1

                processed_count += 1

                # 进度显示
                progress = int(frame_count * 100 / total_frames)
                if progress != last_progress and progress % 10 == 0:
                    print(f"分析进度: {progress}%")
                    last_progress = progress

            frame_count += 1

        cap.release()

        print(f"分析完成! 处理了 {processed_count} 帧")
        print(f"找到 {len(frame_scores)} 个候选帧, 因纯色区域拒绝了 {solid_rejected_count} 帧")

        # 按总分排序
        frame_scores.sort(key=lambda x: x[1]['total_score'], reverse=True)
        return frame_scores[:num_frames]

    def select_frames_with_solid_color_avoidance(self, video_path: str,
                                                 num_frames: int = 10,
                                                 min_time_gap: float = 2.0,
                                                 **kwargs) -> List[Tuple[int, Dict]]:
        """
        带纯色区域避免和时间间隔的帧选择
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        min_frame_gap = int(min_time_gap * fps)

        # 获取候选帧
        candidate_frames = self.select_frames_avoiding_solid_colors(
            video_path, num_frames * 3, **kwargs
        )

        selected_frames = []
        used_frame_indices = []

        # 优先选择高分帧，确保时间分布
        for frame_idx, score_info in candidate_frames:
            if len(selected_frames) >= num_frames:
                break

            # 检查时间间隔
            valid = True
            for used_idx in used_frame_indices:
                if abs(frame_idx - used_idx) < min_frame_gap:
                    valid = False
                    break

            if valid:
                selected_frames.append((frame_idx, score_info))
                used_frame_indices.append(frame_idx)

        # 如果选不够，补充剩余高分帧
        if len(selected_frames) < num_frames:
            remaining = [f for f in candidate_frames if f[0] not in used_frame_indices]
            remaining = remaining[:num_frames - len(selected_frames)]
            selected_frames.extend(remaining)

        # 按帧序号排序
        selected_frames.sort(key=lambda x: x[0])

        return selected_frames


def analyze_and_select_with_solid_color_avoidance(video_path: str, output_dir: str,
                                                  detailed_analysis: bool = False, **kwargs):
    """
    完整的帧选择流程，包含纯色区域避免
    """
    selector = AdvancedFrameSelector(processing_size=(320, 240))

    # 选择帧
    selected_frames = selector.select_frames_with_solid_color_avoidance(video_path, **kwargs)

    print("\n" + "=" * 80)
    print("选中的帧分析结果 (已避免纯色区域):")
    print("=" * 80)

    for i, (frame_idx, score_info) in enumerate(selected_frames):
        solid_status = "有大面积纯色" if score_info[
            'has_large_solid_region'] else f"纯色占比:{score_info['solid_ratio']:.3f}"
        white_status = "有大面积白色" if score_info[
            'has_large_white_region'] else f"白色占比:{score_info['white_ratio']:.3f}"
        black_status = "有大面积黑色" if score_info[
            'has_large_black_region'] else f"黑色占比:{score_info['black_ratio']:.3f}"

        print(f"\n帧 {i + 1:2d}: 序号={frame_idx:5d}, 总分={score_info['total_score']:.2f}")
        print(f"  亮度变化: {score_info['brightness_variation']:.2f} "
              f"(标准差: {score_info['brightness_std']:.2f})")
        print(f"  纹理复杂度: {score_info['texture_complexity']:.2f}")
        print(f"  纯色区域: {solid_status}")
        print(f"  白色区域: {white_status}")
        print(f"  黑色区域: {black_status}")
        print(f"  纯色惩罚系数: {score_info['solid_penalty']:.2f}")

    # 提取帧
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extract_frames_with_solid_color_info(video_path, selected_frames, output_dir)

    return selected_frames


def extract_frames_with_solid_color_info(video_path: str, selected_frames: List[Tuple[int, Dict]],
                                         output_dir: str):
    """
    提取帧并保存纯色区域信息
    """
    selector = AdvancedFrameSelector()
    cap = cv2.VideoCapture(video_path)

    for frame_idx, score_info in selected_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if ret:
            # 保存原始帧
            output_path = os.path.join(output_dir, f"frame_{frame_idx:06d}.jpg")
            cv2.imwrite(output_path, frame)

            # 可视化纯色区域（可选）
            _, small_frame = selector.preprocess_frame(frame)
            solid_info = selector.detect_solid_color_areas(small_frame)

            # 创建纯色区域可视化
            solid_visual = small_frame.copy()
            solid_visual[solid_info['solid_mask']] = [0, 0, 255]  # 红色标记纯色区域

            visual_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_solid_areas.jpg")
            cv2.imwrite(visual_path, solid_visual)

            # 保存详细评分信息
            info_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_info.txt")
            with open(info_path, 'w') as f:
                f.write("帧选择评分信息:\n")
                f.write("=" * 40 + "\n")
                for key, value in score_info.items():
                    f.write(f"{key}: {value:.4f}\n")

    cap.release()
    print(f"\n帧和纯色区域可视化已保存到: {output_dir}")


# 使用示例
if __name__ == "__main__":
    video_path = "op2.mp4"  # 替换为你的视频路径
    output_dir = "selectoutttted_frames_no_solid_colors"

    try:
        print("开始帧选择（避免纯色区域）...")

        # 选择帧，避免纯色区域
        selected_frames = analyze_and_select_with_solid_color_avoidance(
            video_path=video_path,
            output_dir=output_dir,
            num_frames=30,
            sampling_interval=15,
            min_brightness_std=10.0,
            min_texture_score=20.0,
            max_solid_ratio=0.25,  # 最大允许25%的纯色区域
            max_white_ratio=0.15,  # 最大允许15%的白色区域
            max_black_ratio=0.25,  # 最大允许25%的黑色区域
            color_variance_threshold=8.0,  # 颜色方差阈值
            min_time_gap=2.0
        )

        print(f"\n成功选择了 {len(selected_frames)} 个最佳帧（已避免大面积纯色区域）")

    except Exception as e:
        print(f"处理错误: {e}")


# 批量处理函数
def batch_process_avoiding_solid_colors(video_paths: List[str], output_base_dir: str, **kwargs):
    """
    批量处理多个视频，避免纯色区域
    """
    for video_path in video_paths:
        if not os.path.exists(video_path):
            print(f"文件不存在: {video_path}")
            continue

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = os.path.join(output_base_dir, video_name)

        print(f"\n处理视频: {video_name}")

        try:
            selected_frames = analyze_and_select_with_solid_color_avoidance(
                video_path, output_dir, **kwargs
            )
            print(f"为 {video_name} 选择了 {len(selected_frames)} 帧")

        except Exception as e:
            print(f"处理 {video_path} 时出错: {e}")