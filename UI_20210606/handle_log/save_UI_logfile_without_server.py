#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import os
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

    def Self_logfile(self, testresult):
        modelName = self.lineEdit_modelName.text()
        stationName = config.get("staitonName", "%s" % self.lineEdit_stationName.text())
        robotSN = self.lineEdit_RobotSN.text().upper()
        logfileSaveDate = time.strftime('%Y%m%d')
        logfileSavetime = time.strftime('%H%M%S')
        locallogpath = config.get("locallogPath", "locallogPath")
        PCName = config.get("PCinformation", "PCName")
        testResult = testresult
        sntime = robotSN + '_' + testResult + '_' + PCName + '_' + logfileSavetime
        logfilesourcePath = './Ginger_UI_log.txt'
        # 在本地和服务器端文件路径

        while not os.path.exists('%s/%s' % (locallogpath, modelName)):
            os.mkdir('%s/%s' % (locallogpath, modelName), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s' % (locallogpath, modelName, logfileSaveDate)):
            os.mkdir('%s/%s/%s' % (locallogpath, modelName, logfileSaveDate), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s/%s' % (locallogpath, modelName, logfileSaveDate, stationName)):
            os.mkdir('%s/%s/%s/%s' % (locallogpath, modelName, logfileSaveDate, stationName), mode=0o777)
            break


        # 定义外部程序生成logfile本地复制路径
        class targetPath_case(object):
            def case_to_function(self, stationName):
                fun_name = "case_fun_" + str(stationName)
                method = getattr(self, fun_name)
                return method

            def case_fun_Unit(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                    locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_SuperNode(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                    locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Dance(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_dance_wireless(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Ultrasonic(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                    locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Navigation(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                    locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Gravity(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                    locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IMU(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Grasp(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IP200(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IP128(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_map(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_zero(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_compare_version(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

        unit_tc = targetPath_case()
        localtargetPath = unit_tc.case_to_function(stationName)("case_fun_%s" % stationName)

        try:
            shutil.move(logfilesourcePath, localtargetPath)
        except (IOError, NameError) as exceptresult2:
            self.textBrowser.append(exceptresult2)

