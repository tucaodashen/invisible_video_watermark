import platform
import socket
import psutil
import GPUtil
import cpuinfo
import json
from datetime import datetime
import uuid


def get_hardware_report():
    """
    生成当前设备的详细硬件报告

    Returns:
        dict: 包含所有硬件信息的字典
    """

    def get_system_info():
        """获取系统信息"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

            return {
                "操作系统": f"{platform.system()} {platform.release()}",
                "系统版本": platform.version(),
                "系统架构": platform.architecture()[0],
                "主机名": platform.node(),
                "处理器架构": platform.machine(),
                "启动时间": boot_time,
                "当前用户": psutil.Process().username(),
                "设备唯一标识": str(uuid.getnode())
            }
        except Exception as e:
            return {"错误": f"获取系统信息失败: {str(e)}"}

    def get_cpu_info():
        """获取CPU信息"""
        try:
            # 尝试使用py-cpuinfo获取详细信息
            try:
                cpu_details = cpuinfo.get_cpu_info()
                brand = cpu_details.get('brand_raw', '未知')
                features = cpu_details.get('flags', [])
            except:
                brand = platform.processor()
                features = []

            cpu_freq = psutil.cpu_freq()

            return {
                "处理器型号": brand,
                "物理核心数": psutil.cpu_count(logical=False),
                "逻辑核心数": psutil.cpu_count(logical=True),
                "当前频率": f"{cpu_freq.current:.2f} MHz" if cpu_freq else "未知",
                "最大频率": f"{cpu_freq.max:.2f} MHz" if cpu_freq else "未知",
                "最小频率": f"{cpu_freq.min:.2f} MHz" if cpu_freq else "未知",
                "CPU使用率": f"{psutil.cpu_percent(interval=1):.1f}%",
                "特性支持": features[:10]  # 只显示前10个特性
            }
        except Exception as e:
            return {"错误": f"获取CPU信息失败: {str(e)}"}

    def get_memory_info():
        """获取内存信息"""
        try:
            virtual_mem = psutil.virtual_memory()
            swap_mem = psutil.swap_memory()

            def bytes_to_gb(bytes_size):
                return bytes_size / (1024 ** 3)

            return {
                "物理内存": {
                    "总内存": f"{bytes_to_gb(virtual_mem.total):.2f} GB",
                    "可用内存": f"{bytes_to_gb(virtual_mem.available):.2f} GB",
                    "已使用": f"{bytes_to_gb(virtual_mem.used):.2f} GB",
                    "使用率": f"{virtual_mem.percent:.1f}%"
                },
                "交换内存": {
                    "总大小": f"{bytes_to_gb(swap_mem.total):.2f} GB",
                    "已使用": f"{bytes_to_gb(swap_mem.used):.2f} GB",
                    "使用率": f"{swap_mem.percent:.1f}%"
                }
            }
        except Exception as e:
            return {"错误": f"获取内存信息失败: {str(e)}"}

    def get_disk_info():
        """获取磁盘信息"""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "设备": partition.device,
                        "挂载点": partition.mountpoint,
                        "文件系统": partition.fstype,
                        "总空间": f"{usage.total / (1024 ** 3):.2f} GB",
                        "已用空间": f"{usage.used / (1024 ** 3):.2f} GB",
                        "可用空间": f"{usage.free / (1024 ** 3):.2f} GB",
                        "使用率": f"{usage.percent:.1f}%"
                    })
                except PermissionError:
                    continue

            # 获取磁盘IO信息
            disk_io = psutil.disk_io_counters()
            io_info = {
                "读取次数": disk_io.read_count if disk_io else "未知",
                "写入次数": disk_io.write_count if disk_io else "未知",
                "读取数据": f"{disk_io.read_bytes / (1024 ** 3):.2f} GB" if disk_io else "未知",
                "写入数据": f"{disk_io.write_bytes / (1024 ** 3):.2f} GB" if disk_io else "未知"
            }

            return {
                "分区信息": disks,
                "IO统计": io_info
            }
        except Exception as e:
            return {"错误": f"获取磁盘信息失败: {str(e)}"}

    def get_network_info():
        """获取网络信息"""
        try:
            # 获取网络接口信息
            interfaces = []
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                interface_info = {"接口名": interface_name, "地址列表": []}

                for address in interface_addresses:
                    if address.family == socket.AF_INET:  # IPv4
                        interface_info["地址列表"].append({
                            "类型": "IPv4",
                            "地址": address.address,
                            "掩码": address.netmask,
                            "广播": address.broadcast
                        })
                    elif address.family == socket.AF_INET6:  # IPv6
                        interface_info["地址列表"].append({
                            "类型": "IPv6",
                            "地址": address.address
                        })
                    elif address.family == psutil.AF_LINK:  # MAC地址
                        interface_info["MAC地址"] = address.address

                interfaces.append(interface_info)

            # 获取网络IO统计
            net_io = psutil.net_io_counters()
            io_stats = {
                "发送字节": f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
                "接收字节": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB",
                "发送包数": net_io.packets_sent,
                "接收包数": net_io.packets_recv
            }

            return {
                "网络接口": interfaces,
                "IO统计": io_stats
            }
        except Exception as e:
            return {"错误": f"获取网络信息失败: {str(e)}"}

    def get_gpu_info():
        """获取GPU信息"""
        try:
            gpus = []
            try:
                # 使用GPUtil获取GPU信息
                gpu_list = GPUtil.getGPUs()
                for gpu in gpu_list:
                    gpus.append({
                        "ID": gpu.id,
                        "名称": gpu.name,
                        "显存": f"{gpu.memoryTotal} MB",
                        "已用显存": f"{gpu.memoryUsed} MB",
                        "显存使用率": f"{gpu.memoryUtil * 100:.1f}%",
                        "GPU使用率": f"{gpu.load * 100:.1f}%",
                        "温度": f"{gpu.temperature} °C"
                    })
            except:
                # 如果GPUtil失败，尝试其他方法
                gpus.append({"状态": "GPU信息获取失败或没有GPU"})

            return gpus
        except Exception as e:
            return {"错误": f"获取GPU信息失败: {str(e)}"}

    def get_running_processes():
        """获取运行中的进程信息"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append({
                        "PID": proc.info['pid'],
                        "名称": proc.info['name'],
                        "内存使用率": f"{proc.info['memory_percent']:.2f}%",
                        "CPU使用率": f"{proc.info['cpu_percent']:.1f}%"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # 按内存使用率排序，取前10个
            processes.sort(key=lambda x: float(x['内存使用率'].rstrip('%')), reverse=True)
            return processes[:10]
        except Exception as e:
            return {"错误": f"获取进程信息失败: {str(e)}"}

    # 生成完整报告
    report = {
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "系统信息": get_system_info(),
        "CPU信息": get_cpu_info(),
        "内存信息": get_memory_info(),
        "磁盘信息": get_disk_info(),
        "网络信息": get_network_info(),
        "GPU信息": get_gpu_info(),
    }

    return report


