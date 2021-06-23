#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import os
import csv
import time
import shutil
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

    #定义保存外部程序生成logfile
    def local_csv(self, error_code, testresult):
        model_name = self.lineEdit_modelName.text()
        station_name = config.get("staitonName", "%s" % self.lineEdit_stationName.text())
        robot_SN = self.lineEdit_RobotSN.text().upper()
        MO = self.lineEdit_MO.text()
        tester_name = self.lineEdit_tester.text()
        logfileSaveDate = time.strftime('%Y%m%d')
        logfileSavetime = time.strftime('%H%M%S')
        locallogpath = config.get("locallogPath", "locallogPath")
        serverPath = config.get("serverlogPath", "serverlogPath")
        start_time = self.lineEdit_start_time.text()
        stop_time = self.lineEdit_stop_time.text()
        test_time = self.lineEdit_test_time.text()
        PCName = config.get("PCinformation", "PCName")
        testResult_transf = testresult
        sntime = robot_SN + '_' + testResult_transf + '_' + PCName + '_' + logfileSavetime
        #在本地和服务器端文件路径
        local_csv_path = config.get("TestlogPath", "local_csv")
        local_csv_name = 'Ginger' + '_' + PCName + '_' + logfileSaveDate + '.csv'
        local_csv_route = '%s'%local_csv_path + '/' + '%s'%local_csv_name
        if os.path.exists(local_csv_route):
           pass
        else:
           headers = ['Model_Name', 'Station_Name', 'MO', 'ROBOT_SN', 'Error_Code', 'Test_Result', 'Start_Time',
                      'Stop_TIme', 'Test_Time', 'PC_Name', 'Tester_Name']
           with open(local_csv_route, 'w', encoding='utf-8', newline='') as csv_file:
                file_csv = csv.writer(csv_file)
                file_csv.writerow(headers)
                csv_file.close()
        with open(local_csv_route, 'a', encoding='utf-8', newline='') as csv_file:
            csv_row = [ '%s'%model_name, '%s'%station_name, '%s'%MO, '%s'%robot_SN, '%s'%error_code,
                     '%s'%testresult, '%s'%start_time, '%s'%stop_time, '%s'%test_time,
                     '%s'%PCName, '%s'%tester_name
                      ]
            file_csv = csv.writer(csv_file)
            file_csv.writerow(csv_row)
            csv_file.close()

