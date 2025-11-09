import sys
import uuid

from BasicSystem.log_client import setup_logger, get_logger
from modules import networks
from BasicSystem import const
from BasicSystem.VirtualFileSystem import FileSystem
from modules import VideoProcessor, watermarkstamper
import multiprocessing
from pathlib import Path
import os
import cv2
import ffmpeg
from modules.GenerateVideo import merge_sequences, setup_sequence
import subprocess
import json
import coredumpy
import gettext

_ = gettext.gettext

progress_path = "./progressCalc"


frame_format = {
            "process_order":None,
            "process_progress":None,
            "process_message":None,
        }



def extract_audio_to_flac(video_path, start_frame, end_frame, output_audio_path,
                          audio_track=0, fps=None, bitrate=None):
    """
    从视频中提取指定帧范围的音频并保存为FLAC格式

    参数:
    video_path: 输入视频文件路径
    start_frame: 起始帧号
    end_frame: 结束帧号
    output_audio_path: 输出FLAC音频文件路径
    audio_track: 要提取的音轨索引(默认0，即第一个音轨)
    fps: 视频帧率(可选，如果未提供则自动检测)
    bitrate: FLAC编码的比特率(可选，默认使用ffmpeg的默认设置)
    """

    # 如果未提供fps，需要先获取视频信息
    if fps is None:
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams']
                                 if stream['codec_type'] == 'video'), None)
            if video_stream and 'r_frame_rate' in video_stream:
                # 处理帧率字符串（可能是"30000/1001"这样的分数形式）
                frame_rate = video_stream['r_frame_rate']
                if '/' in frame_rate:
                    num, den = map(int, frame_rate.split('/'))
                    fps = num / den
                else:
                    fps = float(frame_rate)
            else:
                # 如果无法获取视频流信息，使用默认值
                fps = 30.0
                print(f"警告: 无法检测视频帧率，使用默认值 {fps}")
        except Exception as e:
            fps = 30.0
            print(f"获取视频信息时出错: {e}，使用默认帧率 {fps}")

    # 计算起始和结束时间
    start_time = start_frame / fps
    duration = (end_frame - start_frame) / fps

    # 构建ffmpeg命令
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-t', str(duration),
        '-i', video_path,
        '-map', f'0:a:{audio_track}',
        '-acodec', 'flac',
        '-ar', '44100',
        '-compression_level', '5',"-y"
    ]

    # 如果指定了比特率，添加比特率参数
    if bitrate:
        cmd.extend(['-b:a', bitrate])

    cmd.append(output_audio_path)

    # 执行转换
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"成功提取音频到: {output_audio_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取音频时出错: {e.stderr}")
        return False


def get_audio_tracks_info(video_path,logger):
    """
    获取视频中所有音频轨道的详细信息
    """
    try:
        probe = ffmpeg.probe(video_path)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

        logger.info("找到的音频轨道:")
        for i, stream in enumerate(audio_streams):
            logger.info(f"轨道 {i}:")
            logger.info(f"  编码器: {stream.get('codec_name', '未知')}")
            logger.info(f"  采样率: {stream.get('sample_rate', '未知')} Hz")
            logger.info(f"  声道数: {stream.get('channels', '未知')}")
            logger.info(f"  语言: {stream.get('tags', {}).get('language', '未知')}")
            logger.info(f"  标题: {stream.get('tags', {}).get('title', '无标题')}")

        return len(audio_streams)
    except Exception as e:
        logger.error(f"获取音频轨道信息时出错: {e}")
        return 0







