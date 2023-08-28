import random
import cv2


frnm=0
def sampler(video,times=10,peroid=1):
    """
    对视频进行抽帧处理
    :param video:
    :param times: 抽帧次数
    :param peroid: 加长帧数
    :return: 抽帧列表
    """
    framelist = []
    video = cv2.VideoCapture(str(video))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(int(times)):
        print("第",i+1,"次采样处理")
        framenumber = random.randint(1, frame_count)
        processfr = framenumber #对视频进行随机抽帧
        for ti in range(int(peroid)):
            if processfr <= frame_count: #加长取样区间，减少解密难度
                framelist.append(processfr) #判断帧号是否超出范围
            processfr = processfr+1
    framelist = list(set(framelist))
    return framelist
def extract_frames(video_path, frame_indexes,output_path="processframe",filetype=".jpg"):
    """
    将视频处理后输出为图片
    :param video_path: 视频地址
    :param frame_indexes: 抽帧列表
    :param output_path: 输出路径
    :return:
    """
    # 打开视频文件
    video_capture = cv2.VideoCapture(video_path)

    # 获取视频总帧数
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # 遍历每个指定的帧位置
    for index in frame_indexes:
        if index >= total_frames:
            print(f"帧位置 {index} 超过视频总帧数，跳过。")
            continue

        # 设置当前帧位置
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, index-1)

        # 读取当前帧
        ret, frame = video_capture.read()

        # 保存当前帧为图片
        output_file = f"{output_path}/{index}"+str(filetype)
        cv2.imwrite(output_file, frame)
        print(f"已保存帧位置 {index} 的图片为 {output_file}.")

    # 关闭视频文件
    video_capture.release()
