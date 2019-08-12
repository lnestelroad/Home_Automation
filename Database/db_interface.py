#!/usr/bin/env python3

import sqlite3
import argparse
import datetime

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
            self.cxn = sqlite3.connect("/home/liam_work/Documents/Home_Automation/Database/Gozer_database.db")
            print("Opening Connections to database")

            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()
        #TODO: add logging for errors and make back up plan for when database fails to connect.
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
        Bedrooms = "CREATE TABLE IF NOT EXISTS Bedrooms(\
                RoomID INTEGER PRIMARY KEY AUTOINCREMENT,\
                RoomName TEXT NOT NULL\
                );"
        self.cursor.execute(Bedrooms)

        # Creates a table for Devices
        Devices = "CREATE TABLE IF NOT EXISTS Devices(\
                DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Name TEXT NOT NULL,\
                Purpose TEXT NOT NULL,\
                Importance TEXT,\
                RoomID INTEGER,\
                FOREIGN KEY(RoomID) REFERENCES BedRooms(RoomID)\
                );"
        # Executes the above sql command
        self.cursor.execute(Devices)

        # Creates a table for Users
        Users = "CREATE TABLE IF NOT EXISTS Users(\
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,\
                UserName TEXT NOT NULL,\
                BluetoothID TEXT NOT NULL,\
                Access TEXT NOT NULL,\
                RoomID INTEGER NOT NULL,\
                FOREIGN KEY(RoomID) REFERENCES Bedrooms(RoomID)\
                );"
        self.cursor.execute(Users)

        # Creates a table for Pictures
        Pictures = "CREATE TABLE IF NOT EXISTS Pictures(\
                PictureID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Date TEXT NOT NULL,\
                Location TEXT,\
                Response TEXT,\
                UserID INTEGER,\
                FOREIGN KEY(UserID) REFERENCES Users(UserID)\
                );"
        self.cursor.execute(Pictures)

        # This is the lowest access level for the house. When a new user is added, the room is set for guest which is why its added along with the table definition
        self.cursor.execute("INSERT INTO Bedrooms (RoomName) VALUES (?);", ("Guest",))
        self.cursor.execute("INSERT INTO Bedrooms (RoomName) VALUES (?);", ("Master",))

        # Execute and commit the sql
        self.cxn.commit()

    def commitChanges(self):
        """
            Summay: This will be used only to commit changes so that its done at specific points rather than after every function call.
            Input: none
            Output: none
        """
        self.cxn.commit()

    def Destroy(self):
        """ Destroys the database. For testing pusposes only """
        self.cursor.execute("DROP TABLE Bedrooms;")
        self.cursor.execute("DROP TABLE Users;")
        self.cursor.execute("DROP TABLE Pictures;")
        self.cursor.execute("DROP TABLE Devices;")
        
        self.commitChanges()

################## Database counting #####################################

    def countUsers(self):
        """ Counts the number of entries in the user database """
        self.cursor.execute("SELECT count(*) FROM Users")
        userCount = self.cursor.fetchone()

        return userCount

    def countDevices(self):
        """ Counts the number of entries in the user database """
        self.cursor.execute("SELECT count(*) FROM Devices")
        deviceCount = self.cursor.fetchone()

        return deviceCount

    def countPictures(self):
        """ Counts the number of entries in the user database """
        self.cursor.execute("SELECT count(*) FROM Pictures")
        pictureCount = self.cursor.fetchone()

        return pictureCount

    def countRooms(self):
        """ Counts the number of entries in the user database """
        self.cursor.execute("SELECT count(*) FROM Bedrooms")
        roomCount = self.cursor.fetchone()

        return roomCount

