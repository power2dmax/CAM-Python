# create_database.py
# Import necessary modules
import sys, random
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class CreateCarLogData:
    """
    Create sample database for project.
    Class demonstrates how to connect to a database, create queries, and
    create tables and records in those tables.
    """
    # Create connection to database. If db file does not exist,
    # a new db file will be created.
    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
    database.setDatabaseName("files/car_log.db")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error code 1 - signifies error

    query = QSqlQuery()
    # Erase database contents so that we don't have duplicates
    query.exec_("DROP TABLE maintenance")
    
    # Create accounts table
    query.exec_("""CREATE TABLE maintenance (
                Date TEXT NOT NULL,
                Mileage TEXT NOT NULL,
                Item TEXT NOT NULL)""")

    # Positional binding to insert records into the database
    query.prepare("""INSERT INTO maintenance (
                  Date, Mileage, Item) VALUES
                  ('01/13/21', '25174', 'Oil Change'),
                  ('02/23/21', '26678', 'Tire Rotation'),
                  ('03/03/21', '28743', 'Tune up')
                  """)

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    CreateCarLogData()