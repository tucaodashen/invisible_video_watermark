import shutil
import os
import zipfile
import tarfile
DOWNLOAD_DIR = "downloads"  # 文件下载存放的目录
EXTRACTION_DIR = "./"  # 文件解压到的目标目录
def extract_archive(file_path, destination_dir):
    """
    根据文件后缀解压文件到指定目录。
    """
    # 确保解压目录存在
    os.makedirs(destination_dir, exist_ok=True)
    print(f"\n🚀 准备将文件解压到目录: {destination_dir}")

    try:
        if file_path.endswith('.zip'):
            # 处理 .zip 文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)
            print("✅ .zip 文件解压成功。")

        elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
            # 处理 .tar.gz 文件
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(destination_dir)
            print("✅ .tar.gz 文件解压成功。")

        else:
            print(f"⚠️ 文件 {os.path.basename(file_path)} 不是支持的压缩格式 (.zip, .tar.gz)，跳过解压。")
            return False

        return True

    except (zipfile.BadZipFile, tarfile.ReadError) as e:
        print(f"❌ 解压文件时发生错误: 压缩包可能已损坏或格式不正确。错误信息: {e}")
        return False
    except Exception as e:
        print(f"❌ 解压过程中发生未知错误: {e}")
        return False


def pre_process():
    exclude_dic = ["FFmpeg","preset","config.json","AobaUpdater.exe","AobaUpdater","aoba_updater.py","download","lua_script"]
    file_list = os.listdir("./")
    for i in file_list:
        if i not in exclude_dic:
            if os.path.isdir(i):
                shutil.rmtree(i)
            else:
                os.remove(i)

def update():
    # 执行所有操作
    pre_process()
    extract_archive("download/archive.zip", "./")
    os.remove("download/archive.zip")
    if os.path.exists("download/AobaUpdater.exe"):
        os.remove("download/AobaUpdater.exe")

if __name__ == "__main__":
    update()

