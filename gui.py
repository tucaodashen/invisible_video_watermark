from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget,QFileDialog
from PySide6.QtCore import Qt,QTime,QTimer,QThread,Signal,QObject,Slot,QRunnable,QThreadPool
import json
from gui.ui_mainwindows import Ui_MainWindow
from gui.ui_recognise import Ui_recongise
from gui.ui_genqrcode import  Ui_genqrcode
from gui.ui_gentextimg import  Ui_gentextimg
from gui.ui_recover import Ui_readwm
from gui.ui_about import Ui_Formabout
from gui.ui_splash import Ui_splashfr
from gui.ui_manul import Ui_manul
import main
import pil
import core
import gui.res_rc

class workThread(QThread): #视频合成的多线程

    def __init__(self,watermark,video,filname,sen,samolelist,peroid,filetype,kbps,maxkbps,videotype,outputtype,processtype,watermarkquality):
        super().__init__()
        print("run")
        self.watermark=watermark
        self.video=video
        self.filename=filname
        self.sen=sen
        self.sampleplit=samolelist
        self.peroid=peroid
        self.filetype=filetype
        self.kbps=kbps
        self.maxkbps=maxkbps
        self.videotype=videotype
        self.outputtype=outputtype
        self.processtype=processtype
        self.watermarkquality=watermarkquality

    def run(self):
        main.process(self.watermark,
                     self.video,
                     self.filename,
                     self.sen,
                     self.sampleplit,
                     self.peroid,
                     self.filetype,
                     self.kbps,
                     self.maxkbps,
                     self.videotype,
                     self.outputtype,
                     self.processtype,
                     self.watermarkquality)
class recover(QThread): #恢复水印用多线程
    ressignal=Signal(str)
    def __init__(self,input,jsonfile,type):
        super().__init__()
        self.input=input
        self.type=type
        self.recoverfile=jsonfile
    def run(self):
        print("sdsd")
        self.result=str(main.recorver(self.recoverfile,self.input,self.type))
        self.ressignal.emit(self.result)
class initthread(QThread):  #初始化防止卡死
    signal=Signal(bool)
    def __init__(self):
        super().__init__()
    def run(self):
        print("init")
        main.initial()
        print("over")
        self.signal.emit(True)



class MainWindows(QMainWindow,Ui_MainWindow):
    def __init__(self):
        self.videopath=""
        self.wmpath=""
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.progressbar)
        self.timer.start(1000)
        #self.pushButton.clicked.connect(self.show_new_window)
        self.button()
        self.inputp()
        self.threadpool = QThreadPool()
        #self.work.deleteLater()

    def hello(self):
        print("helloworld")
    def button(self):
        self.buton_start.clicked.connect(self.start)
        self.browservideo.clicked.connect(self.browservideofunc)
        self.browserimage.clicked.connect(self.imagepath)
        self.recqrcode.triggered.connect(self.recqr)
        self.genqrcode.triggered.connect(self.genqr)
        self.genimg.triggered.connect(self.gentx)
        self.recover.triggered.connect(self.rec)
        self.about.triggered.connect(self.abo)
        self.stopbutton.clicked.connect(self.sto)
        self.manr.triggered.connect(self.man)
    def recqr(self):
        self.w = recogqrcode()
        self.w.show()
    def genqr(self):
        self.w = genqrcode_()
        self.w.show()
    def gentx(self):
        self.w = gentext()
        self.w.show()
    def rec(self):
        self.w=recwm()
        self.w.show()
    def abo(self):
        self.w=about()
        self.w.show()
    def man(self):
        self.w=manulrecover()
        self.w.show()
    def sto(self):
        self.worksto = initthread()
        self.worksto.start()
    def progressbar(self):
        try:
            with open("progress.json", 'r',errors='ignore',encoding='utf-8') as f:
                self.pdata = json.load(f)
            self.operation_label.setText(self.pdata['operation'])
            self.processbar_bo.setValue(self.pdata['cent'])
        except:
            self.pdata={'cent':0,'operation':"等待中......"}
            self.operation_label.setText(self.pdata['operation'])
            self.processbar_bo.setValue(self.pdata['cent'])

    def browservideofunc(self):
        self.videopath = QFileDialog.getOpenFileName(self, "选择输入视频文件", "", "mp4 文件(*.mp4);;mkv 文件(*.mkv);;avi 文件(*.avi);;flv 文件(*.flv)")
        self.videofile.setText(str(self.videopath[0]))
        self.videopath1=self.videofile.text()
    def imagepath(self):
        self.wmpath = QFileDialog.getOpenFileName(self, "选择输入水印文件", "",
                                                         "png 文件(*.png);;jpg 文件(*.jpg);;jpeg 文件(*.jpeg);;bmp 文件(*.bmp)")
        self.imagefile.setText(self.wmpath[0])
        self.wmpath1=self.imagefile.text()
    def inputp(self):
        self.mtype=str(self.filttype.currentText())
        self.videotype = str(self.vtype.currentText())
        self.wmquality = str(self.wm_quality.text())
        self.videoname = str(self.output.text())
        self.sampletimes=str(self.sampletime.text())
        self.peroids=str(self.peroid.text())
        self.deskpbs=str(self.dkbps.text())
        self.mkpbs=str(self.maxkbps.text())
        if self.imagewm.isChecked():#进行类型判断
            self.wmtype="image"
        else:
            self.wmtype="text"
        if str(self.comboBox.currentText())=="视频":
            self.outtype="video"
        else:
            self.outtype="image"
    def start(self):
        self.inputp()
        self.work=workThread(self.wmpath1,self.videopath1,self.videoname,0,self.sampletimes,self.peroids,self.mtype,self.deskpbs,self.mkpbs,self.videotype,self.outtype,self.wmtype,int(self.wmquality))
        self.work.start()
        #main.process(self.wmpath[0],self.videopath[0],self.videoname,0,self.sampletimes,self.peroids,self.mtype,self.deskpbs,self.mkpbs,self.videotype,self.outtype,self.wmtype,int(self.wmquality))


