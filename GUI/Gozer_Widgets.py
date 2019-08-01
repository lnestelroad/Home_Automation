#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QFormLayout, QRadioButton, QProgressBar, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QTableView
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
import os
import shutil
import logging

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
        
        self.db = Database()
        self.db.connectToDatabase()

        # TODO: Change this from relative to absolute
        os.chdir("../Facial_Recognition/dataset")
        #//////////////////////////////////////////////////////////////////////////////// Form layout
        #TODO: add additional options for time frame when guest is selected

        # Widget for the access combo box
        self.accessBox = QComboBox()
        self.accessBox.setEditable(False)

        # Gets rooms from the database and adds them to the combo box
        rooms = self.db.getRooms()
        for room_index in range(0, self.db.countRooms()[0]):
            self.accessBox.addItem(rooms[room_index][0])

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

        self.clear.clicked.connect(self.ClearForm)

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

        self.submit.setDisabled(True)
        self.submit.clicked.connect(self.encodeFace)

        self.upload.clicked.connect(self.uploadPicutes)

        buttonLayout.addWidget(self.upload)
        buttonLayout.addWidget(self.submit)
        
        SubmitLayout.addWidget(self.progress)
        SubmitLayout.addLayout(buttonLayout)

        addUsersLayout.addLayout(SubmitLayout, 0, 1 )

        #//////////////////////////////////////////////////////////////////////////////// Table Layout
        # Here are all of Database interface functions needed to get the user information
        #TODO: code unpacking
        userCount = self.db.countUsers()
        print(userCount)
        # Creates empty table widget with headers
        self.userTable = QTableWidget(userCount[0] + 1, 4, self)
        self.userTable.setHorizontalHeaderLabels(["User Name", "BluetoothID", "Bedroom", "Remove User"])
        
        self.userTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.userTable.horizontalHeader().setSectionResizeMode(3 , QHeaderView.ResizeMode(2))

        self.populateTable()

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

        # TODO: add path which is not a relative path
        if access != "Guest":
            try:
                # Creates a directory for the users pictures if they are not a guest
                os.mkdir("{}".format(name))

                # Enters data information into the database
                self.db.addUser(name, bluetooth, access)
                self.db.commitChanges()

                # Enters new data into table view
                self.populateTable()

                # Clears the form
                self.ClearForm()

                # Added user documented in log
                logging.info("{} added to application".format(name))

            except OSError as error:
                # An error dialog is brought up telling the user what went wrong
                logging.warning("Could not create directory. Error:\n{}".format(error))
                dlg = CustomDialogs("already_Exists", "{}".format(error))
                dlg.exec_()

    def ClearForm(self):
        self.FirstName.setText("")
        self.lastName.setText("")
        self.bluetooth.setText("")

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

        # Logs user removal
        logging.info("{} removed from database".format(userName))

        # if user was perminate, their directory is removed
        path = "./{}".format(userName)
        
        try:
            os.rmdir(path)
        except OSError as error:
            logging.warning("Could not remove directory. Error:\n{}".format(error))
            dlg = CustomDialogs("error", "{}".format(error))
            dlg.exec_()

    def populateTable(self):
        """
            Since this table is recreated every time theres an update, this function will delete the table and 
                rebuild it.
        """
        # Removes all of the rows currently in the table
        self.userTable.setRowCount(0)

        #//////////////////////////////////////////////////////////////////////// Table rebuild
        # Gets both the users and the user count from database
        users = self.db.getUsers()
        userCount = self.db.countUsers()

        self.userTable.setRowCount(userCount[0])

        # Gets all of the users in the database and puts the in the table
        for i in range(0, userCount[0]):
            userName = QTableWidgetItem("{}".format(users[i][0]))
            userBluetooth = QTableWidgetItem("{}".format(users[i][1]))
            userRoom = QTableWidgetItem("{}".format(users[i][2]))
            self.removeButton = QPushButton("Kill")

            self.userTable.setItem(i,0,userName)
            self.userTable.setItem(i,1,userBluetooth)
            self.userTable.setItem(i,2,userRoom)
            self.userTable.setCellWidget(i, 3, self.removeButton)

            self.removeButton.clicked.connect(self.RemoveUser)

    def uploadPicutes(self):
        """
            Summary: This will have python open a camera module and take a picture of the user. Once the picture is
                taken, it will be saved in the users designated directory in the facial recognition site.
        """
        
        self.progress.setValue(self.progress.value() + 5)

        if self.progress.value() == 100:
            self.submit.setEnabled(True)


    def encodeFace(self):
        """
            Summary: Once enough pictures have been uploaded, this will kick off the encode_faces.py script in the
                facial recognition directory
        """
        pass

    def errorDialog(self):
        pass


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
        

class CustomDialogs(QDialog):
    """
        Summary: Depending on the parameter given, this widget brings up a dialog window for 
            the user. 
        Input: An error message which should be given as a string and a dialog type
            error - gives message for errors in removing users
            already_Exists - gives error in 
    """
    def __init__(self, dialogType, errorMessage = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Makes the button box for the dialog window
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        # # Determines what to show in the dialog box
        if dialogType == "error":
            self.setWindowTitle("Error Removing User")
            self.msg = QLabel("Cannot Remove User")
        
        elif dialogType == "already_Exists":
            self.setWindowTitle("Error Adding User")
            self.msg = QLabel("User Already Exists")

        self.error = QLabel(errorMessage)
        self.layout.addWidget(self.error)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Workspace(QWidget):
    """
        Summary:
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Menu = QListWidget()
        logging.basicConfig(filename="GozerGUI.log", filemode="w", level=logging.INFO)
        
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
