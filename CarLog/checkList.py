import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class CheckList(qtw.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initializeUI()
    

    def initializeUI(self):
        
        self.resize(500, 600)
        
        self.createConnection()
        self.main_window()
        self.show()    
        
    def main_window(self):
        
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        top_layout = qtw.QHBoxLayout()
        bottom_layout = qtw.QVBoxLayout()
        
        make_label = qtw.QLabel('Make')
        model_label = qtw.QLabel('Model')
        
        oil_button = qtw.QCheckBox("Oil - Make sure the oil is toped off using the manufacture recomend weight")
        hoses_button = qtw.QCheckBox("Hoses")
        belts_button = qtw.QCheckBox("Belts")
        tp_button = qtw.QCheckBox("Tire Pressure")
        coolent_button = qtw.QCheckBox("Coolent")
        air_filter_button = qtw.QCheckBox("Air Filter")
        brake_system_button = qtw.QCheckBox("Braking System")
        battery_button = qtw.QCheckBox("Battery")
        
        
        top_layout.addWidget(make_label)
        bottom_layout.addWidget(oil_button)
        bottom_layout.addWidget(hoses_button)
        bottom_layout.addWidget(belts_button)
        bottom_layout.addWidget(tp_button)
        bottom_layout.addWidget(coolent_button)
        bottom_layout.addWidget(air_filter_button)
        bottom_layout.addWidget(brake_system_button)
        bottom_layout.addWidget(battery_button)
        
        
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        
        
        
        
        
        
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance', 'gas', 'car'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = CheckList()
    sys.exit(app.exec_())