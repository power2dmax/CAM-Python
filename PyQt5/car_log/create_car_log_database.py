# create_car_log_database.py
# Program to create the database used for the car_log.py program
# using SQLite
# Written by CAM on 01/27/22

# Import the necessary modules
import sys, random
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts

class CreateMaintenanceData:
    """
    Create a simple database for the car_log.py program.
    """
    # Create connection to database. If db deos not exist,
    # create a new db file
    database = qts.QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("files/car_log.db")
    
    if not database.open():
        print ("Unable to open data source file")
        sys.exit(1) # Error code 1 - signifies error
        
    query = qts.QSqlQuery()
    # Erase database so we don't have duplicates
    query.exec_("DROP TABLE maintenance")
        
    # Create accoutns table
    query.exec_("""CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                date INTEGER NOT NULL,
                action VARCHAR(20) NOT NULL,
                """)
    
    # Positional binding to insert records into the database
    query.prepare("""INSERT INTO maintenance (
                  date, action) VALUES (?, ?)""")

    date_entries = ["12/21/21", "12/22/21", "12/23/21"]

    action_entries = ["Oil Change", "Tire Rotation", "Tune-up"]

    # Add the values to the query to be inserted in accounts
    for f_name in date_entries:
        
        
        query.addBindValue(date_entries)
        query.addBindValue(action_entries)
        query.exec_()



    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == '__main__':
    CreateMaintenanceData()