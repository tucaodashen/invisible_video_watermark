"""
铃兰小姐是我们的光！
请保佑代码永远不出bug吧！
"""
from PySide6.QtCore import Qt,QTime,QTimer,QThread,Signal
import os
import random
import time
import blind_watermark as bw
import command
import videoprocess
import core
import cv2
import shutil
import json


recoverdata={}
def initial():
    """
    准备相应文件夹与工作环境
    :return:
    """
    if os.path.exists("processframe"):
        pass
    else:
        os.mkdir("processframe")
    if os.listdir("processframe")!=[]:
        for i in os.listdir("processframe"):
            os.remove("processframe/"+i)
    if os.path.exists("processedframe"):
        pass
    else:
        os.mkdir("processedframe")
    if os.listdir("processedframe")!=[]:
        for i in os.listdir("processedframe"):
            os.remove("processedframe/"+i)
    if os.path.exists("origin"):
        pass
    else:
        os.mkdir("origin")
    if os.listdir("origin") != []:
        for i in os.listdir("origin"):
            os.remove("origin/" + i)
    if os.path.exists("result"):
        pass
    else:
        os.mkdir("result")
    if os.path.exists("recoverresult"):
        pass
    else:
        os.mkdir("recoverresult")
    if os.path.exists("recover"):
        pass
    else:
        os.mkdir("recover")
    if os.listdir("recover")!=[]:
        for i in os.listdir("recover"):
            os.remove("recover/"+i)
    try:
        os.remove("progress.json")
    except:
        pass

def process(watermark,
            video,
            filename,
            sen=0,
            sampletimes=5,
            peroid=1,
            filetype=".png",
            kbps=10000,
            maxkbps=25000,
            videotype=".mp4",
            outputtype="video",
            processtype="image",
            watermarkquality=35,
            ):
    """
    主处理函数
    :param watermark:水印内容
    :param video: 输入视频
    :param filename: 输出视频名
    :param sen: 分辨率，留空默认为输入分辨率
    :param sampletimes: 取样次数
    :param peroid: 取样个数增量
    :param filetype: 抽帧文件类型
    :param quality: 文件质量
    :param videotype: 输出视频格式
    :param watermarkquality:水印质量，建议为30，如果视频压制更厉害需要相应提高
    :return:是否成功
    """
    try:
        progressbar({'cent': 0, 'operation': '初始化...'})
        seed=[]
        for tim in range(2):
            seed.append(random.randint(1,9999))
        seed.append(watermarkquality)
    #生成随机种子用于水印合成
        stats = os.stat(video) #获取视频元数据
        initial() #初始化
        progressbar({'cent':10,'operation':'初始化已完成'})
        if os.path.exists("result/"+str(filename)):
            shutil.rmtree("result/"+str(filename))#防止项目同名
        videoc = cv2.VideoCapture(str(video))
        frame_count = int(videoc.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(videoc.get(cv2.CAP_PROP_FPS))
        # 获取视频的宽度（单位：像素）
        width = videoc.get(cv2.CAP_PROP_FRAME_WIDTH)

        # 获取视频的高度（单位：像素）
        height = videoc.get(cv2.CAP_PROP_FRAME_HEIGHT)
        sen1=str(str(int(width))+"x"+str(int(height)))
        if sen==0: #自动获取分辨率
            sen=sen1
        videoc.release()
        progressbar({'cent': 10, 'operation': '提取原视频，此操作会耗费一定时间'})
        command.extractall(video,filetype) #提取原视频中所有帧
        progressbar({'cent': 35, 'operation': '提取完成，进行水印处理，如果你的采样数很多，这一步也会花费相当时间'})
        print("原视频提取成功")
        samplelist = videoprocess.sampler(video,sampletimes,peroid) #采样
        videoprocess.extract_frames(video,samplelist,filetype=filetype) #抽帧
        processlist = os.listdir("processframe") #进行水印处理
        for fil in processlist:
            if processtype=="text":
                len = str(core.encodewatermark_text(watermark, fil))
            else:
                imlen = core.encodewatermark_image(str(fil),str(watermark),seed)
            shutil.copy("processedframe/"+fil, "origin")#进行帧替换
        print(processlist,"处理已完成")
        progressbar({'cent': 60, 'operation': '处理完成，正在进行文件输出'})
        audextst = command.extractaudio(video) #提取原视频音频
        if audextst == "err":
            print("视频无音频！")
        if outputtype=="video": #进行视频合成
            command.output(origin=video,video=filename,fps=fps,sen=sen,kbps=kbps,maxkbps=maxkbps,mtype=filetype,vtype=videotype)
        os.mkdir("result/"+str(filename))
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        nowtime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))#获取当前时间
        version=str(bw.version.__version__) #获取版本呢
        if processtype=="image":
            len=seed
        recoverdata={ #创建json文件内容
            'algorithm':processtype,
            'date':nowtime,
            'version':version,
            'videoname':str(video),
            'freamdata':samplelist,
            'fps':fps,
            'totalfream':frame_count,
            'metadata':str(stats),
            'seed':len,
            'shape':imlen
        }
        with open("origin/"+filename+".json", "w", encoding='utf-8') as f:
            json.dump(recoverdata, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
        if outputtype == "video":
            shutil.move("origin/" + str(filename)+".json", str("result/" + str(filename)))
            shutil.move("origin/" + str(filename)+str(videotype), str("result/" + str(filename)))#移动到文件夹中
        else:
            for wb in os.listdir("origin"):
                shutil.move("origin/"+str(wb),str("result/" + str(filename)))
        while True: #最终整理文件
            try:
                initial()
            except:
                initial()
            finally:
                break
        print("处理完成")
        progressbar({'cent': 100, 'operation': '处理完成！'})
        print(recoverdata)
        return 0
    except:
        progressbar({'cent': 0, 'operation': '操作失败，请检查输出后重试。当然如果你是点了停止就是你停止了'})
        print("wdnmd又出错!")
        return -1
def recorver(recoverfile,video,processtype):
    initial()
    with open(recoverfile, 'r') as f:
        recoverdata = json.load(f)
    flist=recoverdata['freamdata']
    videoprocess.extract_frames(video,flist,output_path="recover",filetype=".png")
    for sd in os.listdir("recover"):
        try:
            if processtype=="text":
                resu=[]
                resu.append(core.decodewatermark_text(recoverdata['seed'], "recover/" + str(sd)))
                print(resu)
                return resu
            else:
                core.decodewatermark_image(str(sd),recoverdata['shape'],recoverdata['seed'])
        except:
            print("解码失败")
            return ["失败了"]
def progressbar(processcent):
    with open("progress.json", "w", encoding='utf-8') as f:
        json.dump(processcent, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    #process(r"D:\invisible_video_watermark\test.png",r"F:\videos\damedane.flv",filetype=".png",filename="yuanshenqidong",outputtype="video",processtype="image")
    #recorver(r"yuanshenqidong.json",r"yuanshenqidong.mp4","image")
    #core.decodewatermark_image("10.png",[75,75],[5563,2400,25])
    #core.encodewatermark_image("origin/1.png","test.png",[1145,1919,30])
    #core.encodewatermark_image(str("1.png"), str("test.png"), [1145,1419,30])
    #videoprocess.extract_frames("dame.mp4",[10])
    #print(pil.recognize(r"D:\invisible_video_watermark\recoverresult\Y_U_V\U5560051907wm_816.png"))
    #initial()
    initial()
    print("你好")

