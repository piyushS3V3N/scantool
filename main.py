#!/usr/bin/python
from gui import *
import sys

from PyQt5 import QtCore, QtGui, QtWidgets



def run_load():
    app1 = QtWidgets.QApplication(sys.argv)



if __name__ == "__main__":
    platform = sys.platform

    if platform.lower() == 'linux':
        print("Woopy Detected : ", platform)
        try:
            import nmap
            run_load()
        except ImportError as e:
            print("Installing requirements")
            os.system("pip install -r requirements.txt")
    elif platform == 'win32' or platform == 'win64':
        print("Woopy Detected : ", platform)
        try:
          import nmap
        except ImportError as e:
          print("Error found")
          os.system("pip install -r requirements.txt")
    else:
        print("Sorry Not A Supported Platform !!!")
        exit(-1)

    try:
      socket.create_connection(('1.1.1.1',53))
      print("Internet Is Connected")
    except OSError:
      print("Error No Internet connection")
      exit()
    #db_ipscan = data_nmap()
    app = QtWidgets.QApplication(sys.argv)
    # Create and display the splash screen
    splash_pix = QtGui.QPixmap('res/splash.png')

    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(True)
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)

    # splash.setMask(splash_pix.mask())

    splash.show()
    splash.showMessage("<h1><font color='White'>Welcome!</font></h1>", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)

    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
           app.processEvents()

    # Simulate something that takes time
    time.sleep(1)

    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    splash.finish(MainWindow)
    sys.exit(app.exec_())
