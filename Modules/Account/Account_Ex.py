from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (QMainWindow, QTableWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt

from Modules.Account.Account import Ui_Account
from Modules.Category.Category import Ui_Category
from pymongo import MongoClient




class MainWindowEx_Account(QMainWindow):
    def __init__(self):
        super().__init__()
        self.account = Ui_Account()
        self.account.setupUi(self)
        # self.save()

    # def setupUi(self):
    #     self.account.pushButton_Save.clicked.connect(self.save)
    #
    #
    # def save(self):
    #     birthday = self.account.lineEdit_Birthday.dateTime().toString("dd-MM-yyyy")
    #     month_income = self.account.lineEdit_month_income.text().strip()
    #     target_saving = self.account.lineEdit_target_saving.text().strip()



