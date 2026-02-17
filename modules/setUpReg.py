import ctypes
import sys
import os
import winreg


def trigger_UAC():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return

    # Nuitka 编译后，sys.executable 就是你的 exe 路径
    executable = sys.executable

    # 如果有命令行参数，记得传给新进程
    # 对于右键菜单功能，这里通常是空的或者特定的安装指令
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])

    # 再次调用，这次带上 "runas"
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", executable, params, None, 1
    )

    if int(ret) <= 32:
        # 用户点了“否”
        sys.exit(1)
    else:
        # 新进程已启动，旧进程退出
        sys.exit(0)


def set_up_reg():
    menu_name = "我的 Python 图像工具"
    # 获取当前 EXE 的绝对路径
    exe_path = os.path.abspath(sys.executable)
    # 注册表路径：针对系统所有图片类型
    reg_path = r"SystemFileAssociations\image\shell\MyPythonTool"

    try:
        # 创建主菜单项
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, menu_name)
            # 可选：给菜单加个图标（指向 exe 本身）
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)

        # 创建执行命令项
        command_path = rf"{reg_path}\command"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path) as key:
            # "%1" 会被 Windows 替换为被选中的图片路径
            cmd_string = f'"{exe_path}" "%1"'
            winreg.SetValue(key, "", winreg.REG_SZ, cmd_string)

        print("注册成功！现在你可以右键点击图片查看效果了。")
        os.system("pause")  # 方便看结果
    except Exception as e:
        print(f"注册失败: {e}")
        os.system("pause")

def remove_reg():
    pass