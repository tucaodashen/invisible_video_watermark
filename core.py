import os.path
import random

import blind_watermark as bw
from PIL import Image

bw.bw_notes.close()
from algorithm.firekepper.BlindWatermark import watermark as fwatermark

"""
算法1
https://github.com/guofei9987/blind_watermark
折磨了我好几天，不不建议用文字水印，读取出来的概率较低
虽然star很多但是我不理解啊，这个东西真的不好用（,甚至嵌入图片的功能完全是不能用的
"""


def encodewatermark_text(text,
                         input,
                         ):
    """
    对输入源进行隐式图片水印的加工函数
    :param text:输入水印文本
    :param input:加水印的输入图片
    :return:加密完成后的图片以及相应的解码所需数据
    """
    inputfile = "processframe/" + input
    watermark = bw.WaterMark(password_img=1, password_wm=1, processes=None)
    watermark.read_img(inputfile)
    watermark.read_wm(text, mode='str')
    watermark.embed("processedframe/" + input)
    len_wm = len(watermark.wm_bit)
    print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
    return len_wm


def decodewatermark_text(
        len_wm,
        input,
):
    """
    对输入内容进行解水印
    :param input: 输入图片
    :param len_wm: 水印长度，程序生成值
    :return: 水印文字或者图片
    """
    extract = bw.WaterMark(password_img=1, password_wm=1, processes=None)
    result = extract.extract(input, wm_shape=int(len_wm), mode="str")
    return result


def encodewatermark_image(image,
                          input,
                          seed,
                          ):
    """

    :param image:输入图片
    :param input: 输入水印图片
    :param seed: 水印参数
    :return:水印尺寸
    """
    bwm1 = fwatermark(seed[0], seed[1], seed[2])
    bwm1.read_ori_img("origin/"+str(os.path.basename(image)))
    bwm1.read_wm(input)
    bwm1.embed("processedframe/" + str(os.path.basename(image)))
    # 打开图片文件
    img = Image.open(input)

    # 获取图片分辨率
    width, height = img.size
    ren=[width,height]
    return ren


def decodewatermark_image(input,
                          shape,
                          seed,
                          ):
    bwm1 = fwatermark(int(seed[0]), int(seed[1]), int(seed[2]), wm_shape=(int(shape[0]), int(shape[1])))
    bwm1.extract("recover/"+input, "recoverresult/"+str(random.randint(1,9999999999))+"wm_"+input)
# print(decodewatermark(96,r"D:\invisible_video_watermark\result\fuckcao\3009.png"))
