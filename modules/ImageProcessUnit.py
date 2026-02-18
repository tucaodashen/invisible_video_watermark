import json
import os
import sys
import traceback
import uuid

import coredumpy
import cv2
import gettext

import numpy as np
import piexif
from PIL import Image
from PySide6.QtCore import QObject,Signal

_ = gettext.gettext
from BasicSystem import const
from BasicSystem.log_client import setup_logger,get_logger
from modules import watermarkstamper

setup_logger(default_tags="ImageProcessUnit", enable_udp=True, enable_console=True)
logger = get_logger()

class ImageProcessUnit(QObject):
    log_emit = Signal(str)
    switch_image = Signal(str)
    error_occur = Signal(dict)
    process_over = Signal()
    def __init__(self, image,watermark_method,attachment_data,output_path,prefix="",ext=const.IMAGE_TYPE.PNG,quality=100,output_method="exif",content=""):
        super().__init__()
        self.dump_uuid = uuid.uuid4()
        self.image = image
        self.process = 0
        self.output_path = output_path
        self.attachment_data = attachment_data
        self.watermark_method = watermark_method
        self.display_log = []
        self.name_prefix = prefix
        self.ext = ext
        self.quality = quality
        self.output_method = output_method
        self.content = content

    @staticmethod
    def stamp(method, attachment_data, cv2_image, watermark_content):
        if cv2_image is None:
            logger.warning("Empty input image, return None.", tags="ImageProcessUnit:ImageProcessUnit:stamp")
            return None

        proceeded = None
        try:
            if method == const.WatermarkAlgorithm.IMAGE_GUOFEI:
                proceeded = watermarkstamper.guofei_image(cv2_image, watermark_content, attachment_data)
            elif method == const.WatermarkAlgorithm.IMAGE_FIREKEEPER:
                proceeded = watermarkstamper.firekeeper_image(cv2_image, watermark_content, attachment_data)
            elif method == const.WatermarkAlgorithm.TEXT_GOUFEI:
                proceeded = watermarkstamper.guofei_text(cv2_image, watermark_content, attachment_data)
            elif method in [const.WatermarkAlgorithm.TEXT_FREQM, const.WatermarkAlgorithm.TEXT_RIVAGAN]:
                proceeded = watermarkstamper.freqmethod_text(cv2_image, watermark_content, attachment_data)
        except Exception as e:
            logger.error(f"Watermark library crashed: {e}")

        # 核心修复：如果打标失败或库报错，务必返回原图
        if proceeded is None:
            logger.warning("Watermark stamp failed, using original image.",
                           tags="ImageProcessUnit:ImageProcessUnit:stamp")
            return cv2_image

        logger.success("Watermark stamp success.", tags="ImageProcessUnit:ImageProcessUnit:stamp")
        return proceeded

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
        img_array = np.clip(img_array, 0, 255).astype('uint8')

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
                logger.critical(f"Cannot extract EXIF from source image {source_path}: {e}",tags="ImageProcessUnit:ImageProcessUnit:advanced_image_converter_with_exif")

        # 3. 修改目标字段 (保留其他所有原始信息)
        exif_dict["0th"][piexif.ImageIFD.Software] = software.encode('utf-8')
        # 处理 UserComment
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = b"ASCII\0\0\0" + comment.encode('utf-8')

        try:
            exif_bytes = piexif.dump(exif_dict)
        except Exception as e:
            logger.critical(f"Cannot dump EXIF: {e}",tags="ImageProcessUnit:ImageProcessUnit:advanced_image_converter_with_exif")
            exif_bytes = b""

        # 4. 保存
        try:
            # 转换逻辑保持不变...
            if ext in ['.jpg', '.jpeg']:
                pil_img.save(save_path, format='JPEG', exif=exif_bytes, quality=kwargs.get('quality', 80))
            elif ext == '.png':
                pil_img.save(save_path, format='PNG', exif=exif_bytes)
            elif ext == '.webp':
                pil_img.save(save_path, format='WebP', exif=exif_bytes, quality=kwargs.get('quality', 100))
            elif ext == '.avif':
                pil_img.save(save_path, format='AVIF', exif=exif_bytes, quality=kwargs.get('quality', 100))

            logger.success(f"Image {save_path} save success.",tags="ImageProcessUnit:ImageProcessUnit:advanced_image_converter_with_exif")
            return True
        except Exception as e:
            logger.error(f"Save image {save_path} failed: {e}",tags="ImageProcessUnit:ImageProcessUnit:advanced_image_converter_with_exif")
            return False


    def run(self):
        try:

            for images in self.image:
                output_path = os.path.join(self.output_path,
                                           f"{self.name_prefix}{os.path.basename(images).split('.')[0]}{self.ext.value}")
                logger.info(f"Begin to process image {images}",tags="ImageProcessUnit:ImageProcessUnit:run")
                self.log_emit.emit(_("开始处理图片{origin_image} -> {output_image}").format(origin_image=images,output_image=output_path))
                self.switch_image.emit(images)
                if not os.path.exists(images):
                    raise FileNotFoundError(_("图片 {images} 不存在，请检查路径是否正确。").format(images=images))
                cur_img = cv2.imread(images)
                if cur_img is None:
                    raise ValueError(_("图片 {images} 读取失败，请检查文件是否损坏。").format(images=images))
                proceeded_image, ret_atta = self.stamp(self.watermark_method,self.attachment_data,cur_img,self.content)
                ret_atta.update({"software":const.software_name,"version":const.__version__,"method":self.watermark_method.value})
                if proceeded_image is None:
                    raise ValueError(_("图片 {images} 打标失败，请检查文件是否损坏。").format(images=images))
                logger.success(f"Image {images} watermark stamp success. Init convert and embed process.",tags="ImageProcessUnit:ImageProcessUnit:run")
                if not os.path.exists(self.output_path):
                    os.makedirs(self.output_path)
                logger.debug(f"Output path: {output_path}. Begin convert and embed attachment data.",tags="ImageProcessUnit:ImageProcessUnit:run")
                self.advanced_image_converter_with_exif(proceeded_image,output_path,str(ret_atta),images,quality=self.quality)
                if self.output_method == "json":
                    with open(output_path.replace(self.ext.value,".json"),"w") as f:
                        json.dump(ret_atta,f,indent=4,ensure_ascii=False)
                if os.path.exists(output_path):
                    logger.success(f"Image {images} convert and embed attachment data success.",tags="ImageProcessUnit:ImageProcessUnit:run")
                else:
                    logger.error(f"Image {images} convert and embed attachment data failed.",tags="ImageProcessUnit:ImageProcessUnit:run")
                    raise FileNotFoundError(_("图片 {images} 嵌入成功但输出文件不存在，请检查路径是否正确. 避免在输出路径中使用中文或在处理中操作目录.").format(images=images))
        except Exception as e:
            logger.error(f"Image {images} process failed. Error: {e}",tags="ImageProcessUnit:ImageProcessUnit:run")
            path = f"./dumps/coredumpy_Image_{os.path.basename(images)}_{self.dump_uuid}.dump"
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()

            if exc_traceback:
                # 遍历到最深的 traceback（异常发生的位置）
                deepest_tb = exc_traceback
                while deepest_tb.tb_next:
                    deepest_tb = deepest_tb.tb_next

                # deepest_tb.tb_frame 就是异常发生的精确帧
                exception_frame = deepest_tb.tb_frame

                # 只转储异常发生的帧
                coredumpy.dump(frame=exception_frame,
                               description="Exception trigger frame only"
                               , path=path, depth=4)

                # 打印确认位置
                print(f"异常发生在: {exception_frame.f_code.co_filename}:{exception_frame.f_lineno}")
            else:
                coredumpy.dump(description="No traceback available", path=path, depth=4)
            self.error_occur.emit({
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
                "stack_trace": traceback.format_exc(),
                "core_dump": path,
            })
            print({
                "error_type": exc_type.__name__,
                "error_message": str(exc_value),
                "core_dump": path,
            })
        finally:
            self.process_over.emit()







if __name__ == "__main__":
    ImageProcessUnit.process_EXIF(r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228.PNG",r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228.PNG",r"C:\Users\ASUS\Desktop\新建文件夹\IMG_0228_EXIF.PNG","gugugaga guguggggg gugugugugugugugugu gugugugugugu gugugug gugugugu guguu gugugugu gugugugugugugguguguguguggugugu gugu gu gu gu  gu gugugugugu gugugugugugugugu")





