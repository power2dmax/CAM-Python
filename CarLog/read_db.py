# read_car_log_db.py
import os, sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts

class TableDisplay(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setMinimumSize(1000, 500)
        self.setWindowTitle('SQL Table Model')

        self.createConnection()
        self.createTable()

        self.show()
        
    def createConnection(self):
        database = qts.QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("files/car_log.db")
        
        if not database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error
            
        tables_needed = {'contacts'}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(None, 'Error',
                f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 – signifies error
    
    
    def createTable(self):
        model = qts.QSqlTableModel()
        model.setTable('contacts')

        table_view = qtw.QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)

        # Populate the model with data
        model.select()

        # Main layout
        main_v_box = qtw.QVBoxLayout()
        main_v_box.addWidget(table_view)
        self.setLayout(main_v_box)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = TableDisplay()
    sys.exit(app.exec_())