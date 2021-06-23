#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import time
import setup_param.IP128 as IP128
import setup_param.IP200 as IP200
import compare_version.compare_file as compare_file
import copy_document.device as device
import copy_document.write_document as write_document
import CCU.otaCCU as otaCCU
import CCU.upgradeCCU as upgradeCCU
import setup_param.map as map
import collect_param.gatherparam as gatherparam
import collect_param.IMU as IMU
import collect_param.gravity as gravity
import unit.unit as unit
import unit.grasp as grasp
import unit.zero as zero
import reliability.supernode as supernode
import reliability.dance as dance
import reliability.navigation as navigation
import head.station_calibration as station_calibration
import head.station_verify as station_verify
import hotspot.hotspot as hotspot
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    #选择站位,运行对应程序
    def onChooseStation(self):
        robotSN = self.lineEdit_RobotSN.text().upper()
        chooseStation = self.lineEdit_stationName.text()
        model_name = self.lineEdit_modelName.text()
        while chooseStation == '标定':
              station_calibration.MyWin.head_calibration(self)
              time.sleep(1)
              break
        while chooseStation == '校准':
              station_verify.MyWin.head_verify(self)
              time.sleep(1)
              break
        while chooseStation == '版本比对':
              #compare_file.MyWin.compare_version(self)
              hotspot.MyWin.wifi_connect_status(self)
              time.sleep(1)
              break
        while chooseStation == 'device文件':
              device.MyWin.copydevice(self)
              time.sleep(1)
              break
        while chooseStation == '丢零':
              zero.MyWin.back_zero(self)
              time.sleep(1)
              break
        while chooseStation == '刷机':
              upgradeCCU.MyWin.upgradeCCU(self)
              time.sleep(1)
              break
        while chooseStation == 'OTA':
              otaCCU.MyWin.OTA(self)
              time.sleep(1)
              break
        while chooseStation == '导入地图':
              map.MyWin.map(self)
              break
        while chooseStation == '单元测试':
              unit.MyWin.unit(self)
              time.sleep(1)
              break
        while chooseStation == 'IP200':
              IP200.MyWin.IP200(self)
              time.sleep(1)
              break
        while chooseStation == 'IP128':
              IP128.MyWin.IP128(self)
              time.sleep(1)
              break
        while chooseStation == '文件写入':
              write_document.MyWin.write_document(self)
              time.sleep(1)
              break
        while chooseStation == '抓取':
              grasp.MyWin.grasp(self)
              time.sleep(1)
              break
        while chooseStation == '跳舞':
              dance.MyWin.dance(self)
              time.sleep(1)
              break
        while chooseStation == '超节点':
              supernode.MyWin.supernode(self)
              break
        while chooseStation == 'IMU':
              IMU.MyWin.IMU(self)
              time.sleep(1)
              break
        while chooseStation == '重力补偿':
              gravity.MyWin.gravity(self)
              time.sleep(1)
              break
        while chooseStation == '参数采集':
              gatherparam.MyWin.gatherparam(self)
              time.sleep(1)
              break
        while chooseStation == '无线跳舞':
              break
        while chooseStation == '导航':
              navigation.MyWin.navigation(self)
              time.sleep(1)
              break

