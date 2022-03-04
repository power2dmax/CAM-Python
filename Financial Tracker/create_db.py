# create_DB.py
"""
Create the database for the financial program
"""
import sys, os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class FinacialData:
    # Create connection to database. If db file does not exist,
    # a new db file will be created.
    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
    database.setDatabaseName("files/financial_log.db")
    
    if not database.open():
        print("Unable to open data source file.")
        sys.exit(1) # Error code 1 - signifies error

    query = QSqlQuery()
    
    # Erase database contents so that there are not duplicates
    query.exec_("DROP TABLE checking")
    query.exec_("DROP TABLE savings")
    query.exec_("DROP TABLE retirement")
    #query.exec_("DROP TABLE mortgage")
    query.exec_("DROP TABLE amortization")
    

    # Create mortgage table
    query.exec_("""CREATE TABLE mortgage (
                Date INTEGER NOT NULL,
                Payment INTEGER NOT NULL,
                Additional_Payment INTEGER NOT NULL,
                Principle INTEGER NOT NULL,
                Interest INTEGER NOT NULL,
                Escrow INTEGER NOT NULL,
                Balance INTEGER NOT NULL)""")
    
    
    # Create amortization table
    query.exec_("""CREATE TABLE amortization (
                Principle INTEGER NOT NULL)""")
        

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    FinacialData() 