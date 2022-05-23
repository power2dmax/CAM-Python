# address_book.py
"""
Python program for tracking cpontacts and address. The program uses
SQLite as the backend database that stores the user's data
"""

import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtSql as qts

class Model:
    def __init__(self):
        self.model = self.createModel()
        
    def createModel(self):
        """ Create and set up the model"""
        tableModel = qts.QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(qts.QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("Last Name", "First Name", "Home Address", "Phone Number",  "email Address")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, qtc.Qt.Horizontal, header)
        return tableModel
    
    def addContact(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()
        
    def deleteContact(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
    

class Window(qtw.QMainWindow):
    """ Setting up thr Main Window for the address book"""
    def __init__(self, parent=None):
        """ Initializer"""
        super().__init__(parent)
        
        self.setWindowTitle("Address Book")
        self.resize(475, 550)
        self.centralWidget = qtw.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = qtw.QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        if not self.createConnection("contacts.sqlite"):
            sys.exit(1)
        
        self.setupUI() 
        self.show()
        
    def setupUI(self):
        """ Setup the main window's layout and gui """
        self.contactsModel = Model()
        
        # Create the table view widget
        self.table = qtw.QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        
        self.title = qtw.QLabel("Address Book")
        
        # Create the buttons
        self.addButton = qtw.QPushButton("Add")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = qtw.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.exitButton = qtw.QPushButton("Exit", self)
        self.exitButton.clicked.connect(self.close)
        
        # Setup the GUI layout
        layout = qtw.QVBoxLayout()
        topLayout = qtw.QHBoxLayout()
        topLayout.addWidget(self.title)
        topLayout.addWidget(self.addButton)
        topLayout.addWidget(self.deleteButton)
        bottomLayout = qtw.QHBoxLayout()
        topLayout.addStretch()
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.exitButton)
        layout.addLayout(topLayout)
        layout.addWidget(self.table)
        layout.addLayout(bottomLayout)
        self.layout.addLayout(layout)
        
    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == qtw.QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()
            
    def deleteContact(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return
        
        messageBox = qtw.QMessageBox.question(self, 'Warning',
            'Do you want to delete the current contact?')
        
        if messageBox == QMessageBox.Yes:
            self.contactsModel.deleteContact(row)
    
    def createContactsTable(self):
        """ Create the contacts table in the database"""
        createTableQuery = qts.QSqlQuery()
        return createTableQuery.exec_("""CREATE TABLE IF NOT EXISTS contacts(
            name_last VARCHAR(25) NOT NULL,
            name_first VARCHAR(25) NOT NULL,
            address VARCHAR(35),
            phone VARCHAR(10),
            email VARCHAR(25) NOT NULL)""")

    def createConnection(self, databaseName):
        """ Create and open a database conmnection"""
        connection = qts.QSqlDatabase.addDatabase("QSQLITE")
        connection.setDatabaseName(databaseName)
    
        if not connection.open():
            qtw.QMessage.warning(None, "CAM Contact",
                f"Database Error: {connection.lastError().text()}")
            return False
    
        self.createContactsTable()
    
        return True
            
        
class AddDialog(qtw.QDialog):
    """ Pop-up window with dialog for adding the contacts"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add a Contact")
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        
        self.setupUI()
            
    def setupUI(self):
        self.lastName = qtw.QLineEdit()
        self.lastName.setObjectName("name_last")
        self.firstName = qtw.QLineEdit()
        self.firstName.setObjectName("name_last")
        self.address = qtw.QLineEdit()
        self.address.setObjectName("address")
        self.phone = qtw.QLineEdit()
        self.phone.setObjectName("phone")
        self.email = qtw.QLineEdit()
        self.email.setObjectName("email")
        
        layout = qtw.QFormLayout()
        layout.addRow("Last Name", self.lastName)
        layout.addRow("First Name", self.firstName)
        layout.addRow("Address", self.address)
        layout.addRow("Phone", self.phone)
        layout.addRow("email", self.email)
        self.layout.addLayout(layout)
        
        self.buttonsBox = qtw.QDialogButtonBox(self)
        self.buttonsBox.setOrientation(qtc.Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel
            )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)
        
    def accept(self):
        print("Last Name: ", self.lastName)
        self.data = []
        for field in (self.lastName, self.firstName, self.address, self.phone, self.email):
            if not field.text():
                qtw.QMessageBox.critical(self, "Warning:",
                    f"You must provide a contact's {field.objectName()}",)
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()


if __name__=="__main__":
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = Window()
    sys.exit(app.exec_())