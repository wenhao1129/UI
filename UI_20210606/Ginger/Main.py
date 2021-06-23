#coding=UTF-8
import sys
from PyQt5.Qt import QThread,QMutex,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI.Ginger import *
import station.action_trigger as action_trigger
import configparser
config = configparser.ConfigParser()
config.read("../config/config.ini")

#建立新的线程,用来监控外部程序运行,并且会生成tmp.txt
class TextBrowser_thred(QThread):
    signal = pyqtSignal(str)

    def __init__(self, TextBrowser_win, data):
        self.data = data
        self.TextBrowser_win = TextBrowser_win
        super().__init__()

    def run(self):
        while self.data.poll is not None:
            template = self.data.stdout.readline()
            outputs = bytes.decode(template)
            self.signal.emit(str(outputs))
            if outputs == '':
               break


class MyWin(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.setupUi(self)
        self.progressBar.setValue(0)
        # 设置关闭最大化窗口
        self.setFixedSize(self.width(), self.height())
        #设置默认颜色
        self.pushButton_start.setStyleSheet("background-color:deepskyblue")
        self.pushButton_stop.setStyleSheet("background-color:red")
        self.lineEdit_modelName.setStyleSheet("background-color:cyan")
        self.lineEdit_stationName.setStyleSheet("background-color:cyan")
        self.lineEdit_tester.setStyleSheet("background-color:cyan")
        self.lineEdit_RobotSN.setStyleSheet("background-color:cyan")
        self.lineEdit_MO.setStyleSheet("background-color:cyan")
        self.pushbutton_SFIS_ON.setStyleSheet("background-color:lime")
        self.lineEdit_start_time.setStyleSheet("background-color:gold")
        self.lineEdit_stop_time.setStyleSheet("background-color:gold")
        self.lineEdit_test_time.setStyleSheet("background-color:gold")
        self.textBrowser.setStyleSheet("background-color:bisque")
        #读取config.ini,设置默认机种
        modelnamedefault = config.get("modelName", "model_1.1.0")
        self.lineEdit_modelName.setText('%s' % modelnamedefault)
        action_trigger.MyWin.action_connect(self)

    #定义信号和槽,调用时触发
    def start_button_click(self):
        self.TextBrowser_show = TextBrowser_thred(self.textBrowser, self.data)
        self.TextBrowser_show.signal.connect(self.TextBrowser_show_text)
        self.TextBrowser_show.start()

    #定义槽函数,接受外部程序运行结果,生成tmp.txt
    def TextBrowser_show_text(self, msg):
        self.textBrowser.append(msg)
        try:
            f = open('tmp.txt', 'a', encoding='utf-8')
            f.write(msg)
            f.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWin()
    myWindow.show()
    sys.exit(app.exec_())
