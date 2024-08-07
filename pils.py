from PIL import ImageFont, Image, ImageDraw
import qrcode
import cv2
from pyzbar import pyzbar
ttf_path = 'SourceHanSansK-Bold.ttf'
text_size = 200 # text_size 是字号
font = ImageFont.truetype(ttf_path, text_size)
def makeimage(text,resolution,name):
    image = Image.new('RGB', (resolution[0], resolution[1]), (0, 0, 0))
    iwidth, iheight = image.size
    draw = ImageDraw.Draw(image)

    fwidth, fheight = font.getsize(text)  # 获取文字高宽

    fontx = (iwidth - fwidth - font.getoffset(text)[0]) / 2
    fonty = (iheight - fheight - font.getoffset(text)[1]) / 2

    draw.text((fontx, fonty), text, 'white', font)
    image.save(str(name)+'.png')  # 保存图片
def genqrcode(text,pix):

    # 设置相关参数，生成一个二维码对象（QRCode对象）
    qr_obj = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=pix,
        border=0,
    )
    # 设置二维码信息内容
    qr_obj.add_data(str(text))
    # 设置二维码图形的大小
    # 当参数fit为True时，二维码图形根据信息内容大小调节到合适尺寸，
    # 当参数fit为False时，二维码图形不会调节，如果信息内容过大将报错
    qr_obj.make(fit=True)
    # 生成二维码图像，设置二维码颜色为黑色，背景色为白色
    qr_img = qr_obj.make_image(fill_color='black', back_color='white')
    # 显示二维码
    #qr_img.show()
    # 保存二维码图片
    qr_img.save('qrcode.png')
def recognize(input):
    """
    进行二维码识别
    :param input:输入文件路径
    :return:
    """
    image = cv2.imread(input)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 创建二维码解码器
    qr_decoder = pyzbar.decode

    # 解码二维码并输出结果
    decoded_info = ''
    for barcode in qr_decoder(gray):
        decoded_info = barcode.data.decode("utf-8")
        print("解码结果:", decoded_info)
        return decoded_info

    if decoded_info == '':
        print("未检测到二维码")
        return None



if __name__ == "__main__":
    makeimage("哇哦",[1920,1080],"chuyinweilai")
    #genqrcode("我去，初音未来！")
    #recognize("test.png")
