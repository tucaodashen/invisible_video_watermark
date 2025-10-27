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
from BasicSystem.LogSystem import logger
import json
import pickle
import socket
import threading
import gettext
from PySide6.QtCore import Signal,QObject

_ = gettext.gettext



progress_path = "./progressCalc"






class ProcessUnit(QObject):
    update_progress = Signal(float,str)
    def __init__(self):
        super().__init__()
        self.scheduler = None
        self.file = "mul.mov"
        self.watermark_method = const.WatermarkAlgorithm.IMAGE_GUOFEI
        self.attachment_data = {'img_password':1145,'wm_password':1919}
        self.output_name = "coded_mul_"
        self.output_path = "./"
        self.slice_length = 300
        self.sample_times = 10
        self.sample_extend = 16
        self.process_limit = 16
        self.watermark_content = cv2.imread("vm.png")

        self._sample_list = []
        self._sliced_list = []
        self.slice_list = []
        self.result_list = []

        file_path = Path(self.file)
        self.base_file_name = file_path.stem

        self._temporary_path = None

        #FFMPEG
        self.BitRateControl = const.BitRateControl.VBR
        self.MaximumBitRate = "20M"
        self.TargetBitRate = "10M"
        self.FFmpegEncoder = const.Encoder.NVIDIA_H264
        self.FFmpegTune = const.FFmpegTune.NV_H264_HQ
        self.FFmpegPresent = const.FFmpegPreset.NVIDIA_P5
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
        logger.debug(f"Received data from {addr}: {data}")
        try:
            data = json.loads(data)
            if data["process_order"] is None and data['process_message'] is not None:
                logger.debug(f"Received message: {data['process_message']}")
            elif data['process_order'] is not None:
                self.progress_dict.update({int(data['process_order']): float(data['process_progress'])})
                print(f"Progress: {self.progress_dict}")
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON data: {data}")
        if self.progress_dict != {}:
            cur_sum = 0
            for i in list(self.progress_dict.values()):
                cur_sum += i
            cur_percent = (cur_sum/len(self.slice_list))
            self.update_progress.emit(cur_percent,f"Progress: {cur_percent}%")
            print(f"Progress: {cur_percent*100}%___________________________________________________________________________________")


    def set_up_progress_dict(self):
        for i in range(len(self.slice_list)+1):
            self.progress_dict.update(
                {i:0}
            )
        logger.debug(f"Progress dict: {self.progress_dict}")




    def sample(self):
        self._sample_list = VideoProcessor.video_sampler(self.file,self.sample_times,self.sample_extend)

    def generate_queue(self):
        self._sliced_list = VideoProcessor.spitter(VideoProcessor.get_frame_count(self.file),self.slice_length)
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
                                         preset=self.FFmpegPresent.NVIDIA_P5,
                                         foreward=self.FFmpegForeward,
                                         self_adaptive=self.FFmpegSelfAdaptive,
                                         two_pass=True,
                                         progress_id=self.identify,
                                         ipc_port=self.ipc_port,
                                         ))

    def prepare_for_merge(self):

        FileSystem.create_workspace(f"{self.base_file_name}-merge")
        FileSystem.create_directory(f"{self.base_file_name}-merge","./merge")
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
        merge_video_sequnece(lists,os.path.join(self._temporary_path,f"{self.output_name}.{self.output_format}"))
        if os.path.exists("input_list.txt"):
            os.remove("input_list.txt")
        # VideoProcessor.add_audio_to_video(f"{self.output_name}.{self.output_format}","test.mp3","ooout_with_audio.mp4")





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
            self.result_list = self.scheduler.execute_concurrently(self.slice_list,self.process_limit)
        else:
            for ob in self.slice_list:
                self.result_list.append(ob.process())
        self.set_stage(3)
        print(self.result_list)
        self.set_stage(4)
        self.prepare_for_merge()
        self.set_stage(5)
        self.merge()
        self.set_stage(6)
        self.after_processing()
        self.sort_log()

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
        print(f"Progress: {self.progress_percent}%")

    def process_attachment(self):
        list_data = []
        for i in self.result_list:
            if str(i[0]) != "114514":
                list_data.append(i[0])
        logger.debug(f"Attachment data: {list_data}")
        return list_data

    def sort_log(self):
        os.mkdir(os.path.join("./logs",str(self.base_file_name+str(self.identify["UUID"]))))
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










