# paymentcalculator.py

import sys, os, csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PaymentCalculator(qtw.QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Payment Calculator')
                # creating head label
        head = qtw.QLabel("Loan Calculator", self)
  
        # setting geometry to the head
        head.setGeometry(0, 10, 400, 60)
  
        # font
        font = qtg.QFont('Times', 15)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
  
        # setting font to the head
        head.setFont(font)
  
        # setting alignment of the head
        head.setAlignment(qtc.Qt.AlignCenter)
  
        # setting color effect to the head
        color = QGraphicsColorizeEffect(self)
        color.setColor(Qt.darkCyan)
        head.setGraphicsEffect(color)
  
        # creating a interest label
        i_label = qtw.QLabel("Annual Interest", self)
  
        # setting properties to the interest label
        i_label.setAlignment(Qt.AlignCenter)
        i_label.setGeometry(20, 100, 170, 40)
        i_label.setStyleSheet("QLabel"
                              "{"
                              "border : 2px solid black;"
                              "background : rgba(70, 70, 70, 35);"
                              "}")
        i_label.setFont(QFont('Times', 9))
  
        # creating a QLineEdit object to get the interest
        self.rate = qtw.QLineEdit(self)
  
        # accepting only number as input
        onlyInt = QIntValidator()
        self.rate.setValidator(onlyInt)
  
        # setting properties to the rate line edit
        self.rate.setGeometry(200, 100, 180, 40)
        self.rate.setAlignment(Qt.AlignCenter)
        self.rate.setFont(QFont('Times', 9))
  
  
        # creating a number of years label
        n_label = qtw.QLabel("Years ", self)
  
        # setting properties to the years label
        n_label.setAlignment(Qt.AlignCenter)
        n_label.setGeometry(20, 150, 170, 40)
        n_label.setStyleSheet("QLabel"
                              "{"
                              "border : 2px solid black;"
                              "background : rgba(70, 70, 70, 35);"
                              "}")
        n_label.setFont(QFont('Times', 9))
  
        # creating a QLineEdit object to get the years
        self.years = qtw.QLineEdit(self)
  
        # accepting only number as input
        onlyInt = QIntValidator()
        self.years.setValidator(onlyInt)
  
        # setting properties to the rate line edit
        self.years.setGeometry(200, 150, 180, 40)
        self.years.setAlignment(Qt.AlignCenter)
        self.years.setFont(QFont('Times', 9))
  
        # creating a loan amount label
        a_label = qtw.QLabel("Amount", self)
  
        # setting properties to the amount label
        a_label.setAlignment(Qt.AlignCenter)
        a_label.setGeometry(20, 200, 170, 40)
        a_label.setStyleSheet("QLabel"
                              "{"
                              "border : 2px solid black;"
                              "background : rgba(70, 70, 70, 35);"
                              "}")
        a_label.setFont(QFont('Times', 9))
  
        # creating a QLineEdit object to get the amount
        self.amount = qtw.QLineEdit(self)
  
        # accepting only number as input
        onlyInt = QIntValidator()
        self.amount.setValidator(onlyInt)
  
        # setting properties to the rate line edit
        self.amount.setGeometry(200, 200, 180, 40)
        self.amount.setAlignment(Qt.AlignCenter)
        self.amount.setFont(QFont('Times', 9))
  
  
        # creating a push button
        calculate = qtw.QPushButton("Compute Payment", self)
  
        # setting geometry to the push button
        calculate.setGeometry(125, 270, 150, 40)
  
        # adding action to the calculate button
        calculate.clicked.connect(self.calculate_action)
  
        # creating a label to show monthly payment
        self.m_payment = qtw.QLabel(self)
  
        # setting properties to m payment label
        self.m_payment.setAlignment(Qt.AlignCenter)
        self.m_payment.setGeometry(50, 340, 300, 60)
        self.m_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 3px solid black;"
                                     "background : white;"
                                     "}")
        self.m_payment.setFont(QFont('Arial', 11))
  
        # creating a label to show monthly payment
        self.y_payment = qtw.QLabel(self)
  
        # setting properties to y payment label
        self.y_payment.setAlignment(Qt.AlignCenter)
        self.y_payment.setGeometry(50, 410, 300, 60)
        self.y_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 3px solid black;"
                                     "background : white;"
                                     "}")
        self.y_payment.setFont(QFont('Arial', 11))
  
    # method for calculating monthly 
    # and annually payments
    def calculate_action(self):
  
        # getting annual interest rate
        annualInterestRate = self.rate.text()
  
        # if there is no number is entered
        if len(annualInterestRate) == 0 or annualInterestRate == '0':
            return
  
        # getting number of years
        numberOfYears = self.years.text()
  
        # if there is no number is entered
        if len(numberOfYears) == 0 or numberOfYears == '0':
            return
  
        # getting loan amount
        loanAmount = self.amount.text()
  
        # if there is no number is entered
        if len(loanAmount) == 0 or loanAmount == '0':
            return
  
        # converting text to int
        annualInterestRate = int(annualInterestRate)
        numberOfYears = int(numberOfYears)
        loanAmount = int(loanAmount)
  
        # getting monthly interest rate
        monthlyInterestRate = annualInterestRate / 1200
  
        # calculating monthly payemnt
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
  
        # setting formatting
        monthlyPayment = "{:.2f}".format(monthlyPayment)
  
        # setting text to the label
        self.m_payment.setText("Monthly Payment : " + str(monthlyPayment))
  
        # getting total payment
        totalPayment = float(monthlyPayment) * 12 * numberOfYears
        totalPayment = "{:.2f}".format(totalPayment)
  
        # setting text to the label
        self.y_payment.setText("Total Payment : " + str(totalPayment))  
        