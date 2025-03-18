from PyQt6 import QtWidgets
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QDialog
from Modules.Transaction.MainWindow import Ui_MainWindow
from Modules.Transaction.MainWindow2 import Ui_MainWindow2
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chi_tieu"]
collection = db["database"]

class MainWindowEx(QMainWindow):
    PATH = "data/database.json"
    def __init__(self):
        super().__init__()
        self.products = []
        self.selectedProduct = None
        self.Page1 = Ui_MainWindow()
        self.Transaction = Ui_MainWindow2()
        self.Page1.setupUi(self)
        self.setupUi()

    def setupUi(self):
        self.Page1.tableWidgetProduct.setColumnCount(5)
        self.Page1.tableWidgetProduct.setHorizontalHeaderLabels(["Id", "Categories", "Details", "Amount", "Date"])
        self.Page1.tableWidgetProduct.setColumnHidden(0, True)
        self.Page1.tableWidgetProduct.setColumnWidth(1, 150)
        self.Page1.tableWidgetProduct.setColumnWidth(2, 150)
        self.Page1.tableWidgetProduct.setColumnWidth(3, 150)
        self.Page1.tableWidgetProduct.setColumnWidth(4, 150)
        self.Page1.tableWidgetProduct.setColumnWidth(5, 150)
        self.load_data()
        
        self.Page1.pushButton_Edit.clicked.connect(self.open_transaction)
        self.Page1.pushButton_Delete.clicked.connect(self.Delete)

    def open_transaction(self):
         self.Transaction_open = QMainWindow()
         self.Transaction.setupUi(self.Transaction_open)
         self.Transaction.pushButton_Transaction.clicked.connect(self.Save)
         self.Transaction.pushButton_Save.clicked.connect(self.processSave)
         self.Transaction_open.show()
         self.hide()

    def Save(self):
        self.show()
        self.Transaction_open.close()

    def load_data(self):
        products = list(collection.find({}))
        self.Page1.tableWidgetProduct.setRowCount(len(products))
        for row, product in enumerate(products):
            self.Page1.tableWidgetProduct.setItem(row, 0, QTableWidgetItem(str(product["_id"])))
            self.Page1.tableWidgetProduct.setItem(row, 1, QTableWidgetItem(product["Categories"]))
            self.Page1.tableWidgetProduct.setItem(row, 2, QTableWidgetItem(product["Details"]))
            self.Page1.tableWidgetProduct.setItem(row, 3, QTableWidgetItem(str(product["Amount"])))
            self.Page1.tableWidgetProduct.setItem(row, 4, QTableWidgetItem(str(product["Date"])))

    def Delete(self):
        current_row = self.Page1.tableWidgetProduct.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, "Delete Confirmation", "Are you sure?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                selected_id = self.Page1.tableWidgetProduct.item(current_row, 0).text()
                if selected_id:
                    collection.delete_one({"_id": ObjectId(selected_id)})
                    self.Page1.tableWidgetProduct.removeRow(current_row)
                    QMessageBox.information(self, "Success", "Product deleted successfully!")
                    self.load_data()  
                else:
                    QMessageBox.warning(self, "Warning", "Failed to get item ID!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a product to delete")

    def processSave(self):
        # Xác định danh mục từ radio button
        Categories = "Food"
        if self.Transaction.radioButton_Transport.isChecked():
            Categories = "Transport"
        elif self.Transaction.radioButton_Medicine.isChecked():
            Categories = "Medicine"
        elif self.Transaction.radioButton_Groceries.isChecked():
            Categories = "Groceries"
        elif self.Transaction.radioButton_Gift.isChecked():
            Categories = "Gift"
        elif self.Transaction.radioButton_Savings.isChecked():
            Categories = "Savings"
        elif self.Transaction.radioButton_Entertainment.isChecked():
            Categories = "Entertainment"
        elif self.Transaction.radioButton_Rent.isChecked():
            Categories = "Rent"
        Details = self.Transaction.lineEdit_Details.text().strip()
        Amount = self.Transaction.lineEdit_Amount.text().strip()
        Date = self.Transaction.lineEdit_Date.text().strip()

        #Lưu vào Mongo
        new_product = {
            "Categories": Categories,
            "Details": Details,
            "Amount": Amount,
            "Date": Date
        }
        result = collection.insert_one(new_product)
        if result.inserted_id:
            QMessageBox.information(self, "Success", "Product saved successfully!")

            # Thêm vào tableWidget
            row = self.Page1.tableWidgetProduct.rowCount()
            self.Page1.tableWidgetProduct.insertRow(row)

            self.Page1.tableWidgetProduct.setItem(row, 0, QTableWidgetItem(str(result.inserted_id)))  # Lưu ID
            self.Page1.tableWidgetProduct.setItem(row, 1, QTableWidgetItem(Categories))
            self.Page1.tableWidgetProduct.setItem(row, 2, QTableWidgetItem(Details))
            self.Page1.tableWidgetProduct.setItem(row, 3, QTableWidgetItem(str(Amount)))
            self.Page1.tableWidgetProduct.setItem(row, 4, QTableWidgetItem(Date))

        else:
            QMessageBox.warning(self, "Error", "Failed to save product. Please try again.")

