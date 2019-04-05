import sys
import random
import hexdump
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
from CorvusHexDumpWidget import CorvusHexDumpWidget
from CorvusPlotsWidget import CorvusPlotsWidget
from CorvusHeatMapWidget import CorvusHeatMapWidget

appStyle="""
QMainWindow{
background-color: darkgrey;
}
"""

here = path.abspath(path.dirname(__file__))


class CorvusMainWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.hexDump = CorvusHexDumpWidget() 
        self.plotsWidget = CorvusPlotsWidget()
        self.heatMap = CorvusHeatMapWidget()
        self.setLayout(self.creatGridLayout())

    def creatGridLayout(self):
        horizontalGroupBox = QtWidgets.QGroupBox("Main")
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.plotsWidget,0,0,1,1,QtCore.Qt.AlignRight)
        layout.addWidget(self.hexDump,0,1,1,1,QtCore.Qt.AlignCenter)
        layout.addWidget(self.heatMap,0,2,1,1,QtCore.Qt.AlignLeft)
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
            self.hexDump.getBytesFromFile(self.fileName)
            self.hexDump.populateHexDump()
            self.plotsWidget.plot2D.updatePlot(self.hexDump.bytes)
            self.plotsWidget.plot3D.updatePlot(self.hexDump.bytes)
            self.heatMap.addBytesToHeatMap(self.hexDump.bytes)
            self.heatMap.update()


class CorvusMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.mainWidget = CorvusMainWidget()

        self.setStyleSheet(appStyle)
        mainMenu = self.menuBar()
        menuBar = mainMenu.addMenu("File")
        menuBar.addAction("Open",self.mainWidget.openFile)
        self.setWindowIcon(QtGui.QIcon(here + '/bird.png'))
        self.setCentralWidget(self.mainWidget)

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusMainWindow()
    window.show()
    sys.exit(app.exec_())