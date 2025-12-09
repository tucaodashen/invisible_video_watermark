import shutil
import sys
import uuid
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
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="Slice", enable_udp=True, enable_console=True)
logger = get_logger()


_ = gettext.gettext

frame_format = {
            "process_order":None,
            "process_progress":None,
            "process_message":None,
        }










def execute_command(args):

    process = subprocess.Popen(
        args,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # 实时处理 stderr 输出
    for line in process.stderr:
        logger.debug(str(line).replace('\n', ''),tags="Slice:execute_command")

    # 等待命令完成
    return_code = process.wait()
    logger.debug(f"Completed with return code: {return_code},file{args}",tags="Slice:execute_command")
    if return_code!= 0:
        logger.error(f"Completed with return code: {return_code},file{args}",tags="Slice:execute_command")
    return return_code


class Slice:
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
                 ipc_port=None,
                 dump_uuid=None):
        self.logger = logger

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
        self.extract_retry_times = 0


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
        self.ffmpeg_retry_count = 0

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
        self.dump_uuid = dump_uuid


    def stamp_callback(self,prog):
        self.stamp_progress = prog
        self.output_progress_description()

    def extract_callback(self,prog):
        self.extract_progress = prog
        self.output_progress_description()


    def extract(self):
        if self.extract_retry_times >= 5:
            self.logger.error(f"Extract {self.file} {self.video_range[0]} {self.video_range[1]} to {self._extract_path} retry times {self.extract_retry_times} failed",tags=f"Slice:Slice:extract:{os.path.basename(self.file)}:{self.identify['order']}")
            raise RuntimeError(f"Extract {self.file} {self.video_range[0]} {self.video_range[1]} to {self._extract_path} retry times {self.extract_retry_times} failed!\nMaximum retry times exceeded.")
        if self.extract_retry_times == 0:
            self.logger.debug(f"Extract {self.file} {self.video_range[0]} {self.video_range[1]} to {self._extract_path}",tags=f"Slice:Slice:extract:{os.path.basename(self.file)}:{self.identify['order']}")
        else:
            self.logger.debug(f"Extract {self.file} {self.video_range[0]} {self.video_range[1]} to {self._extract_path} retry times {self.extract_retry_times}",tags=f"Slice:Slice:extract:{os.path.basename(self.file)}:{self.identify['order']}")
        try:
            VideoProcessor.extract_frames(self.file,self.video_range[0],self.video_range[1],self._extract_path,formate="png",callback=self.extract_callback)
            self.extract_retry_times = 0
        except RuntimeError as c:
            if "Failed to read frame" in str(c):
                self.extract_retry_times += 1
                self.extract()
            else:
                raise
        except:
            raise



    def process(self):

        try:
            result = self._process()
            return result
        except Exception as e:
            self.logger.debug(f"Exception {e}",tags=f"Slice:Slice:process:{os.path.basename(self.file)}:{self.identify['order']}")
            path = f"./dumps/coredumpy_{os.path.basename(self.file)}_{self.identify['order']}_{self.dump_uuid}.dump"
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
                               ,path=path,depth=4)

                # 打印确认位置
                print(f"异常发生在: {exception_frame.f_code.co_filename}:{exception_frame.f_lineno}")
            else:
                coredumpy.dump(description="No traceback available",path=path,depth=4)
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
        self.logger.debug(f"Start processing {self.identify['order']},sort UUID {str(self.log_sort_uuid)}",tags=f"Slice:Slice:process:{os.path.basename(self.file)}:{self.identify['order']}")
        self.output_progress_description(0,_("Start processing"))
        FileSystem.create_workspace(self.identify['name'])
        self.output_progress_description(1,_("Create workspace"))
        FileSystem.create_directory(self.identify['name'],"extracted")
        self.output_progress_description(2,_("Create extracted directory"))
        self._extract_path = FileSystem.open_file(self.identify['name'],"extracted",const.File_Return_Type.PATH)
        self.output_progress_description(3,_("Open extracted directory"))
        self.logger.info(f"Extracted frames saved to {self._extract_path}",tags=f"Slice:Slice:process:{os.path.basename(self.file)}:{self.identify['order']}")
        self.extract()
        self.output_progress_description(4,_("Extract frames"))
        for sing in FileSystem.ls_directory(self.identify['name'],"extracted"):
            self.file_list.append(FileSystem.open_file(self.identify['name'],sing,const.File_Return_Type.PATH))
        self.output_progress_description(5,_("Get extracted frames"))
        self.output_progress_description(6,_("Start stamping"))
        self.stamp()
        self.output_progress_description(7,_("Stamp frames"))
        self.output_progress_description(8,_("Process audio"))
        self.output()

        for files in self.file_list:
            os.remove(files)
        self.output_progress_description(16, _("Start output"))
        self._file_path = os.path.join(FileSystem.open_file(self.identify['name'],"output",const.File_Return_Type.PATH),f"{self.identify['order']}.{self.output_format}")
        self.output_progress_description(17, _("Create output path"))
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
                elif self.stamp_method == const.WatermarkAlgorithm.TEXT_GOUFEI:
                    self._result, self.attachment_data_result = watermarkstamper.guofei_text(image, self.watermark,
                                                                                    self.attachment_data)
                elif self.stamp_method == const.WatermarkAlgorithm.TEXT_FREQM:
                    self._result, self.attachment_data_result = watermarkstamper.freqmethod_text(image, self.watermark,
                                                                                   self.attachment_data)
                elif self.stamp_method == const.WatermarkAlgorithm.TEXT_RIVAGAN:
                    self._result, self.attachment_data_result = watermarkstamper.freqmethod_text(image, self.watermark,
                                                                                   self.attachment_data)
                else:
                    self._result = image
                os.remove(file)
                cv2.imwrite(file,self._result)
                self.logger.info(f"Stamped frame {number} saved to {file}",tags=f"Slice:Slice:stamp:{os.path.basename(self.file)}:{self.identify['order']}")
            else:
                pass
            index += 1
            self.stamp_callback(index / len(self.file_list))
        logger.success(f"Stamping Complete",tags=f"Slice:Slice:stamp:{os.path.basename(self.file)}:{self.identify['order']}")



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
                fc=self.FFmpegForeward,
                psy=self.FFmpegSelfAdaptive,
                two_pass=self.two_pass,
                output_format=self.output_format
            )
            self.output_progress_description(14, _("Error check"))
            if execute_command(["ffprobe", "-v", "error",output_video_path]) == 0:
                self.correct = True
                self.output_progress_description(15, _("Correct and Output"))
            else:
                self.ffmpeg_retry_count += 1
                if self.ffmpeg_retry_count >= 50:
                    self.output_progress_description(16, _("FFmpeg retry count exceeded"))
                    self.logger.error(f"FFmpeg retry count exceeded",tags=f"Slice:Slice:run:{os.path.basename(self.file)}:{self.identify['order']}")
                    raise SystemError(_("FFmpeg retry count exceeded"))
                self.output_progress_description(16, _("FFmpeg error, retry"))



    def run(self):
        self.logger.info(f"Start process {self.identify['order']}",tags=f"Slice:Slice:run:{os.path.basename(self.file)}:{self.identify['order']}")
        self.object = multiprocessing.Process(target=self.process)
        return self.object

    def start(self):
        self.logger.info(f"Start process {self.identify['order']}",tags=f"Slice:Slice:start:{os.path.basename(self.file)}:{self.identify['order']}")
        results = self.process()
        return results



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
        if st_N and msg:
            self.logger.debug(f"Output progress {st_N} {msg}",tags=f"Slice:Slice:output_progress_description:{os.path.basename(self.file)}:{self.identify['order']}")
        data = json.dumps(frame_format)
        networks.ipc_send(data,"127.0.0.1",self.ipc_port)

    def after_process(self):
        root_dir = FileSystem.open_file(self.identify['name'],"./",const.File_Return_Type.PATH)
        self.logger.info(f"Delete extracted directory {root_dir}",tags=f"Slice:Slice:after_process:{os.path.basename(self.file)}:{self.identify['order']}")
        shutil.rmtree(root_dir)



