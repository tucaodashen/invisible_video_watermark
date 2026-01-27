from html2image import Html2Image


hti = Html2Image(
    custom_flags=['--no-sandbox', '--force-device-scale-factor=2']
)

html_code = """
<style>
    body { 
        margin: 0; 
        background: linear-gradient(45deg, #12c2e9, #c471ed, #f64f59); 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        height: 100vh;
        color: white;
        font-family: "Microsoft YaHei", sans-serif;
    }
    .box {
        border: 2px solid white;
        padding: 40px;
        border-radius: 20px;
        font-size: 40px;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
</style>
<div class="box">清晰水印测试</div>
"""

# 2. 截图时指定 size
# 注意：如果设置了 scale-factor=2，实际生成的图片像素会是 size 的两倍
hti.screenshot(
    html_str=html_code,
    save_as='clear_result.png',
    size=(800, 600)
)