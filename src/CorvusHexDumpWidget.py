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
        self.bytes = []
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
        #print(self.scrollBar.value())
        pass

    def populateHexDump(self):
        self.getHexDump()
        self.setText(self.hexDumpString)
        

    def getBytesFromFile(self,fileName):
        self.fileName = fileName
        try:
            f = open(self.fileName, "rb")
            self.hexDumpString = ""
        except:
            print("ERROR: Could not find %s" % fileName)
            return

        self.bytes = []

        byte = f.read(1)

        while byte:
            self.bytes.append(byte)
            byte = f.read(1)

        self.lines = (len(self.bytes) // 16) + 1
        print("Line Count: ",self.lines)
        self.scrollBar.setMaximum(self.lines)


    def initTextEdit(self):
        self.edit = QtWidgets.QTextEdit()
        self.edit.setReadOnly(True)
        noWrap = QtGui.QTextOption.WrapMode(0)
        self.edit.setWordWrapMode(noWrap)
        self.edit.setFont(QtGui.QFont('Consolas', 10))

    def setText(self, text):
        self.edit.clear()
        self.edit.setPlainText(self.hexDumpString)


    def getHexDump(self):
        with open('/tmp/hexDump.txt', 'w') as f:
            with redirect_stdout(f):
                hexdump.hexdump(b''.join(self.bytes))
            f.close()
        with open('/tmp/hexDump.txt', 'r') as f:
            for line in f:
                self.hexDumpString += line
        os.system("rm /tmp/hexDump.txt")