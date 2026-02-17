import modules.blind_watermark_guofei as guofei
import modules.BlindWatermark_FireKeeper as firekeeper
import modules.imwatermark_ShieldMnt as SM
from BasicSystem.log_client import get_logger,setup_logger
setup_logger(default_tags="watermark_stamper", enable_udp=True, enable_console=True)
logger = get_logger()

"""
all the functions' input are cv2 images and output are cv2 images
    
"""

def guofei_text(cv2_image, wm_text,attachment_data=None):
    print(f"wm_text: {wm_text}")
    if attachment_data is not None:
        bwm1 = guofei.WaterMark(password_img=attachment_data['img_password'], password_wm=attachment_data['wm_password'])
        bwm1.read_img(img=cv2_image)
        bwm1.read_wm(wm_text, mode='str')
        resu = bwm1.embed()
        len_wm = len(bwm1.wm_bit)
        return_attachment_data = {
            'len_wm': len_wm,
            'img_password': bwm1.password_img,
            'wm_password': bwm1.password_wm,
        }
        logger.success(f"Embed text success: {wm_text}",tags="watermark_stamper:guofei_text")
        return resu, return_attachment_data
    bwm1 = guofei.WaterMark(password_img=57508979, password_wm=57508979)
    bwm1.read_img(img=cv2_image)
    bwm1.read_wm(wm_text, mode='str')
    resu = bwm1.embed()
    len_wm = len(bwm1.wm_bit)
    return_attachment_data = {
        'len_wm': len_wm,
        'img_password': bwm1.password_img,
        'wm_password': bwm1.password_wm,
    }
    return resu, return_attachment_data


def guofei_image(cv2_image, cv2_watermark,attachment_data=None):
    if attachment_data is not None:
        bwm1 = guofei.WaterMark(password_img=attachment_data['img_password'], password_wm=attachment_data['wm_password'])
        bwm1.read_img(img=cv2_image)
        bwm1.read_wm(img=cv2_watermark, mode='img')
        resu = bwm1.embed()
        return_attachment_data = {
            'len_wm': cv2_watermark.shape[:2],
            'img_password': bwm1.password_img,
            'wm_password': bwm1.password_wm,
        }
        logger.success(f"Embed image success: {cv2_watermark.shape[:2]}",tags="watermark_stamper:guofei_image")
        return resu, return_attachment_data

    bwm1 = guofei.WaterMark(password_wm=1, password_img=1)
    # read original image
    bwm1.read_img(img=cv2_image)
    # read watermark
    bwm1.read_wm(img=cv2_watermark, mode='img')
    resu = bwm1.embed()
    return_attachment_data = {
        'len_wm': cv2_watermark.shape[:2],
        'img_password': bwm1.password_img,
        'wm_password': bwm1.password_wm,
    }
    return resu, return_attachment_data

def firekeeper_image(cv2_image, cv2_watermark,attachment_data=None):
    if attachment_data is not None:
        if int(attachment_data['mod1']) < int(attachment_data['mod2']):
            logger.error(f"mod1({attachment_data['mod1']}) should be greater than mod2({attachment_data['mod2']})",tags="watermark_stamper:firekeeper_image")
            raise ValueError("mod1 should be greater than mod2")
        bwm1 = firekeeper.watermark(attachment_data['seed1'], attachment_data['seed2'], attachment_data['mod1'], attachment_data['mod2'])
        bwm1.read_ori_img_internal(cv2_image)
        bwm1.read_wm_internal(cv2_watermark)
        result = bwm1.embed()
        return_attachment_data = {
            'len_wm': cv2_watermark.shape[:2],
            'seed1': bwm1.random_seed_wm,
            'seed2': bwm1.random_seed_dct,
            'mod1': bwm1.mod,
            'mod2': bwm1.mod2
        }
        logger.success(f"Embed image success: {cv2_watermark.shape[:2]}",tags="watermark_stamper:firekeeper_image")
        return result, return_attachment_data
    else:
        bwm1 = firekeeper.watermark(4399, 2333, 36, 20)
        bwm1.read_ori_img_internal(cv2_image)
        bwm1.read_wm_internal(cv2_watermark)
        result = bwm1.embed()
        result = bwm1.embed()
        return_attachment_data = {
            'len_wm': cv2_watermark.shape[:2],
            'seed1': bwm1.random_seed_wm,
            'seed2': bwm1.random_seed_dct,
            'mod1': bwm1.mod,
            'mod2': bwm1.mod2
        }
        return result, return_attachment_data

def freqmethod_text(cv2_image,wm_text,attachment_data=None):
    if attachment_data is not None:
        encoder = SM.WatermarkEncoder()
        encoder.set_watermark(attachment_data['wmType'], wm_text.encode('utf-8'))
        if attachment_data['method'] == 'rivaGan':
            encoder.loadModel()
            logger.success(f"Load model success: {attachment_data['method']}",tags="watermark_stamper:freqmethod_text")
        bgr_encoded = encoder.encode(cv2_image, attachment_data['method'])
        length = int(encoder.get_length())
        return_attachment_data = {
            'wmType': attachment_data['wmType'],
            'method': attachment_data['method'],
            'length': length,
        }
        logger.success(f"Embed text success: {wm_text}",tags="watermark_stamper:freqmethod_text")
        return bgr_encoded, return_attachment_data
    else:
        encoder = SM.WatermarkEncoder()
        encoder.set_watermark('bits', wm_text.encode('utf-8'))
        bgr_encoded = encoder.encode(cv2_image, 'dwtDct')
        length = int(encoder.get_length())
        return_attachment_data = {
            'wmType': 'bits',
            'method': 'dwtDct',
            'length': length,
        }
        return bgr_encoded, return_attachment_data


