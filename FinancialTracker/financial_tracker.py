# financial_tracker.py
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
        tabs = qtw.QTabWidget()
        tab1 = Dashboard(self)
        tab2 = Checking(self)
        tab3 = Savings(self)
        tab4 = Retirement(self)
        tab5 = Mortgage(self)
        tabs.resize(300,200)
        
        # Add tabs
        tabs.addTab(tab1, qtg.QIcon("icons/cash.png"), "Dashboard")
        tabs.addTab(tab2,qtg.QIcon("icons/cash.png"), "Checking")
        tabs.addTab(tab3, qtg.QIcon("icons/cash.png"), "Savings")
        tabs.addTab(tab4, qtg.QIcon("icons/cash.png"), "Retirement")
        tabs.addTab(tab5, qtg.QIcon("icons/cash.png"), "Mortgage")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)
        
class Dashboard(qtw.QWidget):
        
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Checking(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass
        

class Savings(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Retirement(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


class Mortgage(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())
