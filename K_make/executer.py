import os
import sys
import uuid
import io

import json
import auto_nuitka
import auto_pyinstaller
import AutoDep
import shutil


# 将标准输出和标准错误的编码设置为 utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class execute():
    def __init__(self):
        self.config = self._load_config()
        self.build_instance = None
        self.project_path = None
        self.entrance = None
        self.target = os.getcwd()+"/"+"_output"

        self._load_config()
        self.get_path()

    def get_path(self):
        base_dir = os.getcwd()
        self.project_path = os.path.split(base_dir)[0]
        self.entrance = self.project_path + "/" + self.config['main_entrance']

        print(self.project_path)
        print(self.entrance)

    def _load_config(self):
        with open('make_config.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def run(self):
        if self.config['generator_type'] == 'pyinstaller':
            self.build_instance = auto_pyinstaller.auto_pyinstaller(self.entrance,self.config['console'],self.config['debug'],self.target,self.config['icon'])
            self.build_instance.compile_start()
            self.build_instance.after()
            dtf = AutoDep.auto_data_files(self.project_path)
            for i in dtf:
                if os.path.isdir(i):
                    AutoDep.copy_path(i, self.target + "/" + os.path.basename(i), mode="merge")
                else:
                    shutil.copy(i, self.target)
            if self.config['attached_data'] != "":
                AutoDep.release_zip(os.path.basename(self.config['attached_data']), self.target)
        else:
            self.build_instance = auto_nuitka.AutoNuitka(self.project_path, self.entrance, self.config['mode'])
            self.build_instance.get_buildin_package()
            self.build_instance.get_pypi_package()
            self.build_instance.enabled_plugin = self.config['enabled_plugin']
            self.build_instance.disabled_pypi = self.config['disabled_pypi']
            self.build_instance.target_path = self.target
            if self.config['icon'] is not None:
                self.build_instance.compile_start("GCC", self.config['uac'], False, False, self.config['console'],
                                                  os.path.basename(self.config['icon']), "A")
            else:
                self.build_instance.compile_start("GCC", self.config['uac'], False, False, self.config['console'],
                                                  "", "A")
            AutoDep.copy_path(
                os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".dist",
                self.target)
            self.build_instance.copy_adding()
            dtf = AutoDep.auto_data_files(self.project_path)
            for i in dtf:
                if os.path.isdir(i):
                    AutoDep.copy_path(i, self.target + "/" + os.path.basename(i), mode="merge")
                else:
                    shutil.copy(i, self.target)
            shutil.rmtree(
                os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".dist")
            shutil.rmtree(
                os.getcwd() + "/" + os.path.splitext(os.path.basename(self.build_instance.entrance))[0] + ".build")

            if self.config['attached_data'] != "":
                AutoDep.release_zip(os.path.basename(self.config['attached_data']), self.target)

    def zip_output(self):
        AutoDep.zip_directory("_output","output.zip")


if __name__ == '__main__':
    bi = execute()
    bi.run()
    bi.zip_output()
