#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import time
from UI.Ginger import *

class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    #结束按钮触发时间
    def onPushButtonClick_stop(self):
        stopTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.lineEdit_stop_time.setText(stopTime)
