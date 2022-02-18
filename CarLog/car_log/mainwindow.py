# car_maintenance_log_2
"""
1-27-22
Program written in Python is used to track vehicle maintenance.
This program uses PyQt5 for the UI and SQLite for the data.
The user can enter the date, millage, and the maintenance performed.
The user will also have the capability to delete a row

2-14-22
New and improved version of the original car maintenance log.
Enhancements includes the ability to not only track maintenance
but to also track gas. Additional updates includes the ability
to change the color scheme through themes in the tool menu and
a car payment calculator
"""

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from .maintenance import Maintenance
from .gas import Gas
from .paymentcalculator import PaymentCalculator

class App(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initializeUI()

    def initializeUI(self):
        
        self.setWindowTitle('Car Log')
        self.resize(500, 650)
        
        self.styleSheet()
        self.createActions()
        self.menuWidget()
        self.toolbarWidget()
        self.mainWindow = MainWindow(self)
        self.setCentralWidget(self.mainWindow)
        
        self.show()
        
    def createActions(self):
        # Create the actions for the "Files Menu"
        self.add_row = qtw.QAction('Add Row', self)
        self.add_row.setShortcut('Ctrl+A')
        
        self.exit_action = qtw.QAction('Exit',
                triggered=lambda: self.statusBar().showMessage('Gonna Quit'))
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setIcon(qtg.QIcon("car_log/icons/exit.png"))
        self.exit_action.triggered.connect(self.exitMessage)
        
        theme_icon = qtg.QIcon("car_log/icons/monitor.png")
        self.defaultTheme = qtw.QAction(theme_icon, 'Default',
                triggered=lambda: self.statusBar().showMessage('Default Theme'))
        self.defaultTheme.triggered.connect(self.defaultStyleSheet)
        self.blueTheme = qtw.QAction(theme_icon, 'Blue',
                triggered=lambda: self.statusBar().showMessage('Blue Theme'))
        self.blueTheme.triggered.connect(self.blueStyleSheet)
        self.chromeTheme = qtw.QAction(theme_icon,'Chrome',
                triggered=lambda: self.statusBar().showMessage('Chrome Theme'))
        self.chromeTheme.triggered.connect(self.chromeStyleSheet)
        self.meshTheme = qtw.QAction(theme_icon,'Mesh',
                triggered=lambda: self.statusBar().showMessage('Mesh Theme'))
        self.meshTheme.triggered.connect(self.meshStyleSheet)
        self.digitalBlueTheme = qtw.QAction(theme_icon, 'Digital Blue', 
                triggered=lambda: self.statusBar().showMessage('Digital Blue Theme'))
        self.digitalBlueTheme.triggered.connect(self.digitalBlueStyleSheet)
        self.southWestTheme = qtw.QAction(theme_icon, 'South West',
                triggered=lambda: self.statusBar().showMessage('South West Theme'))
        self.southWestTheme.triggered.connect(self.southWestStyleSheet)
        self.crazyTheme = qtw.QAction(theme_icon, 'Crazy',
                triggered=lambda: self.statusBar().showMessage('Crazy Theme'))
        self.crazyTheme.triggered.connect(self.crazyStyleSheet)
        
        #self.payCalc = PaymentCalculator(self)
        self.payment_calc = qtw.QAction('Payment Calculator',
                triggered=lambda: self.statusBar().showMessage('Car Payment Calculator'))
        self.payment_calc.setIcon(qtg.QIcon("car_log/icons/calc.png"))
        self.payment_calc.triggered.connect(self.payCalc)
        
        # Create actions for the "Help Menu" menu
        self.about_action = qtw.QAction('About',
                triggered=lambda: self.statusBar().showMessage('About'))
        self.about_action.setIcon(qtg.QIcon("car_log/icons/about.png"))
        self.about_action.triggered.connect(self.aboutInfo)
        
    def menuWidget(self):
        # Create the status bar
        self.statusbar = self.statusBar()
        self.statusBar().showMessage('Welcome to your Car Log')
        
        # Create the menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
       # Create the "File" menu and add the buttons/actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.exit_action)
        
        toolsMenu = menu_bar.addMenu('Tools')
        toolsMenu.addAction(self.payment_calc)
        themesMenu = toolsMenu.addMenu(qtg.QIcon("car_log/icons/theme.png"), 'Themes')
        themesMenu.addAction(self.defaultTheme)
        themesMenu.addAction(self.blueTheme)
        themesMenu.addAction(self.chromeTheme)
        themesMenu.addAction(self.meshTheme)
        themesMenu.addAction(self.digitalBlueTheme)
        themesMenu.addAction(self.southWestTheme)
        themesMenu.addAction(self.crazyTheme)
        
        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(self.about_action)
        
    def toolbarWidget(self):
        toolbar = qtw.QToolBar()
        self.addToolBar(qtc.Qt.BottomToolBarArea, toolbar)
        toolbar.addAction(self.exit_action)
        
    def exitMessage(self):
        message = qtw.QMessageBox.question(self, 'Exit',
            'This will save upon exit. \n Are you sure you want exit?',
            qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if message == qtw.QMessageBox.Yes:
            #self.database.close()
            self.close()
            
    def payCalc(self):
        calc = PaymentCalculator(self)
        calc.resize(350, 350)
        calc.show()
            
    def aboutInfo(self):
        text = "CAM's car log, written in Python\n" \
        "using PyQt5 modules for the GUI\n\n" \
        "The car log allows users to track their\n" \
        "maintence and fuel. Users are also able to \n" \
        "change the color scheme through themes in\n" \
        "the Tool Menu based on their prefrences\n\n" \
        "             Written by CAM: 2022"
        qtw.QMessageBox.about(self, "CAM's Car Log", text)
            
    def defaultStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background-color: whitesmoke
        }
        QTableView {
            background-color: white
        }
        """
        self.setStyleSheet(stylesheet)
        
    def blueStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox {
            background-color: lightsteelblue
        }
        QPushButton {
            font-size: 10pt
            background-color: azure
        }
        QLabel {
            color: white
        }
        QTableView {
            background-color: aliceblue
        }
        QMenuBar, QTabWidget {
            background-color: powderblue
        }
        .QWidget {
           background: url(car_log/images/tile.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def chromeStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(car_log/images/chrome.png)
        }
        QLabel {
            color: silver
        }
        QMessageBox {
            background: url(car_log/images/chrome.png)
        }
        """
        self.setStyleSheet(stylesheet)
        
    def meshStyleSheet(self):
        stylesheet = """
        QMainWindow, QMessageBox {
            background: url(car_log/images/mesh.png)
        }
        QTableView {
            background: lightgray
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def digitalBlueStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(car_log/images/blue_mesh.png)
        }
        QLabel {
            color: white;
            font: bold
        }
        QTableView, QMessageBox, QComboBox, QPushButton  {
            background: url(car_log/images/light_blue_steel.png)
        }
        QPushButton:hover {
            background: lightblue
        }     
        QTableView {
            selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.75, y2: 0.75,
            stop: 0 #2E97AC, stop: 1 #C6E4E7)
        }
        QMenuBar {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 lightgray, stop:1 darkgray);
            spacing: 3px; /* spacing between menu bar items */
        }
        QMenuBar::item {
            padding: 1px 4px;
            background: transparent;
            border-radius: 4px;
        }
        QMenuBar::item:selected { /* when selected using mouse or keyboard */
            background: #a8a8a8;
        }
        QMenuBar::item:pressed {
            background: #888888;
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid #C2C7CB;
        }
        QTabWidget::tab-bar {
            left: 5px; /* move to the right by 5px */
        }
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB; /* same as the pane color */
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            min-width: 8ex;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
        }
        QTabBar::tab:selected {
            border-color: #9B9B9B;
            border-bottom-color: #C2C7CB; /* same as pane color */
        }
        QTabBar::tab:!selected {
            margin-top: 2px; /* make non-selected tabs look smaller */
        }
        QDialog {
            background: url(car_log/images/blue_mesh.png)
        }
        QDialog QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def southWestStyleSheet(self):
        stylesheet = """
        QMainWindow {
            background: url(car_log/images/south_west.png)
        }
        QTableView {
            background: url(car_log/images/south_rug.png);
            color: white;
            font: bold 14px
        }
        QLabel {
            color: white;
            font: bold 12px
        }
        QStatusBar {
            color: white;
            font: bold 12px
        }
        """
        self.setStyleSheet(stylesheet)
    
    def crazyStyleSheet(self):
        stylesheet = """
        QMainWindow { 
            background-color: lightgreen
        }
        QPushButton {
            font-size: 10pt
        }
        QTableView {
            background-color: plum
        }
        QLabel, QPushButton {
            background-color: yellow
        }
        """
        self.setStyleSheet(stylesheet)
    

class MainWindow(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        layout = qtw.QVBoxLayout(self)
        
        # Initialize tab screen
        tabs = qtw.QTabWidget()
        tab1 = Maintenance(self)
        tab2 = Gas(self)
        #tab3 = CarInformation(self)
        tabs.resize(300,200)
        
        # Add tabs
        
        tabs.addTab(tab1,"Maintenance")
        tabs.addTab(tab2,"Gas")
        #tabs.addTab(tab3,"Information")
        
        # Add tabs to widget
        layout.addWidget(tabs)
        self.setLayout(layout)

class CarInformation(qtw.QWidget):
    
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)
        
        layout = qtw.QVBoxLayout(self)


