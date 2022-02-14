# create_DB.py
# Import necessary modules
import sys, random
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class CreateCarLogData:
    """
    Create the database for the car log program
    """
    # Create connection to database. If db file does not exist,
    # a new db file will be created.
    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
    database.setDatabaseName("files/car_log.db")
    #database.setDatabaseName("files/gas.db")

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
                Item TEXT NOT NULL)""")
    
    query.exec_("""INSERT INTO maintenance(Date, Mileage, Item)
                VALUES('01/12/21', '22135', 'Oil Change'),
                ('05/18/21', '24385', 'Tire Rotation'),
                ('07/08/21', '25875', 'Air Filter'),
                ('08/21/21', '26897', 'Oil Change')
                """)
    
    # Create gas table
    query.exec_("""CREATE TABLE gas (
                Date INTEGER NOT NULL,
                Gallons INTEGER NOT NULL,
                Cost INTEGER NOT NULL,
                Odometer_Reading INTEGER NOT NULL)""")

    query.exec_("""INSERT INTO gas(Date, Gallons, Cost, Odometer_Reading)
                VALUES('01/08/21', '12', '$23.75', '220'),
                ('01/17/21', '11', '$22.63', '188'),
                ('01/24/21', '9', '$21.05', '175')
                """)
    

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    CreateCarLogData()