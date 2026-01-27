import shutil
import subprocess
import traceback

import ffmpeg

from modules import VideoProcessor, packup
from pathlib import Path
from BasicSystem import const
from modules.Slice import Slice
from modules import networks
import uuid
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
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="ProcessUnit", enable_udp=True, enable_console=True)
logger = get_logger()

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
                    logger.debug(f"Identify video fps {fps}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")
            else:
                # 如果无法获取视频流信息，使用默认值
                fps = 30.0
                logger.warning(f"Can not identify video fps,use default fps {fps}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")
        except Exception as e:
            fps = 30.0
            logger.warning(f"Occur error when extract audio to flac: {e}，use default fps {fps}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")


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
    logger.debug(f"Extract audio to flac command: {' '.join(cmd)}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")



    # 执行转换
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.success(f"Success extract audio to flac: {output_audio_path}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Extract audio to flac error: {e.stderr}",tags=f"ProcessUnit:extract_audio_to_flac:{os.path.basename(video_path)}")
        return False


def get_audio_tracks_info(video_path):
    """
    获取视频中所有音频轨道的详细信息
    """
    text = []
    try:
        probe = ffmpeg.probe(video_path)
        audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

        text.append("Found audio tracks:")
        for i, stream in enumerate(audio_streams):
            text.append(f"Track {i}:")
            text.append(f"  Decoder: {stream.get('codec_name', '未知')}")
            text.append(f"  Sample Rate: {stream.get('sample_rate', '未知')} Hz")
            text.append(f"  Channels: {stream.get('channels', '未知')}")
            text.append(f"  Language: {stream.get('tags', {}).get('language', '未知')}")
            text.append(f"  Title: {stream.get('tags', {}).get('title', '无标题')}")
            logger.debug(f"Audio track {i} details: {stream}",tags=f"ProcessUnit:get_audio_tracks_info:{os.path.basename(video_path)}")

        return len(audio_streams)
    except Exception as e:
        logger.error(f"Error when get audio tracks info: {e}",tags=f"ProcessUnit:get_audio_tracks_info:{os.path.basename(video_path)}")
        return 0







