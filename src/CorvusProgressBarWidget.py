from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QBasicTimer
from PyQt5 import QtCore
import sys

# Author: Yoann
# Date: Oct 18, 2013
# Availability: https://stackoverflow.com/questions/19442443/busy-indication-with-pyqt-progress-bar

class CorvusProgressBarWidget(QWidget):

    def __init__(self, parent=None):
        super(CorvusProgressBarWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setRange(0,1)
        layout.addWidget(self.progressBar)
        button = QtGui.QPushButton("Start", self)
        layout.addWidget(button)      

        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

    def onStart(self): 
        self.progressBar.setRange(0,0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0,1)


class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        time.sleep(3)
        self.taskFinished.emit()