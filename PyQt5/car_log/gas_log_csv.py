# gas_log_csv.py
# Import necessary modules
import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

file_name = "files/gas.csv"

class CarGasLog(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        
        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen.
        """
        self.setMinimumSize(550, 600)
        self.setWindowTitle('Car Gas GUI')

        self.setupModelView()
        
        self.setupWidgets()

        self.show()


    def setupModelView(self):
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
        self.exit_action = qtw.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        
        self.save_action = qtw.QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save_data)
        
        # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.exit_action)
        
        
        self.model = qtg.QStandardItemModel()
        
        table_view = qtw.QTableView()
        table_view.SelectionMode(3)
        table_view.setModel(self.model)
        self.model.setRowCount(3)
        self.model.setColumnCount(3)
               
        self.loadCsvFile()
        
        self.setCentralWidget(table_view)
        
        

    def loadCsvFile(self):       
    
        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            self.model.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(csv.reader(csv_f)):
                items = [qtg.QStandardItem(item) for item in row]
                self.model.insertRow(i, items)

    def save_data(self):
        pass

    def setupWidgets(self):
        pass
        
    def addRecord(self):
        pass

    def deleteRecord(self):
        pass
        
    def aboutInfo(self):
        pass
    
    
    def exitMessage(self):
        message = qtw.QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            self.database.close()
            self.close()
            
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = CarGasLog()
    sys.exit(app.exec_())
