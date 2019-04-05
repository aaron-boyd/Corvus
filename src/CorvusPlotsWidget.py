from PyQt5 import QtCore,QtWidgets,QtGui
from Corvus2DPlotWidget import Corvus2DPlotWidget
from Corvus3DPlotWidget import Corvus3DPlotWidget

class CorvusPlotsWidget(QtWidgets.QTabWidget):

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        
        self.label2D = QtWidgets.QLabel("2D Plot")
        self.label3D = QtWidgets.QLabel("3D Plot")
        self.plot2D = Corvus2DPlotWidget(self)
        self.plot3D = Corvus3DPlotWidget(self)

        self.addTab(self.plot2D,"2D Plot")
        self.addTab(self.plot3D,"3D Plot")
        self.setFixedSize(QtCore.QSize(600,600))