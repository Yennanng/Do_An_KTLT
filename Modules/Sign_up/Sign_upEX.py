import json
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QDialog
from Modules.Sign_up.Sign_up import Ui_MainWindow
# from Modules.Login.Sign_inEx import Sign_inEX
# import Modules.Login.Sign_inEx

import sys
from Api.Signup_API import SignupAPI

class Sign_upEx(QMainWindow, Ui_MainWindow, SignupAPI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.Login = self.some_other_function()
        self.checkShowPassword.stateChanged.connect(self.show_password)
        self.pushSign_in.clicked.connect(self.sign_in)
        # self.pushRegister.clicked.connect(self.register)


        self.pushRegister.clicked.connect(self.register)
    # Sign_upEX.py

    def some_other_function(self):
        from Modules.Login.Sign_inEx import Sign_inEX
        obj = Sign_inEX()
        return obj
    def register(self):
        username = self.lineUserName.text().strip()
        password = self.linePassword.text().strip()
        confirm_password = self.lineConfirm.text().strip()
        signup_signal= self.check_user_signup(username=username, password=password,repassword=confirm_password)
        match signup_signal:
            case 1:
                QMessageBox.warning(self.MainWindow, "Error", "Error 1: Username or password is empty")
            case 2:
                QMessageBox.warning(self.MainWindow, "Error", "Error 2: Password is not the same")
            case 3:
                QMessageBox.warning(self.MainWindow, "Error", "Error 3: Username is already exist")
            case _:
                QMessageBox.warning(self.MainWindow, "Notification", f"Successful registration")




    def show_password(self):
        if self.checkShowPassword.isChecked():
            self.linePassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.lineConfirm.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.linePassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.lineConfirm.setEchoMode(QLineEdit.EchoMode.Password)

    def sign_in(self):
        self.Login_Window = QMainWindow()
        self.Login.setupUi(self.Login_Window)
        self.Login_Window.show()
        self.MainWindow.hide()

    def show(self):
        self.MainWindow.show()
