from functools import cache
import cpuinfo
from BasicSystem.log_client import setup_logger, get_logger

setup_logger(default_tags="pltform", enable_udp=True, enable_console=True)
logger = get_logger()


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

    # 2. 尝试获取 AMD 显卡 (使用 pyadl)
    try:
        # 延迟导入，只有在调用函数时才尝试加载 pyadl
        from pyadl import ADLManager

        instance = ADLManager.getInstance()
        if instance:
            devices = instance.getDevices()
            for device in devices:
                adapter_name = str(device.adapterName).replace("b'", "").replace("'", "")
                if "AMD" in adapter_name.upper():
                    device_list.update({adapter_name: "amd"})
                elif "NVIDIA" in adapter_name.upper():
                    device_list.update({adapter_name: "nvidia"})
    except Exception as e:
        # 如果没有 AMD 显卡，pyadl 会报 ADLError
        # 这里我们捕获它，记录日志并跳过，确保程序不崩溃
        logger.warning(f"AMD 设备检测跳过 (可能无AMD显卡或驱动): {e}")

    # 3. 如果你需要更准确地检测 NVIDIA 显卡，建议在此处额外添加 nvidia-smi 的逻辑
    # 目前保持你原有的逻辑结构

    logger.info(f"获取到渲染设备列表: {device_list}", tags="pltform:get_render_devices")
    return device_list


if __name__ == "__main__":
    devices = get_render_devices()
    for name, dev_type in devices.items():
        print(f"设备: {name} | 类型: {dev_type}")