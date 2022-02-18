# maintenance.py

import sys
from os import path
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
        
class Maintenance(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        bottom_layout = qtw.QHBoxLayout(self)
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("car_log/icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("car_log/icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        sorting_options = ["Sort by Mileage", "Sort by Cost", "Sort by Description"] # Set up sorting combo box
        sort_name_cb = qtw.QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)
        
        sorting_text = qtw.QLabel("Sorting Options: ")
        
        top_layout.addWidget(add_row)
        top_layout.addWidget(del_row)
        top_layout.addStretch()
        top_layout.addWidget(sorting_text)
        top_layout.addWidget(sort_name_cb)
        top_layout.addStretch()
        #self.setLayout(top_layout)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Maintenance Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        # Calculate the total cost of the maintenance performed by adding the results in the costs column
        result = 0
        query = QSqlQuery("SELECT Cost FROM maintenance")
        while query.next():
            result = result + query.value(0)
        totalCost =str("%.2f" % (result))
        totalCostText_1 = qtw.QLabel('The Total Maintenance Cost is: $')
        totalCostText_1.setFont(qtg.QFont('Arial', 9))
        totalCostText_2 = qtw.QLabel(totalCost)
        totalCostText_2.setFont(qtg.QFont('Arial', 9))
        bottom_layout.addWidget(totalCostText_1)
        bottom_layout.addWidget(totalCostText_2)
        bottom_layout.addStretch()
                
        # Set the overall layouit
        layout.addLayout(top_layout)
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("car_log/files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error

    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('maintenance')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Mileage'), qtc.Qt.Horizontal, "Mileage")
        self.model.setHeaderData(self.model.fieldIndex('Cost'), qtc.Qt.Horizontal, "Cost")
        self.model.setHeaderData(self.model.fieldIndex('Description'), qtc.Qt.Horizontal, "Description")
        
        # Populate the model with data
        self.model.select()
        
    def addRow(self):
        """
        Add a new record to the last row of the table
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = qts.QSqlQuery()
        query.exec_("SELECT MAX (id) FROM maintenance")
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
    
    def setSortingOrder(self, text):
        """
        Sort the rows in table
        """
        if text == "Sort by Date":
            self.model.setSort(self.model.fieldIndex('Date'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Mileage":
            self.model.setSort(self.model.fieldIndex('Mileage'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Cost":
            self.model.setSort(self.model.fieldIndex('Cost'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Description":
            self.model.setSort(self.model.fieldIndex('Description'), qtc.Qt.AscendingOrder)
        
        self.model.select()
