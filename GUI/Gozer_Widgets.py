#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QFormLayout, QRadioButton, QProgressBar, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractScrollArea
from PyQt5.QtCore import Qt
import os

sys.path.append("../Database")
from db_interface import Database

class ManageUsers(QWidget):
    """
        Summary: This is the widget that will be used to manage the users in the database. There
            are 2 main parts to this view: The add user form and the current user table. The form is
            made with a form layout out and the over all layout is the grid layout. 
        Input: None 
        Output: None
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manageUsersLayout = QGridLayout(self)
        addUsersLayout = QGridLayout()
        
        #//////////////////////////////////////////////////////////////////////////////// Form layout
        #TODO: add additional options for time frame when guest is selected

        # Widget for the access combo box
        self.accessBox = QComboBox()
        self.accessBox.setEditable(False)
        self.accessBox.addItems(["Guest", "Ryan's Room", "Liam's room", "Isaac's Room", "Izzy's Room", "Master"])

        self.FirstName = QLineEdit()
        self.lastName = QLineEdit()
        self.bluetooth = QLineEdit()

        # Layout which holds all of the user data input fields
        self.form = QFormLayout()
        self.form.addRow(QLabel("First Name"), self.FirstName)
        self.form.addRow(QLabel("Last Name"), self.lastName)
        self.form.addRow(QLabel("BluetoothID"), self.bluetooth)
        self.form.addRow(QLabel("Access"), self.accessBox)

        # Connect fields
        self.FirstName.textChanged.connect(self.enableAddUserButton)

        # Here is the button section of the grid layout for uploading and submitting
        submitUserButtonLayout = QHBoxLayout()

        self.add = QPushButton("Add User")
        self.clear = QPushButton("Clear Form")

        self.add.setDisabled(True)
        self.add.clicked.connect(self.CreateUser)

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
        # Here are all of Database interface functions needed to get the user information
        Database.connectToDatabase(self)
        users = Database.getUsers(self)
        self.userCount = Database.countUsers(self)
        
        self.userTable = QTableWidget(self.userCount[0], 4, self)
        self.userTable.setHorizontalHeaderLabels(["User Name", "BluetoothID", "Bedroom"])
        
        # Gets all of the users in the database and puts the in the table
        for i in range(0, self.userCount[0]):
            userName = QTableWidgetItem("{}".format(users[i][0]))
            userBluetooth = QTableWidgetItem("{}".format(users[i][1]))
            userRoom = QTableWidgetItem("{}".format(users[i][2]))
            removeButton = QPushButton("Kill")

            self.userTable.setItem(i,0,userName)
            self.userTable.setItem(i,1,userBluetooth)
            self.userTable.setItem(i,2,userRoom)
            self.userTable.setCellWidget(i, 3, removeButton)

        # These are used to make sure the table is sized to fit all of the information
        self.userTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.userTable.resizeColumnsToContents()

        #//////////////////////////////////////////////////////////////////////////////// Main Layout Configuration
        widgetTitle = QLabel("Manage Users")
        widgetTitle.setAlignment(Qt.AlignCenter)

        manageUsersLayout.addWidget(widgetTitle, 0, 0)
        manageUsersLayout.addLayout(addUsersLayout, 1, 0)
        manageUsersLayout.addWidget(self.userTable, 2, 0)

    def enableAddUserButton(self):
        self.add.setDisabled(False)

    def CreateUser(self):
        """
            Summary: Here is where the python script will add all of the user info to both the data base
                and a directory for pictures to be stored.
        """
        # Gets the data from the form.
        name = self.FirstName.text() + "_" + self.lastName.text()
        bluetooth = self.bluetooth.text()
        access = self.accessBox.currentText()

        # Enters data information into the database
        Database.addUser(self, name, bluetooth, access)
        Database.commitChanges(self)

        # Enters new data into table view
        rowPosition = self.userTable.rowCount()
        self.userTable.insertRow(rowPosition)

        userName = QTableWidgetItem("{}".format(name))
        userBluetooth = QTableWidgetItem("{}".format(bluetooth))
        userAccess = QTableWidgetItem("{}".format(access))

        self.userTable.setItem(rowPosition, 0, userName)
        self.userTable.setItem(rowPosition, 1, userBluetooth)
        self.userTable.setItem(rowPosition, 2, userAccess)

        # Creates a directory for the users pictures if they are not a guest
        if access != "Guest":
            os.mkdir("../Facial_Recognition/dataset/{}".format(name))

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
