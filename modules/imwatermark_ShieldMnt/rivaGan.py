import numpy as np
import cv2
import os
import time
import onnxruntime as ort

def create_onnx_session(model_path, device_id=0):
    available_providers = ort.get_available_providers()

    providers = []
    if 'CUDAExecutionProvider' in available_providers:
        providers.append(('CUDAExecutionProvider', {'device_id': device_id}))
    elif 'DmlExecutionProvider' in available_providers:
        providers.append(('DmlExecutionProvider', {'device_id': device_id}))

    providers.append('CPUExecutionProvider')

    session = ort.InferenceSession(model_path, providers=providers)

    print(f"Using providers: {session.get_providers()}")
    return session




modelDir = os.path.dirname(os.path.abspath(__file__))
enc_mod = create_onnx_session(
            os.path.join(modelDir, 'rivagan_encoder.onnx'))
dec_mod = create_onnx_session(
            os.path.join(modelDir, 'rivagan_decoder.onnx'))




class RivaWatermark(object):
    encoder = None
    decoder = None

    def __init__(self, watermarks=[], wmLen=32, threshold=0.52):
        self._watermarks = watermarks
        self._threshold = threshold
        if wmLen not in [32]:
            raise RuntimeError('rivaGan only supports 32 bits watermarks now.')
        self._data = np.array([self._watermarks], dtype=np.float32)

    @classmethod
    def loadModel(cls):
        if RivaWatermark.encoder and RivaWatermark.decoder:
            return
        RivaWatermark.encoder = enc_mod
        RivaWatermark.decoder = dec_mod

    def encode(self, frame):
        if not RivaWatermark.encoder:
            raise RuntimeError('call loadModel method first')

        # 确保输入是3通道图像
        if len(frame.shape) == 2:  # 灰度图
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # 使用numpy替代torch进行预处理
        frame = frame.astype(np.float32) / 127.5 - 1.0

        # 正确的维度变换顺序: (H, W, C) -> (1, C, 1, H, W)
        # 1. 添加batch维度: (H, W, C) -> (1, H, W, C)
        frame = np.expand_dims(frame, axis=0)
        # 2. 转置: (1, H, W, C) -> (1, C, H, W)
        frame = np.transpose(frame, (0, 3, 1, 2))
        # 3. 添加时间维度: (1, C, H, W) -> (1, C, 1, H, W)
        frame = np.expand_dims(frame, axis=2)

        inputs = {
            'frame': frame,
            'data': self._data
        }

        outputs = RivaWatermark.encoder.run(None, inputs)
        wm_frame = outputs[0]

        # 使用numpy.clip替代torch.clamp
        wm_frame = np.clip(wm_frame, -1.0, 1.0)

        # 后处理: 移除batch和时间维度，调整通道顺序
        # (1, C, 1, H, W) -> (C, H, W) -> (H, W, C)
        wm_frame = wm_frame[0]  # 移除batch维度 -> (C, 1, H, W)
        wm_frame = wm_frame[:, 0, :, :]  # 移除时间维度 -> (C, H, W)
        wm_frame = np.transpose(wm_frame, (1, 2, 0))  # (C, H, W) -> (H, W, C)
        wm_frame = ((wm_frame + 1.0) * 127.5).astype(np.uint8)

        return wm_frame

    def decode(self, frame):
        if not RivaWatermark.decoder:
            raise RuntimeError('you need load model first')

        # 确保输入是3通道图像
        if len(frame.shape) == 2:  # 灰度图
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # 使用numpy替代torch进行预处理
        frame = frame.astype(np.float32) / 127.5 - 1.0

        # 正确的维度变换顺序: (H, W, C) -> (1, C, 1, H, W)
        # 1. 添加batch维度: (H, W, C) -> (1, H, W, C)
        frame = np.expand_dims(frame, axis=0)
        # 2. 转置: (1, H, W, C) -> (1, C, H, W)
        frame = np.transpose(frame, (0, 3, 1, 2))
        # 3. 添加时间维度: (1, C, H, W) -> (1, C, 1, H, W)
        frame = np.expand_dims(frame, axis=2)

        inputs = {
            'frame': frame,
        }
        outputs = RivaWatermark.decoder.run(None, inputs)
        data = outputs[0][0]
        return np.array(data > self._threshold, dtype=np.uint8)