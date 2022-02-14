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
    database.setDatabaseName("files/gas.db")

    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error code 1 - signifies error

    query = QSqlQuery()
    # Erase database contents so that we don't have duplicates
    query.exec_("DROP TABLE gas")
    
    # Create gas table
    query.exec_("""CREATE TABLE gas (
                Date TEXT NOT NULL,
                Odometer_Reading TEXT NOT NULL,
                Gallons TEXT NOT NULL,
                Cost TEXT NOT NULL)""")

    
    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    CreateCarLogData()