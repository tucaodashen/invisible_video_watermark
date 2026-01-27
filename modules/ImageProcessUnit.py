import os

import cv2
import gettext

import numpy as np
import piexif
from PIL import Image

_ = gettext.gettext
from BasicSystem import const
from BasicSystem.log_client import setup_logger,get_logger
from modules import watermarkstamper

setup_logger(default_tags="ImageProcessUnit", enable_udp=True, enable_console=True)
logger = get_logger()

class ImageProcessUnit:
    def __init__(self, image,watermark_method,attachment_data,output_path):
        self.image = image
        self.process = 0
        self.output_path = output_path
        self.attachment_data = attachment_data
        self.watermark_method = watermark_method
        self.display_log = []

    @staticmethod
    def stamp(method,attachment_data,image_path):
        image = cv2.imread(image_path)
        if not image:
            proceeded = None
            if method == const.WatermarkAlgorithm.IMAGE_GUOFEI:
                proceeded = watermarkstamper.guofei_image(image,attachment_data)
            if method == const.WatermarkAlgorithm.IMAGE_FIREKEEPER:
                proceeded = watermarkstamper.firekeeper_image(image,attachment_data)
            if method == const.WatermarkAlgorithm.TEXT_GOUFEI:
                proceeded = watermarkstamper.guofei_text(image,attachment_data)
            if method == const.WatermarkAlgorithm.TEXT_FREQM or method == const.WatermarkAlgorithm.TEXT_RIVAGAN:
                proceeded = watermarkstamper.freqmethod_text(image,attachment_data)
            if not proceeded:
                proceeded = image
                logger.warning(f"Image {image_path} watermark stamp failed, use original image instead.",tags="ImageProcessUnit:ImageProcessUnit:stamp")
            else:
                logger.success(f"Image {image_path} watermark stamp success.",tags="ImageProcessUnit:ImageProcessUnit:stamp")
                return proceeded
        logger.warning("Empty input image, return None.",tags="ImageProcessUnit:ImageProcessUnit:stamp")
        return None

    @staticmethod
    def advanced_image_converter_with_exif(img_array, save_path, comment="Custom Tag",
                                           source_path=None, **kwargs):
        """
        :param source_path: 传入原图路径，以便提取并保留原有的相机参数等元数据
        """
        software = f"{const.software_name} {const.__version__}"
        if img_array is None or not isinstance(img_array, np.ndarray):
            raise ValueError(f"❌ 传入的图像数据无效，请检查路径是否包含中文或文件是否存在。")

        ext = os.path.splitext(save_path)[1].lower()

        # 1. BGR 转 RGB
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)

        # 2. 提取并合并 EXIF
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}}

        if source_path and os.path.exists(source_path):
            try:
                # 尝试从原图提取 EXIF
                with Image.open(source_path) as src_img:
                    raw = src_img.info.get("exif")
                    if raw:
                        exif_dict = piexif.load(raw)
            except Exception as e:
                print(f"⚠️ 无法读取原图元数据: {e}")

        # 3. 修改目标字段 (保留其他所有原始信息)
        exif_dict["0th"][piexif.ImageIFD.Software] = software.encode('utf-8')
        # 处理 UserComment
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = b"ASCII\0\0\0" + comment.encode('utf-8')

        try:
            exif_bytes = piexif.dump(exif_dict)
        except Exception as e:
            print(f"⚠️ EXIF 写入失败（可能是原图包含非标准私有标签）: {e}")
            exif_bytes = b""

        # 4. 保存
        try:
            # 转换逻辑保持不变...
            if ext in ['.jpg', '.jpeg']:
                pil_img.save(save_path, format='JPEG', exif=exif_bytes, quality=kwargs.get('quality', 95))
            elif ext == '.png':
                pil_img.save(save_path, format='PNG', exif=exif_bytes)
            elif ext == '.webp':
                pil_img.save(save_path, format='WebP', exif=exif_bytes, quality=kwargs.get('quality', 100))
            elif ext == '.avif':
                pil_img.save(save_path, format='AVIF', exif=exif_bytes, quality=kwargs.get('quality', 80))

            print(f"✨ 转换并打标完成: {save_path}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False



if __name__ == "__main__":
    ImageProcessUnit.process_EXIF(r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228.PNG",r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228.PNG",r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228_EXIF.PNG","gugugaga guguggggg gugugugugugugugugu gugugugugugu gugugug gugugugu guguu gugugugu gugugugugugugguguguguguggugugu gugu gu gu gu  gu gugugugugu gugugugugugugugu")





