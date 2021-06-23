# coding=UTF-8
from PyQt5.Qt import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
import subprocess
import time
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
from UI.Ginger import *


# 建立新的线程,用来监控外部程序运行,并且会生成tmp.txt
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

    # 定义信号和槽,调用时触发
    def start_button_click(self):
        self.TextBrowser_show = TextBrowser_thred(self.textBrowser, self.data)
        self.TextBrowser_show.signal.connect(self.TextBrowser_show_text)
        self.TextBrowser_show.start()

    # 定义槽函数,接受外部程序运行结果,生成tmp.txt
    def TextBrowser_show_text(self, msg):
        self.textBrowser.append(msg)
        try:
            f = open('tmp.txt', 'a', encoding='utf-8')
            f.write(msg)
            f.close()
        except Exception as e:
            print(e)

    def copydevice(self):
        testStatusText_device = ''
        model_name = self.lineEdit_modelName.text()
        if model_name == 'Ginger1.0.x':
            QMessageBox.information(None, '机器确认', 'Ginger1.0不需要复制device文件', QMessageBox.Ok)
        else:
            if os.path.exists('tmp.txt'):
                time.sleep(1)
                os.remove('tmp.txt')
            if os.path.exists('Ginger_UI_log.txt'):
                time.sleep(1)
                os.remove('Ginger_UI_log.txt')
            self.textBrowser.clear()
            Begintext = '开始测试'
            self.textBrowser.append(Begintext)
            startResult = QMessageBox.information(None, '机器确认', '请确认机器已开机且连接网线', QMessageBox.Yes | QMessageBox.No)
            testStatusText = '测试中'
            self.lineEdit_teststatus.setText(testStatusText)
            self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
            if startResult == QMessageBox.No:
                testStatusText_device = 'Fail'
                self.lineEdit_teststatus.setText(testStatusText_device)
                self.lineEdit_teststatus.setStyleSheet("background-color:red")
            elif startResult == QMessageBox.Yes:
                self.textBrowser.append('复制device文件')
                self.data = subprocess.Popen('../copy_document/scp_device.sh', stdout=subprocess.PIPE,
                                             stdin=subprocess.PIPE,
                                             shell=True)
                MyWin.start_button_click(self)
                while not self.TextBrowser_show.isFinished():
                    time.sleep(0.5)
                    QApplication.processEvents()
                time.sleep(1)
                with open('tmp.txt', 'r') as deviceFile:
                    devicefailkeyword1 = 'No route to host'
                    devicefailkeyword2 = '0 passed, 2 failed'
                    devicepasskeyword = '100%'
                    for tempdevice in deviceFile.readlines():
                        if devicefailkeyword1 in tempdevice or devicefailkeyword2 in tempdevice:
                            testStatusText_device = 'Fail'
                            self.lineEdit_teststatus.setText(testStatusText_device)
                            self.lineEdit_teststatus.setStyleSheet("background-color:red")
                            self.textBrowser.append('复制device文件失败')
                            with open('tmp.txt', 'r') as tmpfile:
                                with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                                    for line in tmpfile:
                                        Gingerfile.write(line)
                            if os.path.exists('tmp.txt'):
                                time.sleep(1)
                                os.remove('tmp.txt')
                            testresult = 'Fail'
                            errorcode = 'copy_device_fail'
                            stop_button.MyWin.onPushButtonClick_stop(self)
                            total_time.MyWin.Total_Test_time(self)
                            UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                            save_UI_logfile.MyWin.Self_logfile(self, testresult)
                            break
                        elif devicepasskeyword in tempdevice:
                            testStatusText_device = 'PASS'
                            self.lineEdit_teststatus.setText(testStatusText_device)
                            self.lineEdit_teststatus.setStyleSheet("background-color:green")
                            self.textBrowser.append('复制device文件成功')
                            with open('tmp.txt', 'r') as tmpfile:
                                with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                                    for line in tmpfile:
                                        Gingerfile.write(line)
                            if os.path.exists('tmp.txt'):
                                time.sleep(1)
                                os.remove('tmp.txt')
                            testresult = 'PASS'
                            errorcode = 'copy_device_PASS'
                            UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                            break
        return testStatusText_device
