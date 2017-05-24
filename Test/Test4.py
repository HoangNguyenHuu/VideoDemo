import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        # self.textQVBoxLayout = QVBoxLayout()
        # self.textUpQLabel    = QLabel()
        # self.textDownQLabel  = QLabel()
        # self.textQVBoxLayout.addWidget(self.textUpQLabel)
        # self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QHBoxLayout()
        self.myLayout = QVBoxLayout()
        self.iconQLabel      = QLabel()
        # self.allQHBoxLayout.addWidget(self.iconQLabel)
        # self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.myLayout.addWidget(self.iconQLabel)
        self.setLayout(self.myLayout)
        # self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        # self.textUpQLabel.setStyleSheet('''
        #     color: rgb(0, 0, 255);
        # ''')
        # self.textDownQLabel.setStyleSheet('''
        #     color: rgb(255, 0, 0);
        # ''')

    # def setTextUp (self, text):
    #     self.textUpQLabel.setText(text)
    #
    # def setTextDown (self, text):
    #     self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath).scaled(200, 200))

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.myQListWidget = QListWidget(self)
        files = []
        for file in os.listdir("/home/hoangnh/OpenCVJupyter/"):
            if file.endswith(".jpg"):
                files.append(os.path.join("/home/hoangnh/OpenCVJupyter/", file))

        for x in files:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setIcon(x)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        # for index, name, icon in [
        #     ('No.1', 'Meyoko',  'icon.png'),
        #     ('No.2', 'Nyaruko', 'icon.png'),
        #     ('No.3', 'Louise',  'icon.png')]:
        #     # Create QCustomQWidget
        #     myQCustomQWidget = QCustomQWidget()
        #     # myQCustomQWidget.setTextUp(index)
        #     # myQCustomQWidget.setTextDown(name)
        #     myQCustomQWidget.setIcon(icon)
        #     # Create QListWidgetItem
        #     myQListWidgetItem = QListWidgetItem(self.myQListWidget)
        #     # Set size hint
        #     myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        #     # Add QListWidgetItem into QListWidget
        #     self.myQListWidget.addItem(myQListWidgetItem)
        #     self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.setCentralWidget(self.myQListWidget)

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())