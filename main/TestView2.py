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
        self.myLayout = QVBoxLayout()
        self.iconQLabel      = QLabel()
        self.myLayout.addWidget(self.iconQLabel)
        self.setLayout(self.myLayout)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath).scaled(200, 200))

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
        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('Test')
        self.show()

    def buttonClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        video = VideoDemo(fname[0])
        list_distance = video.calcDifferent();

        # Chuyen ve dang numpy.array de ve do thi tren matplotlib
        array_distance = np.array(list_distance.items(), dtype='float')
        higher = video.calcHigherDegree(list_distance)
        list_threshold = video.calcAdaptiveThreshold(list_distance, 1, higher)
        print higher
        arr_threshold = np.array(list_threshold.items(), dtype='float')  # nguong adaptive

        list_boundary = video.calcBoundary(list_distance, list_threshold)
        video.getBoundary(list_boundary)

        plt.plot(arr_threshold[0:200, 0], arr_threshold[0:200, 1], 'red', array_distance[0:200, 0],
                 array_distance[0:200, 1], 'blue')
        plt.ylabel('distance')
        plt.show()

    def showBoundaryFrame(self, video, list_boundary):
        start = video.rfind('/')
        end = video.rfind('.')
        name = video[start + 1: end]
        dirname = '/home/hoangnh/boundary/' + name + '_boundary/'
        self.myQListWidget = QListWidget(self.rightFrame)
        files = []
        for file in os.listdir(dirname):
            if file.endswith(".png"):
                files.append(os.path.join(dirname, file))

        for image in files:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setIcon(image)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.rightFrame.setCentralWidget(self.myQListWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = exampleQMainWindow()
    sys.exit(app.exec_())