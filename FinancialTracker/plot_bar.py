import sys
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtSql as qts
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
    

class GasGraph(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(600, 100, 500, 600)
        
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)
        
        total_principle = 185000.00
        current_principle = 40979.73
        current_interest = 33912.69
        total_interest = 114062.00
        
        
        labels = ['G1', 'G2', 'G3', 'G4', 'G5']
        men_means = [20, 34, 30, 35, 27]
        women_means = [25, 32, 34, 20, 25]

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, men_means, width, label='Men')
        rects2 = ax.bar(x + width/2, women_means, width, label='Women')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()

        plt.show()
        
        #self.layout.addWidget(self.static_canvas)
        #self.setLayout(self.layout)




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