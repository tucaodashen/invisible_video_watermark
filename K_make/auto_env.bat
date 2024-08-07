@echo off
pip install --upgrade pip

pip install -r requirements.txt

pip install -r selfreq.txt




set /a retry_count=0
set max_retries=5
set retry_delay=2  ; 等待时间，单位为秒

:run_command
echo 尝试执行命令: %retry_count% 次...
python -m nuitka --mingw64 --standalone helloworld.py < auto.txt
if errorlevel 1 (
    set /a retry_count+=1
    echo 命令执行失败，正在等待 %retry_delay% 秒后重试...
    timeout /t %retry_delay%
    if %retry_count% lss %max_retries% (
        goto run_command
    ) else (
        echo 达到最大重试次数，命令未能成功执行。
        exit /b 1
    )
) else (
    echo 命令成功执行。
    echo 继续执行后续指令...
    rd /S /Q helloworld.dist
	rd /S /Q helloworld.build
    goto :eof
)

:eof