class recogqrcode(QWidget, Ui_recongise): #识别二维码
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.select)
        self.pushButton_2.clicked.connect(self.rec)
    def select(self):
        self.wmpath = QFileDialog.getOpenFileName(self, "选择输入水印文件", "",
                                                  "png 文件(*.png);;jpg 文件(*.jpg);;jpeg 文件(*.jpeg);;bmp 文件(*.bmp)")
        self.lineEdit.setText(self.wmpath[0])
    def rec(self):
        self.result=str(pil.recognize(self.wmpath[0]))
        self.label_3.setText(self.result)
class genqrcode_(QWidget, Ui_genqrcode): #生成二维码
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.gen)
    def gen(self):
        self.text=self.lineEdit.text()
        self.pix=int(self.spinBox.text())
        pil.genqrcode(self.text,self.pix)
class gentext(QWidget, Ui_gentextimg): #生成文字图
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.gen)
    def gen(self):
        self.res=[int(self.spinBox.text()),int(self.spinBox_2.text())]
        self.text=str(self.lineEdit.text())
        pil.makeimage(self.text,self.res,self.text)

class recwm(QWidget, Ui_readwm): #识别水印
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.selectj)
        self.pushButton_2.clicked.connect(self.selectv)
        self.pushButton_3.clicked.connect(self.start)
        if self.comboBox.currentText()=="图片":
            self.type="image"
        else:
            self.type="text"


    def selectv(self):
        self.videopath = QFileDialog.getOpenFileName(self, "选择输入视频文件", "", "mp4 文件(*.mp4);;mkv 文件(*.mkv);;avi 文件(*.avi);;flv 文件(*.flv)")
        self.lineEdit_2.setText(self.videopath[0])
    def selectj(self):
        self.jsonpath = QFileDialog.getOpenFileName(self, "选择配置文件", "","json 文件(*.json)")
        self.lineEdit.setText(self.jsonpath[0])
    def start(self):
        self.work=recover(self.videopath[0],self.jsonpath[0],self.type)
        self.work.start()
        self.work.ressignal.connect(self.set)
    def set(self,rec):
        self.label_5.setText(rec)


class about(QWidget, Ui_Formabout):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.timer = QTimer()
        #self.timer.timeout.connect(self.isclo)
        #self.timer.start(50)

    def mousePressEvent(self, event):
        self.close()
class splashwindow(QWidget,Ui_splashfr):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.st)
        self.timer.start(3500)
        self.work = initthread()
        self.work.start()
        self.work.signal.connect(self.recsig)
    def recsig(self,mes):
        try:
            self.isover=mes
        except:
            self.isover=False
    def st(self):
        if self.isover:
            self.mw=MainWindows()
            self.mw.show()
            self.close()
            self.timer.stop()
        else:
            pass
class manulrecover(QWidget,Ui_manul):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.rec)
    def rec(self):
        self.seed1=int(self.lineEdit_2.text())
        self.seed2=int(self.lineEdit_3.text())
        self.qua=int(self.lineEdit_4.text())
        self.path=str(self.lineEdit.text())
        self.senw=int(self.lineEdit_5.text())
        self.senh=int(self.lineEdit_6.text())
        self.sen=[self.senw,self.senh]
        core.decodewatermark_image(self.path,self.sen,[self.seed1,self.seed2,self.qua])





if __name__ =="__main__":
    app=QApplication([])
    #window=MainWindows()
    #window.show()
    window=splashwindow()
    window.show()
    app.exec()