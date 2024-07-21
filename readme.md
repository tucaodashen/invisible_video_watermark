![Alt](https://repobeats.axiom.co/api/embed/30e3f4c85c3c74c1e22a1c0872a1165809c7ace8.svg "Repobeats analytics image")


# **基于python的视频盲水印制作工具**

 ### Python Based video blind water mark tool.
 
 ![Alt](https://moe-counter.glitch.me/get/@:tucaodashen?theme=rule34 "Repobeats analytics image")
 
 ![Alt](https://github.com/tucaodashen/invisible_video_watermark/blob/main/readme/splash.png?raw=true "Repobeats analytics image")

## 简介

此软件使用pyside6并用~~Natsuki~~Nuitka编译。使用ffmpeg进行视频合成。

算法部分使用了fire_kepper的图片盲水印算法进行图片操作，文字盲水印使用了guofei9987的算法。各位可自行搜索。

[B站视频演示](https://www.bilibili.com/video/BV1Rp4y1P71r/?spm_id_from=top_right_bar_window_dynamic.content.click&vd_source=e1f1e5e71aad5101946baba5c0d06773)

逻辑为对视频进行随机抽帧进行水印处理，达到隐蔽并不易去除的目的。

最后为用户输出一个json文件，可用于自动化恢复水印。用户也可以手动截图输入来进行解码。

致力于帮助广大创作者抵抗盗版狗！
## 环境配置

运行该软件需要python3.10的环境
Windows&linux

```
pip install -r requirement.txt
```

你也可以使用conda进行安装
除此以外，你需要在ffmpeg目下放置ffmpeg的发布版
目录结构如下

```
-algorithm #算法目录
-gui #gui文件
-guiproject #qt designer文件
-ffmpeg #ffmpeg根目录
|-bin
|-doc
|-presest
|-LICENCE
|-README.txt
```

如果你直接从GitHub上下载，默认是带有ffmpeg的
## 注意事项
如果软件报错，可以注意观察黑色cmd窗口在哪一步报错。

报错后可以先重试一下，不能解决再提issue，因为确实有一定概率会莫名其妙报错。

视频路径和视频名不要太复杂，尽量只包含数字与英文字母，图片要求同样。

软件中采样帧延续意为再采样帧之后延续几帧。

软件暂时没有防呆保护，所以先检查你的设置有没有错再开始。

如果水印图过大会报错，合适的水印图大小各位可以自己试一试试出来，因为原作者好像没有给判断方法。




ToDo：
改进软件UI
修复无声音视频无法处理的错误
创建Action自动编译
添加错误报告功能
