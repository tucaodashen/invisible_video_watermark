from loguru import logger
import time
import os
import uuid

# 创建日志目录
if not os.path.exists("./logs"):
    os.makedirs("./logs")

temp = {
    "project_name":None,
    "project_UUID":None,
    "process_trace":{"process_UUID":None,"process_name":None}
}

ids = uuid.uuid4()  # 重命名避免覆盖内置函数id()
LOGNAME = f"log_{time.strftime('%Y-%m-%d-%H%M%S')}_{ids}.log"
logger.add(f"./logs/{LOGNAME}", level="DEBUG")
