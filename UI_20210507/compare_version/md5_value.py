#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import subprocess
import time
import configparser
import hashlib
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
from UI.Ginger import *

config = configparser.ConfigParser()
config.read("../config/config.ini")
robot_factory_tool_path = config.get("TestlogPath", "robot_factory_tool")
Ginger_test_env_path = config.get("TestlogPath", "Ginger_test_env")


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

    def code_md5(data):
        #self.data = data
        new_md5 = hashlib.md5()
        new_md5.update(data.encode('utf8'))
        md5_value = new_md5.hexdigest()
        return md5_value

    def txt_md5(fileMd5):
        import hashlib
        md5_value = hashlib.md5()
        with open(fileMd5, 'rb') as f:
            while True:
                  data = f.read(2048)
                  if not data:
                         break
                  md5_value.update(data)
        return md5_value.hexdigest()

    def compare_version(self):
        #self.textBrowser.clear()
        data1 = '../version/original/ccu_version.txt'
        md5_value1 = MyWin.txt_md5(data1)
        data11 = '../version/backup/temp_ccu_version.txt'
        md5_value11 = MyWin.txt_md5(data11)
        self.textBrowser.append('ccu version:')
        self.textBrowser.append(md5_value1)
        self.textBrowser.append(md5_value11)
        data2 = '../version/original/ecu_version.txt'
        md5_value2 = MyWin.txt_md5(data2)
        data22 = '../version/backup/temp_ecu_version.txt'
        md5_value22 = MyWin.txt_md5(data22)
        self.textBrowser.append('ecu version:')
        self.textBrowser.append(md5_value2)
        self.textBrowser.append(md5_value22)
        data3 = '../version/original/sca_version.txt'
        md5_value3 = MyWin.txt_md5(data3)
        data33 = '../version/backup/temp_sca_version.txt'
        md5_value33 = MyWin.txt_md5(data33)
        self.textBrowser.append('sca version:')
        self.textBrowser.append(md5_value3)
        self.textBrowser.append(md5_value33)
        data4 = '../version/original/iris_camera.txt'
        md5_value4 = MyWin.txt_md5(data4)
        data44 = '../version/backup/temp_iris_camera.txt'
        md5_value44 = MyWin.txt_md5(data44)
        self.textBrowser.append('supernode version:')
        self.textBrowser.append(md5_value4)
        self.textBrowser.append(md5_value44)