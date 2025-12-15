# InvisibleVideoWatermarkNEXT

<div align="center">

![Logo](readme/Splash.jpg)

**先进的视频隐形水印解决方案**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [技术架构](#技术架构) • [贡献指南](#贡献指南)

</div>

## 📖 项目简介

InvisibleVideoWatermarkNEXT 是一个功能强大的视频隐形水印处理工具，专注于为视频内容提供不可见的版权保护和内容认证解决方案。该项目集成了多种先进的水印算法，提供了直观的图形界面和高效的批处理能力。

### 水印特点

- **隐形性**：水印在肉眼下基本不可察觉
- **鲁棒性**：可以抵抗一般程度的视频压缩处理
- **安全性**：密码学保护确保水印安全

## ✨ 功能特性

### 🔐 多样化水印算法
- **文本水印**：支持多种文本嵌入算法
  - Guofei 算法 (`TEXT_GOUFEI`)
  - RivaGAN 算法 (`TEXT_RIVAGAN`) 
  - 频域算法 (`TEXT_FREQM`)
- **图像水印**：支持将图片嵌入视频
  - FireKeeper 算法 (`IMAGE_FIREKEEPER`)
  - Guofei 图像算法 (`IMAGE_GUOFEI`)

### 🎥 全格式视频支持
- **输入格式**：MP4, AVI, MOV, MKV 等主流视频格式
- **输出格式**：MP4, AVI 等格式，支持自定义编码参数
- **编码器支持**：
  - NVIDIA 硬件加速 (H.264, HEVC, AV1)
  - AMD 硬件加速 (H.264, HEVC)
  - 软件编码器 (x264)
  - Resolume DXV 编码器

### ⚡ 高性能处理
- **多线程处理**：充分利用多核 CPU 性能
- **GPU 加速**：支持 CUDA 和 DirectML 加速
- **批处理**：支持多文件并行处理
- **内存优化**：智能内存管理，支持大文件处理

### 🎨 现代化界面
- **Fluent Design**：基于 Microsoft Fluent Design 的现代化界面
- **实时预览**：水印嵌入效果实时预览
- **进度监控**：详细的处理进度和状态显示
- **多语言支持**：国际化界面支持

### 🔧 高级配置
- **采样策略**：随机、全量、平均、心理视觉等多种采样方式
- **码率控制**：CBR、VBR 等多种码率控制模式
- **质量预设**：从超快到最佳质量的多档预设
- **自定义参数**：丰富的参数调节选项

## 🚀 快速开始

### 环境要求

- **Python**：3.10 或更高版本
- **操作系统**：Windows 10/11, Linux, macOS
- **硬件**：推荐使用 NVIDIA GPU（支持 CUDA）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/InvisibleVideoWatermarkNEXT.git
cd InvisibleVideoWatermarkNEXT
```

2. **创建虚拟环境**
```bash
uv sync
```


3**运行应用**
```bash
uv run MainEntrance.py
```

### 首次运行

应用启动时会自动检查：
- 必需的 assets 文件夹是否存在
- 端口 1165 和 9999 是否可用

确保满足这些条件后，应用将显示启动画面并进入主界面。

## 📖 使用指南

### 基本操作流程

1. **添加文件**：点击"添加文件"按钮选择要处理的视频
2. **选择算法**：根据需求选择合适的水印算法
3. **设置参数**：配置水印内容、密码等参数
4. **开始处理**：点击"开始处理"按钮
5. **查看结果**：处理完成后查看输出文件

### 高级功能

#### 批处理模式
- 支持多文件同时处理
- 可为每个文件设置不同参数
- 支持处理队列管理

#### 预设管理
- 保存常用参数组合为预设
- 快速应用预设到新文件
- 预设导入/导出功能

## 🏗️ 技术架构

### 项目结构

```
InvisibleVideoWatermarkNEXT/
├── GUI/                    # 图形界面模块
│   ├── main.py            # 主界面逻辑
│   ├── MainWindows.py     # 主窗口界面
│   └── Setting.py         # 设置界面
├── modules/               # 核心处理模块
│   ├── watermarkstamper.py    # 水印嵌入
│   ├── watermarkdecoder.py    # 水印提取
│   ├── VideoProcessor.py      # 视频处理
│   └── ProcessUnit.py         # 处理单元
├── BasicSystem/           # 基础系统模块
│   ├── const.py          # 常量定义
│   └── log_client.py     # 日志系统
├── assets/               # 资源文件
├── preset/               # 预设配置
└── MainEntrance.py       # 程序入口
```

### 核心技术

#### 水印算法
- **DCT 域水印**：基于离散余弦变换的频域嵌入
- **DWT 域水印**：基于小波变换的多尺度嵌入
- **深度学习**：基于神经网络的鲁棒水印

#### 视频处理
- **FFmpeg 集成**：高性能视频编解码
- **PyAV**：Python 视频处理库
- **OpenCV**：计算机视觉算法支持

#### 界面框架
- **PySide6**：Qt6 的 Python 绑定
- **qfluentwidgets**：Fluent Design 组件库

## 🔧 配置说明

### 系统要求

#### 最低配置
- **CPU**：四核 3.0GHz
- **内存**：8GB RAM
- **存储**：10GB 可用空间
- **显卡**：支持 OpenGL 3.3

#### 推荐配置
- **CPU**：四核 3.0GHz 或更高
- **内存**：16GB RAM 或更高
- **存储**：SSD，15GB 可用空间
- **显卡**：NVIDIA GTX 1660 或更高

### 参数配置

#### 输出参数
- **视频编码器**：选择合适的编码器
- **质量设置**：码率、预设、调优选项
- **格式选择**：输出容器格式

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目的支持：
- [PySide6](https://doc.qt.io/qtforpython/) - Qt6 Python 绑定
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [FFmpeg](https://ffmpeg.org/) - 多媒体处理框架
- [qfluentwidgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) - Fluent Design 组件

## 📞 联系我们

- **项目主页**：[GitHub Repository](https://github.com/your-username/InvisibleVideoWatermarkNEXT)
- **问题反馈**：[Issues](https://github.com/your-username/InvisibleVideoWatermarkNEXT/issues)
- **讨论交流**：[Discussions](https://github.com/your-username/InvisibleVideoWatermarkNEXT/discussions)

---

<div align="center">

**[⬆ 回到顶部](#invisiblevideowatermarknext)**

Made with ❤️ by PraySoftware
![Logo](readme/slogan.png)
</div>