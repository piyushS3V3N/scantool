#!/usr/bin/python3

####################
from PyQt5 import QtCore, QtGui, QtWidgets
import time,os,socket


def get_my_ip():
  """
  Find my IP address
  :return:
  """
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  return ip        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 449)
        MainWindow.setFixedWidth(531)
        MainWindow.setFixedHeight(449)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/ico.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("background-color: rgb(10, 10, 10);\n"
        "alternate-background-color: rgb(255, 255, 255);\n" "color: rgb(0, 255,0);\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.outputwindow = QtWidgets.QTextEdit(self.centralwidget)
        self.outputwindow.setGeometry(QtCore.QRect(10, 10, 511, 271))
        self.outputwindow.setAutoFillBackground(True)
        self.outputwindow.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"xos4 Terminus\";")
        self.outputwindow.setObjectName("outputwindow")
        self.outputwindow.setAlignment(QtCore.Qt.AlignCenter)
        self.rundiscovery = QtWidgets.QPushButton(self.centralwidget)
        self.rundiscovery.setGeometry(QtCore.QRect(30, 300, 80, 23))
        self.rundiscovery.setObjectName("rundiscovery")
        self.rundiscovery.clicked.connect(self.rdiscovery)
        self.portscan = QtWidgets.QPushButton(self.centralwidget)
        self.portscan.setGeometry(QtCore.QRect(400, 320, 80, 23))
        self.portscan.setObjectName("portscan")
        self.portscan.clicked.connect(self.runportscan)
        self.hostname = QtWidgets.QLineEdit(self.centralwidget)
        self.hostname.setGeometry(QtCore.QRect(320, 290, 171, 23))
        self.hostname.setStyleSheet("background-color: rgb(170,255,0);\n""color: rgb(0,0,0);\n")
        self.hostname.setObjectName("hostname")
        self.hostname.returnPressed.connect(self.runportscan)
        self.scannedips = QtWidgets.QListWidget(self.centralwidget)
        self.scannedips.setGeometry(QtCore.QRect(120, 300, 131, 131))
        self.scannedips.setObjectName("listWidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sukyan Tsuru"))
        self.rundiscovery.setText(_translate("MainWindow", "Discover"))
        self.portscan.setText(_translate("MainWindow", "Port Scan"))

    def runportscan(self):
      sys.path.insert(1,'tool/')
      host = self.hostname.text()
      if host == "":
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Alert !!")
        msg.setInformativeText("You Forgot to Enter a host")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()
        return
      else:
        import portscanner
        data, ip= portscanner.run(host)
      self.outputwindow.clear()
      self.outputwindow.setAlignment(QtCore.Qt.AlignCenter)
      self.outputwindow.setTextColor(QtGui.QColor(0,255,0))
      self.outputwindow.append("[LIST OF OPEN PORTS]\n")
      self.outputwindow.setTextColor(QtGui.QColor(255,255,255))
      for i in data:
        self.outputwindow.append(i)
        self.outputwindow.append("[Status:")
        self.outputwindow.setTextColor(QtGui.QColor(0,255,0))
        self.outputwindow.insertPlainText("Open")
        self.outputwindow.setTextColor(QtGui.QColor(255,255,255))
        self.outputwindow.insertPlainText("]\n")
        QtWidgets.QApplication.processEvents()
      self.outputwindow.setAlignment(QtCore.Qt.AlignLeft)
      self.outputwindow.append("[HOST IP : ")
      self.outputwindow.setTextColor(QtGui.QColor(0,255,0))
      self.outputwindow.insertPlainText(ip)
      self.outputwindow.setTextColor(QtGui.QColor(255,255,255))
      self.outputwindow.insertPlainText("]\n")
   
    def rdiscovery(self):
      self.scannedips.clear()
      import nmap
      nm = nmap.PortScanner()
      ip_parts = get_my_ip().split('.')
      base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.1/24'
      nm.scan(hosts=base_ip, arguments='-n -sP -PE -PA21,23,80,3389')
      hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
      hosts_list = list(dict.fromkeys(hosts_list))  
      for host, status in hosts_list:
        self.scannedips.addItem(host)
        QtWidgets.QApplication.processEvents()

if __name__ == "__main__":
    import sys
    #db_ipscan = data_nmap()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
