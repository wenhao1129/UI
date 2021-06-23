#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import station.choose_station as choose
import common.sfis as sfis
import common.start_button as start_button
import common.stop_button as stop_button
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    def action_connect(self):
        #绑定按钮触发机种选择
        self.actionGinger1_0.triggered.connect(lambda: choose.MyWin.onChooseModel_1_0(self))
        self.actionGinger1_1.triggered.connect(lambda: choose.MyWin.onChooseModel_1_1(self))
        self.actionGinger1_1_1.triggered.connect(lambda: choose.MyWin.onChooseModel_1_1_1(self))
        self.actionGinger1_1_0_Pro.triggered.connect(lambda: choose.MyWin.onChooseModel_1_1_Pro(self))
        self.actionGinger1_1_0_Plus.triggered.connect(lambda: choose.MyWin.onChooseModel_1_1_Plus(self))
        #绑定按钮触发站位选择
        self.action_hari_IP128.triggered.connect(lambda:choose.MyWin.onChooseHariIP128(self))
        self.action_write_document.triggered.connect(lambda:choose.MyWin.onChooseWriteDocument(self))
        self.action_unit.triggered.connect(lambda: choose.MyWin.onChooseUnit(self))
        self.action_supernode.triggered.connect(lambda: choose.MyWin.onChooseSuperNode(self))
        self.action_ultrasonic.triggered.connect(lambda: choose.MyWin.onChooseUltrasonic(self))
        self.action_dance.triggered.connect(lambda: choose.MyWin.onChooseDance(self))
        #self.action_dance.triggered.connect(lambda: self.onChoosedance_wireless(self))
        self.action_navigation.triggered.connect(lambda: choose.MyWin.onChooseNavigation(self))
        self.action_gravity.triggered.connect(lambda: choose.MyWin.onChooseGravity(self))
        self.action_IMU.triggered.connect(lambda: choose.MyWin.onChooseIMU(self))
        self.action_grasp.triggered.connect(lambda: choose.MyWin.onChooseGrasp(self))
        self.actionIP200.triggered.connect(lambda: choose.MyWin.onChooseHost200(self))
        self.actionIP128.triggered.connect(lambda: choose.MyWin.onChooseHost128(self))
        self.action_head_calibrate.triggered.connect(lambda: choose.MyWin.onChoose_head_calibration(self))
        self.action_head_veri.triggered.connect(lambda: choose.MyWin.onChoose_head_verify(self))
        self.action_device.triggered.connect(lambda: choose.MyWin.onChoose_device(self))
        self.action_map.triggered.connect(lambda: choose.MyWin.onChoosemap(self))
        self.action_zero.triggered.connect(lambda: choose.MyWin.onChooseZero(self))
        self.actionUpgrade.triggered.connect(lambda: choose.MyWin.onChooseUpgradeCCU(self))
        self.actionOTA.triggered.connect(lambda: choose.MyWin.onChooseCCUOTA(self))
        self.action_versionCompare.triggered.connect(lambda: choose.MyWin.onChooseVersionCompare(self))
        self.actionversion.triggered.connect(choose.MyWin.version)
        self.action_gatherparam.triggered.connect(lambda: choose.MyWin.onChoose_gatherparam(self))
        #开始按钮触发选择
        self.pushbutton_SFIS_ON.clicked.connect(lambda:sfis.MyWin.onPushButton_SFIS_ON(self))
        self.pushButton_start.clicked.connect(lambda:start_button.MyWin.onPushButtonClick_start(self))
        self.pushButton_stop.clicked.connect(lambda:stop_button.MyWin.onPushButtonClick_stop(self))
        #self.pushButton_stop.clicked.connect(self.saveLogfile)
