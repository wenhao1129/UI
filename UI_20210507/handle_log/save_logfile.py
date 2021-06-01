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

    #定义保存外部程序生成logfile
    def outer_logfile(self, testresult):
        modelName = self.lineEdit_modelName.text()
        stationName = config.get("staitonName", "%s" % self.lineEdit_stationName.text())
        robotSN = self.lineEdit_RobotSN.text().upper()
        logfileSaveDate = time.strftime('%Y%m%d')
        logfileSavetime = time.strftime('%H%M%S')
        locallogpath = config.get("locallogPath", "locallogPath")
        serverPath = config.get("serverlogPath", "serverlogPath")
        PCName = config.get("PCinformation", "PCName")
        testResult_transf = testresult
        sntime = robotSN + '_' + testResult_transf + '_' + PCName + '_' + logfileSavetime
        #在本地和服务器端文件路径
        while not os.path.exists('%s/%s' % (locallogpath, modelName)):
            os.mkdir('%s/%s' % (locallogpath, modelName), mode=0o777)
            break
        while not os.path.exists('%s/%s' % (serverPath, modelName)):
            os.mkdir('%s/%s' % (serverPath, modelName), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s' % (locallogpath, modelName, logfileSaveDate)):
            os.mkdir('%s/%s/%s' % (locallogpath, modelName, logfileSaveDate), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s' % (serverPath, modelName, logfileSaveDate)):
            os.mkdir('%s/%s/%s' % (serverPath, modelName, logfileSaveDate), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s/%s' % (locallogpath, modelName, logfileSaveDate, stationName)):
            os.mkdir('%s/%s/%s/%s' % (locallogpath, modelName, logfileSaveDate, stationName), mode=0o777)
            break
        while not os.path.exists('%s/%s/%s/%s' % (serverPath, modelName, logfileSaveDate, stationName)):
            os.mkdir('%s/%s/%s/%s' % (serverPath, modelName, logfileSaveDate, stationName), mode=0o777)
            break

        #定义外部程序生成logfile本地路径
        class sourcePath_case(object):
            def case_to_function(self, stationName):
                fun_name = "case_fun_" + str(stationName)
                method = getattr(self, fun_name)
                return method

            def case_fun_Unit(self, sourcePath):
                unitName = config.get("TestlogPath", "Unit")
                sourcePath = '%s/unit.xlsx' % unitName
                return sourcePath

            def case_fun_SuperNode(self, sourcePath):
                SuperNodeName = config.get("TestlogPath", "SuperNode")
                sourcePath = '%s/log.html' % SuperNodeName
                return sourcePath

            def case_fun_Dance(self, sourcePath):
                DanceName = config.get("TestlogPath", "Dance")
                sourcePath = '%s/result.txt' % (DanceName)
                return sourcePath

            def case_fun_dance_wireless(self, sourcePath):
                DanceName = config.get("TestlogPath", "Dance")
                sourcePath = '%s/result.txt' % (DanceName)
                return sourcePath

            def case_fun_Ultrasonic(self, sourcePath):
                UltrasonicName = config.get("TestlogPath", "Ultrasonic")
                sourcePath = '%s/AllStation.xlsx' % UltrasonicName
                return sourcePath

            def case_fun_Navigation(self, sourcePath):
                NavigationName = config.get("TestlogPath", "Navigation")
                sourcePath = '%s/log.html' % NavigationName
                return sourcePath

            def case_fun_Gravity(self, sourcePath):
                GravityName = config.get("TestlogPath", "Gravity")
                sourcePath = '%s/log.html' % GravityName
                return sourcePath

            def case_fun_IMU(self, sourcePath):
                IMUName = config.get("TestlogPath", "IMU")
                sourcePath = '%s/log.html' % IMUName
                return sourcePath

            def case_fun_collect_param(self, sourcePath):
                IMUName = config.get("TestlogPath", "IMU")
                sourcePath = '%s/log.html' % IMUName
                return sourcePath

            def case_fun_Grasp(self, sourcePath):
                GraspName = config.get("TestlogPath", "Grasp")
                sourcePath = '%s/log.html' % GraspName
                return sourcePath

            def case_fun_IP200(self, sourcePath):
                IP200Name = config.get("TestlogPath", "IP200")
                sourcePath = '%s/log.html' % IP200Name
                return sourcePath

            def case_fun_IP128(self, sourcePath):
                IP128Name = config.get("TestlogPath", "IP200")
                sourcePath = '%s/log.html' % IP128Name
                return sourcePath
            def case_fun_map(self, sourcePath):
                MapName = config.get("TestlogPath", "map")
                sourcePath = '%s/log.html' % MapName
                return sourcePath

            def case_fun_zero(self, sourcePath):
                ZeroName = config.get("TestlogPath", "zero")
                sourcePath = '%s/result.xlsx' % ZeroName
                return sourcePath

        # 定义外部程序生成logfile本地复制路径
        class targetPath_case(object):
            def case_to_function(self, stationName):
                fun_name = "case_fun_" + str(stationName)
                method = getattr(self, fun_name)
                return method

            def case_fun_Unit(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.xlsx' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_SuperNode(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Dance(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_dance_wireless(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.txt' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Ultrasonic(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.xlsx' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Navigation(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Gravity(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (
                locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IMU(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_Grasp(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IP200(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_IP128(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_map(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.html' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

            def case_fun_zero(self, localtargetPath):
                localtargetPath = '%s/%s/%s/%s/%s.xlsx' % (locallogpath, modelName, logfileSaveDate, stationName, sntime)
                return localtargetPath

        # 定义外部程序生成logfile服务器复制路径
        class ServertargetPath_case(object):
            def case_to_function(self, stationName):
                fun_name = "case_fun_" + str(stationName)
                method = getattr(self, fun_name)
                return method

            def case_fun_Unit(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.xlsx' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_SuperNode(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_Dance(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.txt' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_dance_wireless(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.txt' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_Ultrasonic(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.xlsx' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_Navigation(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_Gravity(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_IMU(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_Grasp(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath


            def case_fun_IP200(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_IP128(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_map(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.html' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

            def case_fun_zero(self, serverTargetPath):
                serverTargetPath = '%s/%s/%s/%s/%s.xlsx' % (serverPath, modelName, logfileSaveDate, stationName, sntime)
                return serverTargetPath

        unit_sc = sourcePath_case()
        unit_tc = targetPath_case()
        serverTargetPath = ServertargetPath_case()
        sourcePath = unit_sc.case_to_function(stationName)("case_fun_%s" % stationName)
        localtargetPath = unit_tc.case_to_function(stationName)("case_fun_%s" % stationName)
        serverTargetPath = serverTargetPath.case_to_function(stationName)("case_fun_%s" % stationName)

        if not os.path.exists(sourcePath):
           self.textBrowser.append('没有找到logfile, 请联系TE')
           self.lineEdit_teststatus.setText('Fail')
        else:
            try:
                shutil.copyfile(sourcePath, serverTargetPath)
            except (IOError, NameError) as exceptresult1:
                self.textBrowser.append(exceptresult1)

            try:
                shutil.move(sourcePath, localtargetPath)
            except (IOError, NameError) as exceptresult2:
                self.textBrowser.append(exceptresult2)

