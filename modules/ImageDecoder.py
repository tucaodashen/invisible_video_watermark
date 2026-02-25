import os
import json
import threading

import cv2
import exif
import numpy as np
from PIL import Image
from PySide6.QtCore import QObject, Signal
from av import InvalidDataError

from BasicSystem import const
from BasicSystem.const import WatermarkAlgorithm
from BasicSystem.log_client import setup_logger, get_logger
from modules.watermarkdecoder import freqm_text_decoder, guofei_image_decoder, firekeeper_image_decoder, \
    goufei_text_decoder, rivagan_text_decoder

setup_logger(default_tags="ImageDecoder", enable_udp=True, enable_console=True)
logger = get_logger()


def load_avif_to_cv2(image_path):
    # 1. 使用 PIL 读取 AVIF 文件
    pil_img = Image.open(image_path).convert("RGB")

    # 2. 将 PIL 图像转换为 NumPy 数组
    # PIL 的形状是 (H, W, 3)，格式是 RGB
    numpy_array = np.array(pil_img)

    # 3. 将 RGB 转换为 BGR (OpenCV 标准格式)
    cv2_img = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)

    return cv2_img

class ImageDecoder(QObject):
    process_over = Signal(list)
    error_occur = Signal(str)
    process_percentage = Signal(float)

    def __init__(self, tasks):
        """
        tasks 格式: [{"image": path, "type": "json"/"exif", "data": dict_or_none}, ...]
        """
        super().__init__()
        self.tasks = tasks
        self._result = []
        self._stop_event = threading.Event()

        # 内部处理用的数据状态
        self.final_data_map = {}  # {img_path: data_dict}
        self.is_consistent = False
        self.common_data = None

    def stop(self):
        """外部调用以停止任务"""
        self._stop_event.set()

    def _prepare_data(self):
        """
        在开始循环前，补全 EXIF 数据并判定一致性
        """
        all_data = []
        for task in self.tasks:
            img_path = task["image"]

            # 如果是 JSON 类型，数据已经由 UI 层传入
            if task["type"] == "json":
                data = task["data"]

            # 如果是 EXIF 类型，此时需要读取具体的 data 内容
            else:
                try:
                    with open(img_path, "rb") as f:
                        img_obj = exif.Image(f)
                        user_comment = getattr(img_obj, "user_comment", "")
                        data = json.loads(user_comment)
                except Exception as e:
                    logger.error(f"Failed to read EXIF data for {img_path}: {e}",
                                 tags=f"ImageDecoder:ImageDecoder:_prepare_data:{os.path.basename(img_path)}")
                    return False

            self.final_data_map[img_path] = data
            all_data.append(data)

        # 判定是否所有 JSON 数据一致
        if all_data:
            self.is_consistent = all(d == all_data[0] for d in all_data)
            if self.is_consistent:
                self.common_data = all_data[0]

        return True

    def check_and_run(self):
        try:

            print(114514)
            self._stop_event.clear()

            # 1. 预处理数据映射和一致性判定
            if not self._prepare_data():
                raise ValueError("预处理任务数据失败，请检查文件权限或格式")

            # 2. 开始执行解码循环
            total = len(self.tasks)
            for idx, task in enumerate(self.tasks):
                img_path = task["image"]
                base_name = os.path.basename(img_path)

                # 停止检查点
                if self._stop_event.is_set():
                    logger.warning(f"Task stopped by user at {img_path}",
                                   tags=f"ImageDecoder:ImageDecoder:check_and_run:{base_name}")
                    return

                # --- 核心逻辑：选择对应的配置信息 (atta) ---
                # 如果一致用 common_data，不一致则从 map 里根据路径取
                atta = self.common_data if self.is_consistent else self.final_data_map.get(img_path)

                if not atta:
                    logger.error(f"Missing metadata for {img_path}",
                                 tags=f"ImageDecoder:ImageDecoder:check_and_run:{base_name}")
                    continue

                # 确定算法类型
                method_val = atta.get('method')
                method = None
                for alg in WatermarkAlgorithm:
                    if method_val == alg.value:
                        method = alg
                        break

                if not method:
                    logger.error(f"Unsupported method: {method_val}",
                                 tags=f"ImageDecoder:ImageDecoder:check_and_run:{base_name}")
                    continue

                # 读取图片并执行解码
                arr = load_avif_to_cv2(img_path)
                if arr is not None:
                    self._execute_decode(arr, atta, method, img_path)

                # 更新进度
                self.process_percentage.emit(float((idx + 1) / total * 100))

            # 3. 完成
            self.process_over.emit(self._result)

        except Exception as e:
            logger.error(f"Critical error during execution: {e}", tags="ImageDecoder:ImageDecoder:check_and_run:error")
            self.error_occur.emit(str(e))

    def _execute_decode(self, arr, atta, method, i_path):
        """执行具体的解码分发，严格复原你的 Tag 系统"""
        tag = f"ImageDecoder:ImageDecoder:check_and_run:{os.path.basename(i_path)}"
        try:
            if method == WatermarkAlgorithm.IMAGE_GUOFEI:
                self._result.append([method,guofei_image_decoder(arr, atta)])

            elif method == WatermarkAlgorithm.IMAGE_FIREKEEPER:
                resu, yuv = firekeeper_image_decoder(arr, atta)
                self._result.extend([[method,resu], [method,yuv[0]], [method,yuv[1]], [method,yuv[2]]])

            elif method == WatermarkAlgorithm.TEXT_FREQM:
                try:
                    result, valid = freqm_text_decoder(arr, atta)
                    if valid: self._result.append([method,result])
                except (UnicodeDecodeError, InvalidDataError):
                    pass
                except Exception as e:
                    logger.error(f"decode error {e}", tags=tag)
                    raise

            elif method == WatermarkAlgorithm.TEXT_GOUFEI:
                try:
                    result = goufei_text_decoder(arr, atta)
                    garbage_count = sum(1 for char in result if not char.isprintable())

                    rec = (garbage_count / len(result) >= 0.2)
                    if result and not rec:
                        self._result.append([method,result])
                except (ValueError, ZeroDivisionError):
                    pass
                except Exception as e:
                    logger.error(f"decode error {e}", tags=tag)
                    raise

            elif method == WatermarkAlgorithm.TEXT_RIVAGAN:
                try:
                    result = rivagan_text_decoder(arr, atta)
                except UnicodeDecodeError:
                    result = None
                except Exception as e:
                    logger.error(f"decode error {e}", tags=tag)
                    raise
                self._result.append([method,result])

        except Exception as e:
            logger.error(f"Unexpected algorithm failure: {e}", tags=tag)