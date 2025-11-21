import shutil
import subprocess

import ffmpeg

from BasicSystem.log_client import setup_logger, get_logger
from modules import VideoProcessor
from pathlib import Path
from BasicSystem import const
from modules.Slice import Slice
from modules import networks
import uuid
import cv2
import os
from BasicSystem.VirtualFileSystem import FileSystem
from modules.GenerateVideo import merge_video_sequnece
from modules.ProcessSchedulerSusFec import ConcurrentExecutor, manage_process_by_pid
from modules.decorator import timer_decorator
import json
import pickle
import socket
import threading
import gettext
from PySide6.QtCore import Signal,QObject

_ = gettext.gettext



progress_path = "./progressCalc"



def extract_audio_to_flac(video_path,output_audio_path,
                          audio_track=0, fps=None, bitrate=None):
    """
    从视频中提取指定帧范围的音频并保存为FLAC格式

    参数:
    video_path: 输入视频文件路径
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


    # 构建ffmpeg命令
    cmd = [
        'ffmpeg',
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







class ProcessUnit(QObject):
    update_progress = Signal(float,str,str)
    OccurError = Signal(list,str,list)
    def __init__(self,file):
        super().__init__()
        self.audio_file_list = []
        self.error_occured = False
        self.scheduler = None
        self.file = file
        self.watermark_method = None
        self.attachment_data = {'img_password':1145,'wm_password':1919}
        self.output_name = "coded_mul_"
        self.output_path = "./"
        self.slice_length = 10
        self.sample_times = 10
        self.sample_extend = 16
        self.process_limit = 16
        self.sample_type = const.SamplerType.RANDOM
        self.manual_sample_sheet = "1"
        self.watermark_content = None

        self._sample_list = []
        self._sliced_list = []
        self.slice_list = []
        self.result_list = []

        file_path = Path(self.file)
        self.base_file_name = file_path.stem

        self._temporary_path = None

        #FFMPEG
        self.BitRateControl = None
        self.MaximumBitRate = "20M"
        self.MaximumBitRate = "10M"
        self.FFmpegEncoder = None
        self.FFmpegTune = None
        self.FFmpegPresent = None
        self.FFmpegForeward = None
        self.FFmpegSelfAdaptive = None
        self.output_format = "mov"
        self.two_pass = True

        #IDENTIFY
        self.identify = {
            "name":f"{self.base_file_name}",
            "UUID":str(uuid.uuid4())
        }

        #progress
        self.total_progress_stage = 0
        self.current_progress_stage = 0
        self.process_unit_stage = 0
        self.slice_stage = 0
        self.progress_percent = None

        #ipc
        self.ipc_listener = None
        self.ipc_port = None
        self.progress_dict = {}

        #sort_log
        default_tags={"module":"ProcessUnit","task":f"{self.base_file_name}_Process{self.identify['name']}"}
        setup_logger(default_tags=default_tags, enable_udp=True, enable_console=True)
        self.logger = get_logger()

        #GUI

        self.index = None
        self.running = False
        self.completed = False
        self.status = _("等待中")
        self.progress_identify = None

        self.dump_file = []
        self.saved_file_path = [None,None]
        self.dump_uuid = None
        self.root_dir = None
        self.frame_count = VideoProcessor.get_frame_count(file)
        self.progress = 0
        self.batch_files = []


    def audio_process(self,input_video, path,tags=None):
        track_count = get_audio_tracks_info(input_video,self.logger)
        self.logger.info(f"视频{input_video}有{track_count}个音轨",tags=tags)
        FileSystem.create_directory(self.identify['name'], "audio_track")
        for i in range(track_count):
            output_path = os.path.join(path, f"{int(i)}.flac")
            extract_audio_to_flac(input_video, output_path,i)

    def set_args(self,**kwargs):
        for key, value in kwargs.items():
            if key == "version" and value != const.__version__:
                raise ValueError(_("版本号不匹配"))
            setattr(self, key, value)


    def search_dump_file(self):
        file = os.listdir("./dumps")
        for i in file:
            if self.dump_uuid in str(i):
                self.dump_file.append(i)
        print(self.dump_file)
        self.dump_file = list(set(self.dump_file))



    def setup_ipc(self):
        with socket.socket() as s:
            s.bind(('', 0))  # 绑定到所有接口，端口0表示自动分配
            port = s.getsockname()[1]
        self.ipc_listener = threading.Thread(target=networks.ipc_recv,args=('127.0.0.1',int(port),self.ipc_callback),daemon=True)
        self.ipc_port = port

    def start_ipc(self):
        self.ipc_listener.start()
        frame_format = {
            "process_order":None,
            "process_progress":None,
            "process_message":None,
        }

    def ipc_callback(self,data,addr):
        self.logger.debug(f"Received data from {addr}: {data}")
        try:
            data = json.loads(data)
            if data["process_order"] is None and data['process_message'] is not None:
                self.logger.debug(f"Received message: {data['process_message']}")
            elif data['process_order'] is not None:
                self.progress_dict.update({int(data['process_order']): float(data['process_progress'])})
                # print(self.FFmpegTune, self.FFmpegEncoder, self.FFmpegPresent, "IDENTIFY")
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON data: {data}")
        if self.progress_dict != {}:
            cur_sum = 0
            for i in list(self.progress_dict.values()):
                cur_sum += i
            cur_percent = (cur_sum/len(self.slice_list))
            self.update_progress.emit(cur_percent,f"Progress: {cur_percent}%",self.progress_identify)
            self.progress = cur_percent
            # print(f"Progress: {cur_percent*100}%___________________________________________________________________________________")


    def set_up_progress_dict(self):
        for i in range(len(self.slice_list)+1):
            self.progress_dict.update(
                {i:0}
            )
        self.logger.debug(f"Progress dict: {self.progress_dict}")




    def sample(self):
        self._sample_list = VideoProcessor.video_sampler(self.file,self.sample_times,self.sample_extend,self.sample_type,self.manual_sample_sheet)

    def generate_queue(self):
        count = self.frame_count
        print(count,self.file)
        self._sliced_list = VideoProcessor.spitter(count,self.slice_length)
        print(len(self._sliced_list))
        for r in self._sliced_list:
            print(r)
        index = 0
        for ranges in self._sliced_list:
            index += 1

            identify = {
                "name":f"{index}-{self.base_file_name}",
                "order":index
            }
            self.slice_list.append(Slice(range=ranges,
                                         encoder=self.FFmpegEncoder,
                                         output_format=self.output_format,
                                         file=self.file,
                                         identify=identify,
                                         stamp_list=self._sample_list,
                                         attachment_data=self.attachment_data,
                                         watermark=self.watermark_content,
                                         quality_control=self.BitRateControl,
                                         method=self.watermark_method,
                                         max_bitrate=self.MaximumBitRate,
                                         target_bitrate=self.TargetBitRate,
                                         tune=self.FFmpegTune,
                                         preset=self.FFmpegPresent,
                                         foreward=self.FFmpegForeward,
                                         self_adaptive=self.FFmpegSelfAdaptive,
                                         two_pass=True,
                                         progress_id=self.identify,
                                         ipc_port=self.ipc_port,
                                         dump_uuid = self.dump_uuid
                                         ))
        print(len(self.slice_list),"Length of slice list")

    def prepare_for_merge(self):

        FileSystem.create_workspace(f"{self.base_file_name}-merge")
        FileSystem.create_directory(f"{self.base_file_name}-merge","./merge")
        FileSystem.create_directory(f"{self.base_file_name}-merge", "./audio_track")
        output_path = FileSystem.open_file(f"{self.base_file_name}-merge",f"./audio_track",const.File_Return_Type.PATH)
        self.audio_process(self.file,output_path)
        perfix = FileSystem.open_file(f"{self.base_file_name}-merge",f"./audio_track",const.File_Return_Type.PATH)
        for i in os.listdir(perfix):
            self.audio_file_list.append(os.path.join(perfix,i))
        for obj in self.result_list:
            FileSystem.import_file(f"{self.base_file_name}-merge",obj[1],"./merge")
            os.remove(obj[1])
        FileSystem.create_directory(f"{self.base_file_name}-merge", "./output")
        self._temporary_path = FileSystem.open_file(f"{self.base_file_name}-merge",f"./output",const.File_Return_Type.PATH)


    def merge(self):
        lists = []
        ti = len(self.slice_list)
        for i in range(1,ti+1):
            lists.append(FileSystem.open_file(f"{self.base_file_name}-merge",f"./merge/{i}.{self.output_format}",const.File_Return_Type.PATH))
        print(lists)
        merge_video_sequnece(lists,os.path.join(self._temporary_path,f"{self.output_name}.{self.output_format}"),logger=self.logger,audio_file=self.audio_file_list,output_format=self.output_format)
        saved_path = FileSystem.open_file(f"{self.base_file_name}-merge",f"./output/{self.output_name}.{self.output_format}",const.File_Return_Type.PATH)
        self.saved_file_path[0] = saved_path

    def report_error(self,error_list):
        self.search_dump_file()
        self.OccurError.emit(error_list,self.progress_identify,self.dump_file)
        self.error_occured = True
        print("?????????????????????????????????????????????????????????????????")

    def output_packed_file(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        shutil.move(str(self.saved_file_path[0]),self.output_path)
        shutil.move(str(self.saved_file_path[1]),self.output_path)
        self.logger.info(f"文件已保存到{self.output_path}")










    @timer_decorator
    def run(self):
        self.setup_ipc()
        self.set_stage(0)
        self.sample()
        self.set_stage(1)
        self.generate_queue()
        self.set_stage(2)
        self.start_ipc()
        if self.process_limit != 1:
            self.scheduler = None
            self.scheduler = ConcurrentExecutor()
            self.result_list = self.scheduler.execute_concurrently(self.slice_list,self.process_limit,self.report_error)
        else:
            for ob in self.slice_list:
                self.result_list.append(ob.process())
        if not self.error_occured and self.result_list[0] != 'Terminated':
            self.set_stage(3)
            print(self.result_list)
            self.set_stage(4)
            self.prepare_for_merge()
            self.set_stage(5)
            self.merge()
            self.set_stage(6)
            self.after_processing()
            self.sort_log()
            self.output_packed_file()
            self.remove_workspace()
            self.completed = True
            self.running = False
            self.status = 1
            return True
        else:
            self.completed = _("发生错误")
            self.running = False
            self.status = 0
            try:
                self.remove_workspace()
            except:
                pass
            return False



    def suspend(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "suspend")

    def resume(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "resume")

    def stop(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "terminate")
        manage_process_by_pid(self.scheduler.manager_pid, "terminate")

    def after_processing(self):
        print(self.result_list)
        recover_data = {
            "version":const.__version__,
            "sample_list":list(self._sample_list),
            "attachment_data":self.process_attachment() ,
            "watermark_method":self.watermark_method,
        }
        json_path = os.path.join(self._temporary_path,f"recover.pkl")
        data = pickle.dumps(recover_data)
        print(data)

        if os.path.exists(json_path):
            os.remove(json_path)
        with open(json_path,"wb") as f:
            f.write(data)
        print(recover_data)
        FileSystem.mapping_list = {}
        self.saved_file_path[1] = json_path
        self.stop()


    def set_stage(self,stage):
        self.process_unit_stage = int(stage)

    def calculate_total_progress_stage(self):
        if not self._slice_list:
            slice_length = len(self._sliced_list)
        slice_length = self.process_limit
        slice_stage = slice_length*19
        process_unit_stage = 6
        self.total_progress_stage = slice_stage + process_unit_stage

    def calculate_current_progress_stage(self):
        file_dir = "./progressCalc"
        pgdf_list = os.listdir(file_dir)
        self.slice_stage = 0
        for i in pgdf_list:
            if os.path.basename(i).split(".")[0] == self.identify["UUID"]:
                with open(os.path.join(file_dir,i),"r") as f:
                    json_data = json.load(f)
                    self.slice_stage += json_data["stage"]
        self.current_progress_stage = self.slice_stage + self.process_unit_stage

    def calculate_percent(self):
        self.calculate_total_progress_stage()
        self.calculate_current_progress_stage()
        self.progress_percent = (self.current_progress_stage/self.total_progress_stage)*100
        # print(f"Progress: {self.progress_percent}%")

    def process_attachment(self):
        list_data = []
        for i in self.result_list:
            if str(i[0]) != "114514":
                list_data.append(i[0])
        self.logger.debug(f"Attachment data: {list_data}")
        return list_data

    def remove_workspace(self):
        vi = os.path.dirname(os.path.normpath(str(self.saved_file_path[0])))
        root = os.path.dirname(os.path.normpath(vi))
        shutil.rmtree(root)

    def sort_log(self):
        pass
        # for i in os.listdir("./logs"):
        #     with open(os.path.join("./logs",i), 'r') as file:
        #         lines = []
        #         for ina in range(100):
        #             line = file.readline()
        #             if not line:  # 文件行数不足100时提前终止
        #                 break
        #             for identify in self.slice_list:
        #                 if str(identify.log_sort_uuid) in str(line):
        #                     shutil.move(os.path.join("./logs",i),os.path.join("./logs",str(self.base_file_name+str(self.identify["UUID"])),i))
            # for identify in self.slice_list:
            #     if i.split(".")[0].split("_")[-1] == identify.log_sort_uuid:
            #         shutil.move(os.path.join("./logs",i),os.path.join("./logs",str(self.base_file_name+str(self.identify["UUID"])),i))










