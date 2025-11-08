#DeepSeek写的 我这辈子都够呛能写出来
import numpy as np
import cv2
from sklearn.cluster import MiniBatchKMeans
import matplotlib.pyplot as plt
from numba import jit, prange

# 如果numba不可用，可以注释掉@jit装饰器
try:
    from numba import jit
except ImportError:
    # 定义一个空的装饰器作为回退
    def jit(*args, **kwargs):
        def decorator(func):
            return func

        return decorator


def calculate_perceptual_color_complexity_fast(img_array, method='perceptual_entropy',
                                               n_colors=8, color_space='BGR',
                                               downsample=True, max_pixels=50000):
    """
    优化后的快速颜色复杂度计算
    """
    # 验证输入
    if not isinstance(img_array, np.ndarray) or len(img_array.shape) != 3:
        raise ValueError("Input must be a 3D numpy array")

    # 处理颜色空间转换
    if color_space == 'BGR':
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    elif color_space == 'RGB':
        img_rgb = img_array.copy()
    else:
        raise ValueError("color_space must be 'BGR' or 'RGB'")

    # 下采样以减少计算量
    if downsample:
        h, w = img_rgb.shape[:2]
        total_pixels = h * w

        if total_pixels > max_pixels:
            scale = np.sqrt(max_pixels / total_pixels)
            new_h, new_w = int(h * scale), int(w * scale)
            img_rgb = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 转换为CIELAB颜色空间
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

    if method == 'perceptual_entropy':
        return _perceptual_entropy_fast(img_lab)
    elif method == 'kmeans_lab':
        return _kmeans_lab_complexity_fast(img_lab, n_colors)
    elif method == 'colorfulness':
        return _colorfulness_metric_fast(img_rgb)
    elif method == 'rms_contrast':
        return _rms_contrast_complexity_fast(img_lab)
    elif method == 'local_contrast':
        return _local_contrast_complexity_fast(img_lab)
    else:
        raise ValueError("Unsupported method")


