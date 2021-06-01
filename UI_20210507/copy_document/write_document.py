#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
import os
import subprocess
import sys
import copy_document.device as device
import copy_document.IP200_setup as IP200_setup
import copy_document.copy_map as copy_map
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
from UI.Ginger import *
import time

#建立新的线程,用来监控外部程序运行,并且会生成tmp.txt
class TextBrowser_thred(QThread):
    signal = pyqtSignal(str)

    def __init__(self, TextBrowser_win, data):
        self.data = data
        self.TextBrowser_win = TextBrowser_win
        super().__init__()

    def run(self):
        while self.data.poll is not None:
            template = self.data.stdout.readline()
            outputs = bytes.decode(template)
            self.signal.emit(str(outputs))
            if outputs == '':
               break



class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    #定义信号和槽,调用时触发
    def start_button_click(self):
        self.TextBrowser_show = TextBrowser_thred(self.textBrowser, self.data)
        #msg = self.TextBrowser_show.run.outputs
        self.TextBrowser_show.signal.connect(self.TextBrowser_show_text)
        self.TextBrowser_show.start()

    #定义槽函数,接受外部程序运行结果,生成tmp.txt
    def TextBrowser_show_text(self, msg):
        self.textBrowser.append(msg)
        try:
            f = open('tmp.txt', 'a', encoding='utf-8')
            f.write(msg)
            f.close()
        except Exception as e:
            print(e)

    def write_document(self):
        testStatusText_device = device.MyWin.copydevice(self)
        if testStatusText_device == 'PASS':
           testStatusText_IP200 = IP200_setup.MyWin.IP200(self)
           if testStatusText_IP200 == 'PASS':
              time.sleep(5)
              testStatusText_map = copy_map.MyWin.map(self)
              if testStatusText_map == 'PASS':
                 testStatusText = 'PASS'
                 self.lineEdit_teststatus.setText(testStatusText)
                 self.lineEdit_teststatus.setStyleSheet("background-color:green")
              else:
                 testStatusText = 'Fail'
                 self.lineEdit_teststatus.setText(testStatusText)
                 self.lineEdit_teststatus.setStyleSheet("background-color:red")
           else:
               testStatusText = 'Fail'
               self.lineEdit_teststatus.setText(testStatusText)
               self.lineEdit_teststatus.setStyleSheet("background-color:red")





