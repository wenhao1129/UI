#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
import os
import subprocess
import time
import configparser
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile_without_server as slws
import handle_log.save_UI_logfile_without_server as sulws
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

    def navigation_go(self):
        self.data = subprocess.Popen('../reliability/navigation_go.sh', stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        self.textBrowser.append('Go is already closed')
        with open('tmp.txt', 'r') as NavigationFile:
            Navigationfailkeyword1 = '2 passed, 1 failed'
            Navigationfailkeyword2 = '1 passed, 2 failed'
            Navigationfailkeyword3 = '0 passed, 3 failed'
            Navigationpasskeyword = '3 passed, 0 failed'
            for tempsetup in NavigationFile.readlines():
                if Navigationfailkeyword1 in tempsetup or Navigationfailkeyword2 in tempsetup or Navigationfailkeyword3 in tempsetup:
                    testStatusText_navigo = 'Fail'
                    self.lineEdit_teststatus.setText(testStatusText_navigo)
                    self.lineEdit_teststatus.setStyleSheet("background-color:red")
                    self.textBrowser.append('导航失败')
                    if os.path.exists('tmp.txt'):
                        time.sleep(1)
                        os.remove('tmp.txt')
                    stop_button.MyWin.onPushButtonClick_stop(self)
                    total_time.MyWin.Total_Test_time(self)
                    slws.MyWin.outer_logfile(testStatusText_navigo)
                    sulws.MyWin.Self_logfile(testStatusText_navigo)
                    break
                elif Navigationpasskeyword in tempsetup:
                    testStatusText_navigo = 'PASS'
                    self.lineEdit_teststatus.setText(testStatusText_navigo)
                    self.lineEdit_teststatus.setStyleSheet("background-color:green")
                    if os.path.exists('tmp.txt'):
                        time.sleep(1)
                        os.remove('tmp.txt')
                    stop_button.MyWin.onPushButtonClick_stop(self)
                    total_time.MyWin.Total_Test_time(self)
                    slws.MyWin.outer_logfile(testStatusText_navigo)
                    sulws.MyWin.Self_logfile(testStatusText_navigo)
        return testStatusText_navigo
