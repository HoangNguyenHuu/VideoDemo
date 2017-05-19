import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MyVideo import VideoDemo
import numpy as np
import matplotlib.pyplot as plt
import cv2

class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        # self.textQVBoxLayout = QVBoxLayout()
        # self.textUpQLabel    = QLabel()
        # self.textDownQLabel  = QLabel()
        # self.textQVBoxLayout.addWidget(self.textUpQLabel)
        # self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        # self.myLayout = QVBoxLayout()
        self.textLabel = QLabel()
        self.iconQLabel1      = QLabel()
        self.iconQLabel2      = QLabel()

        self.allQHBoxLayout.addWidget(self.textLabel, 0)
        self.allQHBoxLayout.addWidget(self.iconQLabel1, 1)
        self.allQHBoxLayout.addWidget(self.iconQLabel2, 2)
        # self.setLayout(self.myLayout)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        # self.textUpQLabel.setStyleSheet('''
        #     color: rgb(0, 0, 255);
        # ''')
        # self.textDownQLabel.setStyleSheet('''
        #     color: rgb(255, 0, 0);
        # ''')

    def setText(self, text):
        self.textLabel.setText(text)
    def setLeftIcon (self, imagePath):
        self.iconQLabel1.setPixmap(QPixmap(imagePath).scaled(240, 135))
    def setRightIcon (self, imagePath):
        self.iconQLabel2.setPixmap(QPixmap(imagePath).scaled(240, 135))

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.leftFrame = QFrame(self)
        self.rightFrame = QFrame(self)

        self.leftFrame.resize(300, 600)
        self.leftFrame.move(0,0)
        self.leftFrame.setStyleSheet("background-color: green")

        self.rightFrame.resize(700, 600)
        self.rightFrame.move(300,0)

        btn1 = QPushButton("Select your video", self.leftFrame)
        btn1.move(80, 300)

        self.myQListWidget = QListWidget(self.rightFrame)
        self.myQListWidget.resize(700, 600)
        self.myQListWidget.move(0,0)

        files = []
        for file in os.listdir("/home/hoangnh/boundary/testvideo_boundary/"):
            if file.endswith(".png"):
                files.append(os.path.join("/home/hoangnh/boundary/testvideo_boundary/", file))

        files = sorted(files)
        step = len(files) / 2
        file1 = files[0: step]
        file1.sort(key=len)
        file2 = files[step: len(files)]
        file2.sort(key=len)
        for key in range(0, len(file1)):
            print key
            text = "Shot " + str(key)
            imageLeft = file1[key]
            imgeRight = file2[key]
            print imageLeft
            print imgeRight

            print "----"

            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setLeftIcon(imageLeft)
            myQCustomQWidget.setRightIcon(imgeRight)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('Test')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = exampleQMainWindow()
    sys.exit(app.exec_())