import modules.blind_watermark_guofei as guofei
import modules.BlindWatermark_FireKeeper as firekeeper
import modules.imwatermark_ShieldMnt as SM
import cv2

from modules.imwatermark_ShieldMnt import WatermarkDecoder

"""
all the functions' input are cv2 images and output are cv2 images

"""

def goufei_text_decoder(img,attachment_data):
    bwm1 = guofei.WaterMark(password_img=attachment_data['img_password'], password_wm=attachment_data['wm_password'])
    wm_extract = bwm1.extract(embed_img=img, wm_shape=attachment_data['len_wm'], mode='str')
    return wm_extract

def guofei_image_decoder(img,attachment_data):
    bwm1 = guofei.WaterMark(password_wm=attachment_data['wm_password'], password_img=attachment_data['img_password'])
    # notice that wm_shape is necessary
    resu = bwm1.extract(embed_img=img, wm_shape=attachment_data['len_wm'])
    return resu

def firekeeper_image_decoder(img,attachment_data):
    if not attachment_data['len_wm']:
        bwm1 = firekeeper.watermark(4399, 2333, 36, 20, wm_shape=(64, 64))
        result,YUV = bwm1.extract_internal(img)
        return result,YUV
    else:
        bwm1 = firekeeper.watermark(attachment_data['seed1'],attachment_data['seed2'],attachment_data['mod1'],attachment_data['mod2'],attachment_data['len_wm'])
        result, YUV = bwm1.extract_internal(img)
        return result, YUV

def freqm_text_decoder(img,attachment_data):
    decoder = WatermarkDecoder('bytes', attachment_data['length'])
    watermark = decoder.decode(img, 'dwtDct')
    if b'\x00' in watermark:
        is_valid = False
    else:
        is_valid = True
    return watermark.decode('utf-8'),is_valid

def rivagan_text_decoder(img,attachment_data):
    decoder = WatermarkDecoder('bytes', attachment_data['length'])
    decoder.loadModel()
    watermark = decoder.decode(img, 'rivaGan')
    print(watermark.decode('utf-8'))
    return watermark.decode('utf-8')





