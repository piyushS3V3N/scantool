from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout,QLabel,QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from subprocess import Popen,PIPE
import sys,shlex

class commwin(QWidget):
  errorSignal = pyqtSignal(str)
  outputSignal =pyqtSignal(str)
  def __init__(self):
    super().__init__()
    Term = self
    if not Term.objectName():
      Term.setObjectName(u"NM-CVE-SUGGEST")
    Term.resize(915,485)
    Term.setStyleSheet(u"background-color: rgb(50, 50, 50);")
    icon = QIcon()
    icon.addPixmap(QPixmap("res/ico.png"), QIcon.Normal, QIcon.Off)
    Term.setWindowIcon(icon)
    self.gridLayout = QGridLayout(Term)
    self.gridLayout.setObjectName(u"gridLayout")
    self.outcommand = QTextBrowser(Term)
    self.outcommand.setObjectName(u"outcommand")
    self.outcommand.setStyleSheet(u"background-color: rgb(50, 50, 50);\n""alternate-background-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);")
    self.gridLayout.addWidget(self.outcommand,0,0,1,1)
    #self.command = QLineEdit(Term)
    #self.command.setObjectName(u"command")
    #self.command.returnPressed.connect(self.runcommand)
    #self.gridLayout.addWidget(self.command,1,0,1,1)
    self.gridLayout.addWidget(self.outcommand, 0, 0, 1, 1)
    self.output = None
    self.error = None
    self.stat = None
    self.process = QProcess()
    self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
    self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
    self.retranslateUi(Term)
    QMetaObject.connectSlotsByName(Term)
    Term.setLayout(self.gridLayout)

  def retranslateUi(self,Term):
    Term.setWindowTitle(QCoreApplication.translate("Term",u"NM-CVE-SUGGEST",None))
  def closeEvent(self, event):
    if hasattr(self, 'process'):
      self.process.terminate()
      self.process.waitForFinished()
      self.process.kill()
  def onReadyReadStandardError(self):
    error = self.process.readAllStandardError().data().decode()
    self.outcommand.append(error)
    self.errorSignal.emit(error)

  def onReadyReadStandardOutput(self):
    result = self.process.readAllStandardOutput().data().decode()
    self.outcommand.append(result)
    self.outputSignal.emit(result)

  def handle_state(self,state):
    states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
    state_name = states[state]
    self.stat = state_name

    #print("State changed: {}".format(state_name))
  def run(self,host):
    self.outcommand.clear()
    self.process.start("nmap -sV --script=vulners "+host)
