from pyadl import ADLManager
import cpuinfo
from functools import cache
from BasicSystem.log_client import setup_logger,get_logger
setup_logger(default_tags="pltform", enable_udp=True, enable_console=True)
logger = get_logger()


@cache
def get_render_devices():
    device_list = {}
    info = cpuinfo.get_cpu_info()
    device_list.update({info.get('brand_raw', '未知'): "cpu"})
    devices = ADLManager.getInstance().getDevices()
    for device in devices:
        if "AMD" in str(device.adapterName):
            device_list.update({str(device.adapterName).replace("b'", "").replace("'", ""):"amd"})
        elif "NVIDIA" in str(device.adapterName):
            device_list.update({str(device.adapterName).replace("b'", "").replace("'", ""):"nvidia"})
        else:
            pass
    logger.info(f"Get render devices {device_list}",tags="pltform:get_render_devices")
    return device_list


if __name__ == "__main__":
    for i in get_render_devices():
        print(i)

