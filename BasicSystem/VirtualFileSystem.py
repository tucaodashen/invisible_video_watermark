import time
import uuid
import os
import shutil
import psutil
import json
from pathlib import Path
from enum import Enum

from BasicSystem.NetworkLogSender import NetworkLogSender

with open("./default_port.txt","r") as f:
    default_port = int(f.read())
logger = NetworkLogSender(default_port)
logger.debug("Import over")

from BasicSystem.const import File_Return_Type

base_path = Path.cwd() / "WorkPath"
base_path.mkdir(parents=True, exist_ok=True)
logger.success(f"Base path: {base_path} has been created")


class WorkSpace:
    def __init__(self):
        self.mapping_list = {}
        self.identifys = {}

    """
    Functions related to work space management.
    """


    def create_workspace(self, name): # 创建基础工作目录
        s_uuid = uuid.uuid4()
        if self.mapping_list != {}:
            name_list = list(self.mapping_list.keys())
            if name in name_list:
                raise Exception(f"Workspace name {name} already exists")
            self.add_mapping({name: s_uuid})
        else:
            self.add_mapping({name: s_uuid})

        os.mkdir(f"{base_path}/{s_uuid}")
        logger.success(f"Workspace {name} has been created")

    def clone_workspace(self, name,new_name):
        name_list = list(self.mapping_list.keys())
        if name not in name_list:
            raise Exception(f"Workspace name {name} does not exist")
        else:
            self.create_workspace(new_name)
            shutil.copytree(f"{base_path}/{self.mapping_list[name]}", f"{base_path}/{self.mapping_list[new_name]}",dirs_exist_ok=True)
        logger.debug(f"Workspace {name} has been cloned to {new_name}")

    def destroy_workspace(self, name):
        try:
            c_uuid = self.mapping_list[name]
            shutil.rmtree(f"{base_path}/{c_uuid}")
            del self.mapping_list[name]
        except KeyError as ke:
            logger.error(f"Workspace name {name} does not exist.Details: {ke}")
        except Exception as e:
            logger.error(f"Unknown error: {e}")
        logger.debug(f"Workspace {name} has been destroyed")

    def after_processing(self): # 完成后删除所有目录
        shutil.rmtree(base_path)
        logger.debug(f"Base path: {base_path} has been deleted")

    def add_mapping(self, mapping):
        # 检查所有键是否已存在
        for key in mapping:
            if key in self.mapping_list:
                raise ValueError(f"Workspace '{key}' already exists")

        # 添加新映射
        self.mapping_list.update(mapping)
        logger.debug(f"Mapping has been updated: {self.mapping_list}")


    """
    Functions related to file operations.
    """
    def ls_directory(self,workspace, path):
        lsdir = []
        try:
            path_index = self.mapping_list[workspace]
            f_path = os.path.join(base_path, str(path_index), path)
            print(f_path)
            vdirs = []
            result = []
            for root, dirs, files in os.walk(f_path):
                # 打印当前目录下的所有文件
                for file in files:
                    fn = os.path.join(root, file)
                    vdirs.append(fn)

                # 打印当前目录下的所有子目录
                for dir in dirs:
                    dn = os.path.join(root, dir)
                    vdirs.append(dn)
            for i in vdirs:
                result.append(i.split(str(path_index))[1])
            logger.debug(f"List over!{result}")
            return result
        except KeyError:
            logger.error(f"Workspace '{workspace}' does not exist")
        except Exception as e:
            logger.error(f"Unknown error: {e}")


    def open_file(self,work_space,path,return_type : File_Return_Type):
        """
        A Function to open a file in virtual workspace.
        :param work_space: the name of the workspace
        :param path: the path of the file in the virtual workspace
        :param return_type: the return type of the function. Include sting,open-object,binary and attribute.
        :return: str or clas object.
        """
        if return_type == File_Return_Type.PATH:
            workspace = str(self.mapping_list[work_space])
            # 确保 path 不以反斜杠开头
            clean_path = path.lstrip('\\/')

            full_path = base_path / workspace / clean_path
            logger.debug(f"Open file with path mode.File path: {full_path}")
            return str(full_path)

        if return_type == File_Return_Type.ATTRIBUTE:
            pts = os.path.join(base_path, str(self.mapping_list[work_space]), path)
            path_obj = Path(pts)

            if not path_obj.exists():
                logger.error(f"File {path} does not exist")

            stat_info = path_obj.stat()
            logger.debug(f"Open file with attribute mode.File path: {pts}")

            return {
                "name": path_obj.name,
                "stem": path_obj.stem,  # 不带后缀的文件名
                "suffix": path_obj.suffix,  # 文件后缀
                "parent": str(path_obj.parent),
                "absolute_path": str(path_obj.absolute()),
                "size": stat_info.st_size,
                "is_file": path_obj.is_file(),
                "is_dir": path_obj.is_dir(),
                "last_modified": stat_info.st_mtime,
                "last_accessed": stat_info.st_atime,
                "created": stat_info.st_ctime,
                "readable": os.access(path, os.R_OK),
                "writable": os.access(path, os.W_OK),
                "executable": os.access(path, os.X_OK)
            }
        logger.error(f"No such return type.{return_type}")
        return None

    def remove_file(self,work_space,path):
        try:
            shutil.rmtree(f"{base_path}/{self.mapping_list[work_space]}/{path}")
            logger.debug(f"File {path} has been removed")
            return True
        except KeyError:
            logger.error(f"Workspace '{work_space}' does not exist")
        except OSError as e:
            logger.error(f"OS Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unknown error: {str(e)}")

    def create_directory(self,work_space,path):
        try:
            os.mkdir(f"{base_path}/{self.mapping_list[work_space]}/{path}")
            logger.debug(f"Directory {path} has been created")
            return True
        except KeyError:
            logger.error(f"Workspace '{work_space}' does not exist")
        except OSError as e:
            logger.error(f"OS Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unknown error: {str(e)}")

    def create_file(self,work_space,path):
        try:
            paths = Path(os.path.join(base_path, str(self.mapping_list[work_space]), path))
            if os.path.exists(paths.parent):
                with open(paths, 'a') as file:
                    pass
                logger.debug(f"File {path} has been created")
            else:
                self.create_directory(work_space,paths.parent)
                with open(paths, 'a') as file:
                    pass
                logger.debug(f"Directory {path} has been created")
        except KeyError:
            logger.error(f"Workspace '{work_space}' does not exist")

    def copy_to(self,workspace,path,target):
        try:
            if os.path.isdir(os.path.join(base_path,str(self.mapping_list[workspace]),path)):
                shutil.copytree(os.path.join(base_path,str(self.mapping_list[workspace]), path), os.path.join(base_path,str(self.mapping_list[workspace]),target),dirs_exist_ok=True)
            else:
                shutil.copy(os.path.join(base_path,str(self.mapping_list[workspace]), path), os.path.join(base_path,str(self.mapping_list[workspace]),target))
            logger.success(f"File {path} has been copied to {target}")

        except OSError as e:
            logger.error(f"OS Error: {str(e)}")

    def move_to(self,work_space,path,target):
        try:
            shutil.copytree(os.path.join(base_path, str(self.mapping_list[work_space]), path),
                            os.path.join(base_path, str(self.mapping_list[work_space]), target), dirs_exist_ok=True)
            shutil.rmtree(os.path.join(base_path, str(self.mapping_list[work_space]), path))
            logger.debug(f"File {path} has been moved to {target}")
        except OSError as e:
            logger.error(f"OS Error: {str(e)}")

    def import_file(self,work_space,path,target):
        try:
            if os.path.isdir(path):
                shutil.copytree(str(os.path.join(path)),os.path.join(base_path,str(self.mapping_list[work_space]), target),dirs_exist_ok=True)
            else:
                shutil.copy(str(path),os.path.join(base_path,str(self.mapping_list[work_space]), target))
            logger.debug(f"File {path} has been imported to {target}")
        except OSError as e:
            logger.error(f"OS Error: {str(e)}")


    def export_file(self,work_space,path,target):
        try:
            if os.path.isdir(path):
                shutil.copytree(os.path.join(base_path, str(self.mapping_list[work_space]), path),str(os.path.join(target)), dirs_exist_ok=True)
            else:
                shutil.copy(os.path.join(base_path, str(self.mapping_list[work_space]), path),str(os.path.join(target)))
            logger.debug(f"File {path} has been exported to {target}")
        except OSError as e:
            logger.error(f"OS Error: {str(e)}")