################### Database inserting ########################################

    # TODO: make procedure for what happens when a foreign key is not in the database

    def addRoom(self, _name):
        """
            Summary: Here is where the admin will be able to add new rooms the the database. Will probably never be used except during setup.
            Input:  Requires a name for the room
            Output: New entry in the rooms table
        """
        self.cursor.execute("INSERT INTO Bedrooms (RoomName) VALUES (?);", (_name,))
    
    def addDevice(self, _name, _purpose, _importance, _room):
        """
            Summary: Here is where the admin can add new devices for specific rooms
            Input: Requires a name, a purpose, and importance, and a room which its located in
            Output: new device entry
        """
        self.cursor.execute("SELECT RoomID FROM Bedrooms WHERE RoomName = ?;", (_room,))
        roomID = self.cursor.fetchall()

        # TODO: see why sql will still allow foreign keys outside of other tables index to still be entered.

        self.cursor.execute("INSERT INTO Devices (Name, Purpose, Importance, RoomID) \
            Values (?,?,?,?);",(_name, _purpose, _importance, roomID[0][0])) 

    def addUser(self, _userName, _bluetooth, _access="Guest"):
        """
            Summary: Here is where the admin can add new users whether they be perminate or temporary
            Input: Requires basically everything about the user.
            Output: new user entry
        """
        self.cursor.execute("SELECT RoomID FROM Bedrooms WHERE RoomName = ?;", (_access,))
        roomID = self.cursor.fetchall()
   
        self.cursor.execute("INSERT INTO Users (UserName, BluetoothID, Access, RoomID)\
            VALUES (?,?,?,?);", (_userName, _bluetooth, _access, roomID[0][0]))

    def addEntry(self, _date, _location, _response, _user):
        """
            Summary: Whenever the camera at the door is activated, the computer will use this function to add 
                an entry of the user entering
            Input: Requires the date, time, location, response, and the user who entered
            Output:
        """
        self.cursor.execute("SELECT UserID FROM Users WHERE UserName = ?;", (_user,))
        IdentifiedUser = self.cursor.fetchall()

        self.cursor.execute("INSERT INTO Pictures (Date, Location, Response, UserID)\
            VALUES (?,?,?,?);", (_date, _location, _response, IdentifiedUser[0][0]))

#################### Database retrieval #######################################
    def getUsers(self, request = 0):
        """
            Summary: This will be used by the GUI to show the admin the current Users Table. Using the request amount method, this function will only
                return a limited amount
            Input: Amount request (optional) <int>
            Output: All entries in the user table <list of tuples>
        """
        # Here the SELECT has no ORDER BY since the users table is not dependent on times
        self.cursor.execute("SELECT Users.UserName, Users.BluetoothID, Users.Access, Bedrooms.RoomName\
            FROM Users\
            INNER JOIN Bedrooms\
            ON Bedrooms.RoomID = Users.RoomID;")

        #TODO: add sql limits instead of doing loops
        # checks to see if the user has given a desired amount of entries to be returned
        if request != 0:

            # initializes required variables
            user_table_entries = []
            amount = 0
        
            # loops for the amount of entries wanted by the user
            while amount < request:

                # saves the first retrieved entry in a temp variable to be saved in list later
                tmp = self.cursor.fetchone()
                
                # determines if the entries in the table are less then the requested amount
                if not tmp:
                    break

                # adds the retrieved data to the return list
                user_table_entries.append(tmp)
                amount += 1
        else:

            # retrieves all entries should the user not give a request amount
            user_table_entries = self.cursor.fetchall()

        # print(user_table_entries)
        return user_table_entries
    
    def getEntry(self, request = 0):
        """
            Summary: This will be used by the GUI to show the admin the current Entries Table. Since this table will eventually get huge,
                two options have been implemented. A size request will let the user select how many entries they want to see. The parameter
                has been given a default size of 0 which will indcate the program to return all entries.
            Input: Requested size (optional) <int>
            Output: All entries into the house <list of tuples>
        """

        # Submits sql query for the pictures table. The table is selected with decreasing order so that the most resent is given first
        self.cursor.execute("SELECT Pictures.Date, Pictures.Location, Pictures.Response, Users.UserName\
            FROM Pictures\
            INNER JOIN Users\
            ON Users.UserID = Pictures.UserID\
            ORDER BY PictureID DESC;")

        # checks to see if the user has given a desired amount of entries to be returned
        if request != 0:

            # initializes required variables
            pictures_table_entries = []
            amount = 0
        
            # loops for the amount of entries wanted by the user
            while amount < request:

                # saves the first retrieved entry in a temp variable to be saved in list later
                tmp = self.cursor.fetchone()
                
                # determines if the entries in the table are less then the requested amount
                if not tmp:
                    break

                # adds the retrieved data to the return list
                pictures_table_entries.append(tmp)
                amount += 1
        else:

            # retrieves all entries should the user not give a request amount
            pictures_table_entries = self.cursor.fetchall()

        # print(pictures_table_entries)
        return pictures_table_entries

    def getRooms(self):
        """
            Summary: This will be used by the GUI to show the admin the current Rooms Table. Lets be real, unless some millionair with a
                giant manssion uses this, the Rooms will not need to be limited during retrieval. There for it will always grab every entry
            Input: none
            Output: All rooms in the house <list of tuples>
        """

        # Gets all of the rooms in the house
        self.cursor.execute("SELECT RoomName FROM Bedrooms;")
        bedroom_table_entries = self.cursor.fetchall()

        # print(bedroom_table_entries)
        return bedroom_table_entries
    
    def getDevices(self, roomName = "All"):
        """
            Summary: This will be used by the GUI to show the admin the current Devices Table. Same deal as before, the amount
                of devices in a given room probably wont be more than 5-10. Therefore this function will not need a request buffer.
                This function is special however in that it will only be called with getRooms. Hence, it will only get devices for
                one room at a time
            Input: Room name <string>
            Output: All entries in the devices table <list of tuples>
        """ 
        if roomName != "All":
            # sql query to get roomID
            self.cursor.execute("SELECT RoomID FROM Bedrooms WHERE RoomName = ?", (roomName,))
            bedRoomID = self.cursor.fetchall()

            # sql query for device information
            self.cursor.execute("SELECT Devices.Name, Devices.Purpose, Devices.Importance, Bedrooms.RoomName\
                FROM Devices\
                INNER JOIN Bedrooms\
                ON Bedrooms.RoomID = Devices.RoomID\
                WHERE Bedrooms.RoomID = ?", (bedRoomID[0][0],))

            devices_per_room = self.cursor.fetchall()
            # print(devices_per_room)

        else:
            self.cursor.execute("SELECT Devices.Name, Devices.Purpose, Devices.Importance, Bedrooms.RoomName\
                FROM Devices\
                INNER JOIN Bedrooms\
                ON Bedrooms.RoomID = Devices.RoomID;")

            devices_per_room = self.cursor.fetchall()
        
        return(devices_per_room)
    
