import sys
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)
import OpenGL.GL as gl

class CorvusHeatMapGLWidget(QGLWidget):

    def __init__(self, parent=None):
        super(CorvusHeatMapGLWidget, self).__init__(parent)

        self.object = 0
        self.bytesPerLine = 32
        self.pixelsPerByte = self.bytesPerLine / 4
        self.bytes = []
        self.points = [(0,0)]

        self.width =500
        self.height = 500

        self.points = []

        self.black = QColor.fromRgb(0.0,0.0,0.0)

    def createPoints(self,byts):
        self.bytes = byts
        x = 1
        y = 1
        for i in range(0, len(self.bytes)):
            self.points.append((x,y))
            x += 1
            if((x+1) % self.bytesPerLine == 0 ):
                x = 1
                y += 1
        print(len(self.points))

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(self.width, self.height)


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
        gl.glOrtho(0, self.width, self.height, 0, -255.0, 255.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)


    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)
        gl.glBegin(gl.GL_QUADS)

        for i in range(0,len(self.points)):

            x1 = self.points[i][0] * self.pixelsPerByte
            y1 = self.points[i][1] * self.pixelsPerByte

            x3 = x1 + self.pixelsPerByte
            y3 = y1 + self.pixelsPerByte

            x2 = x1
            y2 = y1 + self.pixelsPerByte

            x4 = x1 + self.pixelsPerByte
            y4 = y1 
            self.qglColor(QColor.fromRgb(0.0, int(self.bytes[i].hex(), 16), 0.0))

            self.quad(x1, y1, x2, y2, x3, y3, x4, y4)

        gl.glEnd()

        gl.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        #gl.glBegin(primitive)

        gl.glVertex2d(x1, y1)
        gl.glVertex2d(x2, y2)
        gl.glVertex2d(x3, y3)
        gl.glVertex2d(x4, y4)

        #gl.glEnd()

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())


def main():
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusHeatMapGLWidget()
    #window.createPoints([1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1,6,3,6,32,2,52,1])
    window.createPoints([b'i', b'm', b'p', b'o', b'r', b't', b' ', b'm', b'a', b't', b'p', b'l', b'o', b't', b'l', b'i', b'b', b'.', b'p', b'y'])
    window.updateObject()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()