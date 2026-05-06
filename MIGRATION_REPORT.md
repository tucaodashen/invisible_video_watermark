# FFmpeg → PyAV 渲染 API 迁移报告

## 项目概述

- **项目名称**: InvisibleVideoWatermarkNEXT
- **项目路径**: `/Users/ankh/project/python/IVW_PYAV`
- **迁移目标**: 将视频渲染管线从 FFmpeg 命令行/ffmpeg-python 迁移到 PyAV
- **测试框架**: pytest
- **测试结果**: **52/52 passed, 2 skipped (DXV macOS)** ✅

---

## 迁移架构对比

```
Before (FFmpeg 命令行走)              After (PyAV libav* 库调用)
┌─────────────────────┐              ┌─────────────────────┐
│  subprocess.Popen() │              │     av.open('w')    │
│  subprocess.run()   │  ────────►   │  VideoStream.encode │
│  ffmpeg-python 库   │              │  container.mux()    │
│  ffprobe 子进程     │              │  stream.metadata    │
└─────────────────────┘              └─────────────────────┘
```

---

## 修改文件清单

### 核心模块 (5 个文件)

| 文件 | 改动说明 |
|------|----------|
| `modules/GenerateVideo.py` | 重写：编码、合并、探测全部改为 PyAV |
| `modules/VideoProcessor.py` | 重写：帧提取、音频混流改为 PyAV |
| `modules/ProcessUnit.py` | 重构：音频函数提取到 AudioProcessor |
| `modules/AudioProcessor.py` | **新增**：独立的音频提取/探测模块 |
| `modules/Slice.py` | 验证逻辑从 ffprobe 改为 PyAV |

### GUI 模块 (2 个文件)

| 文件 | 改动说明 |
|------|----------|
| `GUI/PrepareRequirements.py` | 新增 `check_pyav_installed()` 主检函数 |
| `GUI/Startup_Splash.py` | 启动检查文案更新 |

### 配置

| 文件 | 改动说明 |
|------|----------|
| `pyproject.toml` | 移除 `ffmpeg-python>=0.2.0` 依赖 |

### 测试

| 文件 | 说明 |
|------|------|
| `tests/conftest.py` | **新增**：测试夹具，用 PyAV 生成测试媒体 |
| `tests/test_video_processing.py` | **新增**：32 条单元测试 |
| `tests/test_concurrent.py` | **新增**：14 条并发/DXV/seek 测试 |
| `tests/test_gui.py` | **新增**：8 条 GUI 依赖检查测试 |
| `tests/__init__.py` | **新增**：包标记 |

---

## 逐函数迁移详情

### 1. `modules/GenerateVideo.py` — 核心编码管线

#### `execute_command(args)` — 已移除
原实现：`subprocess.Popen(ffmpeg.exe + args)`
新实现：不需要，PyAV 无子进程

#### `merge_sequences(...)` — 图片序列编码为视频
```python
# Before: subprocess.Popen(["ffmpeg.exe", "-r", fps, "-i", pattern, "-c:v", encoder, ...])
# After:  av.open('w') + add_stream(codec) + encode(frame)
```
- 编码器映射表 `_ENCODER_MAP`: NVIDIA_H264→h264_nvenc, X264→libx264 等
- 比特率控制: `_apply_encoder_options()` 设置 CBR/VBR/CQP
- Preset/Tune 映射: NVIDIA p1-p7, AMD quality/speed, x264 ultrafast-placebo
- 图片输入: `_resolve_image_sequence()` 从 printf 模式自动解析文件列表

#### `merge_video_sequnece(...)` — 多视频拼接
```python
# Before: subprocess + ffmpeg concat demuxer + stream copy
# After:  av.open() decode + re-encode → stream copy PTS 兼容性问题改用重编码
```

#### `get_video_parameters_simple(...)` — 视频元数据
```python
# Before: subprocess.run(["ffprobe", "-print_format", "json", ...])
# After:  av.open() → stream.width, stream.average_rate, stream.duration
```

#### `get_audio_parameters_simple(...)` — 音频元数据
```python
# Before: subprocess.run(["ffprobe", ...])
# After:  av.open() → stream.codec_context.sample_rate, channels
```

