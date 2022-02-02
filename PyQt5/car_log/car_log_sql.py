# car_log_sql.py

"""

Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite for the data.
The user can enter the date, millage, and the maintenance performed.
The user will also have the capability to delete a row

"""


# Import necessary modules
import sys, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class AccountManager(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setMinimumSize(550, 600)
        self.setWindowTitle('Car Log GUI')

        self.createConnection()
        self.createTable()
        self.setupWidgets()

        self.show()

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
        self.model.setHeaderData(self.model.fieldIndex('Item'), qtc.Qt.Horizontal, "Item")
        
        # Populate the model with data
        self.model.select()

    def setupWidgets(self):
        """
        Create instances of widgets, the table view and set layouts.
        """
        
        self.exit_action = qtw.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("icons/exit.png"))
        self.exit_action.triggered.connect(self.exit_message)
        
        # Create the actions for the "Edit Menu"
        self.add_action = qtw.QAction('Add Row', self)
        self.add_action.setShortcut('Ctrl+A')
        self.add_action.setIcon(qtg.QIcon("icons/add_row.png"))
        self.add_action.triggered.connect(self.addRecord)
        
        self.del_action = qtw.QAction('Delete Row', self)
        self.del_action.setShortcut('Ctrl+D')
        self.del_action.setIcon(qtg.QIcon("icons/del_row.png"))
        self.del_action.triggered.connect(self.deleteRecord)
        
        # Create actions for the "Help Menu" menu
        about_action = qtw.QAction('About', self)
        about_action.setIcon(qtg.QIcon("icons/about.png"))
        about_action.triggered.connect(self.about_info)
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
        # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        
        file_menu.addAction(self.exit_action)
        
        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.add_action)
        edit_menu.addAction(self.del_action)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(about_action)
       
        title = qtw.QLabel("Car Maintenance Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
       
        add_record_button = qtw.QPushButton("Add Row")
        add_record_button.setIcon(qtg.QIcon("icons/add_row.png"))
        add_record_button.setStyleSheet("padding: 10px")
        add_record_button.clicked.connect(self.addRecord)
        
        del_record_button = qtw.QPushButton("Delete Row")
        del_record_button.setIcon(qtg.QIcon("icons/del_row.png"))
        del_record_button.setStyleSheet("padding: 10px")
        del_record_button.clicked.connect(self.deleteRecord)

        # Set up sorting combo box
        sorting_options = ["Sort by Date", "Sort by Mileage","Sort by Item"]
        sort_name_cb = qtw.QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)
        
        exit_button = qtw.QPushButton('Exit', self)
        exit_button.setIcon(qtg.QIcon("icons/exit.png"))
        exit_button.setStyleSheet("padding: 10px")
        exit_button.clicked.connect(self.exit_message) 
        
        buttons_h_box = qtw.QHBoxLayout()
        buttons_h_box.addWidget(add_record_button)
        buttons_h_box.addWidget(del_record_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_name_cb)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(exit_button)
                
        # Widget to contain editing buttons
        edit_buttons = qtw.QWidget()
        edit_buttons.setLayout(buttons_h_box)
        
        # Create table view and set model
        self.table_view = qtw.QTableView()
        self.header = self.table_view.horizontalHeader()
        
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
                       
        # Main Layout
        main_v_box = qtw.QVBoxLayout()
        main_v_box.addWidget(title, qtc.Qt.AlignLeft)
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)       
        widget = qtw.QWidget()
        widget.setLayout(main_v_box)
        self.setCentralWidget(widget)
        
    def saveRecord(self):
        pass
        database

    def addRecord(self):
        """
        Add a new record to the last row of the table.
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = qts.QSqlQuery()
        query.exec_("SELECT MAX (id) FROM maintenance")
        if query.next():
            id = int(query.value(0))

    def deleteRecord(self):
        """
        Delete an entire row from the table.
        """
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()

    def setSortingOrder(self, text):
        """
        Sort the rows in table.
        """
        if text == "Sort by Date":
            self.model.setSort(self.model.fieldIndex('Date'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Mileage":
            self.model.setSort(self.model.fieldIndex('Milage'), qtc.Qt.AscendingOrder)
        elif text == "Sort by Item":
            self.model.setSort(self.model.fieldIndex('Item'), qtc.Qt.AscendingOrder)
        
        self.model.select()
        
    def about_info(self):
        text_1 = "CAM's car log, written in Python \n"
        text_2 = "using PyQt5 modules for the GUI \n\n"
        text_3 = "Originally written: 1/27/22"
        
        qtw.QMessageBox.about(self, "CAM's Car Log", text_1 + text_2 + text_3)
        
    def exit_message(self):
        message = qtw.QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            self.database.close()
            self.close()
            
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = AccountManager()
    sys.exit(app.exec_())
