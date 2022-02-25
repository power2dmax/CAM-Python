import sys, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtChart as qtch
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Graph(qtw.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setGeometry(600, 100, 500, 600)
        self.createConnection()
        self.main_window()
        self.show()    
        
    def main_window(self):
       
        price = []
        query = QSqlQuery("SELECT Cost FROM gas")
        while query.next():
            price.append(query.value(0))
            
        date = []
        query = QSqlQuery("SELECT Date FROM gas")
        while query.next():
            date.append(query.value(0))
            
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(price)
        self.setCentralWidget(sc)
        
        toolbar = NavigationToolbar(sc, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        
        widget = qtw.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()
        
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
    #windows_style = qtw.QStyleFactory.create('Windows')
    #app.setStyle(windows_style)
    window = Graph()
    sys.exit(app.exec_())