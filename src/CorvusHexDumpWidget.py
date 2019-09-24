import hexdump
import subprocess
import os
import sys
from PyQt5 import QtCore,QtWidgets,QtGui
from contextlib import redirect_stdout


class CorvusHexDumpWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.fileName = ""
        self.hexDumpString = ""

        self.initTextEdit()
        self.initScrollBar()
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Hex Dump")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
        self.setLayout(self.layout)
        self.width = 575
        self.height = 600
        self.setFixedSize(QtCore.QSize(self.width, self.height))

    def initScrollBar(self):
        self.scrollBar = self.edit.verticalScrollBar()
        self.scrollBar.valueChanged.connect(self.printScrollValue)

    def printScrollValue(self):
        pass

    def populateHexDumpWidget(self,byts):
        self.lines = (len(byts) // 16) + 1
        self.scrollBar.setMaximum(self.lines)
        self.getHexDump(byts)
        self.setText(self.hexDumpString)


    def initTextEdit(self):
        self.edit = QtWidgets.QTextEdit()
        self.edit.setReadOnly(True)
        noWrap = QtGui.QTextOption.WrapMode(0)
        self.edit.setWordWrapMode(noWrap)
        font = QtGui.QFont('Consolas', 9)
        font.setStyleHint(QtGui.QFont.Monospace)
        self.edit.setFont(font)

    def setText(self, text):
        self.edit.clear()
        self.edit.setPlainText(self.hexDumpString)


    def getHexDump(self,byts):
        here = os.path.abspath(os.path.dirname(__file__))
        platform = self.getPlatform()

        fileName = here + "/hexDump.txt"

        if platform == "Windows":
            fileName = here + "\hexDump.txt"

        with open(fileName, 'w') as f:
            with redirect_stdout(f):
                hexdump.hexdump(b''.join(byts))
            f.close()
        with open(fileName, 'r') as f:
            for line in f:
                self.hexDumpString += line

        delCommand = "rm " + fileName
        
        if platform == "Windows" : 
            delCommand = "del " + fileName

        os.system(delCommand)

    # Get Platform Information
    # Author: Nat Dunn
    # Date: 2019
    # Availability: https://www.webucator.com/how-to/how-check-the-operating-system-with-python.cfm
    def getPlatform(self):
        platforms = {
            'linux1' : 'Linux',
            'linux2' : 'Linux',
            'darwin' : 'OS X',
            'win32' : 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        
        return platforms[sys.platform]
