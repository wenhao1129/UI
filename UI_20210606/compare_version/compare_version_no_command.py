#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import subprocess
import time
import configparser
import filecmp
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

    def compare_version(self):
        robotSN = self.lineEdit_RobotSN.text().upper()
        chooseStation = self.lineEdit_stationName.text()
        model_name = self.lineEdit_modelName.text()
        if os.path.exists('tmp.txt'):
            time.sleep(1)
            os.remove('tmp.txt')
        if os.path.exists('Ginger_UI_log.txt'):
            time.sleep(1)
            os.remove('Ginger_UI_log.txt')
        originaltext_ccu = '../version/original/ccu_version.txt'
        originaltext_ecu = '../version/original/ecu_version.txt'
        originaltext_sca = '../version/original/sca_version.txt'
        originaltext_iris = '../version/original/iris_camera.txt'
        self.textBrowser.clear()
        self.textBrowser.append('开始测试')
        testStatusText = '测试中'
        self.lineEdit_teststatus.setText(testStatusText)
        self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
        self.textBrowser.append('版本比对')
        self.textBrowser.append('CCU版本比对')
        if not os.path.exists('../version/temp_ccu_version.txt'):
           self.textBrowser.append('there is not a ccu verson document')
        elif os.path.exists('../version/temp_ccu_version.txt'):
            temptext_ccu = '../version/temp_ccu_version.txt'
            result_ccu = filecmp.cmp(temptext_ccu, originaltext_ccu)
            if result_ccu:
               self.textBrowser.append('CCU版本比对pass')
               ccu_version = True
            else:
               self.textBrowser.append('CCU版本比对fail')
               ccu_version = False
               time.sleep(1)
        temptext_ecu = '../version/temp_ecu_version.txt'
        result_ecu = filecmp.cmp(temptext_ecu, originaltext_ecu)
        if result_ecu:
           self.textBrowser.append('ECU版本比对pass')
           ecu_version = True
        else:
           self.textBrowser.append('ECU版本比对fail')
           ecu_version = False
        time.sleep(1)
        self.textBrowser.append('sca版本比对')
        temptext_sca = '../version/temp_sca_version.txt'
        result_sca = filecmp.cmp(temptext_sca, originaltext_sca)
        if result_sca:
           self.textBrowser.append('SCA版本比对pass')
           sca_version = True
        else:
           self.textBrowser.append('SCA版本比对fail')
           sca_version = False
        time.sleep(1)
        self.textBrowser.append('supernode版本比对')
        temptext_iris = '../version/temp_iris_camera.txt'
        result_iris = filecmp.cmp(temptext_iris, originaltext_iris)
        if result_iris:
           self.textBrowser.append('supernode版本比对pass')
           supernode_version = True
        else:
           self.textBrowser.append('supernode版本比对fail')
           supernode_version = False
        templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
        templog.write('============================================================================\n')
        templog.write('                       Ginger ccu version                                   \n')
        templog.write('============================================================================\n')
        templog.close()
        with open('../version/temp_ccu_version.txt', 'r') as tmpfile:
            with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                for line in tmpfile:
                    Gingerversionfile.write(line)
        if os.path.exists('../version/temp_ccu_version.txt'):
            time.sleep(1)
            os.remove('../version/temp_ccu_version.txt')
        templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
        templog.write('============================================================================\n')
        templog.write('                       Ginger ecu version                                   \n')
        templog.write('============================================================================\n')
        templog.close()
        with open('../version/temp_ecu_version.txt', 'r') as tmpfile:
            with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                for line in tmpfile:
                    Gingerversionfile.write(line)
        if os.path.exists('../version/temp_ecu_version.txt'):
            time.sleep(1)
            os.remove('../version/temp_ecu_version.txt')
        templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
        templog.write('============================================================================\n')
        templog.write('                       Ginger sca version                                   \n')
        templog.write('============================================================================\n')
        templog.close()
        with open('../version/temp_sca_version.txt', 'r') as tmpfile:
            with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                for line in tmpfile:
                    Gingerversionfile.write(line)
        if os.path.exists('../version/temp_sca_version.txt'):
            time.sleep(1)
            os.remove('../version/temp_sca_version.txt')
        templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
        templog.write('============================================================================\n')
        templog.write('                    Ginger supernode version test start                     \n')
        templog.write('============================================================================\n')
        templog.close()
        with open('../version/temp_iris_camera.txt', 'r') as tmpfile:
            with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                for line in tmpfile:
                    Gingerversionfile.write(line)
        if os.path.exists('../version/temp_iris_camera.txt'):
            time.sleep(1)
            os.remove('../version/temp_iris_camera.txt')
        if ccu_version and ecu_version and sca_version and supernode_version:
           self.textBrowser.append('All version is the same')
           self.textBrowser.append('版本比对结束')
           testStatusText = 'PASS'
           self.lineEdit_teststatus.setText(testStatusText)
           self.lineEdit_teststatus.setStyleSheet("background-color:green")
           testresult = 'PASS'
           errorcode = 'version_PASS'
           stop_button.MyWin.onPushButtonClick_stop(self)
           total_time.MyWin.Total_Test_time(self)
           #save_logfile.MyWin.outer_logfile(self, testresult)
           #UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
           #save_UI_logfile.MyWin.Self_logfile(self, testresult)
        else:
           self.textBrowser.append('version is the different')
           self.textBrowser.append('版本比对结束')
           testStatusText = 'fail'
           self.lineEdit_teststatus.setText(testStatusText)
           self.lineEdit_teststatus.setStyleSheet("background-color:red")
           testresult = 'fail'
           errorcode = 'version_Fail'
           stop_button.MyWin.onPushButtonClick_stop(self)
           total_time.MyWin.Total_Test_time(self)
           #save_logfile.MyWin.outer_logfile(self, testresult)
           #UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
           #save_UI_logfile.MyWin.Self_logfile(self, testresult)

