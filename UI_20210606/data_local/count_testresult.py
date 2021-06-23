# coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import os
import time
import datetime
import shutil
import configparser
from UI.Ginger import *

config = configparser.ConfigParser()
config.read("../config/config.ini")
robot_factory_tool_path = config.get("TestlogPath", "robot_factory_tool")
Ginger_test_env_path = config.get("TestlogPath", "Ginger_test_env")
ZERO = 0

class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    # 定义保存外部程序生成logfile
    def sum_testreslut(self, testresult):
        record_current_day = config.get("testResult", "current_day")
        current_time = datetime.datetime.now()
        time_str_current = current_time.strftime("%Y%m%d")
        if time_str_current != record_current_day:
           config.set("testResult", "current_day", '%s' %time_str_current)
           config.write(open('../config/config.ini', 'w'))
           config.set("testResult", "total_pass", '%s'%ZERO)
           config.write(open('../config/config.ini', 'w'))
           config.set("testResult", "total_fail", '%s'%ZERO)
           config.write(open('../config/config.ini', 'w'))
        else:
            pass
        count_pass = int(config.get("testResult", "total_pass"))
        count_fail = int(config.get("testResult", "total_fail"))
        if testresult == "PASS":
            count_pass += 1
        if testresult == "fail":
            count_fail += 1
        config.set("testResult", "total_pass", '%s' % (str(count_pass)))
        config.write(open('../config/config.ini', 'w'))
        config.set("testResult", "total_fail", '%s' % (str(count_fail)))
        config.write(open('../config/config.ini', 'w'))
        count_pass_set = config.get("testResult", "total_pass")
        count_fail_set = config.get("testResult", "total_fail")
        self.lineEdit_testresult_pass.setText(count_pass_set)
        self.lineEdit_testresult_fail.setText(count_fail_set)
        if count_pass + count_fail == 0:
            pass
        else:
            pass_rate = (count_pass / (count_pass + count_fail)) * 100
            self.lineEdit_testresult_rate.setText('%.2f%%' % pass_rate)
