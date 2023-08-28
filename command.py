import subprocess
import psutil
import signal
import cv2
from subprocess import check_output
import os

def __external_cmd(cmd, code="utf8"): #执行命令行的一个函数，用的谁的轮子记不清了（
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            print(line.decode(code, 'ignore'))
def extractall(video,filepartern=".png"): #提取所有视频帧
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    result=r"ffmpeg\bin\ffmpeg.exe -i "+str(video)+" -vf "+'"fps='+str(fps)+'"'+" origin/%0d"+filepartern
    __external_cmd(result)
def extractaudio(video): #提取音频
    if os.path.exists("origin/"+str(os.path.basename(video))+".aac"):
        os.remove("origin/"+str(os.path.basename(video))+".aac")
    st = os.system(r"ffmpeg\bin\ffmpeg.exe -i "+video+" -vn -c:a copy origin/"+str(os.path.basename(video))+".aac")
    return st
def getpid(name): #获取进程pid
    return map(int, check_output(["pidof", name]).split())
def output(origin,video,fps,sen,kbps=10000,maxkbps=15000,mtype=".jpg",vtype=".mp4"): #视频合成
    """
    进行ffmpeg合成
    :param origin:原视频路径
    :param video: 导出视频名
    :param fps: 帧率
    :param kbps: 目标码率
    :param maxkbps: 最大码率
    :param sen: 分辨率 例如1920x1080
    :param mtype: 输入图片类型
    :param vtype: 视频类型
    :return: 是否成功
    """
    if os.path.exists("origin/"+str(os.path.basename(video))+vtype):
        os.remove("origin/"+str(os.path.basename(video))+vtype)
    comm=r"ffmpeg\bin\ffmpeg.exe -r "+str(fps)+" -f image2 -start_number 1 -i origin/%0d"+str(mtype)+" -i origin/"+str(os.path.basename(origin))+".aac -c:v libx264 -b:v "+str(kbps)+"k -maxrate "+str(kbps)+"k -bufsize 10000k -pix_fmt yuv420p -c:a copy origin/"+str(video)+str(vtype)+" -y"
    sta=os.system(comm)
    return sta
