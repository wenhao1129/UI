#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
import os
import subprocess
import time
import configparser
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
import init_ginger_wireless.setupgingerwireless as setup_ginger_wireless
import init_ginger_wireless.gingerservice_wireless as ginger_service_wireless
import reliability.navigation_go as navigo
import reliability.navigation_back as naviback
import data_local.count_testresult as count_testresult
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

    def navigation(self):
          Navigation_cycle_times_str = config.get("testTimes", "navigationTimes")
          Navigation_cycle_times = int(Navigation_cycle_times_str)
          self.textBrowser.clear()
          Begintext = '开始测试'
          self.textBrowser.append(Begintext)
          startResult = QMessageBox.information(None, '机器确认', '请确认机器已开机', QMessageBox.Yes | QMessageBox.No)
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
             Navigationsetupresult = setup_ginger_wireless.MyWin.NavigationsetupGinger(self)
             if Navigationsetupresult == 'fail':
                testStatusText = 'Fail'
                self.lineEdit_teststatus.setText(testStatusText)
                self.lineEdit_teststatus.setStyleSheet("background-color:red")
                testresult = 'fail'
                errorcode = 'setup_fail'
                stop_button.MyWin.onPushButtonClick_stop(self)
                total_time.MyWin.Total_Test_time(self)
                #save_logfile.MyWin.outer_logfile(self, testresult)
                UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                save_UI_logfile.MyWin.Self_logfile(self, testresult)
             elif Navigationsetupresult == 'pass':
                  navigationGingerserviceresult = ginger_service_wireless.MyWin.NavigationGingerservice(self)
                  if navigationGingerserviceresult == 'fail':
                    testStatusText = 'Fail'
                    self.lineEdit_teststatus.setText(testStatusText)
                    self.lineEdit_teststatus.setStyleSheet("background-color:red")
                    testresult = 'fail'
                    errorcode = 'service_fail'
                    stop_button.MyWin.onPushButtonClick_stop(self)
                    total_time.MyWin.Total_Test_time(self)
                    # save_logfile.MyWin.outer_logfile(self, testresult)
                    UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
                    save_UI_logfile.MyWin.Self_logfile(self, testresult)
                  elif navigationGingerserviceresult == 'pass':
                    self.textBrowser.append('Navigation cycle test')
                    for i in range(0, Navigation_cycle_times):
                        testStatusText = 'Cycle %s' % (i + 1)
                        self.lineEdit_teststatus.setText(testStatusText)
                        self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
                        testStatusText_navi_go = navigo.MyWin.navigation_go(self)
                        if testStatusText_navi_go == 'PASS':
                           testStatusText_navi_back = naviback.MyWin.navigation_back(self)
                           if testStatusText_navi_back == 'PASS':
                              testStatusText = 'PASS'
                              continue
                           else:
                               testStatusText = 'Fail'
                               break
                        elif testStatusText_navi_go == 'Fail':
                             testStatusText = 'Fail'
                             break
          if testStatusText == 'Fail':
             self.lineEdit_teststatus.setText(testStatusText)
             self.lineEdit_teststatus.setStyleSheet("background-color:red")
             testresult = 'Fail'
             errorcode = 'Navigation_Fail'
             stop_button.MyWin.onPushButtonClick_stop(self)
             total_time.MyWin.Total_Test_time(self)
             count_testresult.MyWin.sum_testreslut(self, testresult)
             save_logfile.MyWin.outer_logfile(self, testresult)
             UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
             save_UI_logfile.MyWin.Self_logfile(self, testresult)
          elif testStatusText == 'PASS':
              self.lineEdit_teststatus.setText(testStatusText)
              self.lineEdit_teststatus.setStyleSheet("background-color:green")
              testresult = 'PASS'
              errorcode = 'Navigation_PASS'
              stop_button.MyWin.onPushButtonClick_stop(self)
              total_time.MyWin.Total_Test_time(self)
              count_testresult.MyWin.sum_testreslut(self, testresult)
              save_logfile.MyWin.outer_logfile(self, testresult)
              UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
              save_UI_logfile.MyWin.Self_logfile(self, testresult)