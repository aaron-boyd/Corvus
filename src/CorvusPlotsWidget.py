from PyQt5 import QtCore,QtWidgets,QtGui
from CorvusGL2DWidget import CorvusGL2DWidget
from CorvusGL3DWidget import CorvusGL3DWidget
from CorvusHeatMapGLWidget import CorvusHeatMapGLWidget

class CorvusPlotsWidget(QtWidgets.QTabWidget):

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        
        self.label2D = QtWidgets.QLabel("2D Plot")
        self.label3D = QtWidgets.QLabel("3D Plot")
        self.plot2D = CorvusGL2DWidget(self)
        self.plot3D = CorvusGL3DWidget(self)
        self.heatMap = CorvusHeatMapGLWidget(self)
        self.addTab(self.plot2D,"2D Plot")
        self.addTab(self.plot3D,"3D Plot")
        self.addTab(self.heatMap,"Heat Map")
        self.setFixedSize(QtCore.QSize(600,600))

    def create3DPoints(self, byts):
        self.coords3D = self.convertBytesTo3DCoords(byts)

        def shiftPoint(byt):
            x = (byt[0] - (255.0 / 2.0)) / 255.0
            y = (byt[1] - (255.0 / 2.0)) / 255.0
            z = (byt[2] - (255.0 / 2.0)) / 255.0
            return (x, y, z)

        self.coords3D = [shiftPoint(p) for p in self.coords3D]

        self.updateOpen3DGL()

    def create2DPoints(self, byts):
        self.coords2D = self.convertBytesTo2DCoords(byts)

        self.updateOpen2DGL()

    def updateOpen2DGL(self):
        self.plot2D.points = self.coords2D
        self.plot2D.updateObject()
        self.plot2D.repaint()

    def updateOpen3DGL(self):
        self.plot3D.points = self.coords3D
        self.plot3D.updateObject()
        self.plot3D.repaint()


    def convertBytesTo3DCoords(self, byts):
        
        xvals = []
        yvals = []
        zvals = []
        coords = set()

        for i in range(0, len(byts) - 2):
            x = int(byts[i].hex(), 16)
            y = int(byts[i+1].hex(), 16)
            z = int(byts[i+2].hex(), 16)
            if (x,y,z) not in coords:
                xvals.append(x)
                yvals.append(y)
                zvals.append(z)
                coords.add((x,y,z))

        return list(coords)

    def convertBytesTo2DCoords(self, byts):
        
        xvals = []
        yvals = []

        coords = set()

        for i in range(0, len(byts) - 1):
            x = int(byts[i].hex(), 16)
            y = int(byts[i+1].hex(), 16)
            if (x,y) not in coords:
                xvals.append(x)
                yvals.append(y)
                coords.add((x,y))

        return list(coords)