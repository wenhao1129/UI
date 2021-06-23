#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import datetime
from datetime import datetime
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    #计算测试时间
    def Total_Test_time(self):
        TotalstartTime = self.lineEdit_start_time.text()
        TotalstopTime = self.lineEdit_stop_time.text()
        deltatime = datetime.strptime(TotalstopTime,'%Y-%m-%d %H:%M:%S') - datetime.strptime(TotalstartTime,'%Y-%m-%d %H:%M:%S')
        Total_test_time = str(deltatime)
        self.lineEdit_test_time.setText(Total_test_time)
