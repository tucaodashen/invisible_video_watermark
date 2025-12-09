from datetime import datetime
from typing import List


def sort_logs(log_lines: List[str]) -> List[str]:
    """
    更高效的排序版本，预先提取所有时间戳
    """
    # 创建(时间戳, 日志行)对的列表
    log_pairs = []
    for line in log_lines:
        timestamp_str = line.split(" | ")[0]
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        log_pairs.append((timestamp, line))

    # 按时间戳排序
    log_pairs.sort(key=lambda x: x[0])

    # 返回排序后的日志行
    return [line for _, line in log_pairs]

class LogProcessor:
    def __init__(self,log_file:str) -> None:
        self.log_file = log_file
        self.log_lines = []
        self.available_level = []
        self.read_log()

    def read_log(self):
        with open(self.log_file,"r",encoding="utf-8") as f:
            log_lines = f.readlines()
        for i in log_lines:
            if len(i.split("|")) == 4:
                self.log_lines.append(i)

    def extract_modules_tag(self):
        modules_tag = []
        for line in self.log_lines:
            lime_split = str(line).split("|")
            modules_tag.append(lime_split[2])

    def extract_usable_level(self):
        for i in self.log_lines:
            if len(str(i).split("|")) >= 2:
                cur_level = (str(i).split("|")[1]).replace(" ","").lower()
                if cur_level not in self.available_level:
                    self.available_level.append(cur_level)

    def output_process_unit_logs(self,task,level,process):
        non_sorted_log = []
        final_lost = []
        #Slice
        for i in self.log_lines:
            PrimaryTarget = f"Slice:Slice"
            SecondaryTarget = f"{task}"
            if PrimaryTarget in i:
                if SecondaryTarget in i:
                    if int(process) != 0:
                        if int((str(i).split("|")[2]).split(":")[-1]) == int(process):
                            non_sorted_log.append(str(i).replace("\n",""))
                    else:
                        non_sorted_log.append(str(i).replace("\n",""))
        #ProcessUnit
        for i in self.log_lines:
            PrimaryTarget = f"ProcessUnit:ProcessUnit"
            SecondaryTarget = f"{task}"
            if PrimaryTarget in i:
                if SecondaryTarget in i:
                    non_sorted_log.append(str(i).replace("\n",""))
        for ia in sort_logs(non_sorted_log):
            if str(ia).split("|")[1].replace(" ","").lower() in level:
                final_lost.append(ia)
        return final_lost

    def output_extract_unit_logs(self,task,level,process):
        non_sorted_log = []
        final_lost = []
        #Slice
        for i in self.log_lines:
            PrimaryTarget = f"ExtractUnit:ExtractSlice"
            SecondaryTarget = f"{task}"
            if PrimaryTarget in i:
                if SecondaryTarget in i:
                    if int(process) != 0:
                        if int((str(i).split("|")[2]).split(":")[-1]) == int(process):
                            non_sorted_log.append(str(i).replace("\n",""))
                    else:
                        non_sorted_log.append(str(i).replace("\n",""))
        #Unit
        for i in self.log_lines:
            PrimaryTarget = f"ExtractUnit:ExtractUnit"
            SecondaryTarget = f"{task}"
            if PrimaryTarget in i:
                if SecondaryTarget in i:
                    non_sorted_log.append(str(i).replace("\n",""))
        #decoder
        for i in self.log_lines:
            it = str(i).split("|")
            if len(it) == 4:
                if "watermark" in str(i).split("|")[2]:
                    non_sorted_log.append(str(i).replace("\n",""))
        for ia in sort_logs(non_sorted_log):
            if str(ia).split("|")[1].replace(" ","").lower() in level:
                final_lost.append(ia)
        return final_lost
    def output_main_process_logs(self,level):
        non_sorted_log = []
        final_lost = []
        for i in self.log_lines:
            if "main" in str(i).split("|")[2]:
                non_sorted_log.append(str(i).replace("\n",""))
        for ia in sort_logs(non_sorted_log):
            if str(ia).split("|")[1].replace(" ","").lower() in level:
                final_lost.append(ia)
        return final_lost

    def get_all_embed_task(self):
        available_task = []
        for i in self.log_lines:
            if "ProcessUnit:ProcessUnit" in i:
                task = str(i).split("|")[2].split(":")[-1]
                if task not in available_task:
                    available_task.append(task)
        return available_task

    def get_all_extract_task(self):
        available_task = []
        for i in self.log_lines:
            if "ExtractUnit:ExtractUnit" in i:
                task = str(i).split("|")[2].split(":")[-1]
                if task not in available_task:
                    available_task.append(task)
        return available_task




if __name__ == "__main__":
    log_processor = LogProcessor(r"D:\Project\Python\InvisibleVideoWatermarkNEXT\InvisibleVideoWatermarkNEXT\logs\app_20251206_203720.log")
    log_processor.extract_usable_level()
    print(log_processor.available_level)
    log_processor.output_process_unit_logs("short.mp4",["error"],"0")
    resu = log_processor.output_extract_unit_logs("embedded.mp4",["debug","info"],"1")
    # resu = log_processor.get_all_extract_task()
    for i in resu:
        print(i)

