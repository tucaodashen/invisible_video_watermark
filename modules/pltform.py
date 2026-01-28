from functools import cache
import cpuinfo
from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="pltform", enable_udp=True, enable_console=True)
logger = get_logger()


def get_nvidia_gpu():
    try:
        import subprocess
        # 尝试运行 nvidia-smi 获取显卡名称
        cmd = "nvidia-smi --query-gpu=name --format=csv,noheader"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        if output:
            return {output: "nvidia"}
    except Exception:
        pass
    return {}

@cache
def get_render_devices():
    device_list = {}

    # 1. 获取 CPU 信息
    try:
        info = cpuinfo.get_cpu_info()
        device_list.update({info.get('brand_raw', '未知'): "cpu"})
    except Exception as e:
        logger.error(f"CPU信息获取失败: {e}")
        device_list.update({"Unknown CPU": "cpu"})

    try:
        from pyadl import ADLManager

        instance = ADLManager.getInstance()
        if instance:
            devices = instance.getDevices()
            for device in devices:
                adapter_name = str(device.adapterName).replace("b'", "").replace("'", "")
                if "AMD" in adapter_name.upper():
                    device_list.update({adapter_name: "amd"})
    except Exception as e:
        logger.warning(f"AMD 设备检测跳过 (可能无AMD显卡或驱动): {e}")

    device_list.update(get_nvidia_gpu())

    logger.info(f"获取到渲染设备列表: {device_list}", tags="pltform:get_render_devices")
    return device_list


if __name__ == "__main__":
    devices = get_render_devices()
    for name, dev_type in devices.items():
        print(f"设备: {name} | 类型: {dev_type}")