import sys
import os
from json import load
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
import gspread

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        loadUi("landing.ui", self)
        self.show()

        LoginBtn = self.findChild(QPushButton)
        LoginBtn.autoDefault()
        LoginBtn.clicked.connect(self.loginAtt)
    
    def loginAtt(self):
        pw = self.lineEdit.text()
        print(pw)
        if (pw == 'password123'):
            self.close()
        else :
            self.error('Password Salah!')
            self.lineEdit.clear()
            return
            
    def error(self,errormsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(errormsg)
        msg.setWindowTitle("Error")
        msg.exec_()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())