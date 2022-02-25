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
    query.exec_("DROP TABLE car")
    query.exec_("DROP TABLE contacts")
    
    # Create maintenance table
    query.exec_("""CREATE TABLE maintenance (
                Date TETX NOT NULL,
                Mileage FLOAT NOT NULL,
                Cost FLOAT NOT NULL,
                Description TEXT NOT NULL)""")
    
    query.exec_("""INSERT INTO maintenance(Date, Mileage, Cost, Description)
                VALUES('12-27-2007', '7500', '35.33', 'Oil Change'),
                ('05-30-2008', '9500', '125.12', 'Battery'),
                ('12-24-2008', '11629', '35.33', 'Oil Change'),
                ('01-12-2021', '22135', '35.33', 'Oil Change'),
                ('05-18-2021', '24385', '12.21', 'Tire Rotation'),
                ('07-08-2021', '25875', '35.33', 'Air Filter'),
                ('12-21-2008', '26897', '35.33', 'Oil Change'),
                ('01-28-2022', '107868', '125.12', 'Battery')
                """)
    
    # Create gas table
    query.exec_("""CREATE TABLE gas (
                Date TEXT NOT NULL,
                Gallons INTEGER NOT NULL,
                Cost FLOAT NOT NULL,
                Odometer_Reading INTEGER NOT NULL)""")

    query.exec_("""INSERT INTO gas(Date, Gallons, Cost, Odometer_Reading)
                VALUES('01-21-2021', '12', '23.75', '220'),
                ('01-17-2021', '11.0', '22.63', '188'),
                ('01-24-2021', '9.0', '21.05', '175'),
                ('02-12-2021', '8.2', '18.44', '117'),
                ('02-17-2021', '7.5', '17.76', '132'),
                ('02-24-2021', '7.8', '18.12', '143'),
                ('03-02-2021', '8.1', '18.68', '165'),
                ('03-13-2021', '8.7', '19.24', '178'),
                ('03-24-2021', '9.1', '22.75', '196'),
                ('05-24-2021', '7.8', '18.32', '142')
                """)
    
    # Create the car table
    query.exec_("""CREATE TABLE car (
                Make TEXT NOT NULL,
                Model Text NOT NULL,
                Year INTEGER NOT NULL)""")
    
    
    query.exec_("""INSERT INTO car(Make, Model, Year)
                VALUES('Ford', 'Mustang', '2006')
                """)
    
    # Create the contacts
    query.exec_("""CREATE TABLE contacts (
                Location TEXT NOT NULL,
                POC Text NOT NULL,
                Number INTEGER NOT NULL)""")
    
    
    query.exec_("""INSERT INTO contacts(Location, POC, Number)
                VALUES('AAA', 'Customer Rep', '1-800-123-4567')
                """)
    
    

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    CreateCarLogData() 