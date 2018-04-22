from PyQt5 import QtCore, QtGui, QtWidgets
from ui import *
import sys
import math


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_21.setText('')
        self.ui.lineEdit.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_2.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_3.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_4.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_10.setPlaceholderText("Введите значение!")
        self.ui.comboBox.setValidator(QtGui.QIntValidator(0,9999))
        self.ui.lineEdit.editingFinished.connect(self.rascet)
        self.ui.lineEdit_2.editingFinished.connect(self.rascet)
        self.ui.lineEdit_3.editingFinished.connect(self.rascet)
        self.ui.lineEdit_4.editingFinished.connect(self.rascet)
        self.ui.lineEdit_10.editingFinished.connect(self.rascet)

        self.ui.spinBox.valueChanged.connect(self.regeneration)
        self.ui.spinBox_2.valueChanged.connect(self.regeneration)
        self.ui.spinBox_3.valueChanged.connect(self.regeneration)

        self.ui.comboBox.activated.connect(self.zapolnenie)
        self.ui.comboBox_2.activated.connect(self.zapolnenie)
        #self.ui.pushButton.clicked.connect(self.rascet)
        self.ui.pushButton_2.clicked.connect(self.clear)

    def zapolnenie(self):
        lambda_dlinna = str(self.ui.comboBox.currentText())
        self.ui.comboBox_2.setDisabled(False)
        try:
            self.ui.label_21.setText('')
            if str(self.ui.comboBox.currentText()) == "1310 (к)":
                self.ui.lineEdit.setText('1.459')
                self.ui.lineEdit_2.setText('1.456')
                self.ui.lineEdit_3.setText('9')
                self.ui.lineEdit_4.setText('125')
                self.ui.lineEdit_10.setText('7.218')
                self.delta_f()
                self.apertura()
                self.norm_frequency("1310")
                self.disp()
                self.alfa("1310")
                self.regeneration()

            elif str(self.ui.comboBox.currentText()) == "1550 (к)":
                self.ui.lineEdit.setText('1.4681')
                self.ui.lineEdit_2.setText('1.4623')
                self.ui.lineEdit_3.setText('9')
                self.ui.lineEdit_4.setText('125')
                self.ui.lineEdit_10.setText('7.218')
                self.delta_f()
                self.apertura()
                self.norm_frequency("1550")
                self.disp()
                self.alfa("1550")
                self.regeneration()

            elif str(self.ui.comboBox.currentText()) == " ":
                self.ui.label_21.setText('')
                self.ui.lineEdit.setText('')
                self.ui.lineEdit_2.setText('')
                self.ui.lineEdit_3.setText('')
                self.ui.lineEdit_4.setText('')
                self.ui.lineEdit_5.setText('')
                self.ui.lineEdit_6.setText('')
                self.ui.lineEdit_7.setText('')
                self.ui.lineEdit_8.setText('')
                self.ui.lineEdit_15.setText('')
                self.ui.lineEdit_16.setText('')
                self.ui.lineEdit_9.setText('')
                self.ui.lineEdit_10.setPlaceholderText("Введите значение!")
                self.ui.lineEdit_10.setText('')
                self.ui.lineEdit_11.setText('')
                self.ui.lineEdit_12.setText('')
                self.ui.spinBox.setValue(0)

            else:
                self.rascet()

        except ValueError:
            self.ui.label_21.setText('Введите значения!')
            # self.ui.lineEdit_10.setPlaceholderText("Введите значения!")
            # mes = QtWidgets.QMessageBox(2,"Ошибка!","Введите значения!",buttons=QtWidgets.QMessageBox.Ok)
            # mes.exec()

    def delta_f(self):
        n1 = float(self.ui.lineEdit.text())
        n2 = float(self.ui.lineEdit_2.text())
        delta = n1 - n2
        self.ui.lineEdit_5.setText(str(round(delta,4)))

    def apertura(self):
        n1 = float(self.ui.lineEdit.text())
        n2 = float(self.ui.lineEdit_2.text())
        na = math.sqrt((n1**2)-(n2**2))
        self.ui.lineEdit_6.setText(str(round(na,4)))

    def norm_frequency(self,lambda_dlinna):
        lambda_dlinna = int(lambda_dlinna)
        d = float(self.ui.lineEdit_3.text())
        na = float(self.ui.lineEdit_6.text())
        v = math.pi*d*na/(lambda_dlinna/1000)
        self.ui.lineEdit_7.setText(str(round(v,4)))

    def kolvo_mod(self):
        V = float(self.ui.lineEdit_7.text())
        tip_volokna = self.ui.comboBox_2.currentText()
        if tip_volokna =="Ступенчатый":
            M = int(V**2)
            self.ui.lineEdit_13.setText(str(M))
        elif tip_volokna =="Градиентный":
            M = int((V**2)/2)
            self.ui.lineEdit_13.setText(str(M))
        if M < 10:
            self.ui.groupBox_3.setTitle("Одномодовое волокно")
            self.ui.comboBox_2.setCurrentText("Ступенчатое")
            self.ui.lineEdit_14.setText(str(0))
            self.ui.comboBox_2.setDisabled(True)
        if M >= 10:
            self.ui.comboBox_2.setDisabled(False)
            self.ui.groupBox_3.setTitle("Многомодовое волокно")

    def disp(self):
        if int(str(self.ui.comboBox.currentText()).rstrip(" (к)")) <= 1350:
            D = 3.5
        else:
            D = 18 #18 по рекомендации
        L = float(self.ui.lineEdit_10.text())
        tau_hr = 0.13 * L * D
        self.ui.lineEdit_9.setText(str(round(tau_hr,4)))

        tau_pmd = 0.2 * math.sqrt(L)
        self.ui.lineEdit_11.setText(str(round(tau_pmd,4)))
        tip_volokna = self.ui.comboBox_2.currentText()
        NA = float(self.ui.lineEdit_6.text())
        c = 300000
        n1 = float(self.ui.lineEdit.text())

        if tip_volokna =="Ступенчатый":
            tau_mm = ((NA**4)*L/(2*c*n1))*10**9
            self.ui.lineEdit_14.setText(str(round(tau_mm,4)))
        elif tip_volokna =="Градиентный":
            tau_mm = ((NA**2)*L/(8*c*(n1**3)))*10**9
            self.ui.lineEdit_14.setText(str(round(tau_mm,4)))
        self.kolvo_mod()
        M = int(self.ui.lineEdit_13.text())
        if M < 10:
            tau_mm = 0
        tau = math.sqrt(tau_mm**2+ tau_hr**2 + tau_pmd**2)
        self.ui.lineEdit_15.setText(str(round(tau,4)))

    def alfa(self,lambda_dlinna):
        lambda_dlinna = int(lambda_dlinna)
        alfa_r = (0.8/(math.pow((lambda_dlinna/1000),4)))
        alfa_uf = pow(10,((2/(lambda_dlinna/1000))))/2154
        alfa_ik = pow(10,((-21.9/(lambda_dlinna/1000))+12.4))
        alfa_pogl = alfa_uf + alfa_ik
        alfa_kab = 0.2 * (alfa_pogl + alfa_r)
        alfa_all = alfa_pogl + alfa_r + alfa_kab
        self.ui.lineEdit_12.setText(str(round(alfa_all,4)))

    def regeneration(self):
        W = 34 #Энергетический потенциал 26дБ
        P_z = 3 # Запас системы по мощности
        alfa_rs = 0.2 #затухание на разъемных соединениях
        alfa_cc = 0.1 #потери в местах сваривания
        try:
            Lsd = int(self.ui.spinBox_2.value()) #строительная длина
            Nrs = int(self.ui.spinBox.value()) #кол-во неразъемных соед
            Ncc = int(self.ui.spinBox_3.value()) #кол-во сварных соед
            alfa_a = float(self.ui.lineEdit_12.text())
            #Lmax = (W - P_z - Nrs * alfa_rs - Ncc * alfa_cc)/(alfa_a + (alfa_cc/Lsd))
            Lmax= (W - P_z - Nrs * alfa_rs) / (alfa_a + alfa_cc / (Lsd))
            self.ui.lineEdit_8.setText(str(round(Lmax,4)))
            aru = 15
            Lmin = (W - aru - P_z - Nrs * alfa_rs - Ncc * alfa_cc)/(alfa_a + (alfa_cc/Lsd))

            self.ui.lineEdit_16.setText(str(round(Lmin,4)))
        except:
            self.ui.label_21.setText('Введите значения!')

    def clear (self):
        self.ui.label_21.setText('')
        self.ui.lineEdit.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_2.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_3.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_4.setPlaceholderText("Введите значение!")
        self.ui.lineEdit.setText('')
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit_3.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_5.setText('')
        self.ui.lineEdit_6.setText('')
        self.ui.lineEdit_7.setText('')
        self.ui.lineEdit_8.setText('')
        self.ui.lineEdit_15.setText('')
        self.ui.lineEdit_16.setText('')
        self.ui.lineEdit_9.setText('')
        self.ui.lineEdit_10.setPlaceholderText("Введите значение!")
        self.ui.lineEdit_10.setText('')
        self.ui.lineEdit_11.setText('')
        self.ui.lineEdit_12.setText('')
        self.ui.lineEdit_13.setText('')
        self.ui.lineEdit_14.setText('')
        self.ui.spinBox.setValue(0)
        self.ui.spinBox_2.setValue(0)
        self.ui.spinBox_3.setValue(0)

    def rascet(self):
        try:
            lambda_dlinna = int(str(self.ui.comboBox.currentText()).rstrip(" (к)"))
        except:
            pass
        try:
            self.delta_f()
            self.apertura()
            self.norm_frequency(lambda_dlinna)
            self.disp()
            self.alfa(lambda_dlinna)
            self.kolvo_mod()
            self.regeneration()
        except ValueError:
            self.ui.label_21.setText('Введите значения!')
            # mes = QtWidgets.QMessageBox(2,"Ошибка!","Введите значения!",buttons=QtWidgets.QMessageBox.Ok)
            # mes.exec()
        except UnboundLocalError:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    myapp = MyWin()
    myapp.setWindowTitle("Расчёт параметров для курсового проекта")
    myapp.show()
    sys.exit(app.exec_())
