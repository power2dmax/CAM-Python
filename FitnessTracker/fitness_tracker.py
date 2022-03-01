# fitness_tracker.py
"""

"""

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Fitness Tracker')
        self.resize(1000, 750)
        
        self.menuWidget()
        self.mainWindow = MainWindow(self)
        self.setCentralWidget(self.mainWindow)
                
        
        self.show()
        
    def menuWidget(self):
        pass
        
        
class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
                
        # Initialize tab screen
        tabs = qtw.QTabWidget(tabPosition=qtw.QTabWidget.West)
        tab1 = Fitness(self)
        tab2 = Calories(self)
        tabs.resize(300,200)
        
        # Add tabs
        tabs.addTab(tab1, qtg.QIcon("icons/wrench.png"), "Fitness")
        tabs.addTab(tab2,qtg.QIcon("icons/gas.png"), "Calories")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
class Fitness(qtw.QWidget):
        
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Calories(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass
        

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())