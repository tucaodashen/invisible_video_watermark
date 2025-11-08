import cv2
import numpy as np
from modules import VideoProcessor
from PsychologicalSampler import ColorVariables
from modules import PyAv
import matplotlib.pyplot as plt


def draw(data):
    # 方法1：尝试使用不同的中文字体
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        pass

    # 提取坐标
    x = [point[1] for point in data]
    y = [point[0] for point in data]

    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 6))

    # 绘制折线图
    ax.plot(x, y, marker='o', linewidth=2.5, markersize=8,
            markerfacecolor='#FF6B6B', markeredgecolor='#C44D58',
            color='#4ECDC4', markeredgewidth=1)

    # 使用英文标签避免字体问题
    ax.set_title('Data Trend Line Chart', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Data Point Index', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)

    # 设置网格和刻度
    ax.grid(True, alpha=0.3, linestyle='-')
    ax.set_xticks(x)

    # 显示图表
    plt.tight_layout()
    plt.show()


def get_average_brightness_cv2(image_path):
    try:
        # 读取图片
        img = image_path

        # 转换为灰度图
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 计算平均亮度
        average_brightness = np.mean(gray_img)

        return average_brightness

    except Exception as e:
        print(f"处理图片时出错: {e}")
        return None


class AnalysisUnit:
    def __init__(self,video_path,slice_length):
        self.video_path = video_path
        self.frame_range = slice_length


class AnalysisSlice:
    def __init__(self,video_path,frame_range):
        self.video_path = video_path
        self.frame_range = frame_range
        self.frame_index = 0

    def extract_frames(self):
        frame_indices = list(range(self.frame_range[0],self.frame_range[1]+1))
        frames = PyAv.extract_video_frames(self.video_path,frame_indices)
        return frames

    def get_birghtness(self):
        frames = self.extract_frames()
        brightness = []
        for frame in frames:
            brightness.append([float(get_average_brightness_cv2(frame)),self.frame_index])
            self.frame_index += 1
        return brightness

    def get_color_variabilities(self):
        fina_result = []
        frames = self.extract_frames()
        results = ColorVariables.batch_process_complexity(frames)
        for i, result in enumerate(results):
            if result is not None:
                print(f"Image {i + 1}: {result['overall_score']:.4f}")
                fina_result.append([result['overall_score'],self.frame_index])
                self.frame_index += 1
        return fina_result


    def start(self):
        return self.get_color_variabilities()

    def start_bright(self):
        return self.get_birghtness()

if __name__ == "__main__":
    file = "../mul.mov"
    analysis_slice = AnalysisSlice(file,[0,VideoProcessor.get_frame_count(file)-1])
    draw(analysis_slice.start())
    analysis_slice = AnalysisSlice(file, [0, VideoProcessor.get_frame_count(file) - 1])
    draw(analysis_slice.start_bright())




