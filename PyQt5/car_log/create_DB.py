# create_DB.py
"""
Create the database for the car log program
"""
import sys, os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class CreateCarLogData:
    # Create connection to database. If db file does not exist,
    # a new db file will be created.
    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
    database.setDatabaseName("files/car_log.db")
    
    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error code 1 - signifies error

    query = QSqlQuery()
    
    # Erase database contents so that there are not duplicates
    query.exec_("DROP TABLE maintenance")
    query.exec_("DROP TABLE gas")
    
    # Create maintenance table
    query.exec_("""CREATE TABLE maintenance (
                Date INTEGER NOT NULL,
                Mileage INTEGER NOT NULL,
                Cost INTEGER NOT NULL,
                Description TEXT NOT NULL)""")
    
    query.exec_("""INSERT INTO maintenance(Date, Mileage, Cost, Description)
                VALUES('12/27/07', '7500', '35', 'Oil Change'),
                ('2008-05-30', '9500', '125.00', 'Battery'),
                ('12/24/08', '11629', '35.00', 'Oil Change'),
                ('01/12/21', '22135', '35.00', 'Oil Change'),
                ('05/18/21', '24385', '0', 'Tire Rotation'),
                ('07/08/21', '25875', '35.00', 'Air Filter'),
                ('08/21/21', '26897', '35.00', 'Oil Change'),
                ('01/28/22', '107868', '125.00', 'Battery')
                """)
    
    # Create gas table
    query.exec_("""CREATE TABLE gas (
                Date TEXT NOT NULL,
                Gallons TEXT NOT NULL,
                Cost INTEGER NOT NULL,
                Odometer_Reading INTEGER NOT NULL)""")

    query.exec_("""INSERT INTO gas(Date, Gallons, Cost, Odometer_Reading)
                VALUES('01/08/21', '12', '23.75', '220'),
                ('01/17/21', '11', '22.63', '188'),
                ('01/24/21', '9', '21.05', '175')
                """)
    

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    CreateCarLogData()