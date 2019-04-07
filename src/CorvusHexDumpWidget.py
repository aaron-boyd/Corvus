import hexdump
from PyQt5 import QtCore,QtWidgets,QtGui
from contextlib import redirect_stdout
import subprocess
import os

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
        self.setFixedSize(QtCore.QSize(650,600))

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
        self.edit.setFont(QtGui.QFont('Consolas', 10))

    def setText(self, text):
        self.edit.clear()
        self.edit.setPlainText(self.hexDumpString)


    def getHexDump(self,byts):
        with open('/tmp/hexDump.txt', 'w') as f:
            with redirect_stdout(f):
                hexdump.hexdump(b''.join(byts))
            f.close()
        with open('/tmp/hexDump.txt', 'r') as f:
            for line in f:
                self.hexDumpString += line
        os.system("rm /tmp/hexDump.txt")