---

### 2. `modules/VideoProcessor.py` — 帧处理

#### `extract_frames(...)` — 按帧范围提取帧为图片
```python
# Before: ffprobe 获取元数据 + ffmpeg pipe (rawvideo bgr24) 解码
# After:  av.open() → container.decode(stream) → frame.to_ndarray('bgr24')
```
- 帧计数: 从 0 开始顺序解码，保证帧号精确对应
- 输出格式: PNG 文件，文件名 `frame_{frame_idx:06d}.png`

#### `add_audio_to_video(...)` — 为视频添加音频轨
```python
# Before: ffmpeg.input().output().run() (ffmpeg-python 库)
# After:  av.open 两路输入 → 分别 decode → 重编码到统一容器
```

---

### 3. `modules/ProcessUnit.py` — 处理单元

#### `extract_audio_to_flac(...)` — 音频提取为 FLAC
```python
# Before: ffmpeg.probe() + subprocess.run(["ffmpeg", "-acodec", "flac", ...])
# After:  av.open() → decode audio stream → add_stream('flac') → encode
```
已提取到独立模块 `modules/AudioProcessor.py` 避免导入链问题。

#### `get_audio_tracks_info(...)` — 音频轨数量
```python
# Before: ffmpeg.probe(video_path)
# After:  av.open() → len([s for s in container.streams if s.type == 'audio'])
```
已提取到 `modules/AudioProcessor.py`。

---

### 4. `modules/Slice.py` — 视频切片处理

#### `_validate_output(...)` — 输出验证
```python
# Before: subprocess.run(["ffprobe", "-v", "error", output])
# After:  try: av.open(output).close() → True; except: False
```
新增 `_validate_output()` 方法替代 `execute_command(["ffprobe", ...])`。

---

### 5. `modules/AudioProcessor.py` — 新增模块
从 `ProcessUnit.py` 中提取的独立模块，仅依赖 `av` + `BasicSystem.log_client`，无 PySide6/Qt 等重依赖，便于单元测试。

---

## PyAV 版本兼容性处理

迁移过程中遇到的 PyAV 17.x API 变化及解决方案：

| 问题 | 原因 | 解决 |
|------|------|------|
| `stream.width = None` TypeError | PyAV 17 width 必须为 int | 移除无意义的 None 赋值 |
| `astream.channels = 1` AttributeError | AudioCodecContext.channels 只读 | 改用 `options['channels'] = '1'` |
| `add_stream(template=...)` TypeError | PyAV 17 移除了 template 参数 | 改用 `add_stream(codec, rate=fps)` + 手动设置参数 |
| `fc=False` / `psy=False` 被当作有效值 | `is not None` 对 False 也为 True | 改为 truthy 判断 `if fc:` / `if psy:` |
| stream copy PTS 重基址失败 | 跨容器 copy 时 time_base 不兼容 | 视频拼接/音频混流改用 decode→re-encode |
| `rate=float(...)` 传入 Fraction | PyAV 17 `add_stream(rate)` 需 Fraction | 直接传 `stream.average_rate` (Fraction) |
| 音频容器 time_base 为 0/0 | 未初始化音频流参数 | 先设置 `codec_context.sample_rate`，使用 options 字典 |

---

## 测试报告

### 测试统计

| 类别 | 数量 | 状态 |
|------|------|------|
| 视频编码测试 | 7 | ✅ |
| 视频参数探测 | 4 | ✅ |
| 帧提取测试 | 5 | ✅ |
| 采样算法测试 | 4 | ✅ |
| 工具函数测试 | 3 | ✅ |
| 音频处理测试 | 4 | ✅ |
| 编码器映射测试 | 1 | ✅ |
| 集成测试 | 1 | ✅ |
| 音频混流测试 | 1 | ✅ |
| 视频拼接测试 | 1 | ✅ |
| 无效输入测试 | 2 | ✅ |
| 多进程并发测试 | 6 | ✅ |
| 编码器可用性 | 2 | ✅ |
| DXV 编码测试 | 2 | ⏭️ (macOS 不可用) |
| Seek 性能测试 | 3 | ✅ |
| setup_sequence 测试 | 1 | ✅ |
| GUI 依赖检查 | 8 | ✅ |
| **总计** | **54** | **52✅ 2⏭️** |

