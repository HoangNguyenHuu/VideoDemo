import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from MyVideo import VideoDemo
import numpy as np

class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.allQHBoxLayout  = QHBoxLayout()
        self.textLabel = QLabel()
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setFixedWidth(100)
        self.iconQLabel1      = QLabel()
        self.iconQLabel2      = QLabel()

        self.allQHBoxLayout.addWidget(self.textLabel, 0)
        self.allQHBoxLayout.addWidget(self.iconQLabel1, 1)
        self.allQHBoxLayout.addWidget(self.iconQLabel2, 2)
        self.setLayout(self.allQHBoxLayout)

    def setText(self, text):
        self.textLabel.setText(text)
    def setLeftIcon (self, imagePath):
        self.iconQLabel1.setPixmap(QPixmap(imagePath).scaled(270, 150))
    def setRightIcon (self, imagePath):
        self.iconQLabel2.setPixmap(QPixmap(imagePath).scaled(270, 150))

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.leftFrame = QFrame(self)
        self.rightFrame = QFrame(self)

        self.leftFrame.resize(300, 600)
        self.leftFrame.move(0,0)
        # self.leftFrame.setStyleSheet("background-color: green")

        self.rightFrame.resize(700, 600)
        self.rightFrame.move(300,0)

        btn1 = QPushButton("Select your video", self.leftFrame)
        btn1.move(80, 300)

        self.labelShot = QLabel("", self.rightFrame)
        self.labelShot.setAlignment(Qt.AlignCenter)
        self.labelShot.resize(100, 50)
        self.labelShot.move(0,0)

        self.labelFirstFrame = QLabel("Please select your video", self.rightFrame)
        self.labelFirstFrame.setAlignment(Qt.AlignCenter)
        self.labelFirstFrame.resize(270, 50)
        self.labelFirstFrame.move(130, 0)

        self.labelLastFrame = QLabel("", self.rightFrame)
        self.labelLastFrame.setAlignment(Qt.AlignCenter)
        self.labelLastFrame.resize(270, 50)
        self.labelLastFrame.move(400, 0)


        self.myQListWidget = QListWidget(self.rightFrame)
        self.myQListWidget.resize(700, 550)
        self.myQListWidget.move(0, 50)
        # self.myQListWidget.setStyleSheet("background-color: red")

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(200, 100, 1000, 600)
        self.setWindowTitle('Video Demo')
        self.show()

    def buttonClicked(self):
        self.labelFirstFrame.setText("Please Wait...")
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        video = VideoDemo(fname[0])
        list_distance = video.calcDifferent();

        # Chuyen ve dang numpy.array de ve do thi tren matplotlib
        array_distance = np.array(list_distance.items(), dtype='float')
        higher = video.calcHigherDegree(list_distance)
        list_threshold = video.calcAdaptiveThreshold(list_distance, 2, higher)
        # print higher
        arr_threshold = np.array(list_threshold.items(), dtype='float')  # nguong adaptive

        list_boundary = video.calcBoundary(list_distance, list_threshold)
        video.getShotFrame(list_boundary)

        # plt.plot(arr_threshold[0:200, 0], arr_threshold[0:200, 1], 'red', array_distance[0:200, 0],
        #          array_distance[0:200, 1], 'blue')
        # plt.ylabel('distance')
        # plt.show()
        self.link = str(fname[0])

        self.testShow()

    def testShow(self):
        self.labelShot.setText("Shot")
        self.labelFirstFrame.setText("First Frame")
        self.labelLastFrame.setText("Last Frame")
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = '/home/hoangnh/boundary/' + name + '_boundary/'
        files = []
        for file in os.listdir(dirname):
            if file.endswith(".png"):
                files.append(os.path.join(dirname, file))

        files = sorted(files)
        step = len(files) / 2
        file1 = files[0: step]
        file1.sort(key=len)
        file2 = files[step: len(files)]
        file2.sort(key=len)

        for key in range(0, len(file1)):
            # print key
            text = "Shot " + str(key)
            imageLeft = file1[key]
            imgeRight = file2[key]
            # print imageLeft
            # print imgeRight

            # print "----"

            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setLeftIcon(imageLeft)
            myQCustomQWidget.setRightIcon(imgeRight)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def showBoundaryFrame(self):
        dirname = '/home/hoangnh/boundary/testvideo_boundary/'
        files = []
        for file in os.listdir(dirname):
            if file.endswith(".png"):
                files.append(os.path.join(dirname, file))

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

    def insertItem(self, ):
        for i in range(1, 100):
            self.myQListWidget.addItem(str(i))
            self.myQListWidget.repaint()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = exampleQMainWindow()
    sys.exit(app.exec_())