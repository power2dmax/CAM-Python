# car_maintenance_log_2
"""
New and improved version of the original car maintenance log.
Enhancements includes the ability to not only track maintenance
but to also track gas. Additional updates includes the ability
to change the color scheme through themes in the tool menu and
a car payment calculator
"""

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('PyQt5 Examples')
        self.resize(500, 650)
        
        self.styleSheet()
        self.createActions()
        self.menuWidget()
        self.toolbarWidget()
        self.mainWindow = MainWindow(self)
        self.setCentralWidget(self.mainWindow)
        
        self.show()
        
    def createActions(self):
        # Create the actions for the "Files Menu"
        self.add_row = qtw.QAction('Add Row', self)
        self.add_row.setShortcut('Ctrl+A')
        #self.add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        #self.add_row.triggered.connect(self.addRecord)
        
        self.exit_action = qtw.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("icons/exit.png"))
        self.exit_action.triggered.connect(self.exitMessage)
        
        self.nativeTheme = qtw.QAction('Native Theme', self)
        self.nativeTheme.triggered.connect(self.nativeStyleSheet)
        self.blueTheme = qtw.QAction('Blue Theme', self)
        self.blueTheme.triggered.connect(self.blueStyleSheet)
        self.crazyTheme = qtw.QAction('Crazy Theme', self)
        self.crazyTheme.triggered.connect(self.crazyStyleSheet)
        
        self.payment_calc = qtw.QAction('Payment Calculator', self)
        
        # Create actions for the "Help Menu" menu
        self.about_action = qtw.QAction('About', self)
        self.about_action.setIcon(qtg.QIcon("icons/about.png"))
        self.about_action.triggered.connect(self.aboutInfo)
        
    def menuWidget(self):
        # Create the status bar
        self.statusBar().showMessage('Welcome to Car Maintenance Log')
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
       # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.exit_action)
        
        toolsMenu = menu_bar.addMenu('Tools')
        toolsMenu.addAction(self.payment_calc)
        themesMenu = toolsMenu.addMenu('Themes')
        themesMenu.addAction(self.nativeTheme)
        themesMenu.addAction(self.blueTheme)
        themesMenu.addAction(self.crazyTheme)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(self.about_action)
        
    def toolbarWidget(self):
        toolbar = qtw.QToolBar()
        self.addToolBar(qtc.Qt.BottomToolBarArea, toolbar)
        toolbar.addAction(self.exit_action)
        
    def exitMessage(self):
        message = qtw.QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            #self.database.close()
            self.close()
            
    def aboutInfo(self):
        text_1 = "CAM's car log, written in Python \n"
        text_2 = "using PyQt5 modules for the GUI \n\n"
        text_3 = "Originally written: 1/27/22"
        
        qtw.QMessageBox.about(self, "CAM's Car Log", text_1 + text_2 + text_3)
            
    def nativeStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: whitesmoke;
        }
        QPushButton {
            font-size: 10pt;
        }
        QTableView {
            background-color: white;
        }
        
        """
        self.setStyleSheet(stylesheet)
        
    def blueStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: lightblue;
        }
        QPushButton {
            font-size: 10pt;
        }
        QTableView {
            background-color: aliceblue;
        }
        
        """
        self.setStyleSheet(stylesheet)
    
    def crazyStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: lightgreen;
        }
        QPushButton {
            font-size: 10pt;
        }
        QTableView {
            background-color: plum;
        }
        
        """
        self.setStyleSheet(stylesheet)
        
    
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        self.layout = qtw.QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = qtw.QTabWidget()
        self.tab1 = Maintenance(self)
        self.tab2 = Gas(self)
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Maintenance")
        self.tabs.addTab(self.tab2,"Gas")
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
class Maintenance(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        self.layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        
        self.add_row = qtw.QPushButton("Add Row")
        self.add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        self.add_row.setStyleSheet("padding: 6px")
        self.add_row.clicked.connect(self.addRow)
        
        self.del_row = qtw.QPushButton("Delete Row")
        self.del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        self.del_row.setStyleSheet("padding: 6px")
        self.del_row.clicked.connect(self.deleteRow)
        
        self.sorting_options = ["Sort by Date", "Sort by Mileage","Sort by Item"] # Set up sorting combo box
        self.sort_name_cb = qtw.QComboBox()
        self.sort_name_cb.addItems(self.sorting_options)
        self.sort_name_cb.currentTextChanged.connect(self.setSortingOrder)
        
        self.sorting_text = qtw.QLabel("Sorting Options: ")
        
        top_layout.addWidget(self.add_row)
        top_layout.addWidget(self.del_row)
        top_layout.addStretch()
        top_layout.addWidget(self.sorting_text)
        top_layout.addWidget(self.sort_name_cb)
        top_layout.addStretch()
        self.setLayout(top_layout)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Car Maintenance Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        self.layout.addLayout(top_layout)
        self.layout.addWidget(title, qtc.Qt.AlignLeft)
        self.layout.addWidget(self.table_view)
    
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/maintenance.db")

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
        self.model.setHeaderData(self.model.fieldIndex('Item'), qtc.Qt.Horizontal, "Item")
        
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
            self.model.setSort(self.model.fieldIndex('Milage'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Item":
            self.model.setSort(self.model.fieldIndex('Item'), qtc.Qt.AscendingOrder)
        
        self.model.select()


class Gas(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        self.layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        
        self.add_row = qtw.QPushButton("Add Row")
        self.add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        self.add_row.setStyleSheet("padding: 6px")
        self.add_row.clicked.connect(self.addRow)
        
        self.del_row = qtw.QPushButton("Delete Row")
        self.del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        self.del_row.setStyleSheet("padding: 6px")
        self.del_row.clicked.connect(self.deleteRow)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Car Gas Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        top_layout.addWidget(self.add_row)
        top_layout.addWidget(self.del_row)
        top_layout.addStretch()
        self.setLayout(top_layout)
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        self.layout.addLayout(top_layout)
        self.layout.addWidget(title, qtc.Qt.AlignLeft)
        self.layout.addWidget(self.table_view)
        
    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('gas')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), qtc.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Odometer_Reading'), qtc.Qt.Horizontal, "Odometer Reading")
        self.model.setHeaderData(self.model.fieldIndex('Gallons'), qtc.Qt.Horizontal, "Gallons")
        self.model.setHeaderData(self.model.fieldIndex('Cost'), qtc.Qt.Horizontal, "Cost")
                
        # Populate the model with data
        self.model.select()
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/gas.db")

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

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())