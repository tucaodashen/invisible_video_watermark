# InvisibleVideoWatermarkNEXT

[简体中文](README.md) | [繁體中文](readme/README_TW.md) | **English** | [日本語](README.ja.md)

![Logo](readme/Splash_Nano.png)

A GUI-based invisible video watermarking application for content protection, attribution, and watermark extraction. Built with Python, PySide6, FFmpeg, and multiple watermark algorithms.

## Features

- Text watermarking: Guofei, RivaGAN, and frequency-domain approaches.
- Image watermarking: FireKeeper and Guofei implementations.
- Common input containers including MP4, AVI, MOV, and MKV; configurable output encoding.
- Support for software encoding and certain NVIDIA/AMD acceleration paths, depending on hardware and available codecs.
- Batch processing, configurable frame sampling, presets, and progress monitoring.
- Desktop interface built on PySide6 and Fluent-style components.

Watermark robustness varies with compression, codec, video content, and settings; invisible watermarks cannot be guaranteed to survive every transformation.

## Requirements

Python 3.10+, [uv](https://docs.astral.sh/uv/), and a supported FFmpeg installation. Some GPU features have additional hardware, driver, or platform requirements.

## Run from source

```bash
git clone https://github.com/tucaodashen/invisible_video_watermark.git
cd invisible_video_watermark
uv sync
uv run MainEntrance.py
```

At startup, the application checks for assets and availability of ports 1165 and 9999. If automatic FFmpeg installation fails, supply FFmpeg/FFprobe yourself or add them to PATH.

## Basic workflow

1. Add one or more videos.
2. Choose a text or image watermark algorithm.
3. Configure watermark data, sampling, output encoding, and other relevant parameters.
4. Start processing and inspect the generated output.
5. Use the extraction workflow to test the watermark against the intended distribution pipeline.

Frame sampling options include random, full, average, and manually specified modes. Avoid unnecessarily low output bitrate, and do not run multiple application instances simultaneously because of resource conflicts.

## Windows packaging

The project includes a Windows compilation script in `make/compile.bat` and documented Nuitka-based packaging steps in the [Chinese README](README.md#编译并发布). Some build steps require Windows tools, UPX, and bundled runtime assets. Check the project configuration before distributing builds.

## Development status

The original roadmap includes documentation improvements, additional UI localization, performance and logging improvements, memory optimizations, and perceptual sampling. These are planned items rather than guaranteed completed features.

## License and acknowledgements

Licensed under [MIT](LICENSE). The project uses PySide6, FFmpeg, OpenCV, qfluentwidgets, and several external watermark implementations; consult their individual licenses.

[Issues](https://github.com/tucaodashen/invisible_video_watermark/issues) · [Email](mailto:tucaodashenofficial@gmail.com)

Made by PraySoftware.
