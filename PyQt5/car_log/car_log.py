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

class MainWindow(qtw.QMainWindow):
    """
    Main Window constructor
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My Car Log App")
        self.setMinimumSize(qtc.QSize(500, 600))

        self.createMenu()
        self.createToolBar()
        self.car_log_tracker()
        
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
        
    def createToolBar(self):
        """
        Create toolbar for the GUI
        """
        # Set up the toolbar
        tool_bar = qtw.QToolBar("Main ToolBar")
        self.addToolBar(qtc.Qt.BottomToolBarArea, tool_bar)
        
        # Add actrions to the toolbar
        #tool_bar.addAction(self.add_action)
        #tool_bar.addSeparator()
        #tool_bar.addAction(self.del_action)
        #tool_bar.addSeparator()
        tool_bar.addAction(self.exit_action)
        
    def car_log_tracker(self):
        """
        Set up the standard item model and table view
        """
        self.model = qtg.QStandardItemModel()
        
        self.table_view = qtw.QTableView()
        self.table_view.SelectionMode(3)
        self.table_view.setModel(self.model)
        
        self.model.setRowCount(12)
        self.model.setColumnCount(2)
        
        self.loadCSVFile()
        
        self.setCentralWidget(self.table_view)
        
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