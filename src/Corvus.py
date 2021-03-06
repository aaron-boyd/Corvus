#!/usr/bin/python3

import sys
import time
import hexdump
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
from CorvusHexDumpWidget import CorvusHexDumpWidget
from CorvusPlotsWidget import CorvusPlotsWidget
from CorvusHeatMapGLWidget import CorvusHeatMapGLWidget
from CorvusByteFrequencyWidget import CorvusByteFrequencyWidget

here = path.abspath(path.dirname(__file__))

class CorvusMainWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.bytes = []

        self.hexDump = CorvusHexDumpWidget()
        self.plotsWidget = CorvusPlotsWidget()
        self.heatMap = CorvusHeatMapGLWidget()
        self.frequencyMap = CorvusByteFrequencyWidget()
        self.setLayout(self.creatGridLayout())

    def creatGridLayout(self):
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.plotsWidget,0,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.heatMap,0,0,1,1,QtCore.Qt.AlignCenter)
        layout.addWidget(self.hexDump,0,2,1,1,QtCore.Qt.AlignLeft)

        return layout

    # File Dialog
    # Author: Pythonspot
    # Date: 2017
    # Availability: https://pythonspot.com/pyqt5-file-dialog/
    def getFileName(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileNames = QtCore.QStringListModel()

        if dlg.exec_():
            fileNames = dlg.selectedFiles()
            return fileNames[0]
        else:
            return None


    def openFile(self):
        self.fileName = self.getFileName()

        if self.fileName is not None:
            start_time = time.time()
            print("Processing \"%s\"..." % (self.fileName))
            self.getBytesFromFile()
            # self.frequencyMap.frequencyGradients(self.bytes)
            print("Generating hex dump...")
            self.hexDump.populateHexDumpWidget(self.bytes)
            print("Generating 2D plot...")
            self.plotsWidget.create2DPoints(list(self.bytes))
            print("Generating 3D plot...")
            self.plotsWidget.create3DPoints(list(self.bytes))
            print("Generating heat map...")
            self.heatMap.createPoints(list(self.bytes))
            self.heatMap.updateObject()
            print("File size: %0.2fMB" % (len(self.bytes) / 1000000.0))
            print("Process time: %0.5f seconds" % (time.time() - start_time))


    def getBytesFromFile(self): # open up the file and get all the bytes
        try:
            f = open(self.fileName, "rb")
            self.hexDump.hexDumpString = ""
        except:
            print("ERROR: Could not find %s" % self.fileName)
            return

        self.bytes = []

        byte = f.read(1)

        while byte:
            self.bytes.append(byte)
            byte = f.read(1)


class CorvusMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.mainWidget = CorvusMainWidget()

        # appStyle
        # Author: alphanumeric and Trilarion
        # Date: Feb 12, 2015
        # Availability: https://stackoverflow.com/questions/28481109/how-to-change-color-of-qmainwindow-borders-and-title-bar
        appStyle="""
        QMainWindow{
        background-color: black;
        }
        """
        self.setStyleSheet(appStyle)

        mainMenu = self.menuBar()
        menuBar = mainMenu.addMenu("File")
        menuBar.addAction("Open", self.mainWidget.openFile)

        # Corvus Icon
        # Author: John Smith
        # Date: April 24, 2011
        # Availability: http://www.clker.com/clipart-raven-1.html
        self.setWindowIcon(QtGui.QIcon(here + '/CorvusIcon.png'))

        self.setCentralWidget(self.mainWidget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusMainWindow()
    window.show()
    sys.exit(app.exec_())
