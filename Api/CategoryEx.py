from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from Modules.Category.Category import Ui_Category
from Modules.Category.Category_Addexpenses import Ui_add
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chi_tieu"]
collection = db["database"]


class MainWindowExt(QMainWindow):
    PATH = "data/database.json"

    def __init__(self):
        super().__init__()
        self.category = Ui_Category()
        self.add_expenses = Ui_add()
        self.category.setupUi(self)
        self.load_expense_history()
        self.setupUi()

    def setupUi(self):
        """Cấu hình bảng để hiển thị dữ liệu từ MongoDB."""
        self.category.table_expenses.setColumnCount(5)
        self.category.table_expenses.setHorizontalHeaderLabels(["Id", "Categories", "Details", "Amount", "Date"])
        self.category.table_expenses.setColumnHidden(0, True)

        """Kết nối các nút với hàm lọc dữ liệu chung."""
        self.category.pushButton_addexpenses.clicked.connect(self.show_add_expenses)

        radio_buttons = {
            "Food": self.category.radioButton_food,
            "Transport": self.category.radioButton_transport,
            "Medicine": self.category.radioButton_medicine,
            "Groceries": self.category.radioButton_groceries,
            "Rent": self.category.radioButton_rent,
            "Gifts": self.category.radioButton_gifts,
            "Saving": self.category.radioButton_saving,
            "Entertainment": self.category.radioButton_entertainment,
        }

        for category, button in radio_buttons.items():
            if hasattr(self.category, f'radioButton_{category.lower()}'):
                button.toggled.connect(lambda checked, cat=category: self.filter_data(checked, cat))

    def show_add_expenses(self):
        self.add_expenses_window = QMainWindow()
        self.add_expenses.setupUi(self.add_expenses_window)
        self.add_expenses.pushButton_save.clicked.connect(self.save_expense)
        self.add_expenses_window.show()

    def save_expense(self):
        self.show()
        self.add_expenses_window.close()
        self.load_expense_history()
        
    def load_expense_history(self, categories_filter=None):
        """Đọc dữ liệu từ MongoDB và hiển thị trên bảng"""
        query = {"Categories": categories_filter} if categories_filter else {}
        products = list(collection.find(query))
        self.category.table_expenses.setRowCount(len(products))
        for row, product in enumerate(products):
            self.category.table_expenses.setItem(row, 0, QTableWidgetItem(str(product["_id"])))
            self.category.table_expenses.setItem(row, 1, QTableWidgetItem(product["Categories"]))
            self.category.table_expenses.setItem(row, 2, QTableWidgetItem(product["Details"]))
            self.category.table_expenses.setItem(row, 3, QTableWidgetItem(str(product["Amount"])))
            self.category.table_expenses.setItem(row, 4, QTableWidgetItem(str(product["Date"])))

    def filter_data(self, checked, category):
        if checked:
            self.load_expense_history(categories_filter=category)
        else:
            self.load_expense_history()