def test():
    ws = WorkSpace()
    ws.create_workspace("Project1")
    ws.create_workspace("Project2")
    ws.import_file("Project1", r"C:\Users\Tucao\Desktop\ultraresolution", "ua")
    ws.clone_workspace("Project1", "Project1-clone")
    print(ws.ls_directory("Project1-clone", ""))
    ws.destroy_workspace("Project1")
    ws.export_file("Project1-clone", "ua/ouuuu1.png", r"D:/")
    ws.create_directory("Project1-clone", "outs")
    ws.copy_to("Project1-clone", "ua/ouuuu1.png", "outs")
    print(ws.mapping_list)
    input()
    ws.after_processing()

FileSystem = WorkSpace()



if __name__ == '__main__':
    ws = WorkSpace()
    ws.create_workspace("Project1")
    ws.create_workspace("Project2")
    ws.import_file("Project1",r"C:\Users\Tucao\Desktop\ultraresolution","ua")
    ws.clone_workspace("Project1","Project1-clone")
    print(ws.ls_directory("Project1-clone", ""))
    ws.destroy_workspace("Project1")
    ws.export_file("Project1-clone","ua/ouuuu1.png",r"D:/")
    ws.create_directory("Project1-clone","outs")
    ws.copy_to("Project1-clone","ua/ouuuu1.png","outs")
    print(ws.mapping_list)
    input()
    ws.after_processing()