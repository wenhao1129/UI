# coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import time
import configparser
import hotspot.connect_wifi as connect_wifi
#import connect_wifi
from UI.Ginger import *


config = configparser.ConfigParser()
config.read("../config/config.ini")


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    def wifi_connect_status(self):
        """
        判断本机是否有无线网卡,以及连接状态
        :return: 已连接或存在无线网卡返回1,否则返回0
        """
        connect_status = connect_wifi.MyWin.connect_wifi(self)
        print(connect_status)
