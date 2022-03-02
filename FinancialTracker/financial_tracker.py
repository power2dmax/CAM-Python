# financial_tracker.py
"""

"""

import sys, os, csv
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class DateDelegate(qtw.QStyledItemDelegate):

    def createEditor(self, parent, option, proxyModelIndex):
        # make sure to explicitly set the parent
        # otherwise it pops up in a top-level window!
        date_inp = qtw.QDateEdit(parent, calendarPopup=True)
        d = qtc.QDate.currentDate()
        date_inp.setDate(d)
        return date_inp
    

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Fitness Tracker')
        self.setWindowIcon(qtg.QIcon("icons/cam_3.png"))
        self.resize(1125, 750)
        
        self.createActions()
        self.menuWidget()
        self.mainWindow = MainWindow(self)
        self.setCentralWidget(self.mainWindow)
                
        
        self.show()
        
    def createActions(self):
        self.exit_action = qtw.QAction('Exit')
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("icons/exit.png"))
        self.exit_action.triggered.connect(self.close)
        
        
        
    def menuWidget(self):
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
       # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.exit_action)
        
        
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
        self.createConnection()
                
        # Initialize tab screen
        tabs = qtw.QTabWidget()
        tab1 = Dashboard(self)
        tab2 = Checking(self)
        tab3 = Savings(self)
        tab4 = Retirement(self)
        tab5 = Mortgage(self)
        tabs.resize(300,200)
        
        # Add tabs
        tabs.addTab(tab1, qtg.QIcon("icons/cash.png"), "Dashboard")
        tabs.addTab(tab2,qtg.QIcon("icons/cash.png"), "Checking")
        tabs.addTab(tab3, qtg.QIcon("icons/cash.png"), "Savings")
        tabs.addTab(tab4, qtg.QIcon("icons/cash.png"), "Retirement")
        tabs.addTab(tab5, qtg.QIcon("icons/cash.png"), "Mortgage")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/financial_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'mortgage'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
class Dashboard(qtw.QWidget):
        
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        title = qtw.QLabel("Coming Soon")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        layout.addWidget(title)


class Checking(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass
        

class Savings(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Retirement(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Mortgage(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        self.createTable()
        
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        
        left_layout = qtw.QVBoxLayout()
        left_top_layout = qtw.QHBoxLayout()
        left_bottom_layout = qtw.QHBoxLayout()
        
        right_layout = qtw.QVBoxLayout()       
        right_top_layout = qtw.QVBoxLayout()
        right_middle_layout = qtw.QVBoxLayout()
        right_bottom_layout = qtw.QVBoxLayout()
        
        title = qtw.QLabel("Mortgage Balance")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.table_view.setModel(self.model)
        #header.setStretchLastSection(True)
        #self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows + qtw.QTableView.SelectColumns)
        
        # Using a custom delegate
        self.dateDelegate = DateDelegate()
        self.table_view.setItemDelegateForColumn(
            self.model.fieldIndex('Date'),
            self.dateDelegate)
                
        # Populate the model with data
        self.model.select()
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        left_bottom_layout.addWidget(add_row)
        left_bottom_layout.addWidget(del_row)
        left_bottom_layout.addStretch()
        
        left_layout.addWidget(title)
        left_layout.addWidget(self.table_view)
        left_layout.addLayout(left_bottom_layout)
        
        
        balance = []
        query = QSqlQuery("SELECT Balance FROM mortgage")
        while query.next():
            balance.append(query.value(0))
        
        self.static_canvas = FigureCanvas(Figure(figsize=(6, 3)))
        right_top_layout.addWidget(NavigationToolbar(self.static_canvas, self))

        self.static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self.static_ax.plot(balance)
        
        right_top_layout.addWidget(self.static_canvas)
        
        total_principle = 185000.00
        current_principle = 40979.73
        current_interest = 33912.69
        total_interest = 114062.00
        
        
        
        
        
        right_layout.addLayout(right_top_layout)
        right_layout.addLayout(right_middle_layout)
        right_layout.addLayout(right_bottom_layout)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        
        
        
    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('mortgage')
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, " Date ")
        self.model.setHeaderData(self.model.fieldIndex('Payment'), qtc.Qt.Horizontal, " Payment ")
        self.model.setHeaderData(self.model.fieldIndex('Additional_Payment'), qtc.Qt.Horizontal, " Additional ")
        self.model.setHeaderData(self.model.fieldIndex('Principle'), qtc.Qt.Horizontal, " Principle ")
        self.model.setHeaderData(self.model.fieldIndex('Interest'), qtc.Qt.Horizontal, " Interest ")
        self.model.setHeaderData(self.model.fieldIndex('Escrow'), qtc.Qt.Horizontal, " Escrow ")
        self.model.setHeaderData(self.model.fieldIndex('Balance'), qtc.Qt.Horizontal, " Balance ")
        
    def addRow(self):
        """
        Add a new record to the last row of the table
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)
            
    def deleteRow(self):
        """
        Delete an entire row from the table
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())
