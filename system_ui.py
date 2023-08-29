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

        # set colors of window
        self.setStyleSheet("background-color: #232426")

        # set up QVboxLayout
        vertical_layout = QVBoxLayout()

        self.title_label = QtWidgets.QLabel("Zendesk Automation System")
        self.title_label.setGeometry(0, 0, 100, 40)
        self.title_label.setStyleSheet("color: #959597; font-weight: bold; font-size: 18pt")


        


        # add the elements to the vertical_layout
        vertical_layout.addWidget(self.title_label)

        # not sure why but nothing shows up without this and I'm scared
        main_widget = QWidget()
        main_widget.setLayout(vertical_layout)
        self.setCentralWidget(main_widget)



        """
        
        # text input
        self.input_bar = QtWidgets.QLineEdit(self)
        self.input_bar.setGeometry(0, 0, 100, 40)
        self.input_bar.setText("")

        # set up a button
        self.button1 = QtWidgets.QPushButton("Show", self)
        self.button1.setGeometry(0, 0, 100, 50)
        self.button1.setStyleSheet("color: white; font-size: 14pt")
        self.button1.clicked.connect(self.button1_clicked)

        # label setup
        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setText("Zendesk Automation System")
        self.title_label.setGeometry(0, 0, 400, 30)
        self.title_label.setStyleSheet("color: #959597; font-weight: bold; font-size: 18pt")
        self.title_label.update()

        # update frequency label
        self.update_frequency_title_label = QtWidgets.QLabel(self)
        self.update_frequency_title_label.setText("Update frequency (sec):")
        self.update_frequency_title_label.setGeometry(0, 0, 400, 30)
        self.update_frequency_title_label.setStyleSheet("color: #959597; font-weight: bold; font-size: 18pt")
        self.update_frequency_title_label.update()

        # update frequnecy value label
        self.update_frequency_value_label = QtWidgets.QLabel(self)
        self.update_frequency_value_label.setText("5")
        self.update_frequency_value_label.setGeometry(0, 0, 400, 30)
        self.update_frequency_value_label.setStyleSheet("color: #959597; font-weight: bold; font-size: 18pt")
        self.update_frequency_value_label.update()

        # add items to QVboxLayout
        vertical_layout.addWidget(self.input_bar, self.button1, self.title_label, self.update_frequency_title_label, self.update_frequency_value_label)
        """

    def button1_clicked(self):

        # get value from input bar
        new_frequency_value = self.input_bar.text()

        try:
            # convert the entered frequency to an int
            new_frequency_value = int(new_frequency_value)
            print('type of new freqyency value is now ', type(new_frequency_value))
        except Exception as e:
            print(str(e))
        
        # update frequency wait time 
        
        

        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()