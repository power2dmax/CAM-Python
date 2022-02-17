# gas.py

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Gas(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        bottom_layout = qtw.QHBoxLayout(self)
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Gas Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Calculate the MPG and display on the bottom of the table
        result = 0
        gasQuery = QSqlQuery("SELECT Gallons FROM gas")
        while gasQuery.next():
            gasUsed = int(gasQuery.value(0))
        mileQuery = QSqlQuery("SELECT Odometer_Reading FROM gas")
        while mileQuery.next():
            mileUsed = int(mileQuery.value(0))
        mpg = ("%.2f" % (mileUsed/gasUsed))
        
        avgMpgText = qtw.QLabel("Your Latest Fuel Economy is:")
        avgMpgText.setFont(qtg.QFont('Arial', 9))
        avgMpgCalc = qtw.QLabel(mpg)
        avgMpgCalc.setFont(qtg.QFont('Arial', 9))
        mpgText = qtw.QLabel("MPG")
        mpgText.setFont(qtg.QFont('Arial', 9))
        
        # Setting up the 
        top_layout.addWidget(add_row)
        top_layout.addWidget(del_row)
        top_layout.addStretch()
        top_layout.addStretch()
        
        bottom_layout.addWidget(avgMpgText)
        bottom_layout.addWidget(avgMpgCalc)
        bottom_layout.addWidget(mpgText)
        bottom_layout.addStretch()
                
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        layout.addLayout(top_layout)
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)        
        
    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('gas')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Gallons'), qtc.Qt.Horizontal, "Gallons")
        self.model.setHeaderData(self.model.fieldIndex('Cost'), qtc.Qt.Horizontal, "Cost")
        self.model.setHeaderData(self.model.fieldIndex('Odometer_Reading'), qtc.Qt.Horizontal, "Odometer Reading")
                
        # Populate the model with data
        self.model.select()
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("car_log/files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'gas'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
    def addRow(self):
        """
        Add a new record to the last row of the table
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = qts.QSqlQuery()
        query.exec_("SELECT MAX (id) FROM gas")
        if query.next():
            id = int(query.value(0))
            
    def deleteRow(self):
        """
        Delete an entire row from the table
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()