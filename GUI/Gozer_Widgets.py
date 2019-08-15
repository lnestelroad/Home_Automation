#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QComboBox, QLabel, QDockWidget, QTextEdit, QListWidget
from PyQt5.QtWidgets import QStackedWidget, QFormLayout, QRadioButton, QProgressBar, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QHeaderView, QTableView
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
import os
import shutil
import logging
import cv2
import subprocess

sys.path.append("../Database")
from db_interface import Database

class ManageUsers(QWidget):
    #TODO: fix file path stuff
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

        #TODO: Make the combo box only accept certain characters
        # Widget for the access combo box
        self.accessBox = QComboBox()
        self.accessBox.setEditable(False)

        # Gets rooms from the database and adds them to the combo box
        rooms = self.db.getRooms()
        for room_index in range(0, self.db.countRooms()[0]):
            self.accessBox.addItem(rooms[room_index][0])

        self.firstName = QLineEdit()
        self.lastName = QLineEdit()
        self.bluetooth = QLineEdit()
        self.bluetooth.setMaxLength(12)
        
        # Layout which holds all of the user data input fields
        self.form = QFormLayout()
        self.form.addRow(QLabel("First Name"), self.firstName)
        self.form.addRow(QLabel("Last Name"), self.lastName)
        self.form.addRow(QLabel("BluetoothID"), self.bluetooth)
        self.form.addRow(QLabel("Access"), self.accessBox)

        # Connect fields
        self.firstName.textChanged.connect(self.enableAddUserButton)
        self.lastName.textChanged.connect(self.enableAddUserButton)
        self.bluetooth.textChanged.connect(self.enableAddUserButton)

        # Here is the button section of the grid layout for uploading and submitting
        submitUserButtonLayout = QHBoxLayout()

        self.add = QPushButton("Add User")
        self.clear = QPushButton("Clear Form")
        self.edit = QPushButton("Change")

        self.add.setDisabled(True)
        self.add.clicked.connect(self.createUser)

        self.clear.clicked.connect(self.clearForm)

        self.edit.setDisabled(True)
        self.edit.clicked.connect(self.Modify)

        submitUserButtonLayout.addWidget(self.add)
        submitUserButtonLayout.addWidget(self.edit)
        submitUserButtonLayout.addWidget(self.clear)

        addUsersLayout.addLayout(self.form, 0, 0)
        addUsersLayout.addLayout(submitUserButtonLayout, 1, 0)

     #//////////////////////////////////////////////////////////////////////////////// Progress bar layout
        SubmitLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setAlignment(Qt.AlignCenter)

        self.upload = QPushButton("Upload")
        self.submit = QPushButton("Submit")

        self.submit.setDisabled(True)
        self.submit.clicked.connect(self.encodeFace)

        self.upload.setDisabled(True)
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
        """
            Summary: This function is used to activated both the add user and upload button only when the form is filled out.
        """

        # Determines if the form fields are empty or not
        validfirstName = self.firstName.text() != ""
        validLastName = self.lastName.text() != ""
        validBluetooth = self.bluetooth.text() != ""
        
        # Checks to see if the length for the bluetooth is correct
        if len(self.bluetooth.text()) != 12:
            validBluetooth = False

        
        # Activates the upload picture and add user button
        self.add.setEnabled(validBluetooth and validfirstName and validLastName)
        self.upload.setEnabled(validBluetooth and validfirstName and validLastName)

    def createUser(self):
        """
            Summary: Here is where the python script will add all of the user info to both the data base
                and a directory for pictures to be stored.
        """
        # Gets the users information from the database
        users = self.db.getUsers()

        # Gets the data from the form.
        name = self.firstName.text() + "_" + self.lastName.text()
        bluetooth = self.bluetooth.text()
        access = self.accessBox.currentText()

        # Formats the bluetooth ID into its proper form
        bluetooth = bluetooth.upper()
        bluetooth = ':'.join(a+b for a,b in zip(bluetooth[::2], bluetooth[1::2]))

        # Checks to see if user already exists in the database
        flag = True
        for userIndex in range(0, len(users)):
            if name in users[userIndex]:
                flag = False

        # If user does exit, the flag is tripped skipping this and erroring out
        if flag:
            os.chdir("/home/liam_work/Documents/Home_Automation/Facial_Recognition/dataset")

            # TODO: add path which is not a relative path
            # Enters data information into the database
            self.db.addUser(name, bluetooth, access)
            self.db.commitChanges()

            # Enters new data into table view
            self.populateTable()

            # Clears the form
            self.clearForm()

            # Added user documented in log
            logging.info("{} added to application".format(name))

            if access != "Guest":
                try:
                    # Creates a directory for the users pictures if they are not a guest
                    os.mkdir("{}".format(name))

                except OSError as error:
                    # An error dialog is brought up telling the user what went wrong
                    logging.warning("Could not create directory. \n\tError:\n\t{}".format(error))
                    dlg = CustomDialogs("already_Exists", "{}".format(error))
                    dlg.exec_()
                    self.clearForm()
        else:
            logging.warning("Could not create directory. \n\tError:\n\tDuplicate Entry")
            dlg = CustomDialogs("already_Exists", "Duplicate Entry")
            dlg.exec_()
            self.clearForm()

    def clearForm(self):
        self.firstName.setText("")
        self.lastName.setText("")
        self.bluetooth.setText("")
        self.accessBox.setCurrentIndex(0)

        self.bluetooth.setMaxLength(12)

        self.setProgressBar("")
        self.submit.setDisabled(True)

    def removeUser(self):
        #TODO: add function to remove user from face encoding
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
        os.chdir("/home/liam_work/Documents/Home_Automation/Facial_Recognition/dataset")
        path = "./{}".format(userName)
        
        try:
            # removes the directory of the user being removed
            shutil.rmtree(path, ignore_errors=True)
            self.setProgressBar("")
            self.clearForm()
            self.encodeFace()

            #TODO: add re-encoding process here

        except OSError as error:
            logging.warning("Could not remove directory. \n\tError:\n\t{}".format(error))
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

            self.removeButton.clicked.connect(self.removeUser)
        
        # Allows double clicking on rows for editing
        self.userTable.setEditTriggers( QTableWidget.NoEditTriggers)

        # Connects a double click to an edit menu
        self.userTable.itemDoubleClicked.connect(self.editItem)
        
    def setProgressBar(self, userName):
        """
            Summary: This is used to set the state of the progess bar for any given user
                NOTE: make userName "" to set the bar to neutral (0/20).
        """
        if userName == "":
            self.progress.setValue(0)
            self.progress.setFormat("0/20")
        
        else:
            os.chdir("/home/liam_work/Documents/Home_Automation/Facial_Recognition/dataset/{}".format(userName))
            files = len([name for name in os.listdir('.') if os.path.isfile(name)])
            print(files)
            print(userName)
            
            progressValue = 5 * files

            if progressValue >= 100:
                self.submit.setEnabled(True)
                self.progress.setValue(100)
                self.progress.setFormat("{}: {}/20".format(userName, files))

            else:
                self.progress.setValue(progressValue)
                self.progress.setFormat("{}: {}/20".format(userName, files))

    def uploadPicutes(self):
        """
            Summary: This will have python open a camera module and take a picture of the user. Once the picture is
                taken, it will be saved in the users designated directory in the facial recognition site.
        """
        # TODO: Set working derectory to the file's location
        userName = self.firstName.text() + "_" + self.lastName.text()
        os.chdir("/home/liam_work/Documents/Home_Automation/Facial_Recognition/dataset/{}".format(userName))

        # Opens the camera for the user to add pictures of them selves.
        try:
            cam = cv2.VideoCapture(0)
            cv2.namedWindow("")

            img_counter = 0
            while True:
                ret, frame = cam.read()
                cv2.imshow("User Picture add - Press ESC to Exit - Press Space to take Picture", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)

                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break

                # Takes photo when space bar is pressed.
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = "{}{}.png".format(userName, img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1

            cam.release()

            cv2.destroyAllWindows()

            self.setProgressBar(userName)

        except Exception as e:
            logging.warning("No Camera Found")
            dlg = CustomDialogs("camera", "{}".format(e))
            dlg.exec_()

    def encodeFace(self):
        #TODO: add progress bar for this
        """
            Summary: Once enough pictures have been uploaded, this will kick off the encode_faces.py script in the
                facial recognition directory
        """
        os.chdir("/home/liam_work/Documents/Home_Automation/GUI")
        subprocess.call('./encode.sh')
        
    def editItem(self, item):
        """
            Summary: Here is where the form is set up for the user to be edited.
                NOTE: this function will no update the user in the database directly, but rather
                by calling another function.
        """
        userRow = item.row()

        # Splits the users name into first and last
        name = self.userTable.item(userRow, 0).text().split("_")

        # Finds the index of the room in the combo box
        index = self.accessBox.findText(self.userTable.item(userRow, 2).text())
        
        # Allows for the combo box to display the whole modified bluetooth ID
        self.bluetooth.setMaxLength(17)

        # Sets the Add user table to all of the
        self.firstName.setText(name[0])
        self.lastName.setText(name[1])
        self.bluetooth.setText(self.userTable.item(userRow, 1).text())
        self.accessBox.setCurrentIndex(index)

        self.add.setDisabled(True)
        self.edit.setDisabled(False)
        self.upload.setDisabled(False)

        self.ORIGINAL_FIRST_NAME = name[0]
        self.ORIGINAL_LAST_NAME = name[1]
        
        if self.accessBox.currentText() != "Guest":
            self.setProgressBar(self.userTable.item(userRow, 0).text())
        else:
            self.upload.setDisabled(True)
            self.setProgressBar("")

    def Modify(self):
        #TODO: Finish this
        """
            Summary: This is the function that will push the changes to the user into the database
        """
        # Gets the current data in the fom
        firstName = self.firstName.text()
        lastName = self.lastName.text()
        bluetooth = self.bluetooth.text()
        access = self.accessBox.currentText()

        # gets the name of the user for editing
        combinedOriginalName = self.ORIGINAL_FIRST_NAME + "_" + self.ORIGINAL_LAST_NAME

        # removes the user from the database then readds them with the changes
        self.db.removeUser(combinedOriginalName)
        self.db.addUser(combinedOriginalName, bluetooth, access)
        self.db.commitChanges()

        # the table is re populated
        self.populateTable()
        self.clearForm()


class ManageRooms(QWidget):
    """
        Summary: This class will display the manage rooms window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Fix table so that it only has entries for how many devices are in each room
        # TODO: Make add and remove device functions.
        # TODO: Add function to count devices based on room in db_interface

        # Connects the application to the database
        self.db = Database()
        self.db.connectToDatabase()

        # Initiates a layout and a tree widget
        self.layout = QVBoxLayout(self)
        self.roomTree = QTreeWidget()
        self.roomTree.setHeaderLabel("Bedrooms")

        # retrieves the room count and the room names
        roomCount = self.db.countRooms()
        rooms = self.db.getRooms()

        # Adds all of the rooms to the tree widget
        for roomIndex in range(0, roomCount[0]):
            parent = QTreeWidgetItem(self.roomTree)
            parent.setText(0, rooms[roomIndex][0])

            # Makes a special Table for each rooms
            child = QTreeWidgetItem(parent)
            self.deviceTable = QTableWidget(self.db.countDevices()[0], 3, self)
            self.deviceTable.setHorizontalHeaderLabels(["Name", "Purpose", "Importance"])

            # Formats the table to fill up all avaliable space
            self.deviceTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))

            # Populates the table
            self.populateTable(rooms[roomIndex][0])

            # Adds each table to its respective table widget
            self.roomTree.setItemWidget(child, 0, self.deviceTable)

        self.buttonLayout = QHBoxLayout()
        self.addDevice = QPushButton("Add Device")
        self.removeButton = QPushButton("Remove Device")

        self.buttonLayout.addWidget(self.addDevice)
        self.buttonLayout.addWidget(self.removeButton)

        self.addDevice.clicked.connect(self.deviceAdd)
        self.removeButton.clicked.connect(self.deviceRemove)
        
        
        # Adds the dock widget to the main layout for the manage room plane
        self.layout.addWidget(self.roomTree)
        self.layout.addLayout(self.buttonLayout)

    def populateTable(self, room):
        """
            Summary: Since this table will be updated regularly via adding and removing
                devices, it is given its own function which first destroys the table then
                rebuilds it from the top
        """
        # Gets all of the device information from the database
        devices = self.db.getDevices(room)
        deviceCount = len(devices)

        # Here is where all of the information is unpacked and inserted into the table
        for deviceIndex in range(0, deviceCount):
            deviceName = QTableWidgetItem("{}".format(devices[deviceIndex][0]))
            devicePurpose = QTableWidgetItem("{}".format(devices[deviceIndex][1]))
            deviceImportance = QTableWidgetItem("{}".format(devices[deviceIndex][2]))

            self.deviceTable.setItem(deviceIndex, 0, deviceName)
            self.deviceTable.setItem(deviceIndex, 1, devicePurpose)
            self.deviceTable.setItem(deviceIndex, 2, deviceImportance)

   #///////////////////////////////////////////////////////////////////// Device add functions

    def deviceAdd(self):
        # Add to Custom Dialog class
        newAddition = QDialog()
        dialogLayout = QVBoxLayout(newAddition)

        # Widget for the access combo box
        self.accessBox = QComboBox()
        self.accessBox.setEditable(False)

        # Gets rooms from the database and adds them to the combo box
        rooms = self.db.getRooms()
        for room_index in range(0, self.db.countRooms()[0]):
            self.accessBox.addItem(rooms[room_index][0])

        self.deviceName = QLineEdit()
        self.deviceImportance = QLineEdit()
        self.devicePurpose = QLineEdit()

        # Form for the user to enter in new device information
        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Device Name"), self.deviceName)
        formLayout.addRow(QLabel("Device Importance"), self.deviceImportance)
        formLayout.addRow(QLabel("Device Purpose"), self.devicePurpose)
        formLayout.addRow(QLabel("Device Location"), self.accessBox)

        # Adds the okay and cancel button at the bottom
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        
        buttonBox = QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        dialogLayout.addLayout(formLayout)
        dialogLayout.addWidget(buttonBox)

        newAddition.setWindowTitle("Add Device")
        newAddition.exec()

    def accept(self):
        """
            Summary: Loads new device information into the database
        """
        self.db.addDevice(self.deviceName.text(), self.devicePurpose.text(), self.deviceImportance.text(), self.accessBox.currentText())

        logging.info("Added new device: {}".format(self.deviceName))
        
   #///////////////////////////////////////////////////////////////////// Device Remove Functions

    def deviceRemove(self):
        """
            Summary: Displays a table of ever device for users to remove
        """
        removeDeviceDialog = QDialog()

        dialogLayout = QVBoxLayout(removeDeviceDialog)
        
        devices = self.db.getDevices()
        deviceCount = len(devices)

        self.removeDeviceTable = QTableWidget(self.db.countDevices()[0], 5, self)
        self.removeDeviceTable.setHorizontalHeaderLabels(["Name", "Purpose", "Importance", "Location", "Remove"])

        # Formats the table to fill up all avaliable space
        self.removeDeviceTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))

        # Here is where all of the information is unpacked and inserted into the table
        for deviceIndex in range(0, deviceCount):
            deviceName = QTableWidgetItem("{}".format(devices[deviceIndex][0]))
            devicePurpose = QTableWidgetItem("{}".format(devices[deviceIndex][1]))
            deviceImportance = QTableWidgetItem("{}".format(devices[deviceIndex][2]))
            deviceLocation = QTableWidgetItem("{}".format(devices[deviceIndex][3]))
            deviceRemove = QPushButton("Kill")

            self.removeDeviceTable.setItem(deviceIndex, 0, deviceName)
            self.removeDeviceTable.setItem(deviceIndex, 1, devicePurpose)
            self.removeDeviceTable.setItem(deviceIndex, 2, deviceImportance)
            self.removeDeviceTable.setItem(deviceIndex, 3, deviceLocation)
            self.removeDeviceTable.setCellWidget(deviceIndex, 4, deviceRemove)

            deviceRemove.clicked.connect(self.killDevice)

        dialogLayout.addWidget(self.removeDeviceTable)

        removeDeviceDialog.exec_()

    def killDevice(self):
        buttonClicked = self.sender()
        index = self.removeDeviceTable.indexAt(buttonClicked.pos())
        deviceRow = index.row()

        # User name is extracted from the table then removed
        item = self.removeDeviceTable.item(deviceRow, 0)
        deviceName = item.text()

        print(deviceName)

        self.removeDeviceTable.removeRow(deviceRow)

        self.db.removeDevice(deviceName)
        self.db.commitChanges()


class Logs(QWidget):
    """
        Summary: Displays all of the entry logs from the database
    """
    #TODO: Add button to limit amount of logs seen
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)

        # connects to the database
        self.db = Database()
        self.db.connectToDatabase()

        #retrieves data for the logs.
        logsCount = self.db.countPictures()

        # creates the table for the log view
        self.logsTable = QTableWidget(logsCount[0] ,4)
        self.logsTable.setHorizontalHeaderLabels(["Date", "Location", "Response", "User"])
        self.populateTable()

        # Formats the table to fill up all avaliable space
        self.logsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(1))
        self.logsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode(3))

        self.layout.addWidget(self.logsTable)

    def populateTable(self, request=0):
        """
            Summary: This table is really only built once but its good to keep convention
        """
        # Gets all of the log information from the database
        entries = self.db.getEntry()
        print(entries)

        for entryIndex in range(0, len(entries)):

            # Unpacks the information from the database
            date = QTableWidgetItem("{}".format(entries[entryIndex][0]))
            location = QTableWidgetItem("{}".format(entries[entryIndex][1]))
            response = QTableWidgetItem("{}".format(entries[entryIndex][2]))
            user = QTableWidgetItem("{}".format(entries[entryIndex][3]))

            print(date)

            self.logsTable.setItem(entryIndex, 0, date)
            self.logsTable.setItem(entryIndex, 1, location)
            self.logsTable.setItem(entryIndex, 2, response)
            self.logsTable.setItem(entryIndex, 3, user)
            

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

        elif dialogType == "camera":
            self.setWindowTitle("Camera Error")
            self.msg = QLabel("No camera module connected")

        self.error = QLabel(errorMessage)
        self.layout.addWidget(self.msg)
        self.layout.addWidget(self.error)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Workspace(QWidget):
    """
        Summary: Here is where the whole app is layed out. Everything from the menu bar to the
            working space. it all comes together here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initiates logging module
        logging.basicConfig(filename="../GozerLogs/GozerGUI.log", filemode="a", level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info("Admin Login")

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

