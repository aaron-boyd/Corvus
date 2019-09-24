import sys
import OpenGL.GL as gl
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget)

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

class CorvusByteFrequencyWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(CorvusByteFrequencyWidget, self).__init__(parent)

        self.object = 0

        self.width = 400
        self.height = 400
        self.black = QColor.fromRgb(0.0,0.0,0.0)
        self.setFixedSize(self.width, self.height)


    def frequencyGradients(self,byts):
        byteStrs = list(map(lambda b: b.hex().upper(), byts))
        lenBytes = len(byts)

        def convertIntToHexString(x):
            return '%0*X' % (2,x)
        def findFrequency(x):
            return byteStrs.count(convertIntToHexString(x)) / lenBytes
  
        self.frequencies = {convertIntToHexString(x) : findFrequency(x) for x in range(0,256)}
        print(self.frequencies)
    

    def minimumSizeHint(self):
        width = 50
        height = 50
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

    # Drawing rectangles
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