class ProcessUnit(QObject):
    update_progress = Signal(float,str,str)
    OccurError = Signal(list,str,list)
    def __init__(self,file,image=False):
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
        self.TargetBitRate = None
        self.MaximumBitRate = None
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
        self.logger = logger

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
        if not image:
            self.frame_count = VideoProcessor.get_frame_count(file)
        self.progress = 0
        self.batch_files = []
        self.stopped = False
        self.paused = False
        self.start_time = None
        self.consumed_timer = None
        self.statue = None
        if os.path.exists("setting.json"):
            with open("setting.json","r") as f:
                self.preference_args = json.load(f)


    def audio_process(self,input_video, path):
        track_count = get_audio_tracks_info(input_video)
        self.logger.info(f"Video {input_video} has {track_count} audio tracks",tags=f"ProcessUnit:ProcessUnit:extract_audio_to_flac:{os.path.basename(input_video)}")
        FileSystem.create_directory(self.identify['name'], "audio_track")
        for i in range(track_count):
            output_path = os.path.join(path, f"{int(i)}.flac")
            extract_audio_to_flac(input_video, output_path,i)

    def set_args(self,**kwargs):
        for key, value in kwargs.items():
            if key == "version" and value != const.__version__:
                logger.error(f"Version {value} not match {const.__version__}",tags=f"ProcessUnit:ProcessUnit:set_args:{os.path.basename(self.file)}")
                raise ValueError(_("版本号不匹配"))
            setattr(self, key, value)


    def search_dump_file(self):
        file = os.listdir("./dumps")
        for i in file:
            if self.dump_uuid in str(i):
                self.dump_file.append(i)
        logger.debug(f"Found dump file: {self.dump_file}",tags=f"ProcessUnit:ProcessUnit:search_dump_file:{os.path.basename(self.file)}")
        self.dump_file = list(set(self.dump_file))



    def setup_ipc(self):
        with socket.socket() as s:
            s.bind(('', 0))  # 绑定到所有接口，端口0表示自动分配
            port = s.getsockname()[1]
        self.ipc_listener = threading.Thread(target=networks.ipc_recv,args=('127.0.0.1',int(port),self.ipc_callback),daemon=True)
        self.ipc_port = port
        self.logger.info(f"Set up IPC on port: {self.ipc_port}",tags=f"ProcessUnit:ProcessUnit:setup_ipc:{os.path.basename(self.file)}")

    def start_ipc(self):
        self.ipc_listener.start()
        frame_format = {
            "process_order":None,
            "process_progress":None,
            "process_message":None,
        }
        self.logger.debug("Start IPC listener",tags=f"ProcessUnit:ProcessUnit:start_ipc:{os.path.basename(self.file)}")

    def ipc_callback(self,data,addr):
        # self.logger.debug(f"Received data from {addr}: {data}",tags=f"ProcessUnit:ProcessUnit:ipc_callback")
        try:
            data = json.loads(data)
            if data["process_order"] is None and data['process_message'] is not None:
                self.logger.debug(f"Received message: {data['process_message']}",tags=f"ProcessUnit:ProcessUnit:ipc_callback:{os.path.basename(self.file)}")
            elif data['process_order'] is not None:
                self.progress_dict.update({int(data['process_order']): float(data['process_progress'])})
                # print(self.FFmpegTune, self.FFmpegEncoder, self.FFmpegPresent, "IDENTIFY")
        except json.JSONDecodeError:
            self.logger.warning(f"Invalid JSON data: {data}",tags=f"ProcessUnit:ProcessUnit:ipc_callback:{os.path.basename(self.file)}")
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
        # self.logger.debug(f"Progress dict: {self.progress_dict}",tags=f"ProcessUnit:ProcessUnit:set_up_progress_dict")




    def sample(self):
        self._sample_list = VideoProcessor.video_sampler(self.file,self.sample_times,self.sample_extend,self.sample_type,self.manual_sample_sheet)
        # self.logger.debug(f"Sample list: {self._sample_list}",tags=f"ProcessUnit:ProcessUnit:sample")

    def generate_queue(self):
        count = self.frame_count
        self._sliced_list = VideoProcessor.spitter(count,self.slice_length)
        self.logger.debug(f"Slice list length: {len(self._sliced_list)}",tags=f"ProcessUnit:ProcessUnit:generate_queue:{os.path.basename(self.file)}")
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
        self.logger.debug(f"Length of slice list: {len(self.slice_list)}",tags=f"ProcessUnit:ProcessUnit:generate_queue:{os.path.basename(self.file)}")



    def prepare_for_merge(self):
        self.logger.debug(f"Output path: {self.output_path}",tags=f"ProcessUnit:ProcessUnit:prepare_for_merge:{os.path.basename(self.file)}")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        FileSystem.create_workspace(f"{self.base_file_name}-merge")
        FileSystem.create_directory(f"{self.base_file_name}-merge","./merge")
        FileSystem.create_directory(f"{self.base_file_name}-merge", "./audio_track")
        self.logger.debug("Create directory for audio track",tags=f"ProcessUnit:ProcessUnit:prepare_for_merge:{os.path.basename(self.file)}")
        output_path = FileSystem.open_file(f"{self.base_file_name}-merge",f"./audio_track",const.File_Return_Type.PATH)
        self.audio_process(self.file,output_path)
        perfix = FileSystem.open_file(f"{self.base_file_name}-merge",f"./audio_track",const.File_Return_Type.PATH)
        for i in os.listdir(perfix):
            self.audio_file_list.append(os.path.join(perfix,i))
        for obj in self.result_list:
            FileSystem.import_file(f"{self.base_file_name}-merge",obj[1],"./merge")
            os.remove(obj[1])
        self._temporary_path = self.output_path
        self.logger.success(f"Prepare for merge success, output path: {self.output_path}",tags=f"ProcessUnit:ProcessUnit:prepare_for_merge:{os.path.basename(self.file)}")


    def merge(self):
        lists = []
        ti = len(self.slice_list)
        for i in range(1,ti+1):
            self.saved_file_path = FileSystem.open_file(f"{self.base_file_name}-merge",f"./merge/{i}.{self.output_format}",const.File_Return_Type.PATH)
            lists.append(FileSystem.open_file(f"{self.base_file_name}-merge",f"./merge/{i}.{self.output_format}",const.File_Return_Type.PATH))
        self.logger.debug(f"Merge list: {lists}",tags=f"ProcessUnit:ProcessUnit:merge:{os.path.basename(self.file)}")
        merge_video_sequnece(lists,os.path.join(self._temporary_path,f"{self.output_name}.{self.output_format}"),logger=self.logger,audio_file=self.audio_file_list,output_format=self.output_format)

    def report_error(self,error_list):
        self.search_dump_file()
        self.OccurError.emit(error_list,self.progress_identify,self.dump_file)
        self.error_occured = True
        self.logger.critical(f"Report error: {error_list}",tags=f"ProcessUnit:ProcessUnit:report_error:{os.path.basename(self.file)}")










    @timer_decorator
    def run(self):
        self.logger.info(f"Start process unit: {self.identify}",tags=f"ProcessUnit:ProcessUnit:run:{os.path.basename(self.file)}")
        self.setup_ipc()
        self.set_stage(0)
        self.sample()
        self.set_stage(1)
        self.generate_queue()
        self.set_stage(2)
        self.start_ipc()
        # 多进程和单进程行为要一致
        if self.process_limit != 1:
            self.scheduler = None
            self.scheduler = ConcurrentExecutor()
            self.result_list = self.scheduler.execute_concurrently(self.slice_list,self.process_limit,self.report_error)
        else:
            try:
                for ob in self.slice_list:
                    self.result_list.append(ob.process())
            except Exception as e:
                stack_trace = traceback.format_exc()
                frame = [e, stack_trace]
                self.report_error(frame)
        if not self.error_occured and self.result_list[0] != 'Terminated':
            self.set_stage(3)
            print(self.result_list)
            self.set_stage(4)
            self.prepare_for_merge()
            self.set_stage(5)
            self.merge()
            self.set_stage(6)
            self.after_processing()
            self.remove_workspace()
            self.completed = True
            self.running = False
            self.status = 1
            self.logger.success(f"Process unit: {self.identify} completed",tags=f"ProcessUnit:ProcessUnit:run:{os.path.basename(self.file)}")

            return True
        else:
            self.completed = _("发生错误")
            self.running = False
            self.status = 0
            self.logger.critical(f"Process unit: {self.identify} error: {self.completed}",tags=f"ProcessUnit:ProcessUnit:run:{os.path.basename(self.file)}")
            try:
                self.remove_workspace()
            except Exception as e:
                self.logger.critical(f"Remove workspace error: {e}",tags=f"ProcessUnit:ProcessUnit:run:{os.path.basename(self.file)}")
                pass
            return False



    def suspend(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "suspend")
            self.logger.info(f"Suspend process: {i}",tags=f"ProcessUnit:ProcessUnit:suspend:{os.path.basename(self.file)}")

    def resume(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "resume")
            self.logger.info(f"Resume process: {i}",tags=f"ProcessUnit:ProcessUnit:resume:{os.path.basename(self.file)}")

    def stop(self):
        for i in self.scheduler.get_running_pids():
            manage_process_by_pid(i, "terminate")
            self.logger.info(f"Stop process: {i}",tags=f"ProcessUnit:ProcessUnit:stop:{os.path.basename(self.file)}")
        manage_process_by_pid(self.scheduler.manager_pid, "terminate")
        self.logger.info(f"Stop process: {self.scheduler.manager_pid}",tags=f"ProcessUnit:ProcessUnit:stop:{os.path.basename(self.file)}")
        self.stopped = True

    def after_processing(self):
        for i in self.result_list:
            print(i)
        recover_data = {
            "version":const.__version__,
            "sample_list":list(self._sample_list),
            "attachment_data":self.process_attachment() ,
            "watermark_method":self.watermark_method,
        }
        json_path = os.path.join(self._temporary_path,f"recover.pkl")
        data = pickle.dumps(recover_data)
        self.logger.debug(f"Recover data: {recover_data}",tags=f"ProcessUnit:ProcessUnit:after_processing:{os.path.basename(self.file)}")

        if os.path.exists(json_path):
            os.remove(json_path)
        with open(json_path,"wb") as f:
            f.write(data)
        self.logger.debug(f"Recover data saved to: {json_path}",tags=f"ProcessUnit:ProcessUnit:after_processing:{os.path.basename(self.file)}")
        FileSystem.mapping_list = {}
        if os.path.exists("setting.json"):
            with open("setting.json","r") as f:
                data = json.load(f)
            if data['OutputStructure'] != "dir":
                packup.pack_files_to_zip(
                    file_paths=[json_path,os.path.join(self._temporary_path,f"{self.output_name}.{self.output_format}")],
                    output_dir=self._temporary_path,
                    zip_name=f"{self.output_name}",
                    preserve_structure=False
                )
                os.remove(json_path)
                os.remove(os.path.join(self._temporary_path,f"{self.output_name}.{self.output_format}"))
        self.stop()


    def set_stage(self,stage):
        self.process_unit_stage = int(stage)
        self.logger.info(f"Set process unit stage: {self.process_unit_stage}",tags=f"ProcessUnit:ProcessUnit:set_stage:{os.path.basename(self.file)}")



    def process_attachment(self):
        list_data = []
        for i in self.result_list:
            if str(i[0]) != "114514":
                list_data.append(i[0])
        self.logger.debug(f"Attachment data: {list_data}",tags=f"ProcessUnit:ProcessUnit:process_attachment:{os.path.basename(self.file)}")
        return list_data

    def remove_workspace(self):
        vi = os.path.dirname(os.path.normpath(str(self.saved_file_path)))
        root = os.path.dirname(os.path.normpath(vi))
        shutil.rmtree(root)
        self.logger.debug(f"Remove workspace: {root}",tags=f"ProcessUnit:ProcessUnit:remove_workspace:{os.path.basename(self.file)}")













