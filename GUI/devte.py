import qrcode
import numpy as np
import cv2
from typing import Tuple

def generate_qr_cv2(
    data: str,
    border_px: int = 20,
    cell_px: int = 10,
    debug: bool = False
) -> Tuple[np.ndarray, dict]:
    """
    生成 QR 的 OpenCV BGR ndarray，并返回 (img, info)。
    参数:
        data: 要编码的字符串
        border_px: 外边框像素（像素单位）
        cell_px: 每个模块（黑/白小格）的像素大小
        debug: True 时会在 info 中返回调试信息
    返回:
        img: numpy.ndarray, dtype=uint8, BGR
        info: dict 包含 matrix_size, img_shape, used_border_px, used_cell_px 等信息
    """
    if cell_px <= 0:
        raise ValueError("cell_px 必须大于 0")
    if border_px < 0:
        raise ValueError("border_px 不能是负数")

    # 生成模块矩阵（True = 黑）
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
    qr.add_data(data)
    qr.make(fit=True)
    matrix = qr.get_matrix()  # list[list[bool]]
    modules_h = len(matrix)
    modules_w = len(matrix[0]) if modules_h>0 else 0

    # 计算图片像素大小
    img_h = modules_h * cell_px + border_px * 2
    img_w = modules_w * cell_px + border_px * 2

    if img_h <= 0 or img_w <= 0:
        raise RuntimeError("计算到的图片尺寸不正确: img_h={}, img_w={}".format(img_h, img_w))

    # 创建白底 BGR 图像
    img = np.full((img_h, img_w, 3), 255, dtype=np.uint8)

    # 填充黑色模块
    for r in range(modules_h):
        for c in range(modules_w):
            if matrix[r][c]:
                y0 = border_px + r * cell_px
                x0 = border_px + c * cell_px
                # 防止超出边界（理论上不会）
                y1 = min(y0 + cell_px, img_h)
                x1 = min(x0 + cell_px, img_w)
                img[y0:y1, x0:x1] = (0, 0, 0)

    info = {
        "modules_h": modules_h,
        "modules_w": modules_w,
        "img_h": img_h,
        "img_w": img_w,
        "border_px": border_px,
        "cell_px": cell_px,
        "dtype": str(img.dtype),
        "shape": img.shape,
    }

    if debug:
        print("generate_qr_cv2 debug:", info)

    return img, info



if __name__ == "__main__":
    # 简单示例：生成并保存
    sample = "https://exampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexampleexample.com"
    img, info = generate_qr_cv2(sample, border_px=0, cell_px=1000)
    cv2.imwrite("qr_example.png", img)
    print("Saved qr_example.png")
