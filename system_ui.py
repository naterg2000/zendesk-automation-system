from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

import sys
import threading
import subprocess
from runner_proto import ZendeskAutomationSystem as zds

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
        
        vertical_layout = QtWidgets.QVBoxLayout()   # set up VBoxLayout for the window
        self.setStyleSheet("background-color: #232426") # set background color of the window
        
        # title label
        self.title_label = QtWidgets.QLabel("Zendesk Automation System")
        self.title_label.setStyleSheet("color: #959597; \
                                       font-size: 18pt; \
                                       font-weight: bold;")

        # update frequency label
        self.update_frequency_label = QtWidgets.QLabel("Update frequency:")
        self.update_frequency_label.setStyleSheet("color: #959597; \
                                                font-size: 14pt; \
                                                font-weight: bold;")
        
        # update frequency value label
        self.update_frequency_value_label = QtWidgets.QLabel(str(zds.update_frequency))
        self.update_frequency_value_label.setStyleSheet("color: #959597; \
                                                font-size: 14pt; \
                                                font-weight: bold;")
        
        # set up HBoxLayout for frequency information
        frequency_handling_layout = QtWidgets.QHBoxLayout()
        frequency_handling_layout.addWidget(self.update_frequency_label)
        frequency_handling_layout.addWidget(self.update_frequency_value_label)

        # update frequency change text input
        self.update_frequency_input = QtWidgets.QLineEdit()
        self.update_frequency_input.setStyleSheet("height: 30px;")
        # self.update_frequency_input.setGeometry()
        
        # update frequency change button
        self.submit_update_frequency_change_button = QtWidgets.QPushButton("Change Update Frequency", self)
        self.submit_update_frequency_change_button.clicked.connect(self.submit_update_frequency_change_button_clicked)
        self.submit_update_frequency_change_button.setGeometry(0, 0, 100, 50)
        self.submit_update_frequency_change_button.setStyleSheet("color: black; \
                                                                font-size: 14pt;"
                                                                "background-color: #4A82FD")
        
        # status section
        system_status_section = QVBoxLayout()
        self.status_label = QtWidgets.QLabel("Status:")
        self.status_label.setStyleSheet("color: #959597; \
                                       font-size: 12pt;")
        self.status_description_label = QtWidgets.QLabel(zds.system_status)
        self.status_description_label.setStyleSheet("color: #959597; \
                                       font-size: 10pt;")

        # add widgets to system_status_section
        system_status_section.addWidget(self.status_label)
        system_status_section.addWidget(self.status_description_label)

        # add the elements to the vertical_layout
        vertical_layout.addWidget(self.title_label)
        vertical_layout.addLayout(frequency_handling_layout)
        vertical_layout.addWidget(self.update_frequency_input)
        vertical_layout.addWidget(self.submit_update_frequency_change_button)
        vertical_layout.addLayout(system_status_section)

        # not sure why but nothing shows up without this and I'm scared
        main_widget = QWidget()
        main_widget.setLayout(vertical_layout)
        self.setCentralWidget(main_widget)


        self.setLayout(vertical_layout) # set window layout


    def submit_update_frequency_change_button_clicked(self):

        # if the line edit value is not empty
        if self.update_frequency_input.text() != "":
            try:    # try to convert the text to an int
                freq_value = int(self.update_frequency_input.text())
            except Exception as e: 
                print("\nProblelm at submit_update_frequency_button_clicked(): ", e)
            finally:
                zds.changeUpdateFrequency(new_frequency=freq_value)
                self.update_frequency_value_label.setText(str(freq_value))
        else:
            print("Please enter a value to change the update frequency to")

def runTicketHandler():
    zds.main()

thread = threading.Thread(target=runTicketHandler)
thread.start()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

