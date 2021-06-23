#coding=UTF-8
from PyQt5.QtWidgets import QMainWindow
from UI.Ginger import *


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)

    def onPushButton_SFIS_ON(self):
       self.pushbutton_SFIS_ON.setText("SFIS_OFF")
       self.pushbutton_SFIS_ON.setStyleSheet("background-color:darkgrey")
