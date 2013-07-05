#!/usr/bin/python

import sys
import os

from PyQt4 import QtGui, QtCore
from datetime import datetime

import videoWidget

# Main Widget
class MainWidget(QtGui.QWidget):
  
    def __init__(self):

        QtGui.QWidget.__init__(self)

        self.initUI()

        
    def initUI(self):
        
        self.video = videoWidget.VideoWidget()
        self.console = ButtonWidget()

        # initilize a Main Lyout set used widgets to it
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.video)
        mainLayout.addWidget(self.console)
        # Set signals and slots
        self.console.photoBtn.clicked.connect(self.video.screenTimer)
        
        # set Main layout to Dialog
        self.setLayout(mainLayout)

        # create Menubar
        self.show()
        
        
class ButtonWidget(QtGui.QWidget):

    def __init__(self):

        QtGui.QWidget.__init__(self)

        self.initUI()

        
    def initUI(self):

        # Creating Button to call Calendar
        self.photoBtn = QtGui.QPushButton('Ausloeser')
        hbox = QtGui.QHBoxLayout()

        hbox.addWidget(self.photoBtn)       

        self.setLayout(hbox)
        self.show

        
# Main Widget
class MainWindow(QtGui.QMainWindow):
  
    def __init__(self):

        QtGui.QMainWindow.__init__(self)

        self.initUI()

        
    def initUI(self):
        
        self.setCentralWidget(MainWidget())

        # set Initializing Sizes and Name of the Window
        self.setGeometry(300, 300, 1000, 650)
        self.setWindowTitle('Raspberry Pi Photo Booth')

        # Add Menu bar
        menubar = self.menuBar()
        
        #File menu

        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit Application')
        exit.triggered.connect(self.exitFunc)

        self.show()


    def exitFunc(self):

        self.close()

        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
