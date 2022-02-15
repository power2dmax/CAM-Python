# car_maintenance_log_2
"""
1-27-22
Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite for the data.
The user can enter the date, millage, and the maintenance performed.
The user will also have the capability to delete a row

2-14-22
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
        
        self.setWindowTitle('Car Log')
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
        
        #self.payCalc = PaymentCalculator(self)
        self.payment_calc = qtw.QAction('Payment Calculator', self)
        self.payment_calc.setIcon(qtg.QIcon("icons/calc.png"))
        self.payment_calc.triggered.connect(self.payCalc)
        
        # Create actions for the "Help Menu" menu
        self.about_action = qtw.QAction('About', self)
        self.about_action.setIcon(qtg.QIcon("icons/about.png"))
        self.about_action.triggered.connect(self.aboutInfo)
        
    def menuWidget(self):
        # Create the status bar
        self.statusbar = self.statusBar()
        self.statusBar().showMessage('Welcome to your Car Log')
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
       # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.exit_action)
        
        toolsMenu = menu_bar.addMenu('Tools')
        toolsMenu.addAction(self.payment_calc)
        themesMenu = toolsMenu.addMenu(qtg.QIcon("icons/theme.png"), 'Themes')
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
            
    def payCalc(self):
        calc = PaymentCalculator(self)
        calc.resize(350, 250)
        calc.show()
            
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
        QLabel {
            background-color: yellow;
        }
        QPushButton {
            background-color: yellow;
        }
        
        """
        self.setStyleSheet(stylesheet)
    
    
class PaymentCalculator(qtw.QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Payment Calculator')
        self.setLayout(qtw.QGridLayout())
        self.topLabel = qtw.QLabel("<h3>Payment Calculator<h3>")
        self.carPriceText = qtw.QLabel("Enter the Purchase Price:")
        self.carPriceEntry = qtw.QLineEdit()
        self.interestRateText = qtw.QLabel("Enter the Interest Rate:")
        self.interestRateEntry = qtw.QLineEdit()
        self.termLengthText = qtw.QLabel("Enter the Number of Years:")
        self.termLengthEntry = qtw.QLineEdit()
        
        self.monthlyPayment = 0.0
        
        self.calculationButton = qtw.QPushButton('Calculate')
        self.calculationButton.clicked.connect(self.calculatePayment)
        
        self.exitButton = qtw.QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)
        
        self.layout().addWidget(self.topLabel, 0, 0)
        self.layout().addWidget(self.exitButton, 0, 1)
        self.layout().addWidget(self.carPriceText, 1, 0)
        self.layout().addWidget(self.carPriceEntry, 1, 1)
        self.layout().addWidget(self.interestRateText, 2, 0)
        self.layout().addWidget(self.interestRateEntry, 2, 1)
        self.layout().addWidget(self.termLengthText, 3, 0)
        self.layout().addWidget(self.termLengthEntry, 3, 1)
        
        self.layout().addWidget(self.calculationButton, 4, 0)
        #self.layout().addWidget(self.monthlyPayment, 4, 1)
        
        
        
        
    def calculatePayment(self):
        pass
        """self.monthlyPayment = int(carPriceEntry*interestRateEntry)/(12*termLengthEntry)
        return self.monthlyPayment"""
    
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
        # Initialize tab screen
        tabs = qtw.QTabWidget()
        tab1 = Maintenance(self)
        tab2 = Gas(self)
        tabs.resize(300,200)
        
        # Add tabs
        tabs.addTab(tab1,"Maintenance")
        tabs.addTab(tab2,"Gas")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        
class Maintenance(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        sorting_options = ["Sort by Date", "Sort by Mileage", "Sort by Cost", "Sort by Description"] # Set up sorting combo box
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
        
        layout.addLayout(top_layout)
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addWidget(self.table_view)
    
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

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


class Gas(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createConnection()
        self.createTable()
        
        layout = qtw.QVBoxLayout(self)
        top_layout = qtw.QHBoxLayout(self)
        
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
        
        avgMpgText = qtw.QLabel("Average MPG is:")
        avgMpgCalc = qtw.QLabel("32 MPG")
        
        top_layout.addWidget(add_row)
        top_layout.addWidget(del_row)
        top_layout.addStretch()
        #top_layout.addWidget(avgMpgText)
        #top_layout.addWidget(avgMpgCalc)
        top_layout.addStretch()
                
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
        #self.layout.addWidget(bottom_layout)
        
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
        self.database.setDatabaseName("files/car_log.db")

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