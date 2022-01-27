# create_database.py
# Import the necessary modules
import sys, random
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts

class CreateEmployeeData:
    """ Create a simple database for project."""
    # Create connection to database. If db deos not exist,
    # create a new db file
    database = qts.QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("files/accounts.db")
    
    if not database.open():
        print ("Unable to open data source file")
        sys.exit(1) # Error code 1 - signifies error
        
    query = qts.QSqlQuery()
    # Erase database so we don't have duplicates
    query.exec_("DROP TABLE accounts")
    query.exec_("DROP TABLE countries")
    
    # Create accoutns table
    query.exec_("""CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                employee_id INTEGER NOT NULL,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(40) NOT NULL,
                department VARCHAR(20) NOT NULL,
                country_id VARCHAR(20) REFERENCES countries(id))""")
    
    # Positional binding to insert records into the database
    query.prepare("""INSERT INTO accounts (
                  employee_id, first_name, last_name,
                  email, department, country_id)
                  VALUES (?, ?, ?, ?, ?, ?)""")

    first_names = ["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia",
    "Charlotte", "Amelia", "Evelyn", "Abigail", "Valorie", "Teesha",
    "Jazzmin", "Liam", "Noah", "William", "James", "Logan", "Benjamin",
    "Mason", "Elijah", "Oliver", "Jason", "Lucas", "Michael"]

    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez",
    "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]

    employee_ids = random.sample(range(1000, 2500), len(first_names))

    countries = {"USA": 1, "India": 2, "China": 3, "France": 4, "Germany": 5}
    country_names = list(countries.keys())
    country_codes = list(countries.values())

    departments = ["Production", "R&D", "Marketing", "HR",
                   "Finance", "Engineering", "Managerial"]
    
    # Add the values to the query to be inserted in accounts
    for f_name in first_names:
        l_name = last_names.pop()
        email = (l_name + f_name[0]).lower() + "@job.com"
        country_id = random.choice(country_codes)
        dept = random.choice(departments)
        employee_id = employee_ids.pop()
        query.addBindValue(employee_id)
        query.addBindValue(f_name)
        query.addBindValue(l_name)
        query.addBindValue(email)
        query.addBindValue(dept)
        query.addBindValue(country_id)
        query.exec_()

    # Create the second table, countries
    country_query = qts.QSqlQuery()
    country_query.exec_("""CREATE TABLE countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                country VARCHAR(20) NOT NULL)""")

    country_query.prepare("INSERT INTO countries (country) VALUES (?)")

    # Add the values to the query to be inserted in countries
    for name in country_names:
        country_query.addBindValue(name)
        country_query.exec_()

    print("[INFO] Database successfully created.")

    sys.exit(0)

if __name__ == '__main__':
    CreateEmployeeData()