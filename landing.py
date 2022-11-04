import sys
import os
from json import load
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import gspread
from coba import UI

# inisialisasi class untuk UI
class landingUI(QtWidgets.QMainWindow):
    # fungsi untuk membuka mainwindow
    def openmain(self, state):
        self.window = UI(state)

    # panggil UI dan load file.ui untuk landing
    def __init__(self):
        super(landingUI, self).__init__()
        loadUi("landing.ui", self)
        self.show()

        # login button untuk aslab
        LoginBtn = self.findChild(QtWidgets.QPushButton, "LoginBtn")
        LoginBtn.autoDefault()
        LoginBtn.clicked.connect(self.loginAtt)

        # login button untuk praktikan
        PrakBtn = self.findChild(QtWidgets.QPushButton, "PrakBtn")
        PrakBtn.clicked.connect(lambda : self.openmain(False))
    
    # fungsi attempt login
    def loginAtt(self):
        pw = self.lineEdit.text()
        if (pw == 'password123'): # password yang diset adalah 'password123'
            self.aslab = True
            self.close()
            self.openmain(True)
        else :
            self.error('Password Salah!') # error handling password salah
            self.lineEdit.clear()
            return
            
    # fungsi untuk pop up error handling
    def error(self,errormsg):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(errormsg)
        msg.setWindowTitle("Error")
        msg.exec_()
    
# memanggil dan eksekusi app     
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = landingUI()
    window.show()
    sys.exit(app.exec())