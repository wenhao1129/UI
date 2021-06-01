#coding=UTF-8
from PyQt5.Qt import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import subprocess
import time
import hashlib
import configparser
import filecmp
import common.stop_button as stop_button
import common.total_time as total_time
import handle_log.save_logfile as save_logfile
import handle_log.save_UI_logfile as save_UI_logfile
import handle_log.UI_logfile as UI_logfile
from UI.Ginger import *

config = configparser.ConfigParser()
config.read("../compare_version/version_config.ini")


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

    #定义信号和槽,调用时触发
    def start_button_click(self):
        self.TextBrowser_show = TextBrowser_thred(self.textBrowser, self.data)
        #msg = self.TextBrowser_show.run.outputs
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

    def txt_md5(fileMd5):
        import hashlib
        md5_value = hashlib.md5()
        with open(fileMd5, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                md5_value.update(data)
        return md5_value.hexdigest()

    def compare_version(self):
        if os.path.exists('tmp.txt'):
            time.sleep(1)
            os.remove('tmp.txt')
        if os.path.exists('Ginger_UI_log.txt'):
            time.sleep(1)
            os.remove('Ginger_UI_log.txt')
        original_md5_ccu = config.get("versionInformation", "CCU_version_md5")
        original_md5_ecu = config.get("versionInformation", "ECU_version_md5")
        original_md5_sca = config.get("versionInformation", "SCA_version_md5")
        original_md5_iris = config.get("versionInformation", "supernode_version_md5")
        self.textBrowser.clear()
        self.textBrowser.append('开始测试')
        testStatusText = '测试中'
        self.lineEdit_teststatus.setText(testStatusText)
        self.lineEdit_teststatus.setStyleSheet("background-color:yellow")
        self.textBrowser.append('版本比对')
        self.textBrowser.append('CCU版本比对')
        self.data = subprocess.Popen('../compare_version/ssh_ccu_v.sh',
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        if not os.path.exists('../compare_version/temp_ccu_version.txt'):
           self.textBrowser.append('there is not a ccu verson document')
           ccu_version = False
        elif os.path.exists('../compare_version/temp_ccu_version.txt'):
            temp_txt_ccu = '../compare_version/temp_ccu_version.txt'
            md5_value_ccu = MyWin.txt_md5(temp_txt_ccu)
            self.textBrowser.append(md5_value_ccu)
            if original_md5_ccu == md5_value_ccu:
               self.textBrowser.append('CCU版本比对pass')
               ccu_version = True
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger ccu version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_ccu_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_ccu_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_ccu_version.txt')
            else:
               self.textBrowser.append('CCU版本比对fail')
               ccu_version = False
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger ccu version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_ccu_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_ccu_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_ccu_version.txt')
               time.sleep(1)
        self.textBrowser.append('ECU版本比对')
        self.data = subprocess.Popen('../compare_version/ecu_version.sh',
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        if not os.path.exists('../compare_version/temp_ecu_version.txt'):
           self.textBrowser.append('there is not a ecu verson document')
           ecu_version = False
        elif os.path.exists('../compare_version/temp_ecu_version.txt'):
            temp_txt_ecu = '../compare_version/original/temp_ecu_version.txt'
            md5_value_ecu = MyWin.txt_md5(temp_txt_ecu)
            self.textBrowser.append(md5_value_ecu)
            if original_md5_ecu == md5_value_ecu:
               self.textBrowser.append('ECU版本比对pass')
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger ecu version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_ecu_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_ecu_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_ecu_version.txt')
               ecu_version = True
            else:
               self.textBrowser.append('ECU版本比对fail')
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger ecu version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_ecu_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_ecu_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_ecu_version.txt')
               ecu_version = False
               time.sleep(1)
        self.textBrowser.append('SCA版本比对')
        self.data = subprocess.Popen('../compare_version/sca_version.sh',
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        if not os.path.exists('../compare_version/temp_sca_version.txt'):
           self.textBrowser.append('there is not a sca verson document')
           sca_version = False
        elif os.path.exists('../compare_version/temp_sca_version.txt'):
            temp_txt_sca = '../compare_version/original/temp_sca_version.txt'
            md5_value_sca = MyWin.txt_md5(temp_txt_sca)
            self.textBrowser.append(md5_value_sca)
            if original_md5_sca == md5_value_sca:
               self.textBrowser.append('SCA版本比对pass')
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger sca version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_sca_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_sca_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_sca_version.txt')
               sca_version = True
            else:
               self.textBrowser.append('SCA版本比对fail')
               templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
               templog.write('============================================================================\n')
               templog.write('                       Ginger sca version                                   \n')
               templog.write('============================================================================\n')
               templog.close()
               with open('../compare_version/temp_sca_version.txt', 'r') as tmpfile:
                   with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                       for line in tmpfile:
                           Gingerversionfile.write(line)
               if os.path.exists('../compare_version/temp_sca_version.txt'):
                   time.sleep(1)
                   os.remove('../compare_version/temp_sca_version.txt')
               sca_version = False
               time.sleep(1)
        self.textBrowser.append('supernode版本比对')
        self.data = subprocess.Popen('../compare_version/supernode.sh',
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     shell=True)
        MyWin.start_button_click(self)
        while not self.TextBrowser_show.isFinished():
            time.sleep(0.5)
            QApplication.processEvents()
        time.sleep(3)
        if not os.path.exists('../compare_version/temp_iris_camera.txt'):
            self.textBrowser.append('there is not a iris_camera verson document')
            sca_version = False
        elif os.path.exists('../compare_version/temp_iris_camera.txt'):
            temp_txt_iris = '../compare_version/original/temp_iris_camera.txt'
            md5_value_iris = MyWin.txt_md5(temp_txt_iris)
            if original_md5_iris == md5_value_iris:
                self.textBrowser.append('supernode版本比对pass')
                templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                templog.write('============================================================================\n')
                templog.write('                    Ginger supernode version test start                     \n')
                templog.write('============================================================================\n')
                templog.close()
                with open('../compare_version/temp_iris_camera.txt', 'r') as tmpfile:
                    with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                        for line in tmpfile:
                            Gingerversionfile.write(line)
                if os.path.exists('../compare_version/temp_iris_camera.txt'):
                    time.sleep(1)
                    os.remove('../compare_version/temp_iris_camera.txt')
                supernode_version = True
            else:
                self.textBrowser.append('supernode版本比对fail')
                templog = open('Ginger_UI_log.txt', 'a', encoding='utf-8')
                templog.write('============================================================================\n')
                templog.write('                    Ginger supernode version test start                     \n')
                templog.write('============================================================================\n')
                templog.close()
                with open('../compare_version/temp_iris_camera.txt', 'r') as tmpfile:
                    with open('Ginger_UI_log.txt', 'a') as Gingerversionfile:
                        for line in tmpfile:
                            Gingerversionfile.write(line)
                if os.path.exists('../compare_version/temp_iris_camera.txt'):
                    time.sleep(1)
                    os.remove('../compare_version/temp_iris_camera.txt')
                supernode_version = False
                time.sleep(1)
        if ccu_version and ecu_version and sca_version and supernode_version:
           self.textBrowser.append('All version is the same')
           self.textBrowser.append('版本比对结束')
           testStatusText = 'PASS'
           self.lineEdit_teststatus.setText(testStatusText)
           self.lineEdit_teststatus.setStyleSheet("background-color:green")
           testresult = 'PASS'
           errorcode = 'version_PASS'
           stop_button.MyWin.onPushButtonClick_stop(self)
           total_time.MyWin.Total_Test_time(self)
           #save_logfile.MyWin.outer_logfile(self, testresult)
           #UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
           #save_UI_logfile.MyWin.Self_logfile(self, testresult)
        else:
           self.textBrowser.append('version is the different')
           self.textBrowser.append('版本比对结束')
           testStatusText = 'Fail'
           self.lineEdit_teststatus.setText(testStatusText)
           self.lineEdit_teststatus.setStyleSheet("background-color:red")
           testresult = 'Fail'
           errorcode = 'version_Fail'
           stop_button.MyWin.onPushButtonClick_stop(self)
           total_time.MyWin.Total_Test_time(self)
           #save_logfile.MyWin.outer_logfile(self, testresult)
           #UI_logfile.MyWin.txtlogfile(self, testresult, errorcode)
           #save_UI_logfile.MyWin.Self_logfile(self, testresult)

