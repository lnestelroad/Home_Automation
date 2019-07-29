#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QFormLayout, QRadioButton, QProgressBar, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import os

class ManageUsers(QWidget):
    """
        Summary:
        Input:
        Output:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manageUsersLayout = QGridLayout(self)
        addUsersLayout = QGridLayout()
        
        #//////////////////////////////////////////////////////////////////////////////// Form layout
        #TODO: add additional options for time frame when guest is selected
        accessBox = QComboBox()
        accessBox.setEditable(False)
        accessBox.addItems(["Guest", "Ryan's Room", "Liam's room", "Isaac's Room", "Izzy's Room", "Master"])

        self.form = QFormLayout()
        self.form.addRow(QLabel("First Name"), QLineEdit())
        self.form.addRow(QLabel("Last Name"), QLineEdit())
        self.form.addRow(QLabel("BluetoothID"), QLineEdit())
        self.form.addRow(QLabel("Access"), accessBox)

        submitUserButtonLayout = QHBoxLayout()

        self.add = QPushButton("Add User")
        self.clear = QPushButton("Clear Form")

        submitUserButtonLayout.addWidget(self.add)
        submitUserButtonLayout.addWidget(self.clear)

        addUsersLayout.addLayout(self.form, 0, 0)
        addUsersLayout.addLayout(submitUserButtonLayout, 1, 0)

        #//////////////////////////////////////////////////////////////////////////////// Progress bar layout
        SubmitLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.upload = QPushButton("Upload")
        self.submit = QPushButton("Submit")
        self.clear = QPushButton("Clear")

        buttonLayout.addWidget(self.upload)
        buttonLayout.addWidget(self.submit)
        buttonLayout.addWidget(self.clear)
        
        SubmitLayout.addWidget(self.progress)
        SubmitLayout.addLayout(buttonLayout)

        addUsersLayout.addLayout(SubmitLayout, 0, 1 )

        #//////////////////////////////////////////////////////////////////////////////// Table Layout
        #TODO: change the dimension of the table to allow for all database entries
        userTable = QTableWidget(4, 3, self)
        userEntry = QTableWidgetItem("test")
        
        userTable.setItem(0,0,userEntry)

        #////////////////////////////////////////////////////////////////////////////////
        widgetTitle = QLabel("Manage Users")
        widgetTitle.setAlignment(Qt.AlignCenter)

        manageUsersLayout.addWidget(widgetTitle, 0, 0)
        manageUsersLayout.addLayout(addUsersLayout, 1, 0)
        manageUsersLayout.addWidget(userTable, 2, 0)




class ManageRooms(QWidget):
    """
        Summary:
        Input:
        Output:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QLabel("Manages Rooms")
        self.layout.addWidget(self.simpleText)


class Logs(QWidget):
    """
        Summary:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QLineEdit("Logs")
        self.layout.addWidget(self.simpleText)


class Diagnostics(QWidget):
    """
        Summary:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QTextEdit("Diagnostics")
        self.layout.addWidget(self.simpleText)


class SelfDestruct(QWidget):
    """
        Summary:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)
        self.simpleText = QTextEdit("Self Destruct")
        self.layout.addWidget(self.simpleText)
        
        
class Workspace(QWidget):
    """
        Summary:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Menu = QListWidget()
        
        self.Menu.insertItem(0, "Manage Users")
        self.Menu.insertItem(1, "Manage Rooms")
        self.Menu.insertItem(2, "Logs")
        self.Menu.insertItem(3, "Diagnostics")
        self.Menu.insertItem(4, "Self Destruct")

        self.Menu.setFixedWidth(self.Menu.width() * .3)

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(ManageUsers())
        self.Stack.addWidget(ManageRooms())
        self.Stack.addWidget(Logs())
        self.Stack.addWidget(Diagnostics())
        self.Stack.addWidget(SelfDestruct())

        layout = QHBoxLayout(self)
        layout.addWidget(self.Menu)
        layout.addWidget(self.Stack)

        self.setLayout(layout)
        self.Menu.currentRowChanged.connect(self.display)

    def display(self, i):
        self.Stack.setCurrentIndex(i)
