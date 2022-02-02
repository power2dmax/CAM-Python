# Import necessary modules
import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
    QPushButton, QComboBox, QTableView, QHeaderView,
    QHBoxLayout, QVBoxLayout, QSizePolicy, QMessageBox,
    QAction)
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery,
    QSqlRelationalTableModel, QSqlRelation,
    QSqlRelationalDelegate)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AccountManager(QWidget):

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
        database = QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        database.setDatabaseName("files/car_log.db")

        if not database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance'}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error

    def createTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = QSqlRelationalTableModel()
        self.model.setTable('maintenance')
        self.model.setHeaderData(self.model.fieldIndex('id'), Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Date'), Qt.Horizontal, "Date")
        self.model.setHeaderData(self.model.fieldIndex('Mileage'), Qt.Horizontal, "Mileage")
        self.model.setHeaderData(self.model.fieldIndex('Item'), Qt.Horizontal, "Item")
        
        # Populate the model with data
        self.model.select()

    def setupWidgets(self):
        """
        Create instances of widgets, the table view and set layouts.
        """
        title = QLabel("Car Maintenance Log")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")

        add_record_button = QPushButton("Add Maintenance")
        add_record_button.setIcon(QIcon("icons/add_row.png"))
        add_record_button.setStyleSheet("padding: 10px")
        add_record_button.clicked.connect(self.addRecord)

        del_record_button = QPushButton("Delete Record")
        del_record_button.setIcon(QIcon("icons/del_row.png"))
        del_record_button.setStyleSheet("padding: 10px")
        del_record_button.clicked.connect(self.deleteRecord)
        
        exit_button = QPushButton('Exit')
        exit_button.setIcon(QIcon("icons/exit.png"))
        exit_button.setStyleSheet("padding: 10px")
        exit_button.clicked.connect(self.exit_message)

        # Set up sorting combo box
        sorting_options = ["Sort by ID", "Sort by Date", "Sort by Mileage","Sort by Item"]
        sort_name_cb = QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)

        buttons_h_box = QHBoxLayout()
        buttons_h_box.addWidget(add_record_button)
        buttons_h_box.addWidget(del_record_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_name_cb)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(exit_button)

        # Widget to contain editing buttons
        edit_buttons = QWidget()
        edit_buttons.setLayout(buttons_h_box)

        # Create table view and set model
        self.table_view = QTableView()
        self.header = self.table_view.horizontalHeader()
        
        self.table_view.setModel(self.model)
        self.header.setStretchLastSection(True)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        # Instantiate the delegate
        delegate = QSqlRelationalDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        # Main layout
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(title, Qt.AlignLeft)
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def addRecord(self):
        """
        Add a new record to the last row of the table.
        """
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = QSqlQuery()
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
        if text == "Sort by ID":
            self.model.setSort(self.model.fieldIndex('id'),
            Qt.AscendingOrder)
        elif text == "Sort by Date":
            self.model.setSort(self.model.fieldIndex('Date'), Qt.AscendingOrder)
        elif text == "Sort by Mileage":
            self.model.setSort(self.model.fieldIndex('Milage'), Qt.AscendingOrder)
        elif text == "Sort by Item":
            self.model.setSort(self.model.fieldIndex('Item'), Qt.AscendingOrder)
        
        self.model.select()
        
    def exit_message(self):
        message = QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            QMessageBox.Yes | QMessageBox.No)
        if message == QMessageBox.Yes:
            self.close()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AccountManager()
    sys.exit(app.exec_())