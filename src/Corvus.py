import sys
import time
import hexdump
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
from CorvusHexDumpWidget import CorvusHexDumpWidget
from CorvusPlotsWidget import CorvusPlotsWidget
from CorvusHeatMapWidget import CorvusHeatMapWidget
from CorvusHeatMapGLWidget import CorvusHeatMapGLWidget

appStyle="""
QMainWindow{
background-color: black;
}
"""

here = path.abspath(path.dirname(__file__))

class CorvusMainWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.bytes = []

        self.hexDump = CorvusHexDumpWidget()
        self.plotsWidget = CorvusPlotsWidget()
        self.heatMap = CorvusHeatMapGLWidget()
        self.setLayout(self.creatGridLayout())

    def creatGridLayout(self):
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.plotsWidget,0,1,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.heatMap,0,0,1,1,QtCore.Qt.AlignCenter)
        #layout.addWidget(self.hexDump,0,2,1,1,QtCore.Qt.AlignLeft)

        return layout


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
            #print("Generating hex dump...")
            #self.hexDump.populateHexDumpWidget(self.bytes)
            print("Generating 2D plot...")
            self.plotsWidget.create2DPoints(list(self.bytes))
            print("Generating 3D plot...")
            self.plotsWidget.create3DPoints(list(self.bytes))
            print("Generating heat map...")
            self.heatMap.createPoints(list(self.bytes))
            self.heatMap.updateObject()
            print("File size: %0.2fMB" % (len(self.bytes) / 1000000.0))
            print("Process time: %0.5f seconds" % (time.time() - start_time))

    
    def getBytesFromFile(self):
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

        self.setStyleSheet(appStyle)
        mainMenu = self.menuBar()
        menuBar = mainMenu.addMenu("File")
        menuBar.addAction("Open", self.mainWidget.openFile)
        self.setWindowIcon(QtGui.QIcon(here + '/CorvusIcon.png'))
        self.setCentralWidget(self.mainWidget)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusMainWindow()
    window.show()
    sys.exit(app.exec_())
