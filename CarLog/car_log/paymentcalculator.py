# paymentcalculator.py

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class PaymentCalculator(qtw.QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Payment Calculator')
        self.setLayout(qtw.QGridLayout())
        self.topLabel = qtw.QLabel("<h3>Payment Calculator<h3>")
        self.carPriceText = qtw.QLabel("Purchase Price:")
        self.carPrice = qtw.QLineEdit()
        self.carPrice.setValidator(qtg.QIntValidator(0, 100000, self))
        self.interestRateText = qtw.QLabel("Interest Rate:")
        self.interestRate = qtw.QLineEdit()
        self.interestRate.setValidator(qtg.QIntValidator(0, 10, self))
        self.termLengthText = qtw.QLabel("Number of Years:")
        self.termLength = qtw.QLineEdit()
        self.termLength.setValidator(qtg.QIntValidator(1, 10, self))
        
        
        self.payment = qtw.QLabel('Still figuring it out')
        monthlyPayment = str(10)
        self.calculationButton = qtw.QPushButton('Calculate Payment')
        #self.calculationButton.clicked.connect(self.calculatePayment(monthlyPayment))
        print(monthlyPayment)
        
        self.exitButton = qtw.QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)
        
        self.layout().addWidget(self.topLabel, 0, 0)
        self.layout().addWidget(self.carPriceText, 1, 0)
        self.layout().addWidget(self.carPrice, 1, 1)
        self.layout().addWidget(self.interestRateText, 2, 0)
        self.layout().addWidget(self.interestRate, 2, 1)
        self.layout().addWidget(self.termLengthText, 3, 0)
        self.layout().addWidget(self.termLength, 3, 1)
        
        self.layout().addWidget(self.calculationButton, 4, 0)
        self.layout().addWidget(self.payment, 4, 1)
        
        self.layout().addWidget(self.exitButton, 99, 1)
        
        
    def calculatePayment(self, monthlyPayment):
        """price = self.carPrice
        monthlyInterest = self.interestRate / 12
        months = self.termLength*12
        self.monthlyPayment = int((self.price*((monthlyRate)*(1+monthlyRate)**months))/(((1+monthlyRate)**(months)-1)))
        print(self.monthlyPayment)"""
        monthlyPayment = '0'
        return monthlyPayment      
        