@echo off
pip install --upgrade pip
pip install -r selfreq.txt
pip install -r requirements.txt




set /a retry_count=0
set max_retries=5
set retry_delay=2  ; �ȴ�ʱ�䣬��λΪ��

:run_command
echo ����ִ������: %retry_count% ��...
python -m nuitka --mingw64 --standalone helloworld.py < auto.txt
if errorlevel 1 (
    set /a retry_count+=1
    echo ����ִ��ʧ�ܣ����ڵȴ� %retry_delay% �������...
    timeout /t %retry_delay%
    if %retry_count% lss %max_retries% (
        goto run_command
    ) else (
        echo �ﵽ������Դ���������δ�ܳɹ�ִ�С�
        exit /b 1
    )
) else (
    echo ����ɹ�ִ�С�
    echo ����ִ�к���ָ��...
    rd /S /Q helloworld.dist
	rd /S /Q helloworld.build
    goto :eof
)

:eof