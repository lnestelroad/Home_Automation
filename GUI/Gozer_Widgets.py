#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QFormLayout, QRadioButton, QProgressBar, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractScrollArea
from PyQt5.QtCore import Qt
import os
import shutil

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
        #TODO: make the access box select room from database instead of hardcoded.

        # Widget for the access combo box
        self.accessBox = QComboBox()
        self.accessBox.setEditable(False)
        self.accessBox.addItems(["Guest", "Ryan's Room", "Liam's Room", "Isaac's Room", "Izzy's Room", "Master"])

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
        self.lastName.textChanged.connect(self.enableAddUserButton)
        self.bluetooth.textChanged.connect(self.enableAddUserButton)

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
        #TODO: code unpacking
        self.db = Database()
        self.db.connectToDatabase()
        userCount = self.db.countUsers()
    
        # Creates empty table widget with headers
        self.userTable = QTableWidget(userCount[0], 4, self)
        self.userTable.setHorizontalHeaderLabels(["User Name", "BluetoothID", "Bedroom", "Remove User"])
        self.populateTable()
        
        # These are used to make sure the table is sized to fit all of the information
        # self.userTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.userTable.resizeColumnsToContents()

        #//////////////////////////////////////////////////////////////////////////////// Main Layout Configuration
        widgetTitle = QLabel("Manage Users")
        widgetTitle.setAlignment(Qt.AlignCenter)

        manageUsersLayout.addWidget(widgetTitle, 0, 0)
        manageUsersLayout.addLayout(addUsersLayout, 1, 0)
        manageUsersLayout.addWidget(self.userTable, 2, 0)

    def enableAddUserButton(self):
        validFirstName = self.FirstName.text() != ""
        validLastName = self.lastName.text() != ""
        validBluetooth = self.bluetooth.text() != ""
        
        self.add.setEnabled(validBluetooth and validFirstName and validLastName)

    def CreateUser(self):
        """
            Summary: Here is where the python script will add all of the user info to both the data base
                and a directory for pictures to be stored.
        """
        # TODO: Duplicate users?
        # Gets the data from the form.
        name = self.FirstName.text() + "_" + self.lastName.text()
        bluetooth = self.bluetooth.text()
        access = self.accessBox.currentText()

        # Enters data information into the database
        self.db.addUser(name, bluetooth, access)
        self.db.commitChanges()

        # Enters new data into table view
        self.populateTable()

        # Creates a directory for the users pictures if they are not a guest
        # TODO: add path which is not a relative path
        # if access != "Guest":
        #     os.mkdir("../Facial_Recognition/dataset/{}".format(name))

    def RemoveUser(self):
        # Finds the exact row of the button pressed. Thank you Sam from StackOverFlow
        buttonClicked = self.sender()
        index = self.userTable.indexAt(buttonClicked.pos())
        userRow = index.row()

        # User name is extracted from the table then removed
        item = self.userTable.item(userRow, 0)
        userName = item.text()

        self.userTable.removeRow(userRow)

        # Users name is removed from the database.
        self.db.removeUser(userName)
        self.db.commitChanges()

        # if user was perminate, their directory is removed
        path = "../Facial_Recognition/dataset/{}".format(userName)
        if os.path.isdir(path):
            shutil.rmtree(path)

    def populateTable(self):
        """
            Since this table is recreated every time theres an update, this function will delete the table and 
                rebuild it.
        """
        tableCount = self.userTable.rowCount()

        if tableCount != 0:
            for tableIndex in range(0, tableCount):
                self.userTable.removeRow(tableIndex)


        #//////////////////////////////////////////////////////////////////////// Table rebuild
        # Gets both the users and the user count from database
        users = self.db.getUsers()
        userCount = self.db.countUsers()

        print(users)

        # Gets all of the users in the database and puts the in the table
        for i in range(0, userCount[0]):
            print(i)
            userName = QTableWidgetItem("{}".format(users[i][0]))
            userBluetooth = QTableWidgetItem("{}".format(users[i][1]))
            userRoom = QTableWidgetItem("{}".format(users[i][2]))
            self.removeButton = QPushButton("Kill")
            print(userBluetooth)

            self.userTable.setItem(i,0,userName)
            self.userTable.setItem(i,1,userBluetooth)
            self.userTable.setItem(i,2,userRoom)
            self.userTable.setCellWidget(i, 3, self.removeButton)

            self.removeButton.clicked.connect(self.RemoveUser)




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

    def display(self, index):
        self.Stack.setCurrentIndex(index)
