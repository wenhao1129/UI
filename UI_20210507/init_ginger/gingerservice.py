#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import subprocess
import time
from UI.Ginger import *


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

    # 机器启动Ginger服务
    def startGingerservice(self):
        if os.path.exists('tmp.txt'):
            time.sleep(1)
            os.remove('tmp.txt')
        if os.path.exists('Ginger_UI_log.txt'):
            time.sleep(1)
            os.remove('Ginger_UI_log.txt')
        self.textBrowser.append('开始启动Ginger服务')
        self.data = subprocess.Popen('../init_ginger/ginger_start_service.sh', stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        self.progressBar.setMinimum(0)  # 设置进度条最小值
        self.progressBar.setMaximum(60)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 进度条初始值为0
        for i in range (1, 61):
            time.sleep(1)
            self.progressBar.setValue(i)
        #time.sleep(60)
        with open('tmp.txt', 'r') as tempserviceFile:
            tempserviceline = tempserviceFile.readlines()
            tempservicefailkeyword = 'Connection timed out'
            tempservicepasskeyword1 = 'The ginger test service is starting'
            tempservicepasskeyword2 = 'The ginger test service has started'
            for tempservice in tempserviceline:
                if tempservicefailkeyword in tempservice:
                    testStatusText = 'Fail'
                    self.lineEdit_teststatus.setText(testStatusText)
                    self.lineEdit_teststatus.setStyleSheet("background-color:red")
                    self.textBrowser.append('启动Ginger服务失败')
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger service test start                              \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    with open('tmp.txt', 'r') as tmpfile:
                        with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                            for line in tmpfile:
                                Gingerfile.write(line)
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger service test closed                              \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    if os.path.exists('tmp.txt'):
                        time.sleep(1)
                        os.remove('tmp.txt')
                    tempstartGingerserviceresult = 'fail'
                    return tempstartGingerserviceresult
                elif tempservicepasskeyword1 in tempservice or tempservicepasskeyword2 in tempservice:
                    self.textBrowser.append('启动Ginger服务成功')
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger service test start                              \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    with open('tmp.txt', 'r') as tmpfile:
                        with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                            for line in tmpfile:
                                Gingerfile.write(line)
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger service test closed                              \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    if os.path.exists('tmp.txt'):
                        time.sleep(1)
                        os.remove('tmp.txt')
                    tempstartGingerserviceresult = 'pass'
                    return tempstartGingerserviceresult


