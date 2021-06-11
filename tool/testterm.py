from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout,QLabel,QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from subprocess import Popen,PIPE
import sys,shlex,os,signal
class AnotherWindow(QWidget):
  errorSignal = pyqtSignal(str)
  outputSignal =pyqtSignal(str)
  def __init__(self):
    super().__init__()
    Term = self
    if not Term.objectName():
      Term.setObjectName(u"Term")
    Term.resize(415,385)
    Term.setStyleSheet(u"background-color: rgb(50, 50, 50);")

    self.gridLayout = QGridLayout(Term)
    self.gridLayout.setObjectName(u"gridLayout")
    self.outcommand = QTextBrowser(Term)
    self.outcommand.setObjectName(u"outcommand")
    self.outcommand.setStyleSheet(u"background-color: rgb(50, 50, 50);\n""alternate-background-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);")
    self.gridLayout.addWidget(self.outcommand,0,0,1,2)
    #self.command = QLineEdit(Term)
    #self.command.setObjectName(u"command")
    #self.command.returnPressed.connect(self.runcommand)
    #self.gridLayout.addWidget(self.command,1,0,1,1)
    self.command = QLineEdit(Term)
    self.command.setObjectName("command")
    self.command.setFocus(True)
    self.command.setStyleSheet(u"background-color: rgb(50, 50, 50);\n""alternate-background-color: rgb(255, 255, 255);\n" "color: rgb(255, 255, 255);")
    self.gridLayout.addWidget(self.command, 1, 0, 1, 1)
    self.command.returnPressed.connect(self.run)
    self.output = None
    self.error = None
    self._pid = -1
    self.terminate = QPushButton(Term)
    self.terminate.setObjectName(u"terminate")
    self.gridLayout.addWidget(self.terminate, 1, 1, 1, 1)
    self.terminate.clicked.connect(self.stop_process)
    self.process = QProcess()
    self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
    self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
    self.retranslateUi(Term)
    QMetaObject.connectSlotsByName(Term)
    Term.setLayout(self.gridLayout)

  def retranslateUi(self,Term):
    Term.setWindowTitle(QCoreApplication.translate("Term",u"Form",None))
    self.terminate.setText(QCoreApplication.translate("Term", u"Terminate", None))
  def onReadyReadStandardError(self):
    error = self.process.readAllStandardError().data().decode()
    self.outcommand.append(error)
    self.errorSignal.emit(error)

  def onReadyReadStandardOutput(self):
    result = self.process.readAllStandardOutput().data().decode()
    self.outcommand.append(result)
    self.outputSignal.emit(result)
  #def finished(self):
    #self.outcommand.append("Process Finished")
  def stop_process(self):
    if self._pid > 0:
      self.process.terminate()

  def runc(self,command):
    self.outcommand.clear()
    self.process.start(command)
    self._pid = self.process.pid()
  def run(self):
    command = self.command.text()
    self.command.clear()
    if command == "clear":
      self.outcommand.clear()
    elif command == "exit":
      sys.exit(app)
    else:
      self.process.start(command)
      self._pid  = self.process.pid()
      print(self._pid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AnotherWindow()
    w.show()
    w.errorSignal.connect(lambda error: print(error))
    #w.outputSignal.connect(lambda output: print(output))
    #w.process.finished.connect(w.finished)
    w.runc("ls")
    sys.exit(app.exec_())
