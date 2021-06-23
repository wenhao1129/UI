# coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
import time
import configparser
from UI.Ginger import *
import pywifi
from pywifi import const

# # Define interface status.
# IFACE_DISCONNECTED = 0
# IFACE_SCANNING = 1
# IFACE_INACTIVE = 2
# IFACE_CONNECTING = 3
# IFACE_CONNECTED = 4
#
# # Define auth algorithms.
# AUTH_ALG_OPEN = 0
# AUTH_ALG_SHARED = 1
#
# # Define auth key mgmt types.
# AKM_TYPE_NONE = 0
# AKM_TYPE_WPA = 1
# AKM_TYPE_WPAPSK = 2
# AKM_TYPE_WPA2 = 3
# AKM_TYPE_WPA2PSK = 4
# AKM_TYPE_UNKNOWN = 5
#
# # Define ciphers.
# CIPHER_TYPE_NONE = 0
# CIPHER_TYPE_WEP = 1
# CIPHER_TYPE_TKIP = 2
# CIPHER_TYPE_CCMP = 3
# CIPHER_TYPE_UNKNOWN = 4
#
# KEY_TYPE_NETWORKKEY = 0
# KEY_TYPE_PASSPHRASE = 1

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
        # 创建一个元线对象
        wifi = pywifi.PyWiFi()
        # 取当前机器,第一个元线网卡
        iface = wifi.interfaces()[0]  # 有可能有多个无线网卡,所以要指定

        # 判断是否连接成功
        if iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
            print('wifi已连接')
            return 1
        else:
            print('wifi未连接')
        return 0

    def scan_wifi(self):
        """
        扫描附件wifi
        :return: 扫描结果对象
        """
        # 扫苗附件wifi
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        iface.scan()  # 扫苗附件wifi
        time.sleep(1)
        basewifi = iface.scan_results()
        for i in basewifi:
            print('wifi扫描结果:{}'.format(i.ssid))  # ssid 为wifi名称
            print('wifi设备MAC地址:{}'.format(i.bssid))
        return basewifi

    def connect_wifi(self):
        wifi = pywifi.PyWiFi()  # 创建一个wifi对象
        ifaces = wifi.interfaces()  # 取第一个无限网卡
        print(ifaces.name())  # 输出无线网卡名称
        ifaces.disconnect()  # 断开网卡连接
        time.sleep(3)  # 缓冲3秒

        robot_SN = self.lineEdit_RobotSN.text(self)
        profile = pywifi.Profile()  # 配置文件
        #profile.ssid = "acewill"  # wifi名称
        profile.ssid = '%s' % robot_SN
        profile.auth = const.AUTH_ALG_OPEN  # 需要密码
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
        profile.key = '12345678'  # wifi密码

        ifaces.remove_all_network_profiles()  # 删除其他配置文件
        tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

        ifaces.connect(tmp_profile)  # 连接
        time.sleep(10)  # 尝试10秒能否成功连接
        if ifaces.status() == const.IFACE_CONNECTED:
            print('成功连接')
            self.textBrowser.setText('成功连接')
            connect_status = True
        else:
            print('连接失败')
            connect_status = False
        time.sleep(1)
        return connect_status