#################### Database removal #########################################
    def removeUser(self, _userName):
        """
            Summary: This is what will be called whenever a user is needed to be removed from the database
        """
        self.cursor.execute("DELETE FROM Users WHERE UserName = ?;", (_userName,))
        
    def removeDevice(self, _deviceName):
        """
            Summary: This is what will be called whenever a device is needed to be removed from the database
        """
        self.cursor.execute("DELETE FROM Devices WHERE DeviceName = ?;", (_deviceName,))

    def removeRoom(self, _roomName):
        """
            Summary: This is what will be called whenever a room is needed to be removed from the database
        """
        self.cursor.execute("DELETE FROM Bedrooms WHERE UserName = ?;", (_roomName,))

    def removeEntry(self, _entryTime):
        """
            Summary: This is what will be called whenever a picture is needed to be removed from the database
        """
        self.cursor.execute("DELETE FROM Pictures WHERE UserName = ?;", (_entryTime,))


############################################################## Main Testing

def main():
    """ This is used only for testing purposes"""

    print ("Hello, World!")

    # Database add check
    interface = Database()
    interface.connectToDatabase()

    # Database removal check
    interface.Destroy()
    interface.setupTables()

    #/////////////////////////////////////////////////////

    # Room add check
    interface.addRoom("Liam's Room")
    interface.addRoom("Isaac's Room")
    interface.addRoom("Ryan's Room")
    interface.addRoom("Izzy's Room")


    # Device add check
    interface.addDevice("Google Home", "Central Unit", "Medium", "Liam's Room")
    interface.addDevice("Philibs Light", "Lights room", "Low", "Liam's Room")

    interface.addDevice("Philibs Light", "Lights room", "Low", "Isaac's Room")

    # User add Check
    interface.addUser("Liam_Nestelroad", "9C:E3:3F:8C:4F:BE", "Liam's Room")
    interface.addUser("Isaac_Martienz", "12:34:56:78:90", "Isaac's Room")

    # Pictures add check
    now = datetime.datetime.now()
    interface.addEntry(now, "Front Door", "Accepted", "Liam_Nestelroad")
    interface.addEntry(now, "Garage", "Accepted", "Liam_Nestelroad")

    # Change check
    interface.commitChanges()

    #/////////////////////////////////////////////////////

    # User retrieval check 
    interface.getUsers(1)
    interface.getUsers()

    interface.getEntry(1)
    print(interface.getEntry())

    # Room retrieval check
    interface.getRooms()

    # Devices retrieval check
    interface.getDevices("Liam's Room")
    interface.getDevices("Isaac's Room")

    #/////////////////////////////////////////////////////

    # User delete test
    # interface.removeUser("Liam_Nestelroad")
    # interface.commitChanges()

    # Table Counts
    print(interface.countUsers())
    print(interface.countDevices())
    print(interface.countRooms())
    print(interface.countPictures())


if __name__ == "__main__":
    main()