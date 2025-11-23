import uuid

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
from BasicSystem.VirtualFileSystem import FileSystem


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
    print(*args, **kwargs)
class ExtracUnit:
    def __init__(self,video,pkl):
        self.executor = ConcurrentExecutor()
        self.plk_data = pickle.load(open(pkl, 'rb'))
        self.frame_count = get_frame_count(video)
        self.video = video
        self._slice_list = []
        self._slice_length = 4

    def generate_slice(self):
        print("0")
        a = spitter(self.frame_count,self._slice_length)
        print(a)
        for ranges in a:
            self._slice_list.append(ExtractSlice(
                video=self.video,
                frame_range=ranges,
                attachment_data=self.plk_data['attachment_data'],
                method=self.plk_data['watermark_method']
            ))

    def run(self):
        print("1")
        self.generate_slice()
        result = self.executor.execute_concurrently(self._slice_list, 32,dummy)
        return self.post_process(result)

    def run_debug(self):
        result = []
        self.generate_slice()
        for i in self._slice_list:
            result.append(i.start())
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
        else:
            text_result = []
            for texts in result:
                if texts:
                    for item in texts:
                        text_result.append(item)
            ret_result = group_text(text_result)
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
        print("saved")
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

    def start(self):
        print("2")
        frame_list = []
        for i in range(self.frame_range[0],self.frame_range[1]+1):
            frame_list.append(i)
        self._frame_data = get_video_frames(self.video, frame_list)
        self.decode()
        return self._result

    def decode(self):
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
                        except:
                            raise
                    elif self.method == WatermarkAlgorithm.TEXT_GOUFEI:
                        try:
                            print("GUOFEI")
                            result = goufei_text_decoder(arr,atta)
                            # self._result.append(result)
                            if not result.count("�")/len(result) >= 0.2:
                                self._result.append(result)
                        except (ValueError,ZeroDivisionError):
                            pass
                        except:
                            raise
                    elif self.method == WatermarkAlgorithm.TEXT_RIVAGAN:
                        try:
                            result = rivagan_text_decoder(arr,atta)
                        except UnicodeDecodeError:
                            result = None
                        except:
                            raise
                        self._result.append(result)
        del self._frame_data



# t=float(input(""))
# v=5
# try:
#     it = int(t)
#     s=int(60*t*v)
# except:
#     it = float(t)
#     s = float(60 * t * v)
#
# print("移动的距离为",s,"秒")
if __name__ == '__main__':
    eu = ExtracUnit(r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\tet_ruia\embedded.mov",
                    r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\tet_ruia\recover.pkl")
    result = eu.run()
    for i in result:
        print(i)



