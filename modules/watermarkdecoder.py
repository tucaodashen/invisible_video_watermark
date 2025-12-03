import modules.blind_watermark_guofei as guofei
import modules.BlindWatermark_FireKeeper as firekeeper
from modules.imwatermark_ShieldMnt import WatermarkDecoder
from BasicSystem.log_client import get_logger,setup_logger
setup_logger(default_tags="watermark_decoder", enable_udp=True, enable_console=True)
logger = get_logger()

"""
all the functions' input are cv2 images and output are cv2 images

"""

def goufei_text_decoder(img,attachment_data):
    bwm1 = guofei.WaterMark(password_img=attachment_data['img_password'], password_wm=attachment_data['wm_password'])
    wm_extract = bwm1.extract(embed_img=img, wm_shape=attachment_data['len_wm'], mode='str')
    logger.success(f"Extract text success: {wm_extract}",tags="watermark_decoder:guofei_text_decoder")
    return wm_extract

def guofei_image_decoder(img,attachment_data):
    bwm1 = guofei.WaterMark(password_wm=attachment_data['wm_password'], password_img=attachment_data['img_password'])
    # notice that wm_shape is necessary
    resu = bwm1.extract(embed_img=img, wm_shape=attachment_data['len_wm'])
    logger.success(f"Extract image success: {len(resu)}",tags="watermark_decoder:guofei_image_decoder")
    return resu

def firekeeper_image_decoder(img,attachment_data):
    if not attachment_data['len_wm']:
        bwm1 = firekeeper.watermark(4399, 2333, 36, 20, wm_shape=(64, 64))
        result,YUV = bwm1.extract_internal(img)
        logger.success(f"Extract image success: Combined {len(result)},separate {len(YUV)}",
                       tags="watermark_decoder:firekeeper_image_decoder")
        return result,YUV
    else:
        bwm1 = firekeeper.watermark(attachment_data['seed1'],attachment_data['seed2'],attachment_data['mod1'],attachment_data['mod2'],attachment_data['len_wm'])
        result, YUV = bwm1.extract_internal(img)
        logger.success(f"Extract image success: Combined {len(result)},separate {len(YUV)}, with empty attachment_data",
                       tags="watermark_decoder:firekeeper_image_decoder")
        return result, YUV


def freqm_text_decoder(img,attachment_data):
    decoder = WatermarkDecoder('bytes', attachment_data['length'])
    watermark = decoder.decode(img, 'dwtDct')
    if b'\x00' in watermark:
        is_valid = False
        logger.debug(f"Extract text failed: Invalid watermark",tags="watermark_decoder:freqm_text_decoder")
    else:
        is_valid = True
        logger.success(f"Extract text success: {watermark.decode('utf-8')}",tags="watermark_decoder:freqm_text_decoder")
    return watermark.decode('utf-8'),is_valid

def rivagan_text_decoder(img,attachment_data):
    decoder = WatermarkDecoder('bytes', attachment_data['length'])
    decoder.loadModel()
    watermark = decoder.decode(img, 'rivaGan')
    resu = watermark.decode('utf-8')
    logger.success(f"Extract text success: {resu}",tags="watermark_decoder:rivagan_text_decoder")
    return resu





