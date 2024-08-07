"""
Nuitka的自动处理类
꒰ঌ(🎀 ᗜ`v´ᗜ 🌸)໒꒱💈✅
"""
import sys
import time



import AutoDep
import get_dep
import analysis_NDEP
import os
import shutil

import gettext
from rich import print
from rich.console import Console
from rich.table import Column, Table


def cost_time(func):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'func {func.__name__} cost time:{time.perf_counter() - t:.8f} s')
        return result

    return fun

class AutoNuitka:
    def __init__(self, project_path ,main_entrance ,mode='auto',command = ''):
        self.inc_arg = None
        self.analist_list = None
        self.path = project_path
        self.entrance = main_entrance

        self._filelist = []
        self._setup_error_table()
        self.console = Console()
        self.pypi_package = None
        self._1pass_pypi_package = None
        self.import_list = None
        self.buildin_package = None
        self.non_custom_package = None
        self.stdlib = None
        self.plugin_list = []
        self.error_list = []
        self.installed_pypi_dic = AutoDep.get_site_packages_info()
        self.ns_pypi_mapping_list = []
        self.site_dir = analysis_NDEP.get_site_packages_path()
        self.path_list = []
        self.target_path = "D:\copytest"

        self._is_pyx = False

        self.mode = mode
        self.manual_command = command
        self.compiler = None
        self.is_console = None
        self.is_debug = None
        self.icon = None
        self.UAC = None
        self.LTO = None
        self.l_memory = None
        self.req_std = []

        self.disabled_pypi = []  # 不编译的Pypi包
        self.included_py = []  # 自己的py文件
        self.additional_file = []  # 外部数据文件
        self.enabled_plugin = []  # 启用的插件
        self.additional_arguements = []  # 附加参数

        self.analyse_te_dic = {
            "name": "",
            "path": "",
            "associated": [],
            "cost_rate": 0
        }

    def _setup_error_table(self):
        self.error_table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        self.error_table.add_column("错误类型")
        self.error_table.add_column("报错内容")
        self.error_table.add_column("错误优先级", justify="right")

    def get_import(self):  # 这里获取的导入信息是包括自己写的模块的
        self.import_list = AutoDep.extract_imports_from_folder(self.path)

    def get_3rdp_package(self):  # 包括内置包和pypi包
        self.non_custom_package = AutoDep.extract_3rd_part_package_imports_from_dictionary(self.path)

    def get_pypi_package(self):
        self._1pass_pypi_package = []
        self.pypi_package = []
        self._stdlib = AutoDep.get_lib_files().keys()
        for i in self.non_custom_package:
            if i not in self.buildin_package:
                self._1pass_pypi_package.append(i)
        for i in self._1pass_pypi_package:
            if i not in self._stdlib:
                self.pypi_package.append(i)
        print(self._stdlib)

    def get_buildin_package(self):
        if self.non_custom_package is not None:
            self.buildin_package = AutoDep.get_std_lib(self.non_custom_package)
        else:
            self.get_3rdp_package()
            self.buildin_package = AutoDep.get_std_lib(self.non_custom_package)

    def get_essential_nuitka_plugin(self):
        if self.non_custom_package != None:
            # print(self.import_list)
            self.plugin_list = AutoDep.nuitka_plugin_filter(self.non_custom_package)
        else:
            self.get_3rdp_package()
            self.get_essential_nuitka_plugin()

    def print_error_table(self):
        self.error_list = AutoDep.error_list
        for i in self.error_list:
            currrow = list()
            if i["type"] == "ParseError":
                currrow.append("[green]ParseError[/green]")
            else:
                currrow.append("")
            currrow.append("[yellow]" + str(i["context"]) + "/yellow")
            if i["type"] == "ParseError":
                currrow.append("[green]一般无需处理[/green]")
            else:
                currrow.append("")
            self.error_table.add_row(currrow[0], currrow[1], currrow[2])
        self.console.print(self.error_table)

    def get_copy_list(self):
        need_copy_list = []
        analysis_list = []
        trans_list = []  # 需要映射的列表
        normal_list = []  # 不需要映射的列表
        json_data = analysis_NDEP.get_full_dependence()
        self.ns_pypi_mapping_list = analysis_NDEP.get_non_standard_package()
        dec = []
        for i in self.ns_pypi_mapping_list:
            dec += list(i.values())
        decision_list = analysis_NDEP.flatten_list(dec)  # 获取判断包名是否需要映射的决定列表
        # print(decision_list)

        for i in self.pypi_package:
            if i in decision_list:
                # print(i)
                trans_list.append(i)  # 将需要转换的加入列表
            else:
                normal_list.append(i)  # 其余的加入不需要转换的列表
        for i in trans_list:
            for di in self.ns_pypi_mapping_list:
                if i in analysis_NDEP.flatten_list(list(di.values())):
                    # print("a")
                    # print(i)
                    # print(str(list(di.keys())[0]))
                    analysis_list.append(str(list(di.keys())[0]).lower())
        # analysis_list += normal_list #合并
        for i in analysis_list:
            need_copy_list += get_dep.find_dependencies(json_data, i)
        # 获得完整依赖列表
        need_copy_list = list(set(need_copy_list))

        print(need_copy_list)

        # 转回对应文件夹
        nonspack = []
        for i in need_copy_list:
            for dicc in self.ns_pypi_mapping_list:
                if i == str(list(dicc.keys())[0]).lower():
                    print(str(i) + str(dicc))
                    nonspack.append(i)

                    for fi in list(list(dicc.values())[0]):
                        print(self.site_dir + "/" + str(fi))
                        if os.path.exists(self.site_dir + "/" + str(fi)):
                            print("exit")
                            self.path_list.append(self.site_dir + "/" + str(fi))
                        else:
                            print(self.site_dir + "/" + str(list(dicc.keys())[0]).replace("-", "_"))
                            if os.path.exists(self.site_dir + "/" + str(list(dicc.keys())[0]).replace("-", "_")):
                                print("name_exist")
                                self.path_list.append(self.site_dir + "/" + str(list(dicc.keys())[0]).replace("-", "_"))
                            # 获取所有非标准包路径

        print(nonspack)
        for i in nonspack:
            need_copy_list.remove(i)
        print(need_copy_list)
        need_copy_list += normal_list  # 合并规范包
        print(need_copy_list)
        for spack in need_copy_list:
            if os.path.exists(self.site_dir + "/" + str(spack)):
                self.path_list.append(self.site_dir + "/" + str(spack))
            else:
                if os.path.exists(self.site_dir + "/" + str(spack).replace("-", "_")):
                    self.path_list.append(self.site_dir + "/" + str(spack).replace("-", "_"))

        self.path_list = list(set(self.path_list))

        print(self.path_list)

        self.ana_result = self.analysis_std()  # 所有需要的库
        self.req_std = []
        for i in self.ana_result:
            if i in self._stdlib:
                self.req_std.append(i)

        for files in self._filelist:
            if os.path.splitext(files)[1] == ".pyx":
                self._is_pyx = True
    def copy_adding(self):
        if self._is_pyx:
            self.esay_STD()
        else:
            self.copy_std()
        self.copy_pypi()
        self.copy_loose()

    def esay_STD(self):
        self.all_std_lib_dir = AutoDep.get_lib_files().values()
        for i in self.all_std_lib_dir:
            if os.path.splitext(i)[1] != ".py" and os.path.basename(i) != "site-packages":
                AutoDep.copy_path(i, self.target_path + "/" + os.path.basename(i))
            if os.path.splitext(i)[1] == ".py" and os.path.basename(i) != "site-packages":
                shutil.copy(i, self.target_path)

    def copy_loose(self):
        clis = []
        loosefiles = os.listdir(self.site_dir)
        for i in loosefiles:
            if os.path.splitext(i)[1] == ".py":
                clis.append(i)
        for i in clis:
            AutoDep.copy_path(self.site_dir+"/"+i,self.target_path,mode='merge')


    def analysis_std(self):
        all = []

        for i in self.path_list:
            all += AutoDep.extract_3rd_part_package_imports_from_dictionary(i)
            self._filelist += self._get_all_files(i)  # 获取所有文件列表，以判断是否含有pyx

        return list(set(all))

    def copy_std(self):
        copy_list = []
        if self.req_std != []:
            for i in self.req_std:
                if os.path.exists(AutoDep.std_lib_path() + "/" + i):
                    print(i)
                    copy_list.append(AutoDep.std_lib_path() + "/" + i)
                else:
                    if os.path.exists(AutoDep.std_lib_path() + "/" + i + ".py"):
                        print(i + ".py")
                        copy_list.append(AutoDep.std_lib_path() + "/" + i + ".py")
            for na in copy_list:
                if os.path.splitext(na)[1] != ".py":
                    AutoDep.copy_path(na, self.target_path + "/" + os.path.basename(na))
                if os.path.splitext(na)[1] == ".py":
                    shutil.copy(na, self.target_path)

    def copy_pypi(self):
        for path in self.path_list:
            AutoDep.copy_path(path, self.target_path + "/" + os.path.basename(path))

    def _get_all_files(self, path):
        all_files_and_folders = []

        # 遍历目录树
        for root, dirs, files in os.walk(path):
            # 添加目录路径
            for dir in dirs:
                all_files_and_folders.append(os.path.join(root, dir))
            # 添加文件路径
            for file in files:
                all_files_and_folders.append(os.path.join(root, file))

        return all_files_and_folders


    def detect_self(self):
        det_list = []
        pys = os.listdir(self.path)
        for i in pys:
            if os.path.splitext(i)[1] == ".py":
                det_list.append(i)
        for i in det_list:
            self.included_py.append(os.path.splitext(i)[0])


    @cost_time
    def compile_start(self,complier,Uac,debug,lowmemory,console,icon,lto):
        self.autoadd = " "
        self.is_console = console
        self.UAC = Uac
        self.compiler = complier
        self.is_debug = debug
        self.l_memory = lowmemory
        self.inc_arg = None
        self.LTO = lto
        self.icon = icon
        self.command = ''
        self.display_args = " --show-progress --show-memory "
        self.head = "python"+" -m nuitka --standalone "
        if self.mode == 'auto_p':
            if self.included_py != []:
                inclue = " --include-module="
                for i in self.included_py:
                    inclue += i+","
                    include_args = inclue[:-1]
                    self.inc_arg = include_args
            else:
                self.inc_arg = ""
            if self.enabled_plugin != []:
                ep = " --enable-plugins="
                for i in self.enabled_plugin:
                    ep += i+","
                self.plugin_args = ep[:-1]
            else:
                self.plugin_args = ""
            if self.disabled_pypi != []:
                dp = " --nofollow-import-to="
                self.p_args = ""
                for i in self.disabled_pypi:
                    dp += i+","
                self.p_args = dp[:-1]
            else:
                self.p_args = ""


            if self.compiler == "GCC":
                self.c_args = " --mingw64"
            else:
                self.c_args = ""
            self.attached_args = " "
            if self.is_console:
                pass
            else:
                self.attached_args += "--windows-console-mode=attach "
            if self.is_debug:
                self.attached_args += "--debug "
            if self.l_memory:
                self.attached_args += "--low-memory "
            if self.icon != "":
                self.attached_args += "--windows-icon-from-ico="+str(self.icon)+" "
            if self.LTO == "Y":
                self.attached_args += "--lto=yes "
            if self.LTO == "N":
                self.attached_args += "--lto=no "
            self.end_args = self.entrance
            self.command = f"{self.head}{self.c_args}{self.display_args}{self.inc_arg}{self.p_args}{self.plugin_args}{self.attached_args}{self.end_args}{self.autoadd}"
            original_string = self.command
            cleaned_string = ''.join([line for line in original_string.splitlines()])
            print(cleaned_string)
            self.get_copy_list()
            AutoDep.run_command(cleaned_string)
        if self.mode == 'auto_np':
            if self.included_py != []:
                inclue = " --include-module="
                for i in self.included_py:
                    inclue += i+","
                    include_args = inclue[:-1]
                    self.inc_arg = include_args
            else:
                self.inc_arg = ""
            if self.enabled_plugin != []:
                ep = " --enable-plugins="
                for i in self.enabled_plugin:
                    ep += i+","
                self.plugin_args = ep[:-1]
            else:
                self.plugin_args = ""
            self.p_args = ""

            if self.compiler == "GCC":
                self.c_args = " --mingw64"
            else:
                self.c_args = ""
            self.attached_args = " "
            if self.is_console:
                pass
            else:
                self.attached_args += "--windows-console-mode=disable "
            if self.is_debug:
                self.attached_args += "--debug "
            if self.l_memory:
                self.attached_args += "--low-memory "
            if self.icon != "":
                self.attached_args += "--windows-icon-from-ico="+str(self.icon)+" "
            if self.LTO == "Y":
                self.attached_args += "--lto=yes "
            if self.LTO == "N":
                self.attached_args += "--lto=no "
            self.end_args = self.entrance
            self.command = f"{self.head}{self.c_args}{self.display_args}{self.inc_arg}{self.p_args}{self.plugin_args}{self.attached_args}{self.end_args}{self.autoadd}"
            original_string = self.command
            cleaned_string = ''.join([line for line in original_string.splitlines()])
            print(cleaned_string)
            AutoDep.run_command(cleaned_string)






if __name__ == "__main__":
    pass
    path = r"D:\invisible_video_watermark"
    bigpath = r"F:\solidworks\sd-webui-aki-v4.8"
    build_instance = AutoNuitka(path,"")
    build_instance.get_buildin_package()
    build_instance.get_pypi_package()
    build_instance.get_essential_nuitka_plugin()
    print(build_instance.buildin_package)
    print(build_instance.pypi_package)
    print(build_instance.plugin_list)
    # build_instance.print_error_table()
    build_instance.get_copy_list()
    #build_instance.copy_loose()
    build_instance.detect_self()
    build_instance.compile_start("GCC",False,False,False,True,"","A")
    # build_instance.analysis_compile_cost()
    # build_instance.esay_STD()
    # bild_instance.analysis_std()
