from PyQt5 import QtCore, QtGui, QtWidgets
#import time,os,socket,nmap
from tool.netgraph import *
from PyQt5.QtCore import QSize, QObject, QThread, pyqtSignal
from tool import portscanner , discover, threadedcommand, nmap_cvesuggester
import urllib.parse , re
#import matplotlib.pyplot as plt



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        i = 0

        hosts_list = discover.run()
        for host in hosts_list:
          self.progress.emit(host)
        self.finished.emit()

class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
        result = QtWidgets.QMessageBox.question(self, "Confirm Exit...","Are you sure you want to exit ?",QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
          widgetList = QApplication.topLevelWidgets()
          numWindows = len(widgetList)
          print(numWindows)
          if numWindows > 1:
            event.accept()
          else:
            event.ignore()
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("NARAD")
        MainWindow.resize(531, 449)
        MainWindow.setMaximumSize(QSize(531,449))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(50, 50, 50);\n"
"alternate-background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.outputwindow = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputwindow.setGeometry(QtCore.QRect(10, 10, 511, 271))
        self.outputwindow.setAutoFillBackground(True)
        self.outputwindow.setStyleSheet("background-color: rgb(50, 50, 50);\n"
"color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 255, 255);\n"
"font: 75 12pt \"Inconsolata\";")
        self.outputwindow.setObjectName("outputwindow")
        self.rundiscovery = QtWidgets.QPushButton(self.centralwidget)
        self.rundiscovery.setGeometry(QtCore.QRect(20, 290, 80, 23))
        self.rundiscovery.setObjectName("rundiscovery")
        self.rundiscovery.clicked.connect(self.rdiscovery)
        self.portscan = QtWidgets.QPushButton(self.centralwidget)
        self.portscan.setGeometry(QtCore.QRect(450, 320, 71, 23))
        self.portscan.setObjectName("portscan")
        self.portscan.clicked.connect(self.runportscan)
        self.hostname = QtWidgets.QLineEdit(self.centralwidget)
        self.hostname.setGeometry(QtCore.QRect(270, 320, 171, 23))
        self.hostname.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.hostname.setObjectName("hostname")
        self.hostname.returnPressed.connect(self.runportscan)
        self.nmapscan = QtWidgets.QPushButton(self.centralwidget)
        self.nmapscan.setGeometry(QtCore.QRect(280, 360, 121, 23))
        self.nmapscan.setObjectName("nmapscan")
        self.nmapscan.clicked.connect(self.run_viz)
        self.scannedips = QtWidgets.QListWidget(self.centralwidget)
        self.scannedips.setGeometry(QtCore.QRect(120, 300, 131, 131))
        self.scannedips.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.scannedips.addItem(item)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 290, 91, 21))
        self.label.setObjectName("label")
        self.statsname = QtWidgets.QLabel(self.centralwidget)
        self.statsname.setObjectName(u"statsname")
        self.statsname.setGeometry(QtCore.QRect(20, 330, 80, 80))
        self.movie = QtGui.QMovie("res/1479.gif")
        self.statsname.setMovie(self.movie)
        self.movie.start()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NARAD"))
        self.rundiscovery.setText(_translate("MainWindow", "Discover"))
        self.portscan.setText(_translate("MainWindow", "Port Scan"))
        self.nmapscan.setText(_translate("MainWindow", "Visualize PCAP"))
        __sortingEnabled = self.scannedips.isSortingEnabled()
        self.scannedips.setSortingEnabled(False)
        item = self.scannedips.item(0)
        self.scannedips.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "URL/IP (Target)"))
    def runportscan(self):
      self.movie.start()

      host_raw = self.hostname.text()
      if host_raw == "":
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText("Alert !!")
        self.msg.setInformativeText("You Forgot to Enter a host")
        self.msg.setWindowTitle("Warning")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok )
        self.msg.show()
        return
      else:
        regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
        p = re.compile(regex)
        if(re.search(p,host_raw)):
          host_parsed=  urllib.parse.urlparse(host_raw)
          host=host_parsed.netloc
        else:
          host = host_raw
        try:
          data, ip= portscanner.run(host)
        except:
          self.msg = QtWidgets.QMessageBox()
          self.msg.setIcon(QtWidgets.QMessageBox.Warning)
          self.msg.setText("Error")
          self.msg.setInformativeText("You Entered Invalid URL or IP")
          self.msg.setWindowTitle("Error")
          self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
          retval = self.msg.show()
          print("Clicked button ",retval)
          QtWidgets.QApplication.processEvents()
          return
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
      self.cmd_win = threadedcommand.commwin()
      self.cmd_win.process.stateChanged.connect(self.cmd_win.handle_state)
      self.cmd_win.show()
      self.cmd_win.run("nmap -v -A " +host_raw )
      self.cmd_cve = nmap_cvesuggester.commwin()
      self.cmd_cve.process.stateChanged.connect(self.cmd_cve.handle_state)
      self.cmd_cve.show()
      self.cmd_cve.run(host_raw)

    def add_items(self,ips):
      self.scannedips.addItem(str(ips))

    def rdiscovery(self):
      self.scannedips.clear()
      self.thread = QThread()
      self.worker = Worker()
      self.worker.moveToThread(self.thread)
      self.thread.started.connect(self.worker.run)
      self.worker.finished.connect(self.thread.quit)
      self.worker.finished.connect(self.worker.deleteLater)
      self.thread.finished.connect(self.thread.deleteLater)
      self.worker.progress.connect(self.add_items)
      self.thread.start()
      # Final resets
      self.rundiscovery.setEnabled(False)
      self.thread.finished.connect(lambda: self.rundiscovery.setEnabled(True))


      #nm = nmap.PortScanner()

      #nm.scan(hosts=base_ip, arguments='-n -sP -PE -PA21,23,80,3389')
      #hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
      #hosts_list = list(dict.fromkeys(hosts_list))
      #for host, status in hosts_list:

      QtWidgets.QApplication.processEvents()

    def run_viz(self):
      filename = None
      filename = QtWidgets.QFileDialog.getOpenFileName()
      if filename[0] != '':
        w = PlotCanvas(filename[0])
        w.show()

