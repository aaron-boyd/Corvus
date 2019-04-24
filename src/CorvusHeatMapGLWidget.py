import sys
import OpenGL.GL as gl
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)
from CorvusScreenScaler import CorvusScreenScaler

#############################################################################
##
## Copyright (C) 2015 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


class Scrubber():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False

    def getQuadPoints(self):
        x1 = self.x # top left
        y1 = self.y

        x3 = x1 + self.width # top right
        y3 = y1 + self.height

        x2 = x1 # bottom left
        y2 = y1 + self.height

        x4 = x1 + self.width # top right
        y4 = y1
        return x1, y1, x2, y2, x3, y3, x4, y4

    def inside(self,mouseX,mouseY):
        if mouseX >= self.x and mouseX <= self.x + self.width:
            if mouseY >= self.y and mouseY <= self.y + self.height:
                return True
        return False

class CorvusHeatMapGLWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.layout = QtWidgets.QHBoxLayout()

        self.fullHeatMapPlotWidget = FullHeatMapPlotWidget(self)
        self.scrubberHeatMapPlotWidget = HeatMapPlotScrubberWidget(self)
        self.initScrollBar()

        self.layout.addWidget(self.fullHeatMapPlotWidget)
        self.layout.addWidget(self.scrubberHeatMapPlotWidget)
        self.layout.addWidget(self.scrollBar)

        self.setLayout(self.layout)
        self.width = CorvusScreenScaler.scaleX(self.fullHeatMapPlotWidget.width + self.scrubberHeatMapPlotWidget.width + 40)
        self.height = CorvusScreenScaler.scaleY(max(self.fullHeatMapPlotWidget.height, self.scrollBar.height()) + 50)
        self.setFixedSize(QtCore.QSize(self.width,self.height))

    def initScrollBar(self):
        self.scrollBar = QtWidgets.QScrollBar()
        self.scrollBar.setMaximum(10)
        self.scrollBar.setFixedHeight(CorvusScreenScaler.scaleY(self.scrubberHeatMapPlotWidget.height))
        self.scrollBar.valueChanged.connect(self.printScrollValue)

    def printScrollValue(self):
        self.scrubberHeatMapPlotWidget.scroll(self.scrollBar.value())

    def updateObject(self):
        self.fullHeatMapPlotWidget.updateObject()
        self.scrubberHeatMapPlotWidget.updateObject()
        self.scrollBar.setMaximum(self.scrubberHeatMapPlotWidget.numLines)
    
    def createPoints(self, byts):
        self.fullHeatMapPlotWidget.createPoints(byts)
        self.scrubberHeatMapPlotWidget.createPoints(byts)

class FullHeatMapPlotWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(FullHeatMapPlotWidget, self).__init__(parent)

        self.object = 0

        self.bytesPerLine = 250
        self.pixelsPerByte = self.bytesPerLine / 8
        self.bytes = []
        self.points = []
        self.yOffset = 0.0
        self.numLines = 0

        self.width = CorvusScreenScaler.scaleX(250)
        self.height = CorvusScreenScaler.scaleY(550)

        self.scrubbers = [Scrubber(0, 0, self.width, 5),Scrubber(0, 20, self.width, 5)]
        
        
        self.black = QColor.fromRgb(0.0,0.0,0.0)
        self.setFixedSize(self.width, self.height)

    def createPoints(self,byts):
        self.points = []
        self.bytes = byts
        x = 1
        y = 1
        for b in self.bytes:
            self.points.append((x,y))
            x += 1
            if((x+1) % self.bytesPerLine == 0 ):
                self.numLines += 1
                x = 1
                y += 1

    def minimumSizeHint(self):
        width = CorvusScreenScaler.scaleX(50)
        height = CorvusScreenScaler.scaleY(50)
        return QSize(width, height)

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
        gl.glTranslated(0.0, self.yOffset, -10.0)
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
        
        #self.drawScrubbers()

        gl.glBegin(gl.GL_POINTS)

        for i in range(0,len(self.points)):
            colorVal = int(self.bytes[i].hex(),16) / 255.0
            self.setColor(0.0, colorVal, 0.0, 1.0)
            gl.glVertex2d(self.points[i][0], self.points[i][1])
        
        gl.glEnd()
        gl.glEndList()

        return genList

    def drawScrubbers(self):
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND )

        gl.glBegin(gl.GL_QUADS)
        
        for scrubber in self.scrubbers:
            self.setColor(1.0, 1.0, 1.0, 0.8)
            sps = scrubber.getQuadPoints()
            self.quad(sps[0],sps[1],sps[2],sps[3],sps[4],sps[5],sps[6],sps[7])

        gl.glEnd()
        
    def mousePressEvent(self, event):
        mouseX = event.x()
        mouseY = event.y()
        if event.buttons() & Qt.LeftButton:
            for scrubber in self.scrubbers:
                if scrubber.inside(mouseX, mouseY):
                    scrubber.selected = True
                else:
                    scrubber.selected = False
        
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        mouseY = event.y()

        if event.buttons() & Qt.LeftButton:
            for scrubber in self.scrubbers:
                if scrubber.selected:
                    scrubber.y = mouseY

        self.updateObject()
        self.update()
        self.lastPos = event.pos()

    
    # Author: noobtuts.com
    # Date: 2019
    # Availability: http://www.noobtuts.com/python/opengl-introduction
    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        gl.glVertex2d(x1, y1)
        gl.glVertex2d(x2, y2)
        gl.glVertex2d(x3, y3)
        gl.glVertex2d(x4, y4)

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, red, green, blue, alpha):
        gl.glColor4f(red, green, blue, alpha)


class HeatMapPlotScrubberWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(HeatMapPlotScrubberWidget, self).__init__(parent)

        self.object = 0

        self.bytesPerLine = 32
        self.pixelsPerByte = self.bytesPerLine / 8
        self.bytes = []
        self.points = []
        self.yOffset = 0.0
        self.numLines = 0

        self.width = CorvusScreenScaler.scaleX(self.pixelsPerByte * self.bytesPerLine)
        self.height = CorvusScreenScaler.scaleY(550)

        self.black = QColor.fromRgb(0.0,0.0,0.0)
        self.setFixedSize(self.width, self.height)

    def createPoints(self,byts):
        self.points = []
        self.bytes = byts
        x = 1
        y = 1
        for i in range(0, len(self.bytes)):
            self.points.append((x,y))
            x += 1
            if((x+1) % self.bytesPerLine == 0 ):
                self.numLines += 1
                x = 1
                y += 1

    def minimumSizeHint(self):
        width = CorvusScreenScaler.scaleX(50)
        height = CorvusScreenScaler.scaleY(50)
        return QSize(width, height)

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
        gl.glTranslated(0.0, self.yOffset, -10.0)
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


    def scroll(self, offset):
        self.yOffset = -offset
        self.repaint()


    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)
        gl.glBegin(gl.GL_QUADS)

        for i in range(0,len(self.points)):

            x1 = self.points[i][0] * self.pixelsPerByte # top left
            y1 = self.points[i][1] * self.pixelsPerByte

            x3 = x1 + self.pixelsPerByte # top right
            y3 = y1 + self.pixelsPerByte

            x2 = x1 # bottom left
            y2 = y1 + self.pixelsPerByte 

            x4 = x1 + self.pixelsPerByte # top right
            y4 = y1 
            colorVal = int(self.bytes[i].hex(),16) / 255.0 # get heat value from byte

            self.setColor(0.0, colorVal, 0.0, 0.0)
            self.quad(x1, y1, x2, y2, x3, y3, x4, y4) # draw square

        gl.glEnd()

        gl.glEndList()

        return genList

    # Author: noobtuts.com
    # Date: 2019
    # Availability: http://www.noobtuts.com/python/opengl-introduction
    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        gl.glVertex2d(x1, y1)
        gl.glVertex2d(x2, y2)
        gl.glVertex2d(x3, y3)
        gl.glVertex2d(x4, y4)

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, red, green, blue, alpha):
        gl.glColor4f(red, green, blue, alpha)


def main():
    app = QtWidgets.QApplication(["Corvus"])
    window = CorvusHeatMapGLWidget()
    window.createPoints([b'i', b'm', b'p', b'o', b'r', b't', b' ', b'm', b'a', b't', b'p', b'l', b'o', b't', b'l', b'i', b'b', b'.', b'p', b'y'])
    window.updateObject()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()