### 运行命令

```bash
# 安装依赖
uv pip install av opencv-python numpy pytest loguru

# 运行测试
python -m pytest tests/ -v --tb=short

# 结果: 52 passed, 2 skipped in 3.27s
```

### 测试覆盖的关键场景

- **多编码器支持**: 验证 Encoder.X264 到 `libx264` 的映射
- **比特率控制**: CBR、VBR、CQP 三种模式
- **帧范围提取**: 0-9，10-19 (中段)，无效范围
- **回调函数**: 验证进度回调正常工作
- **异常处理**: 无效视频路径、无效编码器
- **集成测试**: 完整管线 提取→编码→合并
- **多进程并发**: ProcessPoolExecutor 下帧提取/编码/完整管线并发安全
- **编码器可用性检测**: libx264, DXV 实际 `ctx.open()` 验证
- **GUI 依赖检查**: PyAV 安装检测、兼容接口、FakeSignal
- **Seek 性能**: 跳过帧解码 vs 从头解码一致性对比

---

## 依赖变化

```diff
# pyproject.toml
  dependencies = [
-     "ffmpeg-python>=0.2.0",
      "av>=16.0.1",         # PyAV (已有)
      ...
  ]
```

---

## 未修改的文件

| 文件 | 保留原因 |
|------|----------|
| `GUI/main.py` → 变量名 `FFmpegEncoder` 等 | 内部变量命名，不影响功能，避免大范围重构 |
| `GUI/main.py` → `kill_process_by_name("ffmpeg")` | 退出清理，无害操作 |
| `modules/VideoProcessor.py` → `ffmpeg_extract_frames()` | 实际使用 OpenCV (非 ffmpeg)，保留为回退方案 |
| `modules/pltform.py` → `subprocess` | 用于 GPU 设备枚举，与视频编码无关 |

### GUI 迁移说明

| 文件 | 改动 |
|------|------|
| `GUI/PrepareRequirements.py` | FFmpeg 下载类 `FFmpegPrepare` 改为空操作 + FakeSignal（已弃用），保留接口兼容 |
| `GUI/Startup_Splash.py` | PyAV 缺失时提示 `pip install av` 安装命令后退出，不再触发无效的 FFmpeg 下载；移除 `FFmpegDownloadPage` 窗口类 |
| `GUI/main.py` | 退出时的 ffmpeg 清理注释更新 |

**关键说明**: GUI 中的编码器选择器（NVIDIA NVENC / AMD AMF / X264 / DXV）**完全保留**。这些编码器依赖于系统安装的 FFmpeg libavcodec 库而非 ffmpeg CLI。PyAV 通过 libavcodec 的 `avcodec_open2()` 调用同样的编码器，硬件加速能力由底层库编译选项决定（与原来的行为一致）。

---

## 文件大小变化

```
modules/GenerateVideo.py:   458 → 430 行 (-6%)   (移除 subprocess，增加 DXV/seek)
modules/VideoProcessor.py:  416 → 290 行 (-30%)  (简化帧提取+seek 优化)
modules/ProcessUnit.py:     521 → 394 行 (-24%)  (函数提取到 AudioProcessor)
modules/AudioProcessor.py:    0 →  92 行 (新增)  (独立音频模块)
modules/Slice.py:            367 → 281 行 (-23%)  (移除 execute_command，递归改循环)
GUI/PrepareRequirements.py: 121 →  68 行 (-44%)  (移除 FFmpeg 下载)
GUI/Startup_Splash.py:      243 → 155 行 (-36%)  (移除 FFmpeg 下载页面)
tests/conftest.py:             0 → 185 行 (新增)  (测试夹具)
tests/test_video_processing.py:    0 → 358 行 (新增)  (32 条测试)
tests/test_concurrent.py:          0 → 340 行 (新增)  (14 条测试)
tests/test_gui.py:                 0 →  72 行 (新增)  (8 条测试)
```
