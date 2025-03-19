from PyQt6 import QtWidgets
import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Modules.Transaction.Transaction import Ui_Transaction
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chi_tieu"]
collection = db["database"]


class MainWindowEx_Transaction(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.p_Transaction = Ui_Transaction()
        self.p_Transaction.setupUi(self)

    def setupUi(self):
        self.p_Transaction.tableWidgetProduct.setColumnCount(5)
        self.p_Transaction.tableWidgetProduct.setHorizontalHeaderLabels(
            ["Id", "Categories", "Details", "Amount", "Date"])
        self.p_Transaction.tableWidgetProduct.setColumnHidden(0, True)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(1, 150)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(2, 150)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(3, 150)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(4, 150)
        self.p_Transaction.pushButton_Transaction_2.clicked.connect(
            lambda: self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction1))
        self.load_data()
        self.p_Transaction.dateTimeEdit.setDate(QDate.currentDate())
        self.p_Transaction.pushButton_Edit.setEnabled(False)
        self.p_Transaction.tableWidgetProduct.itemSelectionChanged.connect(self.enable_edit_button)
        self.p_Transaction.pushButton_Edit.clicked.connect(self.open_edit_page)
        self.p_Transaction.pushButton_Delete.clicked.connect(self.Delete)
        self.p_Transaction.pushButton_save_2.clicked.connect(self.process_update)

    def enable_edit_button(self):
        self.p_Transaction.pushButton_Edit.setEnabled(bool(self.p_Transaction.tableWidgetProduct.selectedItems()))

    def open_edit_page(self):
        current_row = self.p_Transaction.tableWidgetProduct.currentRow()
        if current_row >= 0:
            self.selected_id = self.p_Transaction.tableWidgetProduct.item(current_row, 0).text()
            self.p_Transaction.lineEdit_Details.setText(
                self.p_Transaction.tableWidgetProduct.item(current_row, 2).text())
            self.p_Transaction.lineEdit_Amount.setText(
                self.p_Transaction.tableWidgetProduct.item(current_row, 3).text())
            self.p_Transaction.dateTimeEdit.setDate(
                QDate.fromString(self.p_Transaction.tableWidgetProduct.item(current_row, 4).text(), "dd-MM-yyyy"))

            category = self.p_Transaction.tableWidgetProduct.item(current_row, 1).text().strip()
            self.set_category_radio(category)

            self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction2)

    def set_category_radio(self, category):
        category_map = {
            "Food": self.p_Transaction.radioButton_Food,
            "Transport": self.p_Transaction.radioButton_Transport,
            "Medicine": self.p_Transaction.radioButton_Medicine,
            "Groceries": self.p_Transaction.radioButton_Groceries,
            "Rent": self.p_Transaction.radioButton_Rent,
            "Gifts": self.p_Transaction.radioButton_Gifts,
            "Saving": self.p_Transaction.radioButton_Saving,
            "Entertainment": self.p_Transaction.radioButton_Entertainment
        }
        for key, button in category_map.items():
            button.setChecked(key == category)

    def process_update(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Warning", "Please select an item to update!")
            return

        new_details = self.p_Transaction.lineEdit_Details.text().strip()
        new_amount = self.p_Transaction.lineEdit_Amount.text().strip()
        new_date = self.p_Transaction.dateTimeEdit.date().toString("dd-MM-yyyy")

        selected_category = None
        category_map = {
            "Food": self.p_Transaction.radioButton_Food,
            "Transport": self.p_Transaction.radioButton_Transport,
            "Medicine": self.p_Transaction.radioButton_Medicine,
            "Groceries": self.p_Transaction.radioButton_Groceries,
            "Rent": self.p_Transaction.radioButton_Rent,
            "Gifts": self.p_Transaction.radioButton_Gifts,
            "Saving": self.p_Transaction.radioButton_Saving,
            "Entertainment": self.p_Transaction.radioButton_Entertainment
        }
        for key, button in category_map.items():
            if button.isChecked():
                selected_category = key
                break

        if not new_details or not new_amount:
            QMessageBox.warning(self, "Error", "Details and Amount cannot be empty!")
            return

        try:
            amount = float(new_amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a positive number!")
            return

        collection.update_one({"_id": ObjectId(self.selected_id)},
                              {"$set": {"Categories": selected_category, "Details": new_details, "Amount": amount,
                                        "Date": new_date}})

        self.load_data()
        QMessageBox.information(self, "Success", "Expense updated successfully!")
        self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction1)

    def load_data(self):
        products = list(collection.find({}))
        self.p_Transaction.tableWidgetProduct.setRowCount(len(products))
        for row, product in enumerate(products):
            self.p_Transaction.tableWidgetProduct.setItem(row, 0, QTableWidgetItem(str(product["_id"])))
            self.p_Transaction.tableWidgetProduct.setItem(row, 1, QTableWidgetItem(product["Categories"]))
            self.p_Transaction.tableWidgetProduct.setItem(row, 2, QTableWidgetItem(product["Details"]))
            self.p_Transaction.tableWidgetProduct.setItem(row, 3, QTableWidgetItem(str(product["Amount"])))
            self.p_Transaction.tableWidgetProduct.setItem(row, 4, QTableWidgetItem(str(product["Date"])))

    def Delete(self):
        current_row = self.p_Transaction.tableWidgetProduct.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, "Delete Confirmation", "Are you sure?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                selected_id = self.p_Transaction.tableWidgetProduct.item(current_row, 0).text()
                collection.delete_one({"_id": ObjectId(selected_id)})
                self.p_Transaction.tableWidgetProduct.removeRow(current_row)
                QMessageBox.information(self, "Success", "Product deleted successfully!")
                self.load_data()
        else:
            QMessageBox.warning(self, "Warning", "Please select a product to delete")