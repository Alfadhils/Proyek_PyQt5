from asyncio.windows_events import NULL
from logging import error
import sys
import os
from json import load
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import gspread
import numpy as np
import requests

# global variable untuk counter
hitung = 1

# inisialisasi class untuk UI
class UI(QMainWindow):
    def __init__(self, state=False):
        # panggil UI dan load file.ui untuk mainwindow
        super(UI, self).__init__()
        loadUi("Design_Trial.ui", self)
        self.show()

        # menentukan state login (aslab/praktikan)
        self.deterstate(state)
        # hitung sebagai variabel global
        global hitung

        # tes koneksi internet dan error handling
        try:
            request = requests.get("http://www.google.com", timeout=10)
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.errorfunc("Tidak ada Koneksi Internet")

        # membaca googlesheet menggunakan service account
        open = gspread.service_account(filename="creds.json")
        sheets = open.open_by_key(
            "1gVmaW9uDWLIy7-B90HDruVZSlTZnTSGv_mGj-BmWRTo")

        # inisialisasi worksheet modul 6,7,8 dan array worksheet
        worksheetsSatu = sheets.worksheet("MODUL 6")
        worksheetsDua = sheets.worksheet("MODUL 7")
        worksheetsTiga = sheets.worksheet("MODUL 8")
        wsarr = np.array([worksheetsSatu, worksheetsDua, worksheetsTiga])

        # menunjukkan data awal pada tiap sheet
        self.showData(wsarr)

        # inisialisasi clear button
        clear = self.findChild(QPushButton, "clear")
        clear.clicked.connect(lambda: self.clearData(
            self.tabWidget_2.currentIndex(), wsarr, state))

        # inisialisasi save button untuk praktikan
        simpan = self.findChild(QPushButton, "simpan")
        simpan.clicked.connect(lambda: self.saveJadwal(wsarr))

        # inisialisasi save button untuk praktikan
        saveBtnAslab = self.findChild(QPushButton, "saveaslab")
        saveBtnAslab.clicked.connect(lambda: self.saveJadwalAslab(wsarr))

        # inisialisasi counter urutan kelompok
        nambah = self.findChild(QPushButton, "incButton")
        kurang = self.findChild(QPushButton, "decButton")
        kelompok = self.findChild(QLabel, "layarHitung")
        kelompok.setNum(1)

        nambah.clicked.connect(self.counterUp)
        kurang.clicked.connect(self.counterDown)

    def deterstate(self, state):
        statelabel = self.findChild(QLabel, "label_5")
        statelabel.setStyleSheet("background-color: yellow; font: 12pt;")
        if state == True:
            statelabel.setText("Aslab")
            self.tabWidget.removeTab(0)
        else:
            statelabel.setText("Praktikan")
            self.tabWidget.removeTab(1)

    def saveJadwal(self, sheetp):

        modul6Sesi = self.findChild(QComboBox, "modul6_sesi")
        modul6Tanggal = self.findChild(QComboBox, "modul6_tanggal")
        modul7Sesi = self.findChild(QComboBox, "modul7_sesi")
        modul7Tanggal = self.findChild(QComboBox, "modul7_tanggal")
        modul8Sesi = self.findChild(QComboBox, "modul8_sesi")
        modul8Tanggal = self.findChild(QComboBox, "modul8_tanggal")
        prakarr = np.array([modul6Sesi, modul6Tanggal, modul7Sesi,
                           modul7Tanggal, modul8Sesi, modul8Tanggal])

        ind6 = self.findChild(QLabel, "indModul6")
        ind7 = self.findChild(QLabel, "indModul7")
        ind8 = self.findChild(QLabel, "indModul8")
        indArr = np.array([ind6, ind7, ind8])

        errflag1 = self.pilihModul(sheetp[0], int(modul6Sesi.currentText()),
                                   modul6Tanggal.currentText())
        errflag2 = self.pilihModul(sheetp[1], int(modul7Sesi.currentText()),
                                   modul7Tanggal.currentText())
        errflag3 = self.pilihModul(sheetp[2], int(modul8Sesi.currentText()),
                                   modul8Tanggal.currentText())

        efArr = np.array([errflag1, errflag2, errflag3])
        if False in efArr:
            for i in range(len(efArr)):
                if efArr[i] == False:
                    indArr[i].setText("Bentrok")
                else:
                    indArr[i].setText("Aman")

            self.errorfunc("Jadwal Bentrok")
            for x in indArr:
                x.setText("status")
        else:
            self.clearPrak(prakarr)

        self.showData(sheetp)

    def clearPrak(self, arr):
        self.counterUp()
        for i in range(len(arr)):
            arr[i].setCurrentIndex(0)

    def pilihModul(self, sheetP, sesiPraktikum, hariPraktikum):
        if 'Senin' in hariPraktikum:
            hariP = 1
            if sesiPraktikum == 1:
                curr = sheetP.cell(3, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(3, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        3, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 2:
                curr = sheetP.cell(5, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(5, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        5, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 3:
                curr = sheetP.cell(7, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(7, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        7, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 4:
                curr = sheetP.cell(9, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(9, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        9, 2+hariP, str(curr) + " " + str(hitung))
        elif 'Selasa' in hariPraktikum:
            hariP = 2
            if sesiPraktikum == 1:
                curr = sheetP.cell(3, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(3, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        3, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 2:
                curr = sheetP.cell(5, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(5, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        5, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 3:
                curr = sheetP.cell(7, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(7, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        7, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 4:
                curr = sheetP.cell(9, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(9, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        9, 2+hariP, str(curr) + " " + str(hitung))
        elif 'Rabu' in hariPraktikum:
            hariP = 3
            if sesiPraktikum == 1:
                curr = sheetP.cell(3, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(3, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        3, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 2:
                curr = sheetP.cell(5, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(5, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        5, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 3:
                curr = sheetP.cell(7, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(7, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        7, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 4:
                curr = sheetP.cell(9, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(9, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        9, 2+hariP, str(curr) + " " + str(hitung))
        elif 'Kamis' in hariPraktikum:
            hariP = 4
            if sesiPraktikum == 1:
                curr = sheetP.cell(3, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(3, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        3, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 2:
                curr = sheetP.cell(5, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(5, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        5, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 3:
                curr = sheetP.cell(7, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(7, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        7, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 4:
                curr = sheetP.cell(9, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(9, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        9, 2+hariP, str(curr) + " " + str(hitung))
        elif 'Jumat' in hariPraktikum:
            hariP = 5
            if sesiPraktikum == 1:
                curr = sheetP.cell(3, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(3, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        3, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 2:
                curr = sheetP.cell(5, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(5, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        5, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 3:
                curr = sheetP.cell(7, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(7, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        7, 2+hariP, str(curr) + " " + str(hitung))
            elif sesiPraktikum == 4:
                curr = sheetP.cell(9, 2+hariP).value
                if curr is None:
                    sheetP.update_cell(9, 2+hariP, str(hitung))
                elif " " in curr:
                    return False
                else:
                    sheetP.update_cell(
                        9, 2+hariP, str(curr) + " " + str(hitung))
        return True

    def saveJadwalAslab(self, sheetar):
        kodeAslab = self.findChild(QLineEdit, "kodeaslab")
        modulAslab = self.findChild(QComboBox, "modulaslab")
        hariAslab = self.findChild(QComboBox, "hariaslab")
        sesi1aslab = self.findChild(QCheckBox, "sesi1aslab")
        sesi2aslab = self.findChild(QCheckBox, "sesi2aslab")
        sesi3aslab = self.findChild(QCheckBox, "sesi3aslab")
        sesi4aslab = self.findChild(QCheckBox, "sesi4aslab")
        sesiArray = np.array([sesi1aslab, sesi2aslab, sesi3aslab, sesi4aslab])
        sesiaslab = np.array([sesi1aslab.isChecked(), sesi2aslab.isChecked(
        ), sesi3aslab.isChecked(), sesi4aslab.isChecked()])

        if kodeAslab.text() == '':
            self.errorfunc("Tidak ada Kode Aslab")
            return
        else:
            if modulAslab.currentText() == "Modul 6":
                self.aslabUpdate(
                    sheetar[0], hariAslab.currentText(), sesiaslab, kodeAslab.text())
            elif modulAslab.currentText() == "Modul 7":
                self.aslabUpdate(
                    sheetar[1], hariAslab.currentText(), sesiaslab, kodeAslab.text())
            elif modulAslab.currentText() == "Modul 8":
                self.aslabUpdate(
                    sheetar[2], hariAslab.currentText(), sesiaslab, kodeAslab.text())

            self.aslabclear(hariAslab, modulAslab, sesiArray)

        self.showData(sheetar)

    def aslabUpdate(self, sheet, hari, sesiarr, kode):
        if hari == 'Senin':
            inthari = 1
            for i in range(len(sesiarr)):
                if sesiarr[i] == True:
                    sheet.update_cell(2+2*i, 2+inthari, kode)

        elif hari == 'Selasa':
            inthari = 2
            for i in range(len(sesiarr)):
                if sesiarr[i] == True:
                    sheet.update_cell(2+2*i, 2+inthari, kode)

        elif hari == 'Rabu':
            inthari = 3
            for i in range(len(sesiarr)):
                if sesiarr[i] == True:
                    sheet.update_cell(2+2*i, 2+inthari, kode)

        elif hari == 'Kamis':
            inthari = 4
            for i in range(len(sesiarr)):
                if sesiarr[i] == True:
                    sheet.update_cell(2+2*i, 2+inthari, kode)

        elif hari == 'Jumat':
            inthari = 5
            for i in range(len(sesiarr)):
                if sesiarr[i] == True:
                    sheet.update_cell(2+2*i, 2+inthari, kode)

    def aslabclear(self, hariAslab, modulAslab, sesiarr):
        hariAslab.setCurrentIndex(hariAslab.currentIndex()+1)
        if hariAslab.currentIndex() == -1:
            modulAslab.setCurrentIndex(modulAslab.currentIndex()+1)
            hariAslab.setCurrentIndex(0)
        sesiarr[0].setCheckState(False)
        sesiarr[1].setCheckState(False)
        sesiarr[2].setCheckState(False)
        sesiarr[3].setCheckState(False)

    def counterUp(self):
        global hitung
        if hitung+1 > 99 :
            self.errorfunc("Nomor kelompok tidak bisa lebih dari 99 !")
            return
        else :
            hitung += 1
            kelompok = self.findChild(QLabel, "layarHitung")
            kelompok.setNum(hitung)

    def counterDown(self):
        global hitung
        if hitung-1 < 1 :
            self.errorfunc("Nomor kelompok tidak bisa 0 !")
            return
        else :
            hitung -= 1
            kelompok = self.findChild(QLabel, "layarHitung")
            kelompok.setNum(hitung)

    def insertRowSatu(self, items):
        rowPosition = self.Modul_6.rowCount()
        self.Modul_6.insertRow(rowPosition)
        for x in range(len(items)):
            qtablewidgetitem = QTableWidgetItem()
            self.Modul_6.setItem(rowPosition, x, qtablewidgetitem)
            qtablewidgetitem = self.Modul_6.item(rowPosition, x)
            qtablewidgetitem.setText(items[x])

    def insertRowDua(self, items):
        rowPosition = self.Modul_7.rowCount()
        self.Modul_7.insertRow(rowPosition)
        for x in range(len(items)):
            qtablewidgetitem = QTableWidgetItem()
            self.Modul_7.setItem(rowPosition, x, qtablewidgetitem)
            qtablewidgetitem = self.Modul_7.item(rowPosition, x)
            qtablewidgetitem.setText(items[x])

    def insertRowTiga(self, items):
        rowPosition = self.Modul_8.rowCount()
        self.Modul_8.insertRow(rowPosition)
        for x in range(len(items)):
            qtablewidgetitem = QTableWidgetItem()
            self.Modul_8.setItem(rowPosition, x, qtablewidgetitem)
            qtablewidgetitem = self.Modul_8.item(rowPosition, x)
            qtablewidgetitem.setText(items[x])

    def showData(self, sheetarr):
        self.Modul_6.clear()
        self.Modul_7.clear()
        self.Modul_8.clear()

        self.Modul_6.setRowCount(0)
        self.Modul_7.setRowCount(0)
        self.Modul_8.setRowCount(0)

        jadwalSatu = sheetarr[0].get_all_values()
        for x in range(len(jadwalSatu)):
            self.insertRowSatu(jadwalSatu[x])

        jadwalDua = sheetarr[1].get_all_values()
        for x in range(len(jadwalDua)):
            self.insertRowDua(jadwalDua[x])

        jadwalTiga = sheetarr[2].get_all_values()
        for x in range(len(jadwalTiga)):
            self.insertRowTiga(jadwalTiga[x])

    def clearData(self, tabnum, wsarr, state):
        rangeaslab = ["C2:G2", "C4:G4", "C6:G6", "C8:G8"]
        rangepraktikan = ["C3:G3", "C5:G5", "C7:G7", "C9:G9"]
        if state == True:
            wsarr[tabnum].batch_clear(rangeaslab)
        elif state == False:
            wsarr[tabnum].batch_clear(rangepraktikan)
        self.showData(wsarr)

    def errorfunc(self, errormsg):
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
