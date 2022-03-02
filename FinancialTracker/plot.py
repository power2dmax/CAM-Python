import sys
import time

import numpy as np

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class GasGraph(qtw.QDialog):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(600, 100, 500, 600)
        self.createConnection()
        
        price = []
        query = QSqlQuery("SELECT Cost FROM gas")
        while query.next():
            price.append(query.value(0))
            
        date = []
        query = QSqlQuery("SELECT Date FROM gas")
        while query.next():
            date.append(query.value(0))
        
        #self._main = qtw.QWidget()
        #self.setCentralWidget(self._main)
        self.layout = qtw.QVBoxLayout()

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.layout.addWidget(NavigationToolbar(self.static_canvas, self))
        

        self._static_ax = self.static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(price)
        
        self.layout.addWidget(self.static_canvas)
        self.setLayout(self.layout)
        
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



if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = qtw.QApplication.instance()
    if not qapp:
        qapp = qtw.QApplication(sys.argv)

    app = GasGraph()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()