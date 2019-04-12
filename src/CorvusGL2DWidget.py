from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)
import OpenGL.GL as gl
from CorvusScreenScaler import CorvusScreenScaler
import sys

class CorvusGL2DWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(CorvusGL2DWidget, self).__init__(parent)

        self.object = 0
        
        self.points = []

        self.black = QColor.fromRgb(0.0,0.0,0.0)

    def minimumSizeHint(self):
        width = CorvusScreenScaler.scaleX(50)
        height = CorvusScreenScaler.scaleY(50)
        return QSize(width, height)

    def sizeHint(self):
        width = CorvusScreenScaler.scaleX(500)
        height = CorvusScreenScaler.scaleY(500)
        return QSize(width, height)


    def initializeGL(self):
        self.setClearColor(self.black.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
    
    def updateObject(self):
        self.setClearColor(self.black.darker())
        self.object = self.makeObject()
        self.repaint()
    
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-10.0, +265.0, +265.0, -10.0, -255.0, 255.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)


    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBegin(gl.GL_POINTS)
        
        for p in self.points:
            gl.glVertex2d(p[0],p[1])

        gl.glEnd()
        gl.glEndList()

        return genList


    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

def main():
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusGL2DWidget()
    window.points = [(5,6)]
    window.updateObject()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()