def execute_command(args):
    setup_logger(default_tags="Slice", enable_udp=True, enable_console=True)
    logger = get_logger()

    process = subprocess.Popen(
        args,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # 实时处理 stderr 输出
    for line in process.stderr:
        logger.debug(str(line).replace('\n', ''))

    # 等待命令完成
    return_code = process.wait()
    print(f"Return code: {return_code}")
    if return_code!= 0:
        logger.error(f"Completed with return code: {return_code},file{args[1]} FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    return return_code


class Slice():
    def __init__(self,
                 range,
                 encoder,
                 output_format,
                 file,identify,
                 stamp_list,
                 attachment_data,
                 watermark,
                 quality_control,
                 method=const.WatermarkAlgorithm.IMAGE_FIREKEEPER,
                 max_bitrate=None,
                 target_bitrate=None,
                 tune=None,
                 preset=None,
                 foreward=None,
                 self_adaptive=None,
                 two_pass=None,
                 progress_id=None,
                 ipc_port=None,):
        setup_logger(default_tags={"module":"VideoSlice","task":f"_Slice{identify['order']}"}, enable_udp=True, enable_console=True)
        self.logger = get_logger()

        self.video_range = range

        self.file = file
        self.identify = identify
        self.object = None
        self._extract_path = None
        self.stamp_method = method
        self.stamp_list = stamp_list
        self.file_list = []
        self.attachment_data = attachment_data
        self.watermark = watermark
        self.attachment_data_result = "114514"

        self.fps = cv2.VideoCapture(self.file).get(cv2.CAP_PROP_FPS)
        self._file_path = None


        #FFmpeg
        self.BitRateControl = quality_control
        self.MaximumBitRate = max_bitrate
        self.TargetBitRate = target_bitrate
        self.FFmpegEncoder = encoder
        self.FFmpegTune = tune
        self.FFmpegPresent = preset
        self.FFmpegForeward = foreward
        self.FFmpegSelfAdaptive = self_adaptive
        self.output_format = output_format
        self.two_pass = two_pass

        #ECC
        self.correct = False
        self.audio_correct = False

        #Progeress
        self.progress_id = progress_id
        self.stamp_progress = 0
        self.extract_progress = 0
        self.cur_progress = 0

        #wht?
        self._correct_result = None
        self._result = None
        self.log_sort_uuid = uuid.uuid4()

        #ipc
        self.ipc_port = ipc_port

        self.additional_tags = {"module":"VideoSlice","task":f"_Process{self.identify['order']}"}


    def stamp_callback(self,prog):
        self.stamp_progress = prog
        self.output_progress_description()

    def extract_callback(self,prog):
        self.extract_progress = prog
        self.output_progress_description()


    def extract(self):
        VideoProcessor.extract_frames(self.file,self.video_range[0],self.video_range[1],self._extract_path,formate="png",callback=self.extract_callback)

    def process(self):

        try:
            self._process()
        except Exception as e:
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()

            if exc_traceback:
                # 遍历到最深的 traceback（异常发生的位置）
                deepest_tb = exc_traceback
                while deepest_tb.tb_next:
                    deepest_tb = deepest_tb.tb_next

                # deepest_tb.tb_frame 就是异常发生的精确帧
                exception_frame = deepest_tb.tb_frame

                # 只转储异常发生的帧
                coredumpy.dump(frame=exception_frame,
                               description="Exception trigger frame only"
                               ,path=f"./dumps/coredumpy_{os.path.basename(self.file)}_{self.identify['order']}.dump")

                # 打印确认位置
                print(f"异常发生在: {exception_frame.f_code.co_filename}:{exception_frame.f_lineno}")
            else:
                coredumpy.dump(description="No traceback available",path=f"./dumps/coredumpy_{os.path.basename(self.file)}_{self.identify['order']}.dump")
            raise



        # try:
        #     # 可能出错的代码
        #     self._process()
        # except Exception as e:
        #     # 获取异常发生时的帧信息
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #
        #     if exc_traceback:
        #         # 使用异常发生时的帧
        #         coredumpy.dump(frame=exc_traceback.tb_frame,path=f"./dumps/coredumpy_{os.path.basename(self.file)}_{self.identify['order']}.dump")
        #     else:
        #         # 如果没有 traceback，使用当前帧
        #         coredumpy.dump(path=f"./dumps/coredumpy_{os.path.basename(self.file)}_{self.identify['order']}.dump")
        #     raise

    def _process(self):
        raise RuntimeError("TEST")
        self.logger.debug(f"Start processing {self.identify['order']},sort UUID {str(self.log_sort_uuid)}",tags=self.additional_tags)
        self.output_progress_description(0,_("Start processing"))
        FileSystem.create_workspace(self.identify['name'])
        self.output_progress_description(1,_("Create workspace"))
        FileSystem.create_directory(self.identify['name'],"extracted")
        self.output_progress_description(2,_("Create extracted directory"))
        self._extract_path = FileSystem.open_file(self.identify['name'],"extracted",const.File_Return_Type.PATH)
        self.output_progress_description(3,_("Open extracted directory"))
        self.logger.info(f"Extracted frames saved to {self._extract_path}",tags=self.additional_tags)
        self.extract()
        self.output_progress_description(4,_("Extract frames"))
        for sing in FileSystem.ls_directory(self.identify['name'],"extracted"):
            self.file_list.append(FileSystem.open_file(self.identify['name'],sing,const.File_Return_Type.PATH))
        self.output_progress_description(5,_("Get extracted frames"))
        print(self.file_list)
        self.output_progress_description(6,_("Start stamping"))
        self.stamp()
        self.output_progress_description(7,_("Stamp frames"))
        self.audio_process(self.file, self.video_range,self.logger,self.additional_tags)
        self.output_progress_description(8,_("Process audio"))
        self.output()

        for files in self.file_list:
            os.remove(files)
        self.output_progress_description(16, _("Start output"))
        self._file_path = os.path.join(FileSystem.open_file(self.identify['name'],"output",const.File_Return_Type.PATH),f"{self.identify['order']}.{self.output_format}")
        self.output_progress_description(17, _("Create output path"))
        for audio in os.listdir(FileSystem.open_file(self.identify['name'],"audio_track",const.File_Return_Type.PATH)):
            os.remove(os.path.join(FileSystem.open_file(self.identify['name'],"audio_track",const.File_Return_Type.PATH),audio))
        self.output_progress_description(18, _("Remove audio track"))
        res = [self.attachment_data_result, self._file_path]
        return res



    def stamp(self):
        index = 0
        for file in self.file_list:
            path = Path(file)
            number = int(str(path.stem)[6:])
            image = cv2.imread(file)

            if number in self.stamp_list:

                if self.stamp_method == const.WatermarkAlgorithm.IMAGE_FIREKEEPER:
                    self._result, self.attachment_data_result = watermarkstamper.firekeeper_image(image,self.watermark,self.attachment_data)
                elif self.stamp_method == const.WatermarkAlgorithm.IMAGE_GUOFEI:
                    self._result, self.attachment_data_result = watermarkstamper.guofei_image(image, self.watermark,
                                                                                       self.attachment_data)
                    print(str(self.attachment_data_result)+"FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
                elif self.stamp_method == const.WatermarkAlgorithm.TEXT_GOUFEI:
                    self._result, self.attachment_data_result = watermarkstamper.guofei_text(image, self.watermark,
                                                                                    self.attachment_data)
                elif self.stamp_method == const.WatermarkAlgorithm.TEXT_FREQM:
                    self._result, self.attachment_data_result = watermarkstamper.freqmethod_text(image, self.watermark,
                                                                                   self.attachment_data)
                else:
                    self._result = image
                os.remove(file)
                cv2.imwrite(file,self._result)
                self.logger.info(f"Stamped frame {number} saved to {file}",tags=self.additional_tags)
            else:
                pass
            index += 1
            self.stamp_callback(index / len(self.file_list))
        print("Stamping Complete")

    def output(self):
        image_folder = FileSystem.open_file(self.identify['name'],"extracted",const.File_Return_Type.PATH)
        self.output_progress_description(9, _("Start output"))
        FileSystem.create_directory(self.identify['name'],"output")
        self.output_progress_description(10, _("Create output directory"))
        output_video_path = os.path.join(FileSystem.open_file(self.identify['name'],"output",const.File_Return_Type.PATH),f"{self.identify['order']}.{self.output_format}")
        self.output_progress_description(11, _("Create output video path"))
        while not self.correct:
            self.output_progress_description(12, _("Start merge"))
            if os.path.exists(output_video_path):
                os.remove(output_video_path)
            audio_list = []
            if not len(os.listdir(FileSystem.open_file(self.identify['name'],"audio_track",const.File_Return_Type.PATH))) == 0:
                for aui in os.listdir(FileSystem.open_file(self.identify['name'],"audio_track",const.File_Return_Type.PATH)):
                    audio_list.append(os.path.join(FileSystem.open_file(self.identify['name'],"audio_track",const.File_Return_Type.PATH),aui))
            else:
                audio_list = None
            self.output_progress_description(13, _("Start FFmpeg process"))

            merge_sequences(
                os.path.join(image_folder,setup_sequence(image_folder,)),
                output_video_path,
                self.fps,
                self.BitRateControl,
                self.MaximumBitRate,
                self.TargetBitRate,
                self.FFmpegEncoder,
                self.FFmpegTune,
                self.FFmpegPresent,
                start_index=int(os.listdir(image_folder)[0].split('.')[0].split('_')[1]),
                audio_file=audio_list,
                fc=self.FFmpegForeward,
                psy=self.FFmpegSelfAdaptive,
                two_pass=self.two_pass,
                output_format=self.output_format
            )
            self.output_progress_description(14, _("Error check"))
            if execute_command(["ffprobe", "-v", "error",output_video_path]) == 0:
                self.correct = True
                self.output_progress_description(15, _("Correct and Output"))


    def run(self):
        self.object = multiprocessing.Process(target=self.process)
        return self.object

    def start(self):
        results = self.process()
        return results

    def audio_process(self,input_video, ranges,logger,tags=None):
        track_count = get_audio_tracks_info(input_video,logger)
        logger.info(f"视频{input_video}有{track_count}个音轨",tags=tags)
        FileSystem.create_directory(self.identify['name'], "audio_track")
        for i in range(track_count):
            output_path = os.path.join(FileSystem.open_file(self.identify['name'], "audio_track", const.File_Return_Type.PATH), f"{int(i)}.flac")
            extract_audio_to_flac(input_video, ranges[0], ranges[1], output_path, audio_track=int(i), fps=self.fps)

    def output_progress_description(self,st_N=None,msg=None):
        total_N = 18
        if st_N is not None:
            self.cur_progress = float(st_N / total_N)
        aa = (self.cur_progress+self.extract_progress+self.stamp_progress)/3
        frame_format = {
            "process_order": self.identify['order'],
            "process_progress": aa,
            "process_message": f"{msg}|{self.extract_progress}|{self.stamp_progress}",
        }
        data = json.dumps(frame_format)
        networks.ipc_send(data,"127.0.0.1",self.ipc_port)



