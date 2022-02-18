# paymentcalculator.py

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class PaymentCalculator(qtw.QDialog):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle('Payment Calculator')
        
        pay_label = qtw.QLabel("<h2>Payment Calculator<h2>", self)
        
        loan_label = qtw.QLabel("Amount:", self)
        loan_label.setFont(qtg.QFont('Arial', 10))
        
        self.amount = qtw.QLineEdit(self)
        self.amount.setValidator(qtg.QIntValidator())
        self.amount.setAlignment(qtc.Qt.AlignCenter)
        self.amount.setFont(qtg.QFont('Arial', 10))

        # creating a number of years label
        years_label = qtw.QLabel("Years:", self)
        years_label.setFont(qtg.QFont('Arial', 10))
  
        # creating a QLineEdit object to get the years
        self.years = qtw.QLineEdit(self)
        self.years.setValidator(qtg.QIntValidator())
        self.years.setAlignment(qtc.Qt.AlignCenter)
        self.years.setFont(qtg.QFont('Arial', 10))
  
        interest_label = qtw.QLabel("Annual Interest:", self)
        interest_label.setFont(qtg.QFont('Arial', 10))
  
        # creating a QLineEdit object to get the interest
        self.rate = qtw.QLineEdit(self)
        self.rate.setValidator(qtg.QIntValidator())
        self.rate.setAlignment(qtc.Qt.AlignCenter)
        self.rate.setFont(qtg.QFont('Arial', 10))
  
        # creating a push button
        calculate = qtw.QPushButton("Compute Payment", self)
        calculate.clicked.connect(self.calculate_action)
  
        # creating a label to show monthly payment
        self.monthly_payment = qtw.QLabel(self)
        self.monthly_payment.setAlignment(qtc.Qt.AlignCenter)
        self.monthly_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 3px solid black;"
                                     "background : lightgray;"
                                     "}")
        self.monthly_payment.setFont(qtg.QFont('Arial', 10))
  
        # creating a label to show monthly payment
        self.total_payment = qtw.QLabel(self)
  
        # setting properties to y payment label
        self.total_payment.setAlignment(qtc.Qt.AlignCenter)
        self.total_payment.setStyleSheet("QLabel"
                                     "{"
                                     "border : 3px solid black;"
                                     "background : lightgray;"
                                     "}")
        self.total_payment.setFont(qtg.QFont('Arial', 10))
        
        exitButton = qtw.QPushButton('Exit', self)
        exitButton.clicked.connect(self.close)
        
        # Set up the layout 
        pay_label.move(80, 10)
        loan_label.move(50, 50)
        self.amount.move(150, 50)
        years_label.move(50, 80)
        self.years.move(150, 80)
        interest_label.move(50, 110)
        self.rate.move(150, 110)
        calculate.move(50, 150)
        self.monthly_payment.setGeometry(50, 190, 235, 40)
        self.total_payment.setGeometry(50, 240, 235, 40)
        exitButton.move(240, 300)
          
    def calculate_action(self):
        annualInterestRate = self.rate.text()
  
        if len(annualInterestRate) == 0 or annualInterestRate == '0':
            return
        
        numberOfYears = self.years.text()
  
        if len(numberOfYears) == 0 or numberOfYears == '0':
            return

        loanAmount = self.amount.text()
  
        if len(loanAmount) == 0 or loanAmount == '0':
            return
  
        # converting text to int
        annualInterestRate = int(annualInterestRate)
        numberOfYears = int(numberOfYears)
        loanAmount = int(loanAmount)
  
        # getting monthly interest rate
        monthlyInterestRate = annualInterestRate / 1200
  
        # Calculate the monthly payemnt
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
        monthlyPayment = "{:.2f}".format(monthlyPayment)
        self.monthly_payment.setText("Monthly Payment : " + str(monthlyPayment))
        
        # Calculate the total payment
        totalPayment = float(monthlyPayment) * 12 * numberOfYears
        totalPayment = "{:.2f}".format(totalPayment)
        self.total_payment.setText("Total Payment : " + str(totalPayment))  