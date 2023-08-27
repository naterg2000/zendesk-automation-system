from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

from PyQt5.QtWidgets import QWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # set up window attributes
        self.setWindowTitle("Zendesk Automation System")
        self.setWindowIcon(QtGui.QIcon("assets/fyilogo.png"))
        self.setFixedHeight(500)
        self.setFixedWidth(500)

        # initialize UI
        self.initUI()
        

    def initUI(self):
        
        # text input
        self.input_bar = QtWidgets.QLineEdit(self)
        self.input_bar.setGeometry(150, 250, 100, 40)

        # set up a button
        self.button1 = QtWidgets.QPushButton("Show", self)
        self.button1.setGeometry(200, 200, 200, 50)
        self.button1.setStyleSheet("color: black")
        self.button1.setStyleSheet("font-weight: bold")
        self.button1.setStyleSheet("font-size: 18pt")
        self.button1.clicked.connect(self.button1_clicked)

        # label setup
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Change the title of the window by clicking the button")
        self.label.setGeometry(0, 0, 100, 30)
        self.label.setStyleSheet("font-weight: bold")
        self.label.setStyleSheet("font-size: 18pt")
        self.label.update()


    def button1_clicked(self):

        url_value = self.input_bar.text()
        self.label.setText(url_value)
        self.label.setGeometry(QtCore.QRect(200, 80, 500, 100))

        print("Chagned label text :D")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()