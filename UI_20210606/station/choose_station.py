#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow,QMessageBox
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    #机种选择按钮
    def onChooseModel_1_0(self):
        self.lineEdit_modelName.setText("Ginger1.0.x")

    def onChooseModel_1_1(self):
        self.lineEdit_modelName.setText("Ginger1.1.0")

    def onChooseModel_1_1_1(self):
        self.lineEdit_modelName.setText("Ginger1.1.1")

    def onChooseModel_1_1_Pro(self):
        self.lineEdit_modelName.setText("Ginger1.1.0 Pro")

    def onChooseModel_1_1_Plus(self):
        self.lineEdit_modelName.setText("Ginger1.1.0 Plus")

    # 站位选择按钮
    def onChooseUnit(self):
        self.lineEdit_stationName.setText("单元测试")

    def onChooseVersionCompare(self):
        self.lineEdit_stationName.setText("版本比对")

    def onChooseSuperNode(self):
        self.lineEdit_stationName.setText("超节点")

    def onChooseUltrasonic(self):
        self.lineEdit_stationName.setText("超声波")

    def onChooseDance(self):
        self.lineEdit_stationName.setText("跳舞")

    def onChooseNavigation(self):
        self.lineEdit_stationName.setText("导航")

    def onChooseGravity(self):
        self.lineEdit_stationName.setText("重力补偿")

    def onChooseIMU(self):
        self.lineEdit_stationName.setText("IMU")

    def onChooseGrasp(self):
        self.lineEdit_stationName.setText("抓取")

    def onChooseHost200(self):
        self.lineEdit_stationName.setText("IP200")

    def onChooseHost128(self):
        self.lineEdit_stationName.setText("IP128")

    def onChooseHariIP128(self):
        self.lineEdit_stationName.setText("IP128")

    def onChooseWriteDocument(self):
        self.lineEdit_stationName.setText("文件写入")

    def onChoose_device(self):
        self.lineEdit_stationName.setText("device文件")

    def onChoosemap(self):
        self.lineEdit_stationName.setText("导入地图")

    def onChoose_head_calibration(self):
        self.lineEdit_stationName.setText("标定")

    def onChoose_head_verify(self):
        self.lineEdit_stationName.setText("校准")

    def onChooseZero(self):
        self.lineEdit_stationName.setText("丢零")

    def onChooseUpgradeCCU(self):
        self.lineEdit_stationName.setText("刷机")

    def onChooseCCUOTA(self):
        self.lineEdit_stationName.setText("OTA")

    def onChoosedance_wireless(self):
        self.lineEdit_stationName.setText("无线跳舞")

    def onChoose_gatherparam(self):
        self.lineEdit_stationName.setText("参数采集")
    
    def version(self):
        QMessageBox.information(None, '版本信息', '请参考README', QMessageBox.Ok)
