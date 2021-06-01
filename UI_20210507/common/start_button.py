#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import time
import station.station as station
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

   #开始按钮触发时间和运行所选站位程序
    def onPushButtonClick_start(self):
        self.lineEdit_stop_time.clear()
        self.lineEdit_test_time.clear()
        testStatusText = ''
        self.lineEdit_teststatus.setText(testStatusText)
        startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.lineEdit_start_time.setText(startTime)
        station.MyWin.onChooseStation(self)
