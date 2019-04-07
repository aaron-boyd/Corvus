from PyQt5 import QtCore,QtWidgets,QtGui
from Corvus2DPlotWidget import Corvus2DPlotWidget
from Corvus3DPlotWidget import Corvus3DPlotWidget
from CorvusGLWidget import CorvusGLWidget

class CorvusPlotsWidget(QtWidgets.QTabWidget):

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        
        self.label2D = QtWidgets.QLabel("2D Plot")
        self.label3D = QtWidgets.QLabel("3D Plot")
        self.plot2D = Corvus2DPlotWidget(self)
        self.plot3D = CorvusGLWidget(self)
        self.addTab(self.plot2D,"2D Plot")
        self.addTab(self.plot3D,"3D Plot")
        self.setFixedSize(QtCore.QSize(600,600))

    def create3DPoints(self, byts):
        self.coords = self.convertBytesTo3DCoords(byts)

        def shiftPoint(byt):
            x = (byt[0] - (255.0 / 2.0)) / 255.0
            y = (byt[1] - (255.0 / 2.0)) / 255.0
            z = (byt[2] - (255.0 / 2.0)) / 255.0
            return (x, y, z)

        self.coords = [shiftPoint(p) for p in self.coords]

        self.updateOpenGL()

    def updateOpenGL(self):
        self.plot3D.points = self.coords
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