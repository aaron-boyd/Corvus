import os
import sys
from PyQt5 import QtCore,QtWidgets,QtGui
import random

class CorvusByteHeatMap(QtWidgets.QWidget):
    
    def __init__(self):
        super(CorvusByteHeatMap, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.squareDim = 5
        self.squares = set()
        self.bytesPerRow = 16
        self.numRows = 128
        self.width = self.squareDim * self.bytesPerRow 
        self.height = self.squareDim * self.numRows
        self.currentLine = 0
        self.byts = []
        self.setFixedSize(QtCore.QSize(self.width, self.height))
        self.show()


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBackgroundMode(QtCore.Qt.OpaqueMode)
        self.drawPoints(qp)
        qp.end()

    def createSquares(self, byts):
        self.byts = byts
        
    def drawPoints(self, qp):
        qp.fillRect(QtCore.QRect(QtCore.QPoint(0,0),QtCore.QPoint(self.width, self.height)), QtCore.Qt.black)
        
        numSquares = self.bytesPerRow * self.numRows

        if self.currentLine + numSquares > len(self.byts):
            numSquares = len(self.byts) - self.currentLine

        x = 0
        y = 0
        count = 0
        for b in self.byts[self.currentLine *16:(self.currentLine + numSquares) * 16]:
            val = int(b.hex(), 16)
            qp.fillRect(QtCore.QRect(QtCore.QPoint(x,y),QtCore.QSize(self.squareDim, self.squareDim)),QtGui.QColor(0,val,0))
            count += 1
            x += self.squareDim 
            if (count + 1) % 16 == 0:
                x = 0
                y += self.squareDim 

   

class CorvusHeatMapWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.heatMap = CorvusByteHeatMap()
        self.scrollBar = QtWidgets.QScrollBar()
        self.label = QtWidgets.QLabel("Byte Heat Map")
        self.scrollBar.setMaximum(0)
        self.scrollBar.setFixedHeight(self.heatMap.height)
        self.setLayout(self.creatGridLayout())
        self.scrollBar.valueChanged.connect(self.printScrollValue)
        self.width = self.heatMap.width + self.scrollBar.width()
        self.height = self.heatMap.height + self.label.height()

    def creatGridLayout(self):
        horizontalGroupBox = QtWidgets.QGroupBox("Heat Map")
        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        layout.addWidget(self.label,0,0,1,2,QtCore.Qt.AlignBottom)
        layout.addWidget(self.heatMap,1,0,1,1,QtCore.Qt.AlignTop)
        layout.addWidget(self.scrollBar,1,1,1,1,QtCore.Qt.AlignTop)
        return layout


    def printScrollValue(self):
        self.heatMap.currentLine = self.scrollBar.value()
        self.heatMap.update()

    def addBytesToHeatMap(self,byts):
        self.heatMap.createSquares(byts)
        self.scrollBar.setMaximum(self.heatMap.numRows)


if __name__ == "__main__":
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusHeatMapWidget()
    fileName = "../parrot.gif"
    try:
        f = open(fileName, "rb")
    except:
        print("ERROR: Could not find %s" % fileName)
        sys.exit()

    byts = []

    byte = f.read(1)

    while byte:
        byts.append(byte)
        byte = f.read(1)
    window.addBytesToHeatMap(byts)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
