#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
import os
import subprocess
import time
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
import init_ginger.setupginger as setup_ginger
import init_ginger.gingerservice as ginger_service
import data_local.count_testresult as count_testresult
import data_local.save_csv as save_csv
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

    def grasp(self):
        self.textBrowser.clear()
        Begintext = '开始测试'
        self.textBrowser.append(Begintext)
        startResult = QMessageBox.information(None,'机器确认','请确认机器已开机且连接网线',QMessageBox.Yes | QMessageBox.No)
        testStatusText = '测试中'
        self.lineEdit_teststatus.setText(testStatusText)
        self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
        if startResult == QMessageBox.No:
           testStatusText = 'Fail'
           self.lineEdit_teststatus.setText(testStatusText)
           self.lineEdit_teststatus.setStyleSheet("background-color:red")
           stop_button.MyWin.onPushButtonClick_stop(self)
           total_time.MyWin.Total_Test_time(self)
        elif startResult == QMessageBox.Yes:
             setupresult = setup_ginger.MyWin.setupGinger(self)
             if setupresult == 'fail':
                testStatusText = 'fail'
                self.lineEdit_teststatus.setText(testStatusText)
                self.lineEdit_teststatus.setStyleSheet("background-color:red")
                testresult = 'fail'
                errorcode = 'setup_fail'
                stop_button.MyWin.onPushButtonClick_stop(self)
                total_time.MyWin.Total_Test_time(self)
                count_testresult.MyWin.sum_testreslut(self, testresult)
                save_csv.MyWin.local_csv(self, errorcode, testresult)
                #save_logfile.MyWin.outer_logfile(self, testresult)
                UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                save_UI_logfile.MyWin.Self_logfile(self, testresult)
             elif setupresult == 'pass':
                  startGingerserviceresult = ginger_service.MyWin.startGingerservice(self)
                  if startGingerserviceresult == 'fail':
                     testStatusText = 'fail'
                     self.lineEdit_teststatus.setText(testStatusText)
                     self.lineEdit_teststatus.setStyleSheet("background-color:red")
                     testresult = 'fail'
                     errorcode = 'service_fail'
                     stop_button.MyWin.onPushButtonClick_stop(self)
                     total_time.MyWin.Total_Test_time(self)
                     count_testresult.MyWin.sum_testreslut(self, testresult)
                     save_csv.MyWin.local_csv(self, errorcode, testresult)
                     # save_logfile.MyWin.outer_logfile(self, testresult)
                     UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                     save_UI_logfile.MyWin.Self_logfile(self, testresult)
                  elif startGingerserviceresult == 'pass':
                       self.textBrowser.append('Grasp test')
                       self.data = subprocess.Popen('../unit/grasp.sh', stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                       MyWin.start_button_click(self)
                       while not self.TextBrowser_show.isFinished():
                           time.sleep(0.5)
                           QApplication.processEvents()
                       time.sleep(3)
                       with open('tmp.txt', 'r') as GraspFile:
                           Graspfailkeyword = '0 passed, 1 failed'
                           Grasppasskeyword = '1 passed, 0 failed'
                           for tempgrasp in GraspFile.readlines():
                               if Graspfailkeyword in tempgrasp:
                                   testStatusText = 'fail'
                                   self.lineEdit_teststatus.setText(testStatusText)
                                   self.lineEdit_teststatus.setStyleSheet("background-color:red")
                                   self.textBrowser.append('抓取失败')
                                   with open('tmp.txt', 'r') as tmpfile:
                                       with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                                           for line in tmpfile:
                                               Gingerfile.write(line)
                                   if os.path.exists('tmp.txt'):
                                       time.sleep(1)
                                       os.remove('tmp.txt')
                                   testresult = 'fail'
                                   errorcode = 'Grasp_fail'
                                   stop_button.MyWin.onPushButtonClick_stop(self)
                                   total_time.MyWin.Total_Test_time(self)
                                   count_testresult.MyWin.sum_testreslut(self, testresult)
                                   save_csv.MyWin.local_csv(self, errorcode, testresult)
                                   save_logfile.MyWin.outer_logfile(self, testresult)
                                   UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                                   save_UI_logfile.MyWin.Self_logfile(self, testresult)
                                   break
                               elif Grasppasskeyword in tempgrasp:
                                   testStatusText = 'PASS'
                                   self.lineEdit_teststatus.setText(testStatusText)
                                   self.lineEdit_teststatus.setStyleSheet("background-color:green")
                                   self.textBrowser.append('抓取成功')
                                   with open('tmp.txt', 'r') as tmpfile:
                                       with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                                           for line in tmpfile:
                                               Gingerfile.write(line)
                                   if os.path.exists('tmp.txt'):
                                       time.sleep(1)
                                       os.remove('tmp.txt')
                                   testresult = 'PASS'
                                   errorcode = 'Grasp_PASS'
                                   stop_button.MyWin.onPushButtonClick_stop(self)
                                   total_time.MyWin.Total_Test_time(self)
                                   count_testresult.MyWin.sum_testreslut(self, testresult)
                                   save_csv.MyWin.local_csv(self, errorcode, testresult)
                                   save_logfile.MyWin.outer_logfile(self, testresult)
                                   UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                                   save_UI_logfile.MyWin.Self_logfile(self, testresult)
                                   break



