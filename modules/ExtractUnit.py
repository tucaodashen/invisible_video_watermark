import sys
import threading
import uuid
import coredumpy
from PySide6.QtCore import Signal, QObject
from modules.decorator import timer_decorator
from av.error import InvalidDataError
from modules.text_postprocess import group_text
from modules.PyAv import extract_video_frames as get_video_frames
from modules.PyAv import group_similar_images
from modules.VideoProcessor import spitter, get_frame_count
from modules.ProcessSchedulerSusFec import ConcurrentExecutor
from modules.watermarkdecoder import firekeeper_image_decoder,guofei_image_decoder,goufei_text_decoder,freqm_text_decoder,rivagan_text_decoder
from BasicSystem.const import *
import os
import cv2
import pickle
import modules.networks as network
from BasicSystem.VirtualFileSystem import FileSystem
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="ExtractUnit", enable_udp=True, enable_console=True)
logger = get_logger()


def remove_duplicates(lst):
    seen = set()
    unique = []
    for d in lst:
        # 将字典的键值对转换为frozenset
        frozen = frozenset(d.items())
        if frozen not in seen:
            seen.add(frozen)
            unique.append(d)
    return unique

def dummy(*args, **kwargs):
    logger.debug(f"dummy function called with args: {args}, kwargs: {kwargs}",tags="ExtractUnit:dummy")
class ExtracUnit(QObject):
    update_progress = Signal(float)
    receive_result = Signal()
    def __init__(self, video, pkl, max_worker=6):
        super().__init__()
        self.executor = ConcurrentExecutor()
        self.plk_data = pickle.load(open(pkl, 'rb'))
        self.frame_count = get_frame_count(video)
        self.video = video
        self._slice_list = []
        self._slice_length = 4
        self.progress = 0
        self.cur = 0
        self.total = 1
        self.max_worker = max_worker
        self.dump_uuid = uuid.uuid4()
        self.result = None



    def generate_slice(self):
        threading.Thread(target=network.ipc_recv, args=("127.0.0.1", 1165, self.calcu_progress)).start()
        a = spitter(self.frame_count,self._slice_length)
        logger.debug(f"generate slice {a}",tags="ExtractUnit:ExtractUnit:generate_slice")
        id = 0
        self.total = len(a)
        for ranges in a:
            id += 1
            inst = ExtractSlice(
                video=self.video,
                frame_range=ranges,
                attachment_data=self.plk_data['attachment_data'],
                method=self.plk_data['watermark_method']
            )
            inst.dump_uuid = self.dump_uuid
            inst.identify = {"order":id}
            self._slice_list.append(inst)
            logger.debug(f"append slice {id} {ranges}",tags="ExtractUnit:ExtractUnit:generate_slice")




    @timer_decorator
    def run(self):
        self.generate_slice()
        logger.debug(f"start extract slice",tags="ExtractUnit:ExtractUnit:run")
        result = self.executor.execute_concurrently(self._slice_list, self.max_worker,dummy)
        network.ipc_send("exit", "127.0.0.1", 1165)
        _result = self.post_process(result)
        self.result = _result
        self.receive_result.emit()
        logger.debug(f"extract slice running over",tags="ExtractUnit:ExtractUnit:run")
        return _result


    def calcu_progress(self,msg,a):
        if msg == "Over":
            self.cur += 1
            self.progress = self.cur / self.total
        self.update_progress.emit(self.progress)


    def run_debug(self):
        result = []
        self.generate_slice()
        for i in self._slice_list:
            result.append(i.start())
            logger.debug(f"extract slice {i.identify} {i.frame_range} result {i._result}",tags="ExtractUnit:ExtractUnit:run_debug")
        return self.sort_result(result)

    def post_process(self,result):
        if self.plk_data['watermark_method'] == WatermarkAlgorithm.IMAGE_GUOFEI or self.plk_data['watermark_method'] == WatermarkAlgorithm.IMAGE_FIREKEEPER:
            pp = []
            for aa in result:
                for ig in aa:
                    pp.append(ig)
            sorted = group_similar_images(pp)
            ret_result = []
            for imgset in sorted:
                if len(imgset) >= 1:
                    ret_result += imgset
            logger.debug(f"post processed length {len(ret_result)}",tags="ExtractUnit:ExtractUnit:post_process")
        else:
            text_result = []
            for texts in result:
                if texts:
                    for item in texts:
                        text_result.append(item)
            ret_result = group_text(text_result)
            logger.debug(f"post process {ret_result}",tags="ExtractUnit:ExtractUnit:post_process")

        return ret_result


    def sort_result(self,result,thresholds=0.9):
        FileSystem.create_workspace("extract")
        FileSystem.create_directory("extract","extract_frames")
        path = FileSystem.open_file("extract", "extract_frames", File_Return_Type.PATH)
        ahh_result = []
        for i in result:
            for img in i:
                ahh_result.append(img)
        for imgs in ahh_result:
            cv2.imwrite(imgs,os.path.join(path,f"{str(uuid.uuid4())}.png"))
        logger.success(f"save {len(ahh_result)} images to {path}",tags="ExtractUnit:ExtractUnit:sort_result")
        for i in os.listdir(path):
            pass
        return None



