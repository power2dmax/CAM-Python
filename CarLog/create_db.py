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
                VALUES('2021-01-21', '12', '23.75', '220'),
                ('2021-01-17', '11.0', '22.63', '188'),
                ('2021-01-24', '9.0', '21.05', '175'),
                ('2021-02-12', '8.2', '18.44', '117'),
                ('2021-02-17', '7.5', '17.76', '132'),
                ('2021-02-24', '7.8', '18.12', '143'),
                ('2021-03-02', '8.1', '18.68', '165'),
                ('2021-03-13', '8.7', '19.24', '178'),
                ('2021-03-24', '9.1', '22.75', '196'),
                ('2021-04-06', '9.8', '25.07', '205'),
                ('2021-04-14', '9.2', '24.73', '199'),
                ('2021-04-21', '5.2', '18.35', '123'),
                ('2021-04-28', '9.8', '22.95', '230'),
                ('2021-05-05', '9.9', '23.06', '232'),
                ('2021-05-11', '7.9', '21.79', '145'),
                ('2021-05-18', '6.8', '18.64', '123'),
                ('2021-05-22', '8.2', '19.54', '165'),
                ('2021-05-24', '7.8', '18.32', '142')
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