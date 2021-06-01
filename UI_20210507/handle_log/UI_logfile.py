#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import os
import time
import configparser
from UI.Ginger import *
config = configparser.ConfigParser()
config.read("../config/config.ini")
robot_factory_tool_path = config.get("TestlogPath", "robot_factory_tool")
Ginger_test_env_path = config.get("TestlogPath", "Ginger_test_env")


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    # 生成UI logfile
    def txtlogfile(self,result,errorcode):
        MOnumber = self.lineEdit_MO.text()
        modelName = self.lineEdit_modelName.text()
        stationName = config.get("staitonName", "%s" % self.lineEdit_stationName.text())
        robotSN = self.lineEdit_RobotSN.text().upper()
        start_time = self.lineEdit_start_time.text()
        stop_time = self.lineEdit_stop_time.text()
        testerName = self.lineEdit_tester.text()
        total_testtime = self.lineEdit_test_time.text()
        self.result = result
        self.errorcode = errorcode
        log = open('Ginger.txt','a',encoding='utf-8')
        log.write('\n\n\n')
        log.write('============================================================================\n')
        log.write('                       Ginger UI add information                            \n')
        log.write('============================================================================\n')
        log.write('Model Name: %s\n'%modelName)
        log.write('MO Number: %s\n'%MOnumber)
        log.write('Station Name: %s\n'%stationName)
        log.write('RobotSN: %s\n'%robotSN)
        log.write('tester Name: %s\n'%testerName)
        log.write('test result is: %s\n'% self.result)
        log.write('test errorcode is: %s\n\n' % self.errorcode)
        log.write('start time: %s\n'%start_time)
        log.write('stop time: %s\n'%stop_time)
        log.write('Total Test time is: %s\n'%total_testtime)
        log.close()
        with open('Ginger.txt', 'r') as tmpfile:
            with open('Ginger_UI_log.txt', 'a') as Gingerfile:
                for line in tmpfile:
                    Gingerfile.write(line)
        if os.path.exists('Ginger.txt'):
           time.sleep(1)
           os.remove('Ginger.txt')
