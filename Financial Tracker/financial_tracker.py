# financial_tracker.py
"""
Fincancial tracker; multiple tabs that allwos the user to track their various
accounts. Development will focus on one area at a time and build out the
functioanlity. Develpment is as follows:
 - Mortgage Tracking - Allows the user to track their mortgage. Total loan amount,
 total princple paid to date, total interest paid to date.
"""
import sys
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlQuery
import pyqtgraph as pg
from pyqtgraph.dockarea import *


class DateDelegate(qtw.QStyledItemDelegate):

    def createEditor(self, parent, proxyModelIndex):
        date_inp = qtw.QDateEdit(parent, calendarPopup=True)
        d = qtc.QDate.currentDate()
        date_inp.setDate(d)
        return date_inp
    

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Financial Tracker')
        self.setWindowIcon(qtg.QIcon("icons/cam_3.png"))
        self.resize(1175, 700)
        
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
        #tabs.resize(300,200)
        
        # Add tabs
        #tabs.addTab(tab1, qtg.QIcon("icons/cash.png"), "Dashboard")
        #tabs.addTab(tab2,qtg.QIcon("icons/cash.png"), "Checking")
        #tabs.addTab(tab3, qtg.QIcon("icons/cash.png"), "Savings")
        #tabs.addTab(tab4, qtg.QIcon("icons/cash.png"), "Retirement")
        tabs.addTab(tab5, qtg.QIcon("icons/house.png"), "Mortgage")
        
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
    
    def __init__(self, parent, *args, **kwargs):
        super(qtw.QWidget, self).__init__(parent, *args, **kwargs)
        
        self.createTable()
        
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        
        # Set up the variables
        loan_amount = float("{:.2f}" .format(500000.00))
        est_value = int(650000)
        total_interest_loan = float("{:.2f}" .format(466278.92))
        
        left_layout = qtw.QVBoxLayout()
        left_top_layout = qtw.QGridLayout()
        left_bottom_layout = qtw.QHBoxLayout()
        right_layout = qtw.QVBoxLayout()
        
        # Put together the data that will be needed for creating the graphs and charts
        balance = []
        query = QSqlQuery("SELECT Balance FROM mortgage")
        while query.next():
            balance.append(query.value(0))
            
        amortization = []
        query = QSqlQuery("SELECT Principle FROM amortization")
        while query.next():
            amortization.append(query.value(0))
            
        total_additional = 0
        query = QSqlQuery("SELECT Additional_Payment FROM mortgage")
        while query.next():
            total_additional = total_additional + query.value(0)
        
        total_principle = 0
        query = QSqlQuery("SELECT Principle FROM mortgage")
        while query.next():
            total_principle = total_principle + query.value(0)
        totalPrinciple = float("%.2f" % (total_additional + total_principle))
        
        total_interest = 0
        query = QSqlQuery("SELECT Interest FROM mortgage")
        while query.next():
            total_interest = total_interest + query.value(0)
        totalInterest = float("%.2f" % (total_interest))
        
        balanceQuery = QSqlQuery("SELECT Balance FROM mortgage")
        while balanceQuery.next():
            balanceFinal = (balanceQuery.value(0))
        
        title = qtw.QLabel("Mortgage")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        loan_amount_label = qtw.QLabel("Loan Amount:")
        loan_amount_label.setFont(qtg.QFont('Arial', 10))
        loan_amount_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(loan_amount)))
        
        loan_years_label = qtw.QLabel("Loan Years:")
        loan_years_label.setFont(qtg.QFont('Arial', 10))
        loan_years_text = qtw.QLineEdit(str(30))
        
        interest_rate_label = qtw.QLabel("Interest Rate:")
        interest_rate_label.setFont(qtg.QFont('Arial', 10))
        interest_rate_text = qtw.QLineEdit(str(4))
                
        balance_label = qtw.QLabel("Current Balance:")
        balance_label.setFont(qtg.QFont('Arial', 10))
        balance_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(balanceFinal)))
        
        value_label = qtw.QLabel("Current Value:")
        value_label.setFont(qtg.QFont('Arial', 10))
        value_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(est_value)))
        
        difference = est_value - int(balanceFinal)
        diff_label = qtw.QLabel("Difference:")
        diff_label.setFont(qtg.QFont('Arial', 10))
        diff_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(difference)))
        diff_text.setStyleSheet("""
            QLineEdit {
            background-color: green;
            color: white
            }
            """)
        
        total_principle_label = qtw.QLabel("Total Principle Paid:")
        total_principle_label.setFont(qtg.QFont('Arial', 10))
        total_principle_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(totalPrinciple)))
        
        total_interest_label = qtw.QLabel("Total Interest Paid:")
        total_interest_label.setFont(qtg.QFont('Arial', 10))
        total_interest_text = qtw.QLineEdit(str("$ " + "{:.2f}".format(totalInterest)))
        
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
        del_row.setIcon(qtg.QIcon("icons/delete_row.png"))
        del_row.setStyleSheet("padding: 6px")
        del_row.clicked.connect(self.deleteMessage)
        
        totals_button = qtw.QPushButton("Totals")
        totals_button.setIcon(qtg.QIcon("icons/totals.png"))
        totals_button.setStyleSheet("padding: 6px")
        totals_button.clicked.connect(self.totals)
        
        update_data_button = qtw.QPushButton("Update Data")
        update_data_button.setIcon(qtg.QIcon("icons/update.png"))
        update_data_button.setStyleSheet("padding: 6px")
        update_data_button.clicked.connect(self.updateData)
        #payment_calc.triggered.connect(self.payCalc)

        left_top_layout.addWidget(title, 0, 0)
        left_top_layout.addWidget(update_data_button, 0, 2)
        left_top_layout.addWidget(loan_amount_label, 1, 0)
        left_top_layout.addWidget(loan_amount_text, 2, 0)
        left_top_layout.addWidget(loan_years_label, 1, 1 )
        left_top_layout.addWidget(loan_years_text, 2, 1)
        left_top_layout.addWidget(interest_rate_label, 1, 2)
        left_top_layout.addWidget(interest_rate_text, 2, 2)
        left_top_layout.addWidget(balance_label, 1, 3)
        left_top_layout.addWidget(balance_text, 2, 3)
        left_top_layout.addWidget(value_label, 3, 0)
        left_top_layout.addWidget(value_text, 4, 0)
        left_top_layout.addWidget(diff_label, 3, 1)
        left_top_layout.addWidget(diff_text, 4, 1)
        left_top_layout.addWidget(total_principle_label, 3, 2)
        left_top_layout.addWidget(total_principle_text, 4, 2)
        left_top_layout.addWidget(total_interest_label, 3, 3)
        left_top_layout.addWidget(total_interest_text, 4, 3)
               
        left_bottom_layout.addWidget(add_row)
        left_bottom_layout.addWidget(del_row)
        left_bottom_layout.addStretch()
        left_bottom_layout.addWidget(totals_button)
        left_bottom_layout.addStretch()
        
        #left_layout.addWidget(title)
        left_layout.addLayout(left_top_layout)
        left_layout.addWidget(self.table_view)
        left_layout.addLayout(left_bottom_layout)

        # Set up the graph area on the left using pyqtgrapgh's Docks
        area = DockArea()
        d1 = Dock("Dock1", size=(350, 350))
        d2 = Dock("Dock2", size=(350, 350))
        area.addDock(d1, 'top')
        area.addDock(d2, 'bottom')
             
        # Set up the Line Graph for Mortgage balance vs the amortization
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('floralwhite')
        pen1 = pg.mkPen(color=('#0c3d9c'), width=2)
        pen2 = pg.mkPen(color=('#9c290c'), width=2)
        self.graphWidget.setTitle("Mortgage Balance vs Amortization", color='black', font='bold', size="20pt")
        self.graphWidget.setLabel('left', 'Current Balance')
        self.graphWidget.setLabel('bottom', 'Number of Payments')
        self.graphWidget.setXRange(0, 360, padding=0)
        self.graphWidget.setYRange(0, loan_amount, padding=0)
        
        self.graphWidget.plot(balance, pen=pen1)
        self.graphWidget.plot(amortization, pen=pen2)

        window = pg.PlotWidget()
        x = np.arange(1)
        y1 = loan_amount
        y2 = totalPrinciple
        y3 = totalInterest
        y4 = total_interest_loan
        
        b1 = pg.BarGraphItem(x=x-0.75, height = y1, width=0.35, brush='#1a4582')
        b2 = pg.BarGraphItem(x=x-0.25, height = y2, width=0.35, brush='#396099')
        b3 = pg.BarGraphItem(x=x+0.25, height = y3, width=0.35, brush='#d1722e')
        b4 = pg.BarGraphItem(x=x+0.75, height = y4, width=0.35, brush='#873f0c')
        
        # Add the labels to the bar braphs
        text_bg1 = pg.TextItem("Loan Amount \n$ " +
                str(loan_amount), border='w', color='w',
                fill=('#1a4582'), anchor=(-0.2,1.5))
        window.addItem(text_bg1)
        text_bg1.setPos(-.75, y1)
        arrow1 = pg.ArrowItem(pos=(-.75, y1), angle=-45)
        window.addItem(arrow1)
        
        text_bg2 = pg.TextItem("Total Principle Paid\n$ " +
                str(totalPrinciple), border='w', color='w',
                fill=('#396099'), anchor=(0.5,1.65))
        window.addItem(text_bg2)
        text_bg2.setPos(-.25, y2)
        arrow2 = pg.ArrowItem(pos=(-.25, y2), angle=-90)
        window.addItem(arrow2)

        text_bg3 = pg.TextItem("Total Interest Paid\n$ " +
                str(totalInterest), border='w', color='w',
                fill=('#d1722e'), anchor=(-0.9,1.65))
        window.addItem(text_bg3)
        text_bg3.setPos(-.25, y3)
        arrow3 = pg.ArrowItem(pos=(0.25, y3), angle=-90)
        window.addItem(arrow3)
        
        text_bg4 = pg.TextItem("Total Interest on\n life of the Loan\n$ " +
                str(total_interest_loan), border='w', color='w',
                fill=('#873f0c'), anchor=(-1.9,1.35))
        window.addItem(text_bg4)
        text_bg4.setPos(-.25, y4)
        arrow4 = pg.ArrowItem(pos=(0.75, y4), angle=-135)
        window.addItem(arrow4)
        
        window.addItem(b1)
        window.addItem(b2)
        window.addItem(b3)
        window.addItem(b4)
        window.setBackground('floralwhite')
        window.setTitle("Totals", color='black', font='bold', size="20pt")

        right_layout.addWidget(area)
        d1.addWidget(self.graphWidget)
        d2.addWidget(window)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        
    def deleteMessage(self):
        message = qtw.QMessageBox.question(self, 'Delete',
            'This will perminatly delete the highlighted row(s). \n'
            'The data will not be able to be retrived again. \n'
            'Are you sure you want to delete?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            self.deleteRow()
        
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
        
    def totals(self):
        """
        Populate the totals pop-up window when the button is pushed
        """
        total_additional = 0
        query = QSqlQuery("SELECT Additional_Payment FROM mortgage")
        while query.next():
            total_additional = total_additional + query.value(0)
        
        total_principle = 0
        query = QSqlQuery("SELECT Principle FROM mortgage")
        while query.next():
            total_principle = total_principle + query.value(0)
        
        totalPrinciple = str("%.2f" % (total_additional + total_principle))
        
        total_interest = 0
        query = QSqlQuery("SELECT Interest FROM mortgage")
        while query.next():
            total_interest = total_interest + query.value(0)
        totalInterest =str("%.2f" % (total_interest))
        
        total_escrow = 0
        query = QSqlQuery("SELECT Escrow FROM mortgage")
        while query.next():
            total_escrow = total_escrow + query.value(0)
        totalEscrow =str("%.2f" % (total_escrow))
        
        qtw.QMessageBox.about(self, 'Total Costs',                 
            '\nThe Total Principle Paid is: $ ' + totalPrinciple +
            '\nThe Total in Interest Paid is: $ ' + totalInterest +
            '\nThe Total in Escrow Paid is: $ ' + totalEscrow)
        
    def updateData(self):
        update = MortgageUpdates(self)
        update.resize(350, 350)
        update.show()
        
        
class MortgageUpdates(qtw.QDialog):
                
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Update data')
        self.createTable()
        
        layout = qtw.QHBoxLayout()
        self.setLayout(layout) 
        
        self.table_view = qtw.QTableView()
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.table_view.setModel(self.model)
        header.setStretchLastSection(True)
        #self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        #self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows + qtw.QTableView.SelectColumns)
                
        # Populate the model with data
        self.model.select()
        
        layout.addWidget(self.table_view)
    
    
    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        self.model.setTable('loan_data')
        self.model.setHeaderData(self.model.fieldIndex('loan_amount'), qtc.Qt.Horizontal, "Loan Amount")
        self.model.setHeaderData(self.model.fieldIndex('loan_years'), qtc.Qt.Horizontal, "Loan Years")
        self.model.setHeaderData(self.model.fieldIndex('interest_rate'), qtc.Qt.Horizontal, "Interest Rate")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())