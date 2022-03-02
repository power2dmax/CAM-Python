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
    query.exec_("DROP TABLE mortgage")
    
    
    
    # Create mortgage table
    query.exec_("""CREATE TABLE mortgage (
                Date REAL NOT NULL,
                Payment INT NOT NULL,
                Additional_Payment INT2 NOT NULL,
                Principle INT NOT NULL,
                Interest INT NOT NULL,
                Escrow INT NOT NULL,
                Balance INT2 NOT NULL)""")
    
    #query.exec_("""INSERT INTO mortgage(Date, Payment, Additional_Payment, Principle, Interest, Escrow, Balance)
    #            VALUES('Jun-2016', '1128.04', '21.96', '291.21', '539.52', '297.31', '184686.83'),
    #            ('Jul-2016', '1128.04', '21.96', '291.12', '538.61', '297.31', '184372.75'),
    #            ('Aug-2016', '1128.04', '21.96', '292.98', '537.75', '297.31', '184057.81'),
    #            ('Sep-2016', '1128.04', '71.96', '294.10', '536.63', '297.31', '183691.75'),               
    #            ('Oct-2016', '1128.04', '71.96', '295.17', '535.35', '297.31', '183324.62'),
    #            ('Nov-2016', '1128.04', '71.96', '296.24', '534.49', '297.31', '182956.42')
    #            """)
    
    

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == "__main__":
    FinacialData() 