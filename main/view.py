import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from MyVideo import VideoDemo
import numpy as np
import cv2

class QCustomQWidget (QWidget):
    def __init__ (self, name, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.name = name
        self.allQHBoxLayout  = QHBoxLayout()
        self.textLabel = QLabel("")
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.textLabel.setFixedWidth(300)
        self.iconQLabel1      = QLabel()
        self.buttonShow      = QPushButton("Show")
        self.buttonShow.clicked.connect(self.showShot)

        self.allQHBoxLayout.addWidget(self.textLabel, 0)
        self.allQHBoxLayout.addWidget(self.iconQLabel1, 1)
        self.allQHBoxLayout.addWidget(self.buttonShow, 2)
        self.setLayout(self.allQHBoxLayout)

    def setText(self, text):
        self.textLabel.setText(text)
    def setKeyIcon (self, imagePath):
        self.iconQLabel1.setPixmap(QPixmap(imagePath).scaled(300, 168))
    def showShot (self):
        print self.name
        cap = cv2.VideoCapture(self.name)

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret != True:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', gray)
            if cv2.waitKey(120) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(-1)
        cv2.waitKey(-1)
        cv2.waitKey(-1)
        cv2.waitKey(-1)

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        # self.leftFrame = QFrame(self)
        # self.rightFrame = QFrame(self)
        #
        # self.leftFrame.resize(300, 600)
        # self.leftFrame.move(0,0)
        # # self.leftFrame.setStyleSheet("background-color: green")
        #
        # self.rightFrame.resize(700, 600)
        # self.rightFrame.move(300,0)

        btn1 = QPushButton("Select your video", self)
        btn1.resize(200, 30)
        # btn1.setStyleSheet("background-color: green")
        btn1.move(30, 30)

        self.labelInformation = QLabel("", self)
        # self.labelInformation.setStyleSheet("background-color: red")
        # self.labelInformation.setAlignment(Qt.AlignCenter)
        self.labelInformation.resize(300, 30)
        self.labelInformation.move(300, 30)

        self.labelShot = QLabel("", self)
        self.labelShot.setAlignment(Qt.AlignCenter)
        self.labelShot.resize(300, 50)
        self.labelShot.move(0,50)

        self.labelKeyFrame = QLabel("Please select your video", self)
        self.labelKeyFrame.setAlignment(Qt.AlignCenter)
        self.labelKeyFrame.resize(300, 50)
        self.labelKeyFrame.move(300, 50)

        self.labelShow = QLabel("", self)
        self.labelShow.setAlignment(Qt.AlignCenter)
        self.labelShow.resize(300, 50)
        self.labelShow.move(600, 50)


        self.myQListWidget = QListWidget(self)
        self.myQListWidget.resize(900, 500)
        self.myQListWidget.move(0, 100)
        # self.myQListWidget.setStyleSheet("background-color: red")

        btn1.clicked.connect(self.buttonClicked)

        self.setGeometry(200, 100, 900, 600)
        self.setWindowTitle('Video Demo')
        self.show()

    def buttonClicked(self):
        self.labelKeyFrame.setText("Please Wait...")
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        video = VideoDemo(fname[0])
        validVideo = video.validVideo()
        self.labelInformation.setText(validVideo['info'])
        if validVideo["flag"] == False:
            return

        list_distance = video.calcDifferent()

        # Chuyen ve dang numpy.array de ve do thi tren matplotlib
        array_distance = np.array(list_distance.items(), dtype='float')
        higher = video.calcHigherDegree(list_distance)
        list_threshold = video.calcAdaptiveThreshold(list_distance, 2, higher)
        # print higher
        arr_threshold = np.array(list_threshold.items(), dtype='float')  # nguong adaptive

        list_boundary = video.calcBoundary(list_distance, list_threshold)
        list_key = video.getKeyFrame(list_boundary)
        list_begin = list_key['begin']
        list_end = list_key['end']
        video.getShotVideo(list_begin, list_end)


        # plt.plot(arr_threshold[0:200, 0], arr_threshold[0:200, 1], 'red', array_distance[0:200, 0],
        #          array_distance[0:200, 1], 'blue')
        # plt.ylabel('distance')
        # plt.show()
        self.link = str(fname[0])

        self.testShow()

    def testShow(self):
        self.labelShot.setText("Shot")
        self.labelKeyFrame.setText("Key Frame")
        self.labelShow.setText("Show")
        start = self.link.rfind('/')
        end = self.link.rfind('.')
        name = self.link[start + 1: end]
        dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_keyframe/'
        dirname2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + name + '_shotvideo/'
        files = []
        for file in os.listdir(dirname):
            if file.endswith(".png"):
                files.append(os.path.join(dirname, file))

        files = sorted(files)
        files.sort(key=len)

        for key in range(0, len(files)):
            # print key
            text = "shot " + str(key)
            keyFrame = files[key]
            # print imageLeft
            # print imgeRight

            # print "----"
            this_dirname = dirname2 + "shot"+str(key)+".avi"
            myQCustomQWidget = QCustomQWidget(this_dirname)
            myQCustomQWidget.setText(text)
            myQCustomQWidget.setKeyIcon(keyFrame)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = exampleQMainWindow()
    sys.exit(app.exec_())