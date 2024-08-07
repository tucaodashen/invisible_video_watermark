import shutil
import time
import sys
import os
import AutoDep


def cost_time(func):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'func {func.__name__} cost time:{time.perf_counter() - t:.8f} s')
        return result

    return fun


class auto_pyinstaller:
    def __init__(self,pythonfile,is_console,is_debug,target_path,icon_file):
        self.pythonfile = pythonfile
        self.is_console = is_console
        self.is_debug = is_debug
        self.target_path = target_path
        self.icon_file = icon_file


    def github_action(self):
        pass


    @cost_time
    def compile_start(self):
        #os.mkdir("Pyinstaller")
        if self.is_console:
            console_arg = "-c"
        else:
            console_arg = "-w"
        if self.is_debug:
            debug_arg = "--debug "
        else:
            debug_arg = ""
        of_arg = ""
        if self.icon_file != "":
            shutil.copy(self.icon_file,os.getcwd())
            icon_arg = "-i "+os.path.split(self.icon_file)[1]
        else:
            icon_arg = ""
        command = os.path.split(sys.executable)[0]+"/"+"Scripts/" + f"pyinstaller {of_arg} {console_arg} {debug_arg} {icon_arg} {self.pythonfile}"
        print(command)
        AutoDep.run_command(command)
    def after(self):
        #print(os.getcwd()+"/dist/"+os.path.splitext(os.path.basename(self.pythonfile))[0])
        st = AutoDep.copy_path(os.getcwd()+"/dist/"+os.path.splitext(os.path.basename(self.pythonfile))[0],self.target_path,'overwrite')
        if st == 1:
            shutil.rmtree("build")
            shutil.rmtree("dist")


if __name__ == '__main__':
    buildinstance = auto_pyinstaller(r"D:\KoharuPyEasyBuild\build_test\app.py",True,False,"D:\pv","D:\KoharuPyEasyBuild\edHeadI.jpg")
    buildinstance.compile_start()
    buildinstance.after()
