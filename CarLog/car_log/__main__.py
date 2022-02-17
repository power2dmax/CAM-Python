import sys

from PyQt5 import QtWidgets as qtw
from .mainwindow import App

def main():
    app = qtw.QApplication(sys.argv)
    windows_style = qtw.QStyleFactory.create('Windows')
    app.setStyle(windows_style)
    window = App()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()