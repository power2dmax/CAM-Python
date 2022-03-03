# car_log.py
"""
Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite for the data.
"""

import sys
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Car Log')
        self.setWindowIcon(qtg.QIcon("icons/cam_3.png"))
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
        
        self.exit_action = qtw.QAction('Exit',
                triggered=lambda: self.statusBar().showMessage('Gonna Quit'))
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("icons/exit.png"))
        self.exit_action.triggered.connect(self.exitMessage)
        
        theme_icon = qtg.QIcon("icons/monitor.png")
        self.defaultTheme = qtw.QAction(theme_icon, 'Default',
                triggered=lambda: self.statusBar().showMessage('Default Theme'))
        self.defaultTheme.triggered.connect(self.defaultStyleSheet)
        self.blueTheme = qtw.QAction(theme_icon, 'Blue',
                triggered=lambda: self.statusBar().showMessage('Blue Theme'))
        self.blueTheme.triggered.connect(self.blueStyleSheet)
        self.chromeTheme = qtw.QAction(theme_icon,'Chrome',
                triggered=lambda: self.statusBar().showMessage('Chrome Theme'))
        self.chromeTheme.triggered.connect(self.chromeStyleSheet)
        self.meshTheme = qtw.QAction(theme_icon,'Mesh',
                triggered=lambda: self.statusBar().showMessage('Mesh Theme'))
        self.meshTheme.triggered.connect(self.meshStyleSheet)
        self.digitalBlueTheme = qtw.QAction(theme_icon, 'Digital Blue', 
                triggered=lambda: self.statusBar().showMessage('Digital Blue Theme'))
        self.digitalBlueTheme.triggered.connect(self.digitalBlueStyleSheet)
        self.southWestTheme = qtw.QAction(theme_icon, 'South West',
                triggered=lambda: self.statusBar().showMessage('South West Theme'))
        self.southWestTheme.triggered.connect(self.southWestStyleSheet)
        self.racerTheme = qtw.QAction(theme_icon, 'Racer',
                triggered=lambda: self.statusBar().showMessage('Racer Theme'))
        self.racerTheme.triggered.connect(self.raceStyleSheet)
        self.crazyTheme = qtw.QAction(theme_icon, 'Crazy',
                triggered=lambda: self.statusBar().showMessage('Crazy Theme'))
        self.crazyTheme.triggered.connect(self.crazyStyleSheet)
        
        #self.payCalc = PaymentCalculator(self)
        self.payment_calc = qtw.QAction('Payment Calculator',
                triggered=lambda: self.statusBar().showMessage('Car Payment Calculator'))
        self.payment_calc.setIcon(qtg.QIcon("icons/calc.png"))
        self.payment_calc.triggered.connect(self.payCalc)
        
        # Create actions for the "Help Menu" menu
        self.about_action = qtw.QAction('About',
                triggered=lambda: self.statusBar().showMessage('About'))
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
        themesMenu.addAction(self.defaultTheme)
        themesMenu.addAction(self.blueTheme)
        themesMenu.addAction(self.chromeTheme)
        themesMenu.addAction(self.meshTheme)
        themesMenu.addAction(self.digitalBlueTheme)
        themesMenu.addAction(self.southWestTheme)
        themesMenu.addAction(self.racerTheme)
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
        calc.resize(350, 350)
        calc.show()
            
    def aboutInfo(self):
        text = "CAM's car log, written in Python\n" \
        "using PyQt5 modules for the GUI\n\n" \
        "The car log allows users to track their\n" \
        "maintence and fuel. Users are also able to \n" \
        "change the color scheme through themes in\n" \
        "the Tool Menu based on their prefrences\n\n" \
        "Written by CAM: 2022"
        qtw.QMessageBox.about(self, "CAM's Car Log", text)
            
    def defaultStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: whitesmoke
        }
        QTableView {
            background-color: white
        }
        """
        self.setStyleSheet(stylesheet)
        
    def blueStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox {
            background-color: lightsteelblue
        }
        QPushButton {
            font-size: 10pt
            background-color: azure
        }
        QLabel {
            color: white
        }
        QTableView {
            background-color: aliceblue
        }
        QMenuBar, QTabWidget {
            background-color: powderblue
        }
        .QWidget {
           background: url(images/tile.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def chromeStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(images/chrome.png)
        }
        QLabel {
            color: silver
        }
        QMessageBox {
            background: url(images/chrome.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def meshStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox, QDialog {
            background: url(images/mesh.png)
        }
        QTableView {
            background: lightgray
        }
        QCheckBox{
            color: white;
            font: bold 12px
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def digitalBlueStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(images/blue_mesh.png)
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QTableView, QMessageBox, QComboBox, QPushButton  {
            background: url(images/light_blue_steel.png)
        }
        QPushButton:hover {
            background: lightblue
        }
        QCheckBox{
            color: white;
            font: bold 12px
        }
        QTableView {
            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.75, y2: 0.75,
            stop: 0 #2E97AC, stop: 1 #C6E4E7)
        }
        QMenuBar {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 lightgray, stop:1 darkgray);
            spacing: 3px; /* spacing between menu bar items */
        }
        QMenuBar::item {
            padding: 1px 4px;
            background: transparent;
            border-radius: 4px;
        }
        QMenuBar::item:selected { /* when selected using mouse or keyboard */
            background: #a8a8a8;
        }
        QMenuBar::item:pressed {
            background: #888888;
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid #C2C7CB;
        }
        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }
        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }
        QDialog {
            background: url(images/blue_mesh.png)
        }
        QDialog QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def raceStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(images/race_cam.png)
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def southWestStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(images/south_west.png)
        }
        QTableView {
            background: url(images/south_rug.png);
            color: white;
            font: bold 14px
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QCheckBox{
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def crazyStyleSheet(self):
        stylesheet = """
        QMainWindow { 
            background-color: lightgreen
        }
        QPushButton {
            font-size: 10pt
        }
        QTableView {
            background-color: plum
        }
        QLabel, QPushButton {
            background-color: yellow
        }
        """
        self.setStyleSheet(stylesheet)
    
    
class PaymentCalculator(qtw.QDialog):
            
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Payment Calculator')
        
        pay_label = qtw.QLabel("<h2>Payment Calculator<h2>", self)
        
        loan_label = qtw.QLabel("Amount:", self)
        loan_label.setFont(qtg.QFont('Arial', 10))
        
        self.amount = qtw.QLineEdit(self, placeholderText='$')
        self.amount.setValidator(qtg.QIntValidator())
        self.amount.setAlignment(qtc.Qt.AlignCenter)
        self.amount.setFont(qtg.QFont('Arial', 10))

        # creating a number of years label
        years_label = qtw.QLabel("Years:", self)
        years_label.setFont(qtg.QFont('Arial', 10))
  
        # creating a QLineEdit object to get the years
        self.years = qtw.QLineEdit(self, placeholderText='Years')
        self.years.setValidator(qtg.QIntValidator())
        self.years.setAlignment(qtc.Qt.AlignCenter)
        self.years.setFont(qtg.QFont('Arial', 10))
  
        interest_label = qtw.QLabel("Annual Interest:", self)
        interest_label.setFont(qtg.QFont('Arial', 10))
  
        # creating a QLineEdit object to get the interest
        self.rate = qtw.QLineEdit(self, placeholderText='%')
        self.rate.setValidator(qtg.QIntValidator())
        self.rate.setAlignment(qtc.Qt.AlignCenter)
        self.rate.setFont(qtg.QFont('Arial', 10))
  
        # creating a push button
        calculate = qtw.QPushButton("Calculate Payment", self)
        calculate.clicked.connect(self.calculate_action)
  
        # creating a label to show monthly payment
        self.monthly_payment = qtw.QLabel(self)
        self.monthly_payment.setAlignment(qtc.Qt.AlignCenter)
        self.monthly_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 1px solid black;"
                                     "background : lightgray;"
                                     "}")
        self.monthly_payment.setFont(qtg.QFont('Arial', 10, qtg.QFont.Bold))
  
        # creating a label to show monthly payment
        self.total_payment = qtw.QLabel(self)
  
        # setting properties to y payment label
        self.total_payment.setAlignment(qtc.Qt.AlignCenter)
        self.total_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 1px solid black;"
                                     "background : lightgray;"
                                     "}")
        self.total_payment.setFont(qtg.QFont('Arial', 10, qtg.QFont.Bold))
        
        exitButton = qtw.QPushButton('Exit', self)
        exitButton.clicked.connect(self.close)
        
        # Set up the layout 
        pay_label.move(80, 10)
        loan_label.move(50, 50)
        self.amount.move(150, 50)
        years_label.move(50, 80)
        self.years.move(150, 80)
        interest_label.move(50, 110)
        self.rate.move(150, 110)
        calculate.move(50, 150)
        self.monthly_payment.setGeometry(50, 190, 235, 40)
        self.total_payment.setGeometry(50, 240, 235, 40)
        exitButton.move(240, 300)
          
    def calculate_action(self):
        annualInterestRate = self.rate.text()
        if len(annualInterestRate) == 0 or annualInterestRate == '0':
            return
        
        numberOfYears = self.years.text()
        if len(numberOfYears) == 0 or numberOfYears == '0':
            return

        loanAmount = self.amount.text()
        if len(loanAmount) == 0 or loanAmount == '0':
            return
  
        # converting text to int
        annualInterestRate = int(annualInterestRate)
        numberOfYears = int(numberOfYears)
        loanAmount = int(loanAmount)
  
        # getting monthly interest rate
        monthlyInterestRate = annualInterestRate / 1200
  
        # Calculate the monthly payemnt
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
        monthlyPayment = "{:.2f}".format(monthlyPayment)
        self.monthly_payment.setText("Monthly Payment : " + str(monthlyPayment))
        
        # Calculate the total payment
        totalPayment = float(monthlyPayment) * 12 * numberOfYears
        totalPayment = "{:.2f}".format(totalPayment)
        self.total_payment.setText("Total Payment : " + str(totalPayment))  
    
    
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
        self.createConnection()
        
        # Initialize tab screen
        tabs = qtw.QTabWidget()
        tab1 = Maintenance(self)
        tab2 = Gas(self)
        tab3 = CheckList(self)
        tabs.resize(300,200)
        
        # Add tabs
        tabs.addTab(tab1, qtg.QIcon("icons/wrench.png"), "Maintenance")
        tabs.addTab(tab2,qtg.QIcon("icons/gas.png"), "Gas")
        tabs.addTab(tab3, qtg.QIcon("icons/check-list.png"), "Checklist")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance', 'gas'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error


class Maintenance(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        # Create first tab
        self.createTable()
        
        # setup the overall layout
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        top_layout = qtw.QHBoxLayout()
        bottom_layout = qtw.QHBoxLayout()
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
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
        calculate_cost = qtw.QPushButton('Calculate Cost')
        calculate_cost.clicked.connect(self.calculateCost)
        calculate_cost.setIcon(qtg.QIcon("icons/calc.png"))
        bottom_layout.addWidget(calculate_cost)
        bottom_layout.addStretch()
                
        # Set the overall layout
        layout.addWidget(title, qtc.Qt.AlignLeft)
        layout.addLayout(top_layout)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)
        
    def calculateCost(self):
        result = 0
        query = QSqlQuery("SELECT Cost FROM maintenance")
        while query.next():
            result = result + query.value(0)
        totalCost =str("%.2f" % (result))
                
        qtw.QMessageBox.about(self, 'Total Cost',
            'The Total Maintenance Cost is: \n$' + totalCost)
        
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
        self.createTable()
        
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        bottom_layout = qtw.QHBoxLayout()
        
        add_row = qtw.QPushButton("Add Row")
        add_row.setIcon(qtg.QIcon("icons/add_row.png"))
        add_row.setStyleSheet("padding: 6px")
        add_row.clicked.connect(self.addRow)
        
        del_row = qtw.QPushButton("Delete Row")
        del_row.setIcon(qtg.QIcon("icons/del_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteRow)
        
        fuel_gauge = qtg.QPixmap("images/fuel_gauge_round.png")
        fuel_gauge_label = qtw.QLabel()
        fuel_gauge_label.setPixmap(fuel_gauge)
        
        # Setting up the user actions for the car log tracker 
        title = qtw.QLabel("Gas Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        # Setting up the top layout, gonna have to layer this to get
        #the gas gauge image to show properly
        top_layout = qtw.QHBoxLayout()
        top_left_layout = qtw.QVBoxLayout()
        top_left_inner_layout = qtw.QHBoxLayout()
        top_right_layout = qtw.QHBoxLayout()
        top_left_inner_layout.addWidget(add_row)
        top_left_inner_layout.addWidget(del_row)
        top_left_layout.addWidget(title)
        top_left_layout.addLayout(top_left_inner_layout)
        top_right_layout.addStretch()
        top_right_layout.addWidget(fuel_gauge_label)
        top_right_layout.addStretch()
        top_layout.addLayout(top_left_layout)
        top_layout.addLayout(top_right_layout)
                
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        # Calculate the total cost of the maintenance performed by adding the results in the costs column
        calculate_fuel = qtw.QPushButton('Last Fuel Economy')
        calculate_fuel.clicked.connect(self.calculateFuelEcon)
        calculate_fuel.setIcon(qtg.QIcon("icons/calc.png"))
        
        calculate_total_fuel = qtw.QPushButton('Total Fuel Economy')
        calculate_total_fuel.clicked.connect(self.calculateTotalFuelEcon)
        calculate_total_fuel.setIcon(qtg.QIcon("icons/calc.png"))
        
        gas_graph = qtw.QPushButton('Graph Gas')
        gas_graph.clicked.connect(self.gasGraph)
        gas_graph.setIcon(qtg.QIcon("icons/graphs.png"))
        
        bottom_layout.addWidget(calculate_fuel)
        bottom_layout.addWidget(calculate_total_fuel)
        bottom_layout.addStretch()
        bottom_layout.addWidget(gas_graph)
        bottom_layout.addStretch()
        
        # Set the overall layout
        layout.addLayout(top_layout)
        layout.addWidget(self.table_view)
        layout.addLayout(bottom_layout)
        
    def calculateFuelEcon(self):
        gasQuery = QSqlQuery("SELECT Gallons FROM gas")
        while gasQuery.next():
            gasUsed = int(gasQuery.value(0))
        mileQuery = QSqlQuery("SELECT Odometer_Reading FROM gas")
        while mileQuery.next():
            mileUsed = int(mileQuery.value(0))
        mpg = ("%.2f" % (mileUsed/gasUsed))
        
        qtw.QMessageBox.about(self, 'Fuel Economoy',
            'The Fuel Econmy from last fill up is: \n' + mpg + ' mpg')
        
    def calculateTotalFuelEcon(self):
        gasUsed = 0
        mileUsed = 0
        gasQuery = QSqlQuery("SELECT Gallons FROM gas")
        while gasQuery.next():
            gasUsed = gasUsed + int(gasQuery.value(0))
        mileQuery = QSqlQuery("SELECT Odometer_Reading FROM gas")
        while mileQuery.next():
            mileUsed = mileUsed + int(mileQuery.value(0))
        mpg = ("%.2f" % (mileUsed/gasUsed))
        qtw.QMessageBox.about(self, 'Fuel Econmoy',
            'The Overall Fuel Economy is: \n' + mpg + ' mpg')
    
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
        
    def gasGraph(self):
        graph = GasGraph(self)
        graph.resize(350, 350)
        graph.show()
        
        
class CheckList(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        top_layout = qtw.QVBoxLayout()
        
        title = qtw.QLabel("Maintenance Checklist")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        text = "While performing regular maintenance, there are several things\n" \
               "to consider when maintaining your vehicle. First, you should not\n" \
                "only keep up on it regularly so it doesn't break down or cause\n" \
                "serious issues down the road, but you might also find way of\n" \
                "improving your vehicle's overall performance as well as maintianing\n" \
                "if not improving fuel economyat the same time. This checklist covers\n" \
                "all the major items you need to be mindful of as you continue to\n" \
                "to take care of your vehicle while you put miles on it."
        language = qtw.QLabel(text)
        language.setFont(qtg.QFont('Arial', 11))
        
        top_layout.addWidget(title)
        top_layout.addWidget(language)
        
        bottom_layout_right = qtw.QVBoxLayout()
        bottom_layout_left = qtw.QVBoxLayout()
        
        oil_button = qtw.QCheckBox         ("Oil - Synthetic oils can go further than conventional oils, also consider\n" \
                                            "premium brand oils to reduce wear and friction")
        hoses_button = qtw.QCheckBox       ("Hoses -  Check your hoses at the clamps for integrity and brittleness")
        belts_button = qtw.QCheckBox       ("Belts - Belts need to be checked before being replaced at 150,000 miles")
        tp_button = qtw.QCheckBox          ("Tire Pressure - By maintaining proper inflation levels will ensure maximum\n" \
                                           "performance. Never settle and buy cheap tires")
        coolent_button = qtw.QCheckBox     ("Coolent - At 30,000 miles the levels and integrity should be checked")
        air_filter_button = qtw.QCheckBox  ("Air Filter - Stock filters are paper, and replacing it with an aftermarket \n" \
                                            "panel filter can allow your engine to breathe better")
        brake_system_button = qtw.QCheckBox("Braking - Check brakes annualy yearly, in addition to rotors and \n" \
                                            "brake fluid")
        spark_plug_button = qtw.QCheckBox  ("Spark Plugs - Spark plugs should be checked every 30,000 miles, and if\n" \
                                            " your engine is supercharged, they should be checked yearly")
        battery_button = qtw.QCheckBox     ("Battery -  Check battery connections and clean if necessary")
        shocks_button = qtw.QCheckBox      ("Shocks & Struts—For hard drivers, shocks and struts should be checked at \n" \
                                           "80,000 miles at most")
        
        wrench = qtg.QPixmap("images/wrench_2.png")
        wrench_label = qtw.QLabel()
        wrench_label.setPixmap(wrench)
        
        #bottom_layout_left.addStretch()
        bottom_layout_right.addWidget(wrench_label)
        
        bottom_layout_left.addWidget(oil_button)
        bottom_layout_left.addWidget(hoses_button)
        bottom_layout_left.addWidget(belts_button)
        bottom_layout_left.addWidget(tp_button)
        bottom_layout_left.addWidget(coolent_button)
        bottom_layout_left.addWidget(air_filter_button)
        bottom_layout_left.addWidget(brake_system_button)
        bottom_layout_left.addWidget(spark_plug_button)
        bottom_layout_left.addWidget(battery_button)
        bottom_layout_left.addWidget(shocks_button)
        
        bottom_layout = qtw.QHBoxLayout()
        bottom_layout.addLayout(bottom_layout_left)
        bottom_layout.addLayout(bottom_layout_right)

        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        
    
class GasGraph(qtw.QDialog):
            
    def __init__(self, parent):
        super().__init__(parent)
        
        price = []
        query = QSqlQuery("SELECT Cost FROM gas")
        while query.next():
            price.append(query.value(0))
            
        date = []
        query = QSqlQuery("SELECT Date FROM gas")
        while query.next():
            date.append(query.value(0))

        self.layout = qtw.QVBoxLayout()
        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(NavigationToolbar(self.static_canvas, self))

        self._static_ax = self.static_canvas.figure.subplots()
        self._static_ax.plot(price)
        
        title = qtw.QLabel('Gas Prices')
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        exitButton = qtw.QPushButton('Close Window', self)
        exitButton.clicked.connect(self.close)
        
        self.layout.addWidget(title)
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(exitButton)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())