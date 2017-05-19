import sys
from PyQt5 import QtGui, QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(200,100,600,900)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(20,20,100,700)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(20,800,100,30)
        self.pushButton.setText('show Items')
        self.pushButton.clicked.connect(self.showItems)
        self.timer = QtCore.QTimer()
        for i in range(0,100):
            self.listWidget.addItem(str(i))
            self.listWidget.item(i).setHidden(True)
        self.z = 0

    def showItems(self):
        self.timer.start(100)
        self.timer.timeout.connect(self.nextItem)

    def nextItem(self):
        try:
            self.listWidget.item(self.z).setHidden(False)
            self.listWidget.repaint()
            self.z += 1
        except AttributeError:
            self.timer.stop()
            self.z = 0

app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())