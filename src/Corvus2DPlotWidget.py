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

class CorvusMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        style.use(['dark_background'])

        self.fig = Figure(figsize=(width,height),dpi=dpi,facecolor=(0.0, 0.0, 0.0))

        self.compute_initial_figure()

        FigureCanvas.__init__(self,self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class Corvus2DPlotWidget(CorvusMplCanvas):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.computeInitialFigure()

    def computeInitialFigure(self):
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_off()
        self.axes.set_facecolor((0.0, 0.0, 0.0))
        self.axes.axis([0, 255, 0, 255])
        self.axes.set_ylim(self.axes.get_ylim()[::-1]) 

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

            if len(coords) == 255 * 255:
                break

        return xvals, yvals

    def updatePlot(self, byts):
        self.axes.cla()
        x,y = self.convertBytesTo2DCoords(byts)
        self.axes.plot(x,y,'wo', markersize=1)
        self.axes.set_axis_off()
        self.axes.axis([0, 255, 0, 255])
        self.axes.set_ylim(self.axes.get_ylim()[::-1])
        self.draw()