def print_hardware_report(report=None):
    """
    以友好格式打印硬件报告

    Args:
        report (dict, optional): 硬件报告字典，如果为None则生成新报告
    """
    if report is None:
        report = get_hardware_report()

    print("=" * 60)
    print("设备硬件详细报告")
    print("=" * 60)
    print(f"报告生成时间: {report['生成时间']}")
    print()

    for category, info in report.items():
        if category == "生成时间":
            continue

        print(f"【{category}】")
        if isinstance(info, dict):
            for key, value in info.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}:")
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                for k, v in item.items():
                                    print(f"    {k}: {v}")
                            else:
                                print(f"    {item}")
                            print("    " + "-" * 40)
                    else:
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                else:
                    print(f"  {key}: {value}")
        elif isinstance(info, list):
            for item in info:
                if isinstance(item, dict):
                    for k, v in item.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"  {item}")
                print("  " + "-" * 40)
        else:
            print(f"  {info}")
        print()


def save_report_to_file(report=None, filename=None):
    """
    将硬件报告保存到JSON文件

    Args:
        report (dict, optional): 硬件报告字典
        filename (str, optional): 文件名，如果为None则使用时间戳
    """
    if report is None:
        report = get_hardware_report()

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hardware_report_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"硬件报告已保存到: {filename}")
    except Exception as e:
        print(f"保存文件失败: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 生成硬件报告
    hardware_report = get_hardware_report()

    # 打印报告
    print_hardware_report(hardware_report)

    # 保存到文件
    save_report_to_file(hardware_report)

    # 也可以直接获取JSON字符串
    report_json = json.dumps(hardware_report, ensure_ascii=False, indent=2)
    print("JSON格式的报告已生成")