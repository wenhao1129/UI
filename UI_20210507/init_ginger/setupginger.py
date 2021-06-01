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

    #初始化setup机器
    def setupGinger(self):
        #测试tmp.txt文件是否存在,如果存在删除
        if os.path.exists('tmp.txt'):
            time.sleep(1)
            os.remove('tmp.txt')
        if os.path.exists('Ginger_UI_log.txt'):
            time.sleep(1)
            os.remove('Ginger_UI_log.txt')
        self.textBrowser.append('开始初始化setup')
        #调用外部程序
        self.data = subprocess.Popen('../init_ginger/ginger_setup.sh', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        MyWin.start_button_click(self)
        testStatusText = '测试中'
        self.lineEdit_teststatus.setText(testStatusText)
        self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
        # 运行独立线程监控外部程序运行
        #QApplication.processEvents()保证不会卡顿和异常
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        #读取tmp.txt文件,并且判断是否包含关键字,从而判断pass还是fail
        with open ('tmp.txt', 'r') as setupFile:
            setupfailkeyword1 = '请插入网线连接测试机器'
            setupfailkeyword2 = '100% packet loss'
            setuppasskeyword = '0% packet loss'
            for tempsetup in setupFile.readlines():
                 if setupfailkeyword1 in tempsetup or setupfailkeyword2 in tempsetup :
                    testStatusText = 'Fail'
                    self.lineEdit_teststatus.setText(testStatusText)
                    self.lineEdit_teststatus.setStyleSheet("background-color:red")
                    self.textBrowser.append('初始化setup失败')
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger setup test start                              \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    with open('tmp.txt', 'r') as tmpfile:
                        with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                            for line in tmpfile:
                                Gingerfile.write(line)
                    templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                    templog.write('============================================================================\n')
                    templog.write('                       Ginger setup test closed                             \n')
                    templog.write('============================================================================\n')
                    templog.close()
                    if os.path.exists('tmp.txt'):
                        time.sleep(1)
                        os.remove('tmp.txt')
                    setupresult = 'fail'
                    return setupresult
                 elif setuppasskeyword in tempsetup:
                     self.textBrowser.append('初始化setup成功')
                     templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                     templog.write('============================================================================\n')
                     templog.write('                       Ginger setup test start                              \n')
                     templog.write('============================================================================\n')
                     templog.close()
                     with open('tmp.txt', 'r') as tmpfile:
                         with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                             for line in tmpfile:
                                 Gingerfile.write(line)
                     templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                     templog.write('============================================================================\n')
                     templog.write('                       Ginger setup test closed                             \n')
                     templog.write('============================================================================\n')
                     templog.close()
                     if os.path.exists('tmp.txt'):
                         time.sleep(1)
                         os.remove('tmp.txt')
                     setupresult = 'pass'
                     return setupresult

