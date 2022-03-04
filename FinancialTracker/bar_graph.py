import sys
import time

import numpy as np

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtChart as qtch
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from pyqtgraph.dockarea import *


from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PlotGraph(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(600, 100, 450, 400)
        self.createConnection()
        layout = qtw.QVBoxLayout()
        self.show()
        
        
        loan_amount = 185000
        payment_months = 360
        interest_rate = 3.5 / 100
        
        total_payments = 79679.56
        total_principle = 40607.21
        total_interest = 33382.01
        
        window = pg.plot()
        
        x = [1, 2, 3]
        y = [total_payments, total_principle, total_interest]
        
        bargraph = pg.BarGraphItem(x=x, height = y, width=0.5, brush='g')
        
        window.addItem(bargraph)

        
        layout.addWidget(window)
        self.setLayout(layout)
        
        
        
    def createConnection(self):
        self.database = qts.QSqlDatabase.addDatabase("QSQLITE") # SQLite version 3
        self.database.setDatabaseName("files/financial_log.db")

        if not self.database.open():
            print("Unable to open data source file.")
            sys.exit(1) # Error code 1 - signifies error

        # Check if the tables we need exist in the database
        tables_needed = {'mortgage'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            qtw.QMessageBox.critical(None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1) # Error code 1 - signifies error



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = PlotGraph()
    sys.exit(app.exec_())