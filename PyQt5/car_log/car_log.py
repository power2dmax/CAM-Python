# car_log.py
"""
Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite.
The user can enter the date, millage, and the maintence performed.
The user will also be able to delete a row
"""

import sys, csv

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts

class MainWindow(qtw.QMainWindow):
    """
    Main Window constructor
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My Car Log App")
        self.setMinimumSize(qtc.QSize(500, 600))

        #self.createConnection()
        self.createMenu()

        self.car_log_tracker()
        
    def createConnection(self):
        database = qts.QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("files/car_log.db")
    
        if not database.open():
            print ("Unable to open data source file")
            sys.exit(1) # Error code 1 - signifies error
            
        # Check if the tables we need exist in the database
        tables_needed = {'maintenance'}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error',
                f'The following tables are missing from the database:{tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
    def createMenu(self):
        # Create the actions for the "File" menu
        #save_action
        save_action = qtw.QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        #exit_action.triggered.connect(self.close)
        
        self.exit_action = qtw.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)
        
        # Create the actions for the "Edit Menu"
        self.add_action = qtw.QAction('Add', self)
        self.add_action.setShortcut('Ctrl+A')
        self.add_action.triggered.connect(self.add_entry)
        
        self.del_action = qtw.QAction('Delete', self)
        self.del_action.setShortcut('Ctrl+D')
        self.del_action.triggered.connect(self.delete_entry)
        
        # Create actions for the "Help Menu" menu
        about_action = qtw.QAction('About', self)
        #about_action.triggered.connect(self.close)
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
        # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(save_action)
        file_menu.addAction(self.exit_action)
        
        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.add_action)
        edit_menu.addAction(self.del_action)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(about_action)
        
       
    def car_log_tracker(self):
        """
        Create instances of widgets, the table view and set layouts
        """
        icons_path = "images/icons"
        
        title = qtw.QLabel("Car Maintenance Log")
        title.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        
        add_record_button = qtw.QPushButton("Add Maintenance")
        #add_record_button.setIcon(qtw.QIcon(os.path.join(icons_path, "add_user.png")))
        add_record_button.setStyleSheet("padding: 10px")
        #add_record_button.clicked.connect(self.addRecord)
        
        del_record_button = qtw.QPushButton("Delete")
        #del_record_button.setIcon(qtw.QIcon(os.path.join(icons_path, "del_user.png")))
        del_record_button.setStyleSheet("padding: 10px")
        #del_record_button.clicked.connect(self.deleteRecord)
        
        exit_button = qtw.QPushButton('Exit', self)
        exit_button.setStyleSheet("padding: 10px")
        exit_button.clicked.connect(self.close) 
        
        # Set up the sorting combo box
        sorting_options = ["Date", "Mileage", "Action"]
        sort_name_cb = qtw.QComboBox()
        sort_name_cb.addItems(sorting_options)
        #sort_name_cb.currentTextChanged.connect(self.setSortingOrder)
        
        buttons_h_box = qtw.QHBoxLayout()
        buttons_h_box.addWidget(add_record_button)
        buttons_h_box.addWidget(del_record_button)
        buttons_h_box.addWidget(exit_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_name_cb)
        
        # Widget to contain editing buttons
        edit_buttons = qtw.QWidget()
        edit_buttons.setLayout(buttons_h_box)
        
        self.model = qtg.QStandardItemModel()
        
        self.table_view = qtw.QTableView()
        self.table_view.SelectionMode(3)
        self.table_view.setModel(self.model)
        
        self.model.setRowCount(12)
        self.model.setColumnCount(2)
        
        self.loadCSVFile()
        
               
        # Main Layout
        main_v_box = qtw.QVBoxLayout()
        main_v_box.addWidget(title, qtc.Qt.AlignLeft)
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)       
        widget = qtw.QWidget()
        widget.setLayout(main_v_box)
        self.setCentralWidget(widget)
        
        
    def add_entry(self):
        pass
    
    def delete_entry(self):
        pass
    
    def loadCSVFile(self):
        """
        Load the headers and rows from the car_log csv file
        Items will be constructed before asdding them to the table
        """
        file_name = "files/car_log.csv"
        
        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            self.model.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(csv.reader(csv_f)):
                items = [qtg.QStandardItem(item) for item in row]
                self.model.insertRow(i, items)
    
    
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())