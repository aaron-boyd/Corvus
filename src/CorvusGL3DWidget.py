from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)
import OpenGL.GL as gl
from math import pow, sqrt

class CorvusGL3DWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(CorvusGL3DWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.points = []

        self.lastPos = QPoint()

        self.black = QColor.fromRgb(0.0,0.0,0.0)

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(500,500)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

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
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-1.0, +1.0, +1.0, -1.0, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * -dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * -dy)
            self.setZRotation(self.zRot + 8 * -dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND )
        
        gl.glBegin(gl.GL_POINTS)
        
        red = 147.5 / 255.0
        green = 167.1 / 255.0
        blue = 186.2 / 255.0

        for p in self.points:
            x = p[0]
            y = p[1]
            z = p[2]
            alpha =  pow((1.0 - (sqrt(pow(x,2) + pow(y,2) + pow(z,2)) / sqrt(3.0))), 4)
            self.setColor(red, green, blue, alpha)
            gl.glVertex3d(x,y,z)

        gl.glEnd()
        gl.glEndList()

        return genList


    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, red, green, blue, alpha):
        gl.glColor4f(red, green, blue, alpha)
