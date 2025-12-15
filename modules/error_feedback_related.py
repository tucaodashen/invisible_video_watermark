import datetime
import hashlib
import io
import os
import platform
import re
import shutil
import socket
import tarfile
import time

import psutil
import wmi
import zstandard as zstd
from copy import deepcopy

temple_path = "./error_packup"

def pack_error(error_list,is_device_info = False,output_path="./"):
    if os.path.exists(temple_path):
        shutil.rmtree(temple_path)
    os.mkdir(temple_path)
    log_list = []
    dump_list = []
    stack_list = []
    for i in error_list:
        if i[2] not in stack_list:
            stack_list.append({i[0]:i[2]})
        if i[4] not in log_list:
            log_list.append(i[4])
        for ia in i[3]:
            if ia not in dump_list:
                dump_list.append(ia)
    os.mkdir(os.path.join(temple_path, "log"))
    os.mkdir(os.path.join(temple_path, "dump"))
    os.mkdir(os.path.join(temple_path, "stack"))
    for du in dump_list:
        shutil.copy2(os.path.join("./dumps",du), os.path.join(temple_path, "dump"))
    for lg in log_list:
        shutil.copy2(lg, os.path.join(temple_path, "log"))
    for st in stack_list:
        timestamp = int(time.time())
        error_hash = hashlib.md5(str(list(st.keys())[0]).encode()).hexdigest()[:8]
        # 清理错误消息用于文件名
        clean_msg = re.sub(r'[<>:"/\\|?*]', '_', str(list(st.keys())[0])[:50])
        file_name = f'{timestamp}_{error_hash}_{clean_msg}.txt'
        with open(os.path.join(temple_path, "stack", file_name), "w") as f:
            f.write(list(st.values())[0])
    check_list = deepcopy(error_list)
    with open(os.path.join(temple_path, "check.txt"), "w") as f:
        for i in check_list:
            f.write(f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n")
    if is_device_info:
        with open(os.path.join(temple_path, "device.txt"), "w") as f:
            f.write(str(get_windows_system_info_for_report()))
    compress_dir_to_zst_memory(temple_path,output_path)
    shutil.rmtree(temple_path)
    os.mkdir(temple_path)


def compress_dir_to_zst_memory(source_dir, output_file, compression_level=22):
    """
    在内存中压缩目录，避免创建临时文件
    """
    if not output_file.endswith(('.tar.zst', '.zst')):
        output_file += '.tar.zst'

    print(f"正在压缩目录: {source_dir}")

    # 在内存中创建 tar 数据
    tar_buffer = io.BytesIO()

    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    tar_data = tar_buffer.getvalue()
    print(f"Tar归档大小: {len(tar_data) / 1024 / 1024:.2f} MB")

    # 压缩数据
    cctx = zstd.ZstdCompressor(level=compression_level)
    compressed_data = cctx.compress(tar_data)

    # 写入文件
    with open(output_file, 'wb') as f:
        f.write(compressed_data)

    print(f"压缩完成: {output_file}")
    print(f"压缩后大小: {len(compressed_data) / 1024 / 1024:.2f} MB")
    ratio = (1 - len(compressed_data) / len(tar_data)) * 100
    print(f"压缩率: {ratio:.1f}%")


def get_windows_system_info_for_report():
    """
    获取并返回当前 Windows 设备的详细硬件和软件信息，特别适用于错误报告。
    使用 wmi 获取 Windows 特有的精确数据。
    """
    info = {}

    # 检查是否在 Windows 环境运行
    if platform.system() != 'Windows':
        return {"Error": "此函数仅支持 Windows 操作系统。"}

    try:
        # 初始化 WMI 客户端
        c = wmi.WMI()
    except Exception as e:
        return {"Error": f"无法初始化 WMI：{e}. 请确保已安装 wmi 库。"}

    # --- 1. 报告元数据 ---
    info['Report_Timestamp'] = datetime.datetime.now().isoformat()
    boot_time_ts = psutil.boot_time()
    info['System_Boot_Time'] = datetime.datetime.fromtimestamp(boot_time_ts).strftime("%Y-%m-%d %H:%M:%S")

    # --- 2. 软件/操作系统环境 (WMI + platform) ---
    os_info = c.Win32_OperatingSystem()[0]

    # 使用 WMI 获取更准确的 Windows 版本名称
    info['OS_Name'] = os_info.Caption  # 通常返回 'Microsoft Windows 11...' 或 'Microsoft Windows 10...'
    info['OS_Build_Number'] = os_info.BuildNumber  # 用于精确识别 Windows 11
    info['OS_Architecture'] = os_info.OSArchitecture
    info['Python_Version'] = platform.python_version()

    # --- 3. CPU 硬件与状态 (WMI + psutil) ---
    cpu_info_wmi = c.Win32_Processor()[0]
    info['CPU_Hardware'] = {
        'CPU_Name': cpu_info_wmi.Name.strip(),
        'Physical_Cores': psutil.cpu_count(logical=False),
        'Total_Threads': psutil.cpu_count(logical=True),
        # MaxClockSpeed 是 WMI 提供的 CPU 最大频率
        'Max_Frequency_MHz': f"{cpu_info_wmi.MaxClockSpeed}.00"
    }
    # 获取瞬时使用率
    info['CPU_Usage_Percent'] = psutil.cpu_percent(interval=0.1)

    # --- 4. 内存 (RAM) 硬件与状态 (psutil) ---
    virtual_memory = psutil.virtual_memory()
    info['Memory'] = {
        'Total_Memory_GB': f"{virtual_memory.total / (1024 ** 3):.2f} GB",
        'Available_Memory_GB': f"{virtual_memory.available / (1024 ** 3):.2f} GB",
        'Used_Percent': virtual_memory.percent
    }

    # --- 5. 磁盘摘要 ---
    info['Disk_Summary'] = {}
    for disk in c.Win32_LogicalDisk(DriveType=3):  # DriveType=3 代表本地磁盘
        if disk.Caption == 'C:':
            usage = psutil.disk_usage(disk.Caption + '\\')
            info['Disk_Summary'][disk.Caption] = {
                'Volume_Name': disk.VolumeName or "N/A",
                'File_System': disk.FileSystem,
                'Total_Size_GB': f"{usage.total / (1024 ** 3):.2f} GB",
                'Used_Percent': usage.percent
            }
            break

    # --- 6. 网络连接信息 (WMI + socket) ---
    info['Network_Info'] = {
        'Host_Name': socket.gethostname(),
        'Local_IP': socket.gethostbyname(socket.gethostname()),
    }

    # WMI 获取 MAC 地址 (更可靠)
    nic_info = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    if nic_info:
        info['Network_Info']['MAC_Address'] = nic_info[0].MACAddress

    # --- 7. GPU/显卡信息 (WMI) ---
    gpu_list = []
    for gpu in c.Win32_VideoController():
        gpu_list.append({
            'Name': gpu.Name,
            'Adapter_RAM_MB': gpu.AdapterRAM / (1024 ** 2) if gpu.AdapterRAM else 0
        })
    info['GPU_Details'] = gpu_list

    # 移除或替换 Unix/Linux 特有指标
    info['System_Load_Average'] = "N/A (仅适用于 Unix/Linux)"

    return info


if __name__ == "__main__":
    compress_dir_to_zst_memory("dumps", "error_packup.zst")

