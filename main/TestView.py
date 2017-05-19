import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon, QPixmap


class App(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()


        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self):
        files = []
        self.listWidget = QListWidget()
        for file in os.listdir("/home/hoangnh/OpenCVJupyter/"):
            if file.endswith(".jpg"):
                files.append(os.path.join("/home/hoangnh/OpenCVJupyter/", file))

        for x in files:
            print x
        for x in files:
            item = QListWidgetItem()
            icon = QIcon()
            icon.addPixmap(QPixmap(x), QIcon.Normal, QIcon.Off)
            item.setIcon(icon)
            self.listWidget.addItem(item)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Load image')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())