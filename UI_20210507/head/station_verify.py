#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
import os
import re
import subprocess
import time
import configparser
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
import init_ginger.setupginger as setup_ginger
import init_ginger.gingerservice as ginger_service
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

    def head_verify(self):
        robotSN = self.lineEdit_RobotSN.text().upper()
        chooseStation = self.lineEdit_stationName.text()
        model_name = self.lineEdit_modelName.text()
        localppx = float(config.get("cameraparam", "ppx"))
        localppy = float(config.get("cameraparam", "ppy"))
        localfx = float(config.get("cameraparam", "fx"))
        localfy = float(config.get("cameraparam", "fy"))
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
            testStatusText = 'Fail'
            self.lineEdit_teststatus.setText(testStatusText)
            self.lineEdit_teststatus.setStyleSheet("background-color:red")
        elif startResult == QMessageBox.Yes:
            self.textBrowser.append('校准')
            self.data = subprocess.Popen('../head/scp_head.sh', stdout=subprocess.PIPE,
                                         stdin=subprocess.PIPE,
                                         shell=True)
            MyWin.start_button_click(self)
            while not self.TextBrowser_show.isFinished():
                time.sleep(0.5)
                QApplication.processEvents()
            time.sleep(1)
            with open('tmp.txt', 'r') as headFile:
                headfailkeyword1 = 'No route to host'
                headfailkeyword2 = '0 passed, 2 failed'
                headpasskeyword = '100%'
                for temphead in headFile.readlines():
                    if headfailkeyword1 in temphead or headfailkeyword2 in temphead:
                        testStatusText = 'Fail'
                        self.lineEdit_teststatus.setText(testStatusText)
                        self.lineEdit_teststatus.setStyleSheet("background-color:red")
                        self.textBrowser.append('复制camera文件失败')
                        if os.path.exists('tmp.txt'):
                            time.sleep(1)
                            os.remove('tmp.txt')
                        break
                    elif headpasskeyword in temphead:
                        if os.path.exists('tmp.txt'):
                            time.sleep(1)
                            os.remove('tmp.txt')
                        self.textBrowser.append('复制camera文件成功')
                        with open('head.txt', 'r') as tempheadFile:
                            tempheadline = tempheadFile.readlines()
                            tempfirstline = tempheadline[0]
                            res = re.sub('{|}', '', tempfirstline)
                            temp = res.split(',')
                            temp0 = temp[0]
                            temp1 = temp[1]
                            temp2 = temp[2]
                            temp3 = temp[3]
                            ppx = float(temp0[7:17])
                            ppy = float(temp1[7:17])
                            fx = float(temp2[7:17])
                            fy = float(temp3[7:17])
                            if localppx * 0.8 <= ppx <= localppx * 1.2 and localppy * 0.8 <= ppy <= localppy * 1.2 and localfx * 0.8 <= fx <= localfx * 1.2 and localfy * 0.8 <= fy <= localfy * 1.2:
                                self.textBrowser.append('标定参数在规格内')
                                self.textBrowser.append('开始测试距离')
                                testStatusText = '测试中'
                                self.lineEdit_teststatus.setText(testStatusText)
                                self.lineEdit_teststatus.setStyleSheet("background-color:green")
                                self.data = subprocess.Popen('../head/head_verify.sh',
                                                             stdout=subprocess.PIPE,
                                                             stdin=subprocess.PIPE,
                                                             shell=True)
                                MyWin.start_button_click(self)
                                while not self.TextBrowser_show.isFinished():
                                    time.sleep(0.5)
                                    QApplication.processEvents()
                                time.sleep(3)
                                calibration_result = QMessageBox.information(None, '测试结果确认', '请确认测试结果',
                                                                             QMessageBox.Yes | QMessageBox.No)
                                if calibration_result == QMessageBox.No:
                                    testStatusText = 'Fail'
                                    self.lineEdit_teststatus.setText(testStatusText)
                                    self.lineEdit_teststatus.setStyleSheet("background-color:red")
                                    break
                                elif calibration_result == QMessageBox.Yes:
                                    testStatusText = 'PASS'
                                    self.lineEdit_teststatus.setText(testStatusText)
                                    self.lineEdit_teststatus.setStyleSheet("background-color:green")
                                    break
                            else:
                                for i in range(0, 3):
                                    QMessageBox.information(None, '标定参数确认', '标定参数不在规格内,请重新标定', QMessageBox.Ok)
                                time.sleep(1)
                                self.textBrowser.append('标定参数不在规格内')
                                self.textBrowser.append('测试结束')
                                testStatusText = 'Fail'
                                self.lineEdit_teststatus.setText(testStatusText)
                                self.lineEdit_teststatus.setStyleSheet("background-color:red")
                                break
