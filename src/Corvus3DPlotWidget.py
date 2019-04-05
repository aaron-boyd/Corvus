import sys
import os
import random
from numpy import arange,sin,pi
from PyQt5 import QtCore,QtWidgets,QtGui
import matplotlib
from matplotlib import style
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from Corvus2DPlotWidget import CorvusMplCanvas



class Corvus3DPlotWidget(CorvusMplCanvas):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.computeInitialFigure()

    def computeInitialFigure(self):
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes._axis3don = False

    def convertBytesTo3DCoords(self, byts):
        
        style.use(['dark_background'])
        
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

        return xvals, yvals, zvals


    def updatePlot(self,byts):
        x,y,z = self.convertBytesTo3DCoords(byts)
        self.axes.cla()
        self.axes.set_facecolor((0.0, 0.0, 0.0))
        self.axes._axis3don = False
        self.axes.scatter(x,y,z, c='w', marker='o',s=0.5)
        self.draw()