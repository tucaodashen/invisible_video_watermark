@echo OFF
:: =================================
:: 0. 启动前清理旧的编译残留
:: =================================
echo.
echo 正在清理旧的编译残留文件...
rmdir hw.build /Q /S
rmdir hw.dish /Q /S
echo 清理完成。
echo.

:: =================================
:: 1. 环境同步和初始化
:: =================================
echo 正在同步 uv 环境依赖...
uv sync
echo.

:: =================================
:: 2. 菜单选择
:: =================================
echo.
echo =================================
echo 请选择操作：
echo 1. 全部编译 (LogServer + Updater + Main + 构建结构)
echo 2. 只编译附加组件 (LogServer + Updater)
echo 3. 只构建发布结构 (跳过编译)
echo 4. 退出
echo =================================
echo.

choice /c 1234 /n /m "请输入选择（1-4）:"

:: **重要修复：保存用户选择到变量**
set CHOICE=%errorlevel%

if %CHOICE%==4 goto exit
if %CHOICE%==3 goto build_file_structure
if %CHOICE%==2 goto compile_addons
if %CHOICE%==1 goto compile_all

:: =================================
:: 3. 退出标签
:: =================================
:exit
echo 退出脚本。
goto :eof

:: =================================
:: 4. “全部编译”入口
:: =================================
:compile_all
echo.
echo *** 模式：全部编译 (1) ***
goto compile_logserver

:: =================================
:: 5. “只编译附加组件”入口
:: =================================
:compile_addons
echo.
echo *** 模式：只编译附加组件 (2) ***
goto compile_logserver

:: =================================
:: 6. 编译 LogServer
:: =================================
:compile_logserver
echo.
echo --- 正在编译 LogServer.exe (附加组件 1/2) ---
uv run python -m nuitka --standalone --show-memory --output-filename="LogServer" --main="../LogServer/main.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="NetworkLogger" --onefile --remove-output --product-name="LogServer"
if errorlevel 1 (
    echo LogServer 编译失败!
    pause
    goto :eof
)
goto compile_updater

:: =================================
:: 7. 编译 AobaUpdater
:: =================================
:compile_updater
echo.
echo --- 正在编译 AobaUpdater.exe (附加组件 2/2) ---
uv run python -m nuitka --standalone --show-memory --output-filename="AobaUpdater" --main="../updater/aoba_updater.py" --windows-icon-from-ico="aoba.ico" --company-name="PraySoftware" --product-name="AobaUpdater" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="SoftwareUpdater" --onefile --remove-output
if errorlevel 1 (
    echo AobaUpdater 编译失败!
    pause
    goto :eof
)

:: **重要修复：使用保存的变量进行判断**
if %CHOICE%==2 (
    echo.
    echo 附加组件编译完成。
    goto end
)

:: 否则，继续编译主程序 (只在选择 1 时执行)
goto compile_main

:: =================================
:: 8. 编译主程序
:: =================================
:compile_main
echo.
echo --- 正在编译 主程序 IVW_Omicron.exe ---
uv run python -m nuitka --standalone --show-memory --output-filename="IVW_Omicron" --main="../MainEntrance.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="InvisivleWatermarkMaker" --remove-output --product-name="IVWNext" --output-dir="output" --report="compile_log" --windows-icon-from-ico="pw.ico" --enable-plugins="pyside6","upx" --lto=yes --upx-binary="upx/upx.exe"
if errorlevel 1 (
    echo 主程序编译失败!
    pause
    goto :eof
)
goto build_file_structure

:: =================================
:: 9. 构建发布文件结构
:: =================================
:build_file_structure
echo.
echo --- 正在构建发布文件结构 ---

:: 创建目录
mkdir Release 2>nul
mkdir Release\logs 2>nul
mkdir Release\dumps 2>nul
mkdir Release\download 2>nul
mkdir Release\preset 2>nul
echo 目标文件夹创建完成。

:: 复制文件/资源
echo 正在复制资源和可执行文件...
robocopy output/MainEntrance.dist Release /E /NFL /NDL /NJH /NJS
robocopy ../assets Release/assets /E /NFL /NDL /NJH /NJS
copy LogServer.exe Release\LogServer.exe /Y
copy AobaUpdater.exe Release\AobaUpdater.exe /Y

goto end

:: =================================
:: 10. 结束和暂停
:: =================================
:end
echo.
echo =================================
echo 操作完成！请检查 Release 文件夹。
echo =================================
pause