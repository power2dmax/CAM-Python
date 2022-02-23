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
        self.createCarTable()
        self.createContactTable()
        self.main_window()
        self.show()    
        
    def main_window(self):
        
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)
        top_layout = qtw.QHBoxLayout()
        
        bottom_layout_right = qtw.QVBoxLayout()
        bottom_layout_left = qtw.QVBoxLayout()
        
        
        
        oil_button = qtw.QCheckBox("Oil")
        hoses_button = qtw.QCheckBox("Hoses")
        belts_button = qtw.QCheckBox("Belts")
        tp_button = qtw.QCheckBox("Tire Pressure")
        coolent_button = qtw.QCheckBox("Coolent")
        air_filter_button = qtw.QCheckBox("Air Filter")
        brake_system_button = qtw.QCheckBox("Braking System")
        battery_button = qtw.QCheckBox("Battery")
        
        wrench = qtg.QPixmap("images/wrench.png")
        wrench_label = qtw.QLabel()
        wrench_label.setPixmap(wrench)
        
        bottom_layout_left.addStretch()
        bottom_layout_left.addWidget(wrench_label)
        
        bottom_layout_right.addWidget(oil_button)
        bottom_layout_right.addWidget(hoses_button)
        bottom_layout_right.addWidget(belts_button)
        bottom_layout_right.addWidget(tp_button)
        bottom_layout_right.addWidget(coolent_button)
        bottom_layout_right.addWidget(air_filter_button)
        bottom_layout_right.addWidget(brake_system_button)
        bottom_layout_right.addWidget(battery_button)
        
        
        # Create table view and set model
        self.car_table_view = qtw.QTableView()
        header = self.car_table_view.horizontalHeader()
        self.car_table_view.setModel(self.model)
        header.setStretchLastSection(True)
        self.car_table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.car_table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        self.contact_table_view = qtw.QTableView()
        header = self.contact_table_view.horizontalHeader()
        self.contact_table_view.setModel(self.model_1)
        header.setStretchLastSection(True)
        self.contact_table_view.setSelectionMode(qtw.QTableView.SingleSelection)
        self.contact_table_view.setSelectionBehavior(qtw.QTableView.SelectRows)
        
        bottom_layout = qtw.QHBoxLayout()
        
        bottom_layout.addLayout(bottom_layout_left)
        bottom_layout.addLayout(bottom_layout_right)

        layout.addLayout(top_layout)
        layout.addWidget(self.car_table_view)
        layout.addWidget(self.contact_table_view)
        layout.addLayout(bottom_layout)
        
    def createCarTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model = qts.QSqlRelationalTableModel()
        
        self.model.setTable('car')
        self.model.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('Make'), qtc.Qt.Horizontal, "Make")
        self.model.setHeaderData(self.model.fieldIndex('Model'), qtc.Qt.Horizontal, "Model")
        self.model.setHeaderData(self.model.fieldIndex('Year'), qtc.Qt.Horizontal, "Year")
        
        
        # Populate the model with data
        self.model.select()     
        
    def createContactTable(self):
        """
        Set up the model, headers and populate the model.
        """
        self.model_1 = qts.QSqlRelationalTableModel()
        
        self.model_1.setTable('contacts')
        self.model_1.setHeaderData(self.model.fieldIndex('id'), qtc.Qt.Horizontal, "ID")
        self.model_1.setHeaderData(self.model.fieldIndex('Location'), qtc.Qt.Horizontal, "Location")
        self.model_1.setHeaderData(self.model.fieldIndex('POC'), qtc.Qt.Horizontal, "POC")
        self.model_1.setHeaderData(self.model.fieldIndex('Number'), qtc.Qt.Horizontal, "Number")
        
        
        # Populate the model with data
        self.model_1.select()     
        
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/car_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'maintenance', 'gas', 'car', 'contacts'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error
        
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = CheckList()
    sys.exit(app.exec_())