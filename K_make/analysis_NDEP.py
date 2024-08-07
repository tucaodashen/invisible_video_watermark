"""
为了解决一些Pypi包导入名和下载名不一致的问题
我是真的服了这些作者了....唉
虽然说也不是不能理解，但是Python的包是真的杂
"""

import os
import site
import json
import subprocess
import sys


def get_site_packages_path():
    # 获取site-packages目录的路径列表
    site_packages_paths = [p for p in site.getsitepackages()]
    return site_packages_paths[1]


def find_folders_with_top_level_txt(start_path):
    """
    遍历给定的起始路径，找到包含'top_level.txt'文件的所有文件夹路径。

    :param start_path: 要遍历的起始路径
    :return: 包含'top_level.txt'文件的文件夹路径集合
    """
    folders_with_file = set()  # 使用集合避免重复的路径
    for root, dirs, files in os.walk(start_path):
        if 'top_level.txt' in files:
            folders_with_file.add(root)  # 添加包含文件的根目录路径
    return folders_with_file


def get_download_name(path):
    if os.path.exists(path + "/" + "METADATA"):
        with open(path + "/" + "METADATA", 'r', encoding='utf-8') as file:
            for i in range(1, 2):
                next(file)
            raw_name = next(file)
        #print(raw_name)
        name = raw_name[6:]
        #print(name)
    else:
        cur_name = os.path.basename(str(path)).split("-")
        name = cur_name[0]
    return name


def get_import_name(path):
    ina = []
    lines = []
    fina = []
    with open(path + "\\" + "top_level.txt", 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    for ima in lines:
        ina += ima.split("\\")
    for inna in ina:
        fina += inna.split("/") # 细细地切做臊子（bushi
    return fina


def get_non_standard_package():
    li = []
    for i in find_folders_with_top_level_txt(get_site_packages_path()):
        cur_dic = {
            get_download_name(i).strip(): get_import_name(i)
        }
        li.append(cur_dic)

    return li
def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            # 如果项目是一个列表，则递归地将其扁平化
            flat_list.extend(flatten_list(item))
        else:
            # 如果项目不是列表，则直接添加到结果列表中
            flat_list.append(item)
    return flat_list

def get_full_dependence():
    # 使用subprocess.run来执行命令
    result = subprocess.run(sys.executable + " -m pipdeptree -j", shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    # 输出命令的返回值
    data = result.stdout
    with open("dependence.json", "w", encoding='utf-8') as file:
        file.write(data)

    with open('dependence.json') as json_file:
        json_data = json.load(json_file)
    return json_data

if __name__ == "__main__":
    for i in get_non_standard_package():
        print(i)
    print(get_site_packages_path())



