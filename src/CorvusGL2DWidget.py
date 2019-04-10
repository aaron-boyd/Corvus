import sys
import math
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)
import random
import OpenGL.GL as gl

class CorvusGL2DWidget(QOpenGLWidget):  
    def initializeGL(self):  
        # here openGL is initialized and we can do our real program initialization
        gl.glClearColor(0.1, 0.2, 0.3, 1.0) 

    
    def resizeGL(self, width, height):  
        # openGL remembers how many pixels it should draw,  
        # so every resize we have to tell it what the new window size is it is supposed  
        # to be drawing for
        gl.glViewport(0, 0, width, height)
        

    
    def paintGL(self):  
        # here we can start drawing, on show and on resize the window will redraw  
        # automatically
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  
        # the openGL window has coordinates from (-1,-1) to (1,1), so this fills in   
        # the top right corner with a rectangle. The default color is white.  
        gl.glBegin(gl.GL_POINTS)
        gl.glVertex2d(0.5,0.5)


def main():
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusGL2DWidget()
    window.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    main()
