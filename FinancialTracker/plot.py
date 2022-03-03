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
        
        balance = []
        query = QSqlQuery("SELECT Balance FROM mortgage")
        while query.next():
            balance.append(query.value(0))
            #print(x)
        
        loan_amount = 185000
        payment_months = 360
        interest_rate = 3.5 / 100
        


        
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('lightgray')
        pen = pg.mkPen(color=(0, 0, 0), width=2)
        self.graphWidget.setTitle("Mortgage Balance", color='w', size="20pt")
        self.graphWidget.setLabel('left', 'Current Balance')
        self.graphWidget.setLabel('bottom', 'Number of Payments')
        self.graphWidget.setXRange(0, 360, padding=0)
        self.graphWidget.setYRange(0, 190000, padding=0)
        
        total_principle = 185000
        current_principle = 40979.73
        current_interest = 33912.69
        total_interest = 114062

        
        area = DockArea()
        d1 = Dock("Dock1", size=(150, 150))
        area.addDock(d1, 'top')
        

        # plot data: x, y values
        self.graphWidget.plot(balance, pen=pen)
        
        layout.addWidget(area)
        d1.addWidget(self.graphWidget)
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