from PIL import Image


def png_to_ico_single_size(png_path, ico_path, size=(32, 32)):
    """将PNG转换为指定尺寸的ICO"""
    with Image.open(png_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 调整尺寸
        img_resized = img.resize(size, Image.Resampling.LANCZOS)
        img_resized.save(ico_path, format='ICO')


# 使用示例
png_to_ico_single_size('icon.png', 'icon.ico', size=(256, 256))