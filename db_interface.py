#!/usr/bin/env python3

import sqlite3
import argparse

class Database():
    def __init__(self):
        self.cxn = None
        self.cursor = None

    def createDatabase(self):
        try:
            # Create a connection to the database
            self.cxn = sqlite3.connect("/home/liam_work/Documents/Home_Automation/Gozer_database.db")
            print("Opening Connections to database")

            # Create a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except sqlite3.Error as error:
            print("Error connecting to database. " + str(error))

    def setupTables(self):
        ''' Method to create a table'''

        # Write a SQL statement to create the table
        Devices = "CREATE TABLE Devices(\
                DeviceID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Name TEXT NOT NULL,\
                Purpose TEXT NOT NULL,\
                Importance TEXT\
                );"
        self.cursor.execute(Devices)

        Bedrooms = "CREATE TABLE Bedrooms(\
                RoomID INTEGER PRIMARY KEY AUTOINCREMENT,\
                RoomName TEXT NOT NULL,\
                Machines INTEGER,\
                FOREIGN KEY(Machines) REFERENCES Devices(DeviceID)\
                );"
        self.cursor.execute(Bedrooms)

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

def main():
    print ("Hello, World!")

    test = Database()
    test.createDatabase()
    test.setupTables()

if __name__ == "__main__":
    main()