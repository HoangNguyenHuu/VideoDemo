import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

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
        self.setCentralWidget(self.myQListWidget)

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())