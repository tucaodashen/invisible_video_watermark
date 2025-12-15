# InvisibleVideoWatermarkNEXT
![Alt](https://repobeats.axiom.co/api/embed/30e3f4c85c3c74c1e22a1c0872a1165809c7ace8.svg "Repobeats analytics image")
[简体中文](../README.md) |
繁體中文

 ![Alt](https://moe-counter.glitch.me/get/@:tucaodashen?theme=rule34 "Repobeats analytics image")
<div align="center">


![Logo](readme/Splash.jpg)

**先進的影片隱形浮水印解決方案**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📖 專案簡介

InvisibleVideoWatermarkNEXT 是一個功能強大的視頻隱形浮水印處理工具，專注於為視頻內容提供不可見的版權保護和內容認證解決方案。該專案整合了多種先進的浮水印演算法，提供了直觀的圖形介面和高效的批次處理能力。

### 浮水印特點

- **隱形性**：浮水印在肉眼下幾乎不可察覺
- **穩健性**：可以抵抗一般程度的影片壓縮處理
- **安全性**：密碼學保護確保浮水印安全

## ✨ 功能特性

### 🔐 多樣化浮水印演算法
- **文字浮水印**：支援多種文字嵌入演算法
  - Guofei 演算法 (TEXT_GOUFEI)
  - RivaGAN 演算法 (TEXT_RIVAGAN)
  - 頻域演算法 (TEXT_FREQM)
- **圖片浮水印**：支援將圖片嵌入影片
  - FireKeeper 演算法 (IMAGE_FIREKEEPER)
  - Guofei 圖像演算法 (IMAGE_GUOFEI)

### 🎥 全格式影片支援
- **輸入格式**：MP4, AVI, MOV, MKV 等主流影片格式
- **輸出格式**：MP4, AVI 等格式，支援自訂編碼參數
- **編碼器支援**：
  - NVIDIA 硬體加速 (H.264, HEVC, AV1)
  - AMD 硬體加速 (H.264, HEVC)
  - 軟體編碼器 (x264)
  - Resolume DXV 編碼器

### ⚡ 高效能處理
- **多執行緒處理**：充分利用多核心 CPU 效能
- **GPU 加速**：支援 CUDA 和 DirectML 加速
- **批次處理**：支援多檔案平行處理
- **記憶體最佳化**：智慧記憶體管理，支援大檔案處理

### 🎨 現代化介面
- **Fluent Design**：基於 Microsoft Fluent Design 的現代化介面
- **即時預覽**：浮水印嵌入效果即時預覽
- **進度監控**：詳細的處理進度和狀態顯示
- **多語言支援**：國際化介面支援

### 🔧 進階設定
- **取樣策略**：隨機、全量、平均、心理視覺等多種取樣方式
- **位元率控制**：CBR、VBR 等多位元率控制模式
- **品質預設**：從超快到最佳品質的多檔預設
- **自訂參數**：豐富的參數調整選項

## 🚀 快速開始

### 環境需求

- **Python**：3.10 或更高版本
- **作業系統**：Windows 10/11, Linux, macOS
- **硬體**：建議使用 NVIDIA GPU（支援 CUDA）

### 安裝步驟

1. **複製專案**
```bash
git clone https://github.com/your-username/InvisibleVideoWatermarkNEXT.git
cd InvisibleVideoWatermarkNEXT
```

2. **建立虛擬環境**
```bash
uv sync
```


3. **執行應用程式** 
```bash
uv run MainEntrance.py
```

### 首次執行

應用程式啟動時會自動檢查：
- 必要的 assets 資料夾是否存在
- 連接埠 1165 和 9999 是否可用

確保滿足這些條件後，應用程式將顯示啟動畫面並進入主介面。



## 編譯並發布

### 編譯步驟

#### 使用自動指令碼（推薦）
1. **確保專案目錄結構正確**
   - 專案根目錄下包含 `MainEntrance.py`、`requirements.txt`、`pyproject.toml` 等必要檔案
   - `assets/` 資料夾包含必要的資源檔案

2. **執行編譯指令碼**
```bash
cd make
./compile.bat
```

3. **編譯完成**
   - 編譯後的可執行檔案將在 `Release/` 目錄下產生
   - 包含所有相依項目和資源檔案
#### 手動編譯
1. **同步環境**
```bash
uv sync
```

2. **編譯更新程式**   
```bash
uv run python -m nuitka --standalone --show-memory --output-filename="AobaUpdater" --main="./updater/aoba_updater.py" --windows-icon-from-ico="./make/aoba.ico" --company-name="PraySoftware" --product-name="AobaUpdater" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="SoftwareUpdater" --onefile --remove-output
```

3. **編譯日誌記錄器**
```bash
uv run python -m nuitka --standalone --show-memory --output-filename="LogServer" --main="./LogServer/main.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="NetworkLogger" --onefile --remove-output --product-name="LogServer"
```

4.**編譯主程式**
- 下載[Upx](https://github.com/upx/upx/releases)壓縮包並解壓到`make/upx/`目錄下
```bash
uv run python -m nuitka --standalone --show-memory --output-filename="IVW_Omicron" --main="./MainEntrance.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="InvisivleWatermarkMaker" --remove-output --product-name="IVWNext" --output-dir="output" --report="compile_log" --windows-icon-from-ico="./make/pw.ico" --enable-plugins="pyside6","upx" --lto=yes --upx-binary="./make/upx/upx.exe"
```
5.**準備資源檔案**
- 將`assets/`資料夾複製到`output/MainEntrance.dist/`目錄下
- 將`preset/`資料夾複製到`output/MainEntrance.dist/`目錄下
- 將`dumps/`資料夾複製到`output/MainEntrance.dist/`目錄下
- 將`logs/`資料夾複製到`output/MainEntrance.dist/`目錄下
- 將`download/`資料夾複製到`output/MainEntrance.dist/`目錄下
- 將`AobaUpdater.exe`檔案複製到`output/MainEntrance.dist/`目錄下
- 將`LogServer.exe`檔案複製到`output/MainEntrance.dist/`目錄下

6.**打包發布**
- 將`output/MainEntrance.dist/`目錄下的所有檔案壓縮為`IVWNext.zip`
- 發布`IVWNext.zip`檔案

## 📖 使用指南

### 基本操作流程

1. **新增檔案**：點擊「新增檔案」按鈕選擇要處理的視訊
2. **選擇演算法**：根據需求選擇適合的浮水印演算法
3. **設定參數**：設定浮水印內容、密碼等參數
4. **開始處理**：點擊「開始處理」按鈕開始浮水印嵌入
5. **檢視結果**：處理完成後檢視輸出檔案，包含嵌入浮水印的視訊
#### 取樣器相關
##### 取樣方式
- **隨機取樣**：隨機選擇視訊影格進行浮水印嵌入
- **全量取樣**：對所有視訊影格進行浮水印嵌入
- **平均取樣**：平均選擇視訊影格進行浮水印嵌入
- **手動取樣**：根據手動輸入的取樣表進行取樣

##### 取樣數
- 總共執行的取樣次數
#### 取樣延續
- 即在取樣器原始結果上向後延續的影格數

### 進階功能

#### 批次處理模式
- 支援多檔案同時處理
- 可為每個檔案設定不同參數
- 支援處理佇列管理

#### 預設管理
- 儲存常用參數組合為預設
- 快速套用預設到新檔案
- 預設匯入/匯出功能

## 🏗️ 技術架構

### 專案結構



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
├── LogServer.exe          # 日志服务器
├── AobaUpdater.exe          # 自动更新程序
└── MainEntrance.py       # 程序入口
```

### 核心技術

#### 浮水印演算法
- **DCT 域浮水印**：基於離散餘弦轉換的頻域嵌入
- **DWT 域浮水印**：基於小波轉換的多尺度嵌入
- **深度學習**：基於神經網路的穩健浮水印

#### 視訊處理
- **FFmpeg 整合**：高效能視訊編解碼
- **PyAV**：Python 視訊處理函式庫
- **OpenCV**：電腦視覺演算法支援

#### 介面框架
- **PySide6**：Qt6 的 Python 綁定
- **qfluentwidgets**：Fluent Design 元件庫

## 🔧 設定說明

### 系統需求

#### 最低設定
- **CPU**：四核心 3.0GHz
- **記憶體**：8GB RAM
- **儲存空間**：10GB 可用空間
- **顯示卡**：支援 OpenGL 3.3

#### 建議設定
- **CPU**：四核心 3.0GHz 或更高
- **記憶體**：16GB RAM 或更高
- **儲存空間**：SSD，15GB 可用空間
- **顯示卡**：NVIDIA GTX 1660 或更高

### 參數設定

#### 輸出參數
- **視訊編碼器**：選擇合適的編碼器
- **品質設定**：位元率、預設、調整選項
- **格式選擇**：輸出封裝格式

## 注意事項

- **多程序**：最好設定為自己 CPU 的實體核心數，超出實體核心數的程序不會帶來顯著提升。在使用 RivaGan 演算法時，不建議使用過多程序，容易造成程式當機。

- **浮水印內容**：建議浮水印內容為文字或圖片，避免使用複雜字元或特殊字型，且不要太長或太大。

- **輸出**：不要設定太低的位元率，如果您不知道自己在調整什麼，請不要更動預設參數。

- **FFmpeg**：如果自動下載的 FFmpeg 失敗，您可以自行下載並解壓縮到根目錄下，或者將 FFmpeg 和 FFprobe 路徑加入環境變數中。

## 📄 授權條款

本專案採用 MIT 授權條款 - 檢視 [LICENSE](LICENSE) 檔案了解詳情。

## 🙏 致謝

感謝以下開放原始碼專案的支援：
- [PySide6](https://doc.qt.io/qtforpython/) - Qt6 Python 綁定
- [OpenCV](https://opencv.org/) - 電腦視覺函式庫
- [FFmpeg](https://ffmpeg.org/) - 多媒體處理框架
- [qfluentwidgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) - Fluent Design 元件
- [blind_watermark](https://github.com/guofei9987/blind_watermark) - Guofei 演算法
- [BlindWatermark](https://github.com/fire-keeper/BlindWatermark) - Firekeeper 演算法
- [invisible-watermark](https://github.com/ShieldMnt/invisible-watermark) - ShieldMnt 演算法

### 特別鳴謝
- **「雨澤.」(VJ 行業從業者)** 提供了對專案的一部分資金支援和前期測試(WeChat:byx33448687)
- **"Tifeng_City"** 提供了專案的一部分測試以及 CI/CD 的支援

## 📞 聯絡我們

- **專案首頁**：[GitHub Repository](https://github.com/tucaodashen/invisible_video_watermark)
- **問題回報**：[Issues](https://github.com/tucaodashen/invisible_video_watermark/issues)
- **討論交流**：[Discussions](https://github.com/tucaodashen/invisible_video_watermark/discussions)
- **聯絡作者**：[Email](mailto:tucaodashenofficial@gmail.com)
- **專案贊助**：[愛發電](https://afdian.com/a/AnkhTheOtherSphere)
- **Discord**：[Join our server](https://discord.gg/5fwFVYSV)

## Todo:
- [ ] 完善文件
- [ ] 新增多語言
- [ ] 優化高切片長度下的處理效能
- [ ] 完善日誌系統
- [ ] 優化解碼功能的記憶體佔用
- [ ] 開發心理視覺取樣器

---

<div align="center">

**[⬆ 回到頂部](#invisiblevideowatermarknext)**

Made with ❤️ by PraySoftware
![Logo](readme/slogan.png)
</div>