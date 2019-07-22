#!/usr/bin/env python3

import sqlite3
import argparse

class Database():
    """
        Summary: This class is used for interaction with the Gozer_database.db sql file. Since sqlite3 has nice integration with 
            python, it is the perfect solution for incorporating a database with the PyQt GUI

        Inputs:None
        Outputs: None
    """
    def __init__(self):
        self.cxn = None
        self.cursor = None

################## Database Configuration #####################################
    def connectToDatabase(self):
        """
            Summary: Here is where python makes a connection with the database file. If no connection can 
                be made, the file errors out.

            Inputs: None
            Outputs: A sqlite cursor for interaction with the database.
        """
        try:
            # Create a connection to the database
            self.cxn = sqlite3.connect("/home/liam_work/Documents/Home_Automation/Gozer_database.db")
            print("Opening Connections to database")

            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except sqlite3.Error as error:
            print("Error connecting to database. " + str(error))

    def setupTables(self):
        """
            Summary: Because creating the schema though the command line is a massive pain in the ass, this function will do it for me. 
                The other benifit is for readability as anyone can now see exactly what was done to make this database.

            Inputs: None
            Outputs: Initial database
        """

        # Creates a table for Bedrooms
        Bedrooms = "CREATE TABLE Bedrooms(\
                RoomID INTEGER PRIMARY KEY AUTOINCREMENT,\
                RoomName TEXT NOT NULL\
                );"
        self.cursor.execute(Bedrooms)

        # Creates a table for Devices
        Devices = "CREATE TABLE Devices(\
                DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Name TEXT NOT NULL,\
                Purpose TEXT NOT NULL,\
                Importance TEXT,\
                Room INTEGER,\
                FOREIGN KEY(Room) REFERENCES BedRooms(RoomID)\
                );"
        # Executes the above sql command
        self.cursor.execute(Devices)

        # Creates a table for Users
        Users = "CREATE TABLE Users(\
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,\
                FirstName TEXT NOT NULL,\
                LastName TEXT NOT NULL,\
                BluetoothID TEXT NOT NULL,\
                Access TEXT NOT NULL,\
                LivingStatus TEXT NOT NULL,\
                Bedroom TEXT NOT NULL,\
                FOREIGN KEY(Bedroom) REFERENCES Bedrooms(RoomID)\
                );"
        self.cursor.execute(Users)

        # Creates a table for Pictures
        Pictures = "CREATE TABLE Pictures(\
                PictureID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Date TEXT NOT NULL,\
                Location TEXT,\
                Response TEXT,\
                Person INTEGER,\
                FOREIGN KEY(Person) REFERENCES Users(UserID)\
                );"
        self.cursor.execute(Pictures)

        # Execute and commit the sql
        self.cxn.commit()

################### Database adding ###########################################
    def addDevice(self, _name, _purpose, _importance, _room):
        """
            Summary: Here is where the admin can add new devices for specific rooms
            Input: Requires a name, a purpose, and importance, and a room which its located in
            Output: new device entry
        """
        pass

    def addRoom(self, _name):
        """
            Summary: Here is where the admin will be able to add new rooms the the database. Will probably never be used except during setup.
            Input:  Requires a name for the room
            Output: New entry in the rooms table
        """
        pass

    def addUser(self, _firstName, _lastName, _bluetooth, _access, _livingStatus, _bedroom):
        """
            Summary: Here is where the admin can add new users whether they be perminate or temporary
            Input: Requires basically everything about the user.
            Output: new user entry
        """
        pass

    def addEntry(self, _date, _time, _location, _response, _user):
        """
            Summary: Whenever the camera at the door is activated, the computer will use this function to add 
                an entry of the user entering
            Input: Requires the date, time, location, response, and the user who entered
            Output:
        """
        pass

#################### Database retrieval #######################################
    def getUsers(self):
        """
            Summary: This will be used by the GUI to show the admin the current Users Table
            Input: none
            Output: All entries in the user table
        """
        pass
    
    def getEntry(self):
        """
            Summary: This will be used by the GUI to show the admin the current Entries Table
            Input: none
            Output: All entries into the house
        """
        pass

    def getRooms(self):
        """
            Summary: This will be used by the GUI to show the admin the current Rooms Table
            Input: none
            Output: All rooms in the house
        """
        pass
    
    def getDevices(self):
        """
            Summary: This will be used by the GUI to show the admin the current Devices Table
            Input: none
            Output: All entries in the devices table
        """
        pass

    def commitChanges(self):
        """
            Summay: This will be used only to commit changes so that its done at specific points rather than after every function call.
            Input: none
            Output: none
        """
        self.cxn.commit()

##############################################################

def main():
    """ This is used only for testing purposes"""

    print ("Hello, World!")

    interface = Database()

    interface.connectToDatabase()

if __name__ == "__main__":
    main()