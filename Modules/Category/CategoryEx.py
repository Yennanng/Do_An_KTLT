from datetime import datetime
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from Modules.Category.Category import Ui_Category
from pymongo import MongoClient
from Api.MainAPI import API



class MainWindowEx_Category(QMainWindow,API):
    def __init__(self):
        super().__init__()
        self.category = Ui_Category()
        self.category.setupUi(self)
        self.load_expense_history()
        self.connector()

    def setupUi(self):
        """Cấu hình bảng để hiển thị dữ liệu từ MongoDB."""
        self.category.table_expenses.setColumnCount(4)
        self.category.table_expenses.setHorizontalHeaderLabels([ "Categories", "Details", "Amount", "Date"])
        # self.category.table_expenses.setColumnHidden(0, True)  # Ẩn cột ID
        self.category.dateTimeEdit.setDate(QDate.currentDate())
        # Kết nối các nút với hàm tương ứng
        self.category.pushButton_Category.clicked.connect(
            lambda: self.category.stackedWidget.setCurrentWidget(self.category.page_Category1))
        self.category.pushButton_addexpenses.clicked.connect(
            lambda: self.category.stackedWidget.setCurrentWidget(self.category.page_Category2))
        self.category.pushButton_save.clicked.connect(self.save_expense)

        # Kết nối radio button với bộ lọc
        self.radio_buttons = {
            "Foods": self.category.radioButton_food,
            "Transport": self.category.radioButton_transport,
            "Medicine": self.category.radioButton_medicine,
            "Groceries": self.category.radioButton_groceries,
            "Rent": self.category.radioButton_rent,
            "Gifts": self.category.radioButton_gifts,
            "Saving": self.category.radioButton_saving,
            "Entertainment": self.category.radioButton_entertainment,
        }
        for category, button in self.radio_buttons.items():
            button.toggled.connect(lambda checked, cat=category: self.filter_data(checked, cat))

    def save_expense(self):
        """Lưu khoản chi tiêu vào MongoDB và cập nhật bảng."""
        # Xác định danh mục được chọn
        selected_category = None
        self.radio_buttons2 = {
            "Foods": self.category.radioButton_Food,
            "Transport": self.category.radioButton_Transport,
            "Medicine": self.category.radioButton_Medicine,
            "Groceries": self.category.radioButton_Groceries,
            "Rent": self.category.radioButton_Rent,
            "Gifts": self.category.radioButton_Gifts,
            "Saving": self.category.radioButton_Saving,
            "Entertainment": self.category.radioButton_Entertainment,
        }
        #cho chạy để xem cái nào dc select
        for category, button in self.radio_buttons2.items():
            if button.isChecked():
                selected_category = category
                break

        if not selected_category:
            QMessageBox.warning(self, "Error", "Please select a category!")
            return

        # Lấy dữ liệu từ các ô nhập liệu
        details = self.category.lineEdit_Details.text().strip()
        amount_text = self.category.lineEdit_Amount.text().strip()
        date_text = self.category.dateTimeEdit.dateTime().toString("dd-MM-yyyy")

        # Kiểm tra dữ liệu hợp lệ
        if not details or not amount_text or not date_text:
            QMessageBox.warning(self, "Error", "Details and Amount cannot be empty!")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a positive number!")
            return

        # Lưu vào MongoDB
        new_expense = {
            "Categories": selected_category,
            "Details": details,
            "Amount": amount,
            "Date": date_text
        }
        # add ở vị trí index 0 để tối ưu cái bước vẽ chart cột
        result = self.expenses_collection.update_one(
        {"Username1": {"$exists": True}},
        {"$push": {"Username1": {"$each": [new_expense], "$position": 0}}}
    )

        # if result.inserted_id:
        QMessageBox.information(self, "Success", "Expense saved successfully!")

        # # Thêm vào bảng giao diện
        row = self.category.table_expenses.rowCount()
        self.category.table_expenses.insertRow(row)
        document = self.expenses_collection.find_one({}, {"Username1": 1, "_id": 0})
        products = document['Username1']
        for product in products:
            self.category.table_expenses.setItem(row, 0, QTableWidgetItem(str(product["Categories"])))
            self.category.table_expenses.setItem(row, 1, QTableWidgetItem(str(product["Details"])))
            self.category.table_expenses.setItem(row, 2, QTableWidgetItem(str(product["Amount"])))
            self.category.table_expenses.setItem(row, 3, QTableWidgetItem(str(product["Date"])))
            # self.category.table_expenses.setItem(row, 4, QTableWidgetItem(date_text))

        # Xóa dữ liệu nhập sau khi lưu
        self.category.lineEdit_Details.clear()
        self.category.lineEdit_Amount.clear()
        self.category.dateTimeEdit.setDateTime(datetime.now())

            # Cập nhật danh sách chi tiêu
        self.load_expense_history()
        # else:
        #     QMessageBox.warning(self, "Error", "Failed to save expense. Please try again.")

    def load_expense_history(self, categories_filter=None):
        """Đọc dữ liệu từ MongoDB và hiển thị trên bảng."""
        # query = {"Categories": categories_filter} if categories_filter else {}
        # expenses = list(self.expenses_collection.find(query))
        # query= {"Username1": {"$elemMatch": {"Categories": categories_filter}}} if categories_filter else {}
        # expenses = list(self.expenses_collection.find(query))
        # print(expenses)
        # final_expenses=expenses[0]["Username1"] #[{"_id":"","Username1":[{},{},..]}]
        pipeline = [
            {"$match": {"Username1": {"$exists": True}}},  # Tìm document có "Rent"
            {"$project": {
                "_id": 0,  # Ẩn _id
                "Username1": {
                    "$filter": {
                        "input": "$Username1",
                        "as": "item",
                        "cond": {"$eq": ["$$item.Categories", categories_filter]}
                    }
                }
            }}
        ]

        result = list(self.expenses_collection.aggregate(pipeline))

        # Kiểm tra nếu kết quả rỗng
        if not result or "Username1" not in result[0]:
            print("No matching data found.")
            self.category.table_expenses.setRowCount(0)  # Xóa hết dữ liệu cũ nếu không có dữ liệu mới
            return
        else:
            print(result)
            final_expenses=result[0]["Username1"] #[{"_id":"","Username1":[{},{}}]}]
            # print(final_expenses)
            self.category.table_expenses.setRowCount(len(final_expenses))
        for row, expense in enumerate(final_expenses):
            print(row,expense)
            self.category.table_expenses.setItem(row, 0, QTableWidgetItem(str(expense["Categories"])))
            self.category.table_expenses.setItem(row, 1, QTableWidgetItem(expense["Details"]))
            self.category.table_expenses.setItem(row, 2, QTableWidgetItem(str(expense["Amount"])))
            self.category.table_expenses.setItem(row, 3, QTableWidgetItem(str(expense["Date"])))
            # self.category.table_expenses.setItem(row, 4, QTableWidgetItem(str(products["Date"])))

    def filter_data(self, checked, category):
        """Lọc dữ liệu theo danh mục."""
        if checked:
            self.load_expense_history(categories_filter=category)
        else:
            self.load_expense_history()