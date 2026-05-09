@echo OFF
:: =================================
:: 0. ����ǰ�����ɵı������
:: =================================
echo.
echo ���������ɵı�������ļ�...
rmdir hw.build /Q /S
rmdir hw.dish /Q /S
echo ������ɡ�
echo.

:: =================================
:: 1. ����ͬ���ͳ�ʼ��
:: =================================
echo ����ͬ�� uv ��������...
uv sync
echo.

:: =================================
:: 2. �˵�ѡ��
:: =================================
echo.
echo =================================
echo ��ѡ�������
echo 1. ȫ������ (LogServer + Updater + Main + �����ṹ)
echo 2. ֻ���븽����� (LogServer + Updater)
echo 3. ֻ���������ṹ (��������)
echo 4. �˳�
echo =================================
echo.

choice /c 1234 /n /m "������ѡ��1-4��:"

:: **��Ҫ�޸��������û�ѡ�񵽱���**
set CHOICE=%errorlevel%

if %CHOICE%==4 goto exit
if %CHOICE%==3 goto build_file_structure
if %CHOICE%==2 goto compile_addons
if %CHOICE%==1 goto compile_all

:: =================================
:: 3. �˳���ǩ
:: =================================
:exit
echo �˳��ű���
goto :eof

:: =================================
:: 4. ��ȫ�����롱���
:: =================================
:compile_all
echo.
echo *** ģʽ��ȫ������ (1) ***
goto compile_logserver

:: =================================
:: 5. ��ֻ���븽����������
:: =================================
:compile_addons
echo.
echo *** ģʽ��ֻ���븽����� (2) ***
goto compile_logserver

:: =================================
:: 6. ���� LogServer
:: =================================
:compile_logserver
echo.
echo --- ���ڱ��� LogServer.exe (������� 1/2) ---
uv run python -m nuitka --standalone --show-memory --output-filename="LogServer" --main="../LogServer/main.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="NetworkLogger" --onefile --remove-output --product-name="LogServer"
if errorlevel 1 (
    echo LogServer ����ʧ��!
    pause
    goto :eof
)
goto compile_updater

:: =================================
:: 7. ���� AobaUpdater
:: =================================
:compile_updater
echo.
echo --- ���ڱ��� AobaUpdater.exe (������� 2/2) ---
uv run python -m nuitka --standalone --show-memory --output-filename="AobaUpdater" --main="../updater/aoba_updater.py" --windows-icon-from-ico="aoba.ico" --company-name="PraySoftware" --product-name="AobaUpdater" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="SoftwareUpdater" --onefile --remove-output
if errorlevel 1 (
    echo AobaUpdater ����ʧ��!
    pause
    goto :eof
)

:: **��Ҫ�޸���ʹ�ñ���ı��������ж�**
if %CHOICE%==2 (
    echo.
    echo �������������ɡ�
    goto end
)

:: ���򣬼������������� (ֻ��ѡ�� 1 ʱִ��)
goto compile_main

:: =================================
:: 8. ����������
:: =================================
:compile_main
echo.
echo --- ���ڱ��� ������ IVW_Omicron.exe ---
uv run python -m nuitka --standalone --show-memory --output-filename="IVW_Omicron" --main="../MainEntrance.py" --company-name="PraySoftware" --file-version="0.0.0.1" --product-version="0.0.0.1" --file-description="InvisivleWatermarkMaker" --remove-output --product-name="IVWNext" --output-dir="output" --report="compile_log" --windows-icon-from-ico="pw.ico" --enable-plugins=pyside6 --lto=yes
if errorlevel 1 (
    echo ���������ʧ��!
    pause
    goto :eof
)
goto build_file_structure

:: =================================
:: 9. ���������ļ��ṹ
:: =================================
:build_file_structure
echo.
echo --- ���ڹ��������ļ��ṹ ---

:: ����Ŀ¼
mkdir Release 2>nul
mkdir Release\logs 2>nul
mkdir Release\dumps 2>nul
mkdir Release\download 2>nul
mkdir Release\preset 2>nul
echo Ŀ���ļ��д�����ɡ�

:: �����ļ�/��Դ
echo ���ڸ�����Դ�Ϳ�ִ���ļ�...
robocopy output/MainEntrance.dist Release /E /NFL /NDL /NJH /NJS
robocopy ../assets Release/assets /E /NFL /NDL /NJH /NJS
copy LogServer.exe Release\LogServer.exe /Y
copy AobaUpdater.exe Release\AobaUpdater.exe /Y

goto end

:: =================================
:: 10. ��������ͣ
:: =================================
:end
echo.
echo =================================
echo ������ɣ����� Release �ļ��С�
echo =================================
pause