@jit(nopython=True, cache=True)
def _fast_color_quantize(pixels, l_quant=4, a_quant=8, b_quant=8):
    """
    快速颜色量化 - 使用numba加速
    """
    h, w, c = pixels.shape
    quantized = np.empty((h, w, c), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            quantized[i, j, 0] = pixels[i, j, 0] // l_quant
            quantized[i, j, 1] = pixels[i, j, 1] // a_quant
            quantized[i, j, 2] = pixels[i, j, 2] // b_quant

    return quantized


def _perceptual_entropy_fast(img_lab):
    """
    优化的感知熵计算
    """
    h, w, c = img_lab.shape

    # 使用更粗略的量化
    l_quant = (img_lab[:, :, 0] // 8).astype(np.uint8)
    a_quant = (img_lab[:, :, 1] // 16).astype(np.uint8)
    b_quant = (img_lab[:, :, 2] // 16).astype(np.uint8)

    # 组合量化后的颜色
    quantized_colors = (l_quant.astype(np.uint32) << 16) | (a_quant.astype(np.uint32) << 8) | b_quant.astype(np.uint32)

    # 使用numpy的快速计数
    unique_colors, counts = np.unique(quantized_colors, return_counts=True)

    # 计算概率和熵
    probabilities = counts / (h * w)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))

    # 归一化
    max_entropy = np.log2(len(unique_colors)) if len(unique_colors) > 0 else 0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

    return normalized_entropy


def _kmeans_lab_complexity_fast(img_lab, n_colors=8):
    """
    优化的K-means聚类复杂度计算
    """
    h, w, c = img_lab.shape
    pixels = img_lab.reshape(-1, 3)

    # 限制采样数量
    max_samples = min(5000, len(pixels))

    if len(pixels) > max_samples:
        sample_indices = np.random.choice(len(pixels), max_samples, replace=False)
        sample_pixels = pixels[sample_indices]
    else:
        sample_pixels = pixels

    # 使用MiniBatchKMeans加速
    kmeans = MiniBatchKMeans(n_clusters=n_colors, random_state=42,
                             batch_size=256, max_iter=20, n_init=3)
    labels = kmeans.fit_predict(sample_pixels)

    # 计算簇大小
    cluster_sizes = np.bincount(labels, minlength=n_colors)
    cluster_proportions = cluster_sizes / len(sample_pixels)

    # 计算簇内距离（简化版，只计算到质心的距离）
    intra_distances = []
    for i in range(n_colors):
        if cluster_sizes[i] > 0:
            centroid = kmeans.cluster_centers_[i]
            # 只计算一个代表性距离，而不是所有点
            if cluster_sizes[i] > 1:
                # 随机选择一个点计算距离
                idx = np.random.randint(0, cluster_sizes[i])
                point = sample_pixels[labels == i][idx]
                distance = np.sqrt(np.sum((point - centroid) ** 2))
                intra_distances.append(distance)
            else:
                intra_distances.append(0)
        else:
            intra_distances.append(0)

    # 计算簇间距离（简化版，只计算相邻簇）
    inter_distances = []
    for i in range(n_colors):
        for j in range(i + 1, min(i + 3, n_colors)):  # 只计算相邻的簇
            distance = np.sqrt(np.sum((kmeans.cluster_centers_[i] - kmeans.cluster_centers_[j]) ** 2))
            inter_distances.append(distance)

    # 综合评分
    inter_score = np.mean(inter_distances) / 100 if inter_distances else 0
    intra_score = 1 - (np.mean(intra_distances) / 50) if intra_distances else 0
    uniformity_score = 1 - np.std(cluster_proportions)

    complexity_score = (inter_score * 0.4 + intra_score * 0.3 + uniformity_score * 0.3)
    return max(0, min(complexity_score, 1))


def _colorfulness_metric_fast(img_rgb):
    """
    优化的色彩丰富度计算
    """
    # 使用整数运算加速
    R = img_rgb[:, :, 0].astype(np.int16)
    G = img_rgb[:, :, 1].astype(np.int16)
    B = img_rgb[:, :, 2].astype(np.int16)

    # 计算RG和YB通道
    rg = R - G
    yb = (R + G) // 2 - B  # 使用整数除法

    # 计算标准差
    rg_std = np.std(rg)
    yb_std = np.std(yb)

    # 计算均值
    rg_mean = np.mean(np.abs(rg))  # 使用绝对值均值
    yb_mean = np.mean(np.abs(yb))

    # 计算色彩丰富度
    std_root = np.sqrt(rg_std ** 2 + yb_std ** 2)
    mean_root = np.sqrt(rg_mean ** 2 + yb_mean ** 2)

    colorfulness = std_root + 0.3 * mean_root

    # 归一化
    normalized_colorfulness = min(colorfulness / 0.5, 1.0)

    return normalized_colorfulness


def _rms_contrast_complexity_fast(img_lab):
    """
    优化的RMS对比度计算
    """
    L = img_lab[:, :, 0].astype(np.float32)

    # 计算亮度通道的标准差
    rms_contrast = np.std(L)

    # 归一化
    normalized_contrast = rms_contrast / 128.0

    return min(normalized_contrast, 1.0)


def _local_contrast_complexity_fast(img_lab, window_size=5):
    """
    优化的局部对比度计算
    """
    L = img_lab[:, :, 0].astype(np.float32)
    h, w = L.shape

    # 使用积分图像加速局部标准差计算
    L_sq = L ** 2

    # 计算积分图像
    L_int = cv2.integral(L)
    L_sq_int = cv2.integral(L_sq)

    # 计算局部均值和标准差
    pad = window_size // 2
    contrast_map = np.zeros((h, w), dtype=np.float32)

    for i in range(pad, h - pad):
        for j in range(pad, w - pad):
            # 使用积分图像快速计算区域和
            area_sum = (L_int[i + pad + 1, j + pad + 1] - L_int[i - pad, j + pad + 1] -
                        L_int[i + pad + 1, j - pad] + L_int[i - pad, j - pad])
            area_sq_sum = (L_sq_int[i + pad + 1, j + pad + 1] - L_sq_int[i - pad, j + pad + 1] -
                           L_sq_int[i + pad + 1, j - pad] + L_sq_int[i - pad, j - pad])

            # 计算均值和方差
            n_pixels = window_size * window_size
            mean = area_sum / n_pixels
            variance = (area_sq_sum / n_pixels) - (mean ** 2)

            # 标准差
            contrast_map[i, j] = np.sqrt(max(variance, 0))

    # 使用有效区域
    valid_contrast = contrast_map[pad:h - pad, pad:w - pad]

    if valid_contrast.size == 0:
        return 0.0

    # 计算对比度复杂性指标
    mean_contrast = np.mean(valid_contrast)
    contrast_variation = np.std(valid_contrast)

    # 归一化组合指标
    complexity = (mean_contrast / 50.0 + contrast_variation / 30.0) / 2.0

    return min(complexity, 1.0)


def get_perceptual_complexity_report_fast(img_array, color_space='BGR', downsample=True):
    """
    优化的完整复杂度报告
    """
    methods = ['perceptual_entropy', 'kmeans_lab', 'colorfulness', 'rms_contrast']
    scores = {}

    for method in methods:
        scores[method] = calculate_perceptual_color_complexity_fast(
            img_array, method=method, color_space=color_space, downsample=downsample)

    # 计算综合评分
    weights = {
        'perceptual_entropy': 0.3,
        'kmeans_lab': 0.3,
        'colorfulness': 0.25,
        'rms_contrast': 0.15
    }

    overall_score = sum(scores[method] * weights[method] for method in methods)

    report = {
        'scores': scores,
        'overall_score': overall_score,
        'interpretation': _interpret_perceptual_complexity_en(overall_score)
    }

    return report


def batch_process_complexity(images, color_space='BGR', downsample=True):
    """
    批量处理多张图片的颜色复杂度
    """
    results = []

    for i, img_array in enumerate(images):
        print(f"Processing image {i + 1}/{len(images)}")

        try:
            report = get_perceptual_complexity_report_fast(
                img_array, color_space=color_space, downsample=downsample)
            results.append(report)
        except Exception as e:
            print(f"Error processing image {i + 1}: {e}")
            results.append(None)

    return results


# 辅助函数
def _interpret_perceptual_complexity_en(score):
    """英文复杂度解释"""
    if score < 0.25:
        return "Low Complexity - Monotonous colors, low contrast"
    elif score < 0.5:
        return "Medium Complexity - Some color variation but not rich"
    elif score < 0.75:
        return "High Complexity - Rich colors, good contrast"
    else:
        return "Very High Complexity - Very rich colors, strong visual impact"


# 性能测试函数
def benchmark_complexity_calculation(img_array, iterations=10):
    """
    性能基准测试
    """
    import time

    methods = ['perceptual_entropy', 'kmeans_lab', 'colorfulness', 'rms_contrast']
    timings = {}

    for method in methods:
        start_time = time.time()

        for _ in range(iterations):
            score = calculate_perceptual_color_complexity_fast(
                img_array, method=method, downsample=True)

        end_time = time.time()
        avg_time = (end_time - start_time) / iterations
        timings[method] = avg_time

        print(f"{method}: {avg_time:.4f} seconds per calculation")

    # 测试完整报告
    start_time = time.time()
    for _ in range(iterations):
        report = get_perceptual_complexity_report_fast(img_array, downsample=True)
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations

    print(f"Full report: {avg_time:.4f} seconds per calculation")

    return timings, report


# 使用示例
if __name__ == "__main__":
    # 创建测试图像
    height, width = 400, 600
    img_array = cv2.imread("BandiView_Splash.png")

    # 性能测试
    print("Performance benchmark:")
    timings, report = benchmark_complexity_calculation(img_array, iterations=5)

    print("\nComplexity results:")
    print(f"Overall score: {report['overall_score']:.4f}")
    for method, score in report['scores'].items():
        print(f"{method}: {score:.4f}")
    print(f"Interpretation: {report['interpretation']}")

    # 批量处理示例
    print("\nBatch processing example:")
    images = [np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8) for _ in range(3)]
    results = batch_process_complexity(images)

    for i, result in enumerate(results):
        if result is not None:
            print(f"Image {i + 1}: {result['overall_score']:.4f}")