class ExtractSlice:
    def __init__(self,video,frame_range,attachment_data,method):
        self.video = video
        self.frame_range = frame_range
        self.attachment_data = attachment_data
        self._frame_data = None
        self._result = []
        self.method = method
        self.identify = None
        self.dump_uuid = None


    def start(self):
        try:
            result = self._start()
            return result
        except Exception as e:
            path = f"./dumps/coredumpy_{os.path.basename(self.video)}_{self.identify['order']}_{self.dump_uuid}.dump"
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
                logger.error(f"extract slice {self.identify} {self.frame_range} error {e}",tags=f"ExtractUnit:ExtractUnit:start:{os.path.basename(self.video)}:{self.identify['order']}")
                coredumpy.dump(frame=exception_frame,
                               description="Exception trigger frame only"
                               , path=path, depth=4)

                # 打印确认位置
                logger.error(f"exception frame {exception_frame.f_code.co_filename}:{exception_frame.f_lineno}",tags=f"ExtractUnit:ExtractUnit:start:{os.path.basename(self.video)}:{self.identify['order']}")
            else:
                logger.error(f"extract slice {self.identify} {self.frame_range} error {e}",tags=f"ExtractUnit:ExtractUnit:start:{os.path.basename(self.video)}:{self.identify['order']}")
                coredumpy.dump(description="No traceback available", path=path, depth=4)
            raise

    def _start(self):
        logger.debug(f"extract slice {self.identify} {self.frame_range}",tags=f"ExtractUnit:ExtractUnit:start:{os.path.basename(self.video)}:{self.identify['order']}")
        frame_list = []
        for i in range(self.frame_range[0],self.frame_range[1]+1):
            frame_list.append(i)
        self._frame_data = get_video_frames(self.video, frame_list)
        self.decode()
        return self._result

    def decode(self):
        logger.debug(f"decode {self.identify} {self.frame_range}",tags=f"ExtractUnit:ExtractUnit:decode:{os.path.basename(self.video)}:{self.identify['order']}")
        for arr in self._frame_data:
            for atta in remove_duplicates(self.attachment_data):
                if arr is not None:
                    if self.method == WatermarkAlgorithm.IMAGE_GUOFEI:
                        self._result.append(guofei_image_decoder(arr,atta))
                    elif self.method == WatermarkAlgorithm.IMAGE_FIREKEEPER:
                        resu,yuv = firekeeper_image_decoder(arr,atta)
                        self._result.append(resu)
                        self._result.append(yuv[0])
                        self._result.append(yuv[1])
                        self._result.append(yuv[2])
                    elif self.method == WatermarkAlgorithm.TEXT_FREQM:
                        try:
                            result,valid = freqm_text_decoder(arr,atta)
                            if valid:
                                self._result.append(result)
                        except (UnicodeDecodeError,InvalidDataError):
                            pass
                        except Exception as e:
                            logger.error(f"decode {self.identify} {self.frame_range} error {e}",tags=f"ExtractUnit:ExtractUnit:decode:{os.path.basename(self.video)}:{self.identify['order']}")
                            raise
                    elif self.method == WatermarkAlgorithm.TEXT_GOUFEI:
                        try:
                            result = goufei_text_decoder(arr,atta)
                            # self._result.append(result)
                            if not result.count("�")/len(result) >= 0.2:
                                self._result.append(result)
                        except (ValueError,ZeroDivisionError):
                            pass
                        except Exception as e:
                            logger.error(f"decode {self.identify} {self.frame_range} error {e}",tags=f"ExtractUnit:ExtractUnit:decode:{os.path.basename(self.video)}:{self.identify['order']}")
                            raise
                    elif self.method == WatermarkAlgorithm.TEXT_RIVAGAN:
                        try:
                            result = rivagan_text_decoder(arr,atta)
                        except UnicodeDecodeError:
                            result = None
                        except Exception as e:
                            logger.error(f"decode {self.identify} {self.frame_range} error {e}",tags=f"ExtractUnit:ExtractUnit:decode:{os.path.basename(self.video)}:{self.identify['order']}")
                            raise
                        self._result.append(result)
        network.ipc_send("Over","127.0.0.1",1165)
        del self._frame_data






if __name__ == '__main__':
    eu = ExtracUnit(
        r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\ImageBenchmark\embedded.mp4",
        r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\ImageBenchmark\recover.pkl")
    result = eu.run()
    for i in result:
        path = r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\ImageBenchmark\bench"
        cv2.imwrite(os.path.join(path, f"{str(uuid.uuid4())}.png"), i)
        #print(i)




