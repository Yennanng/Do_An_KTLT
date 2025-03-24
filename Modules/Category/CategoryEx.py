from datetime import datetime
from traceback import TracebackException

from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from Modules.Category.Category import Ui_Category
from Api.MainAPI import API

class MainWindowEx_Category(QMainWindow,API):
    def __init__(self,using_user=None):
        super().__init__()
        self.category = Ui_Category()
        self.API = API()
        self.category.setupUi(self)
        self.using_user = using_user
        self.load_expense_history()
        self.connector()
        self.update_balance()
        self.update_income_saving()
        self.update_total()
        self.category.pushButton_Category.clicked.connect(
            lambda: self.category.stackedWidget.setCurrentWidget(self.category.page_Category1))
        self.category.pushButton_addexpenses.clicked.connect(
            lambda: self.category.stackedWidget.setCurrentWidget(self.category.page_Category2))
        self.category.pushButton_save.clicked.connect(self.save_expense)
    def setupUi(self):
        self.category.table_expenses.setColumnCount(4)
        self.category.table_expenses.setHorizontalHeaderLabels([ "Categories", "Details", "Amount", "Date"])
        # self.category.table_expenses.setColumnHidden(0, True)  # Ẩn cột ID
        self.category.dateEdit.setDate(QDate.currentDate())
        # Kết nối các nút với hàm tương ứng


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)
        self.timer.start(5000)

    def update_all(self):
        """Gọi cả 3 hàm cập nhật cùng lúc"""
        self.update_income_saving()
        self.update_total()
        self.update_balance()
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
        date_text = self.category.dateEdit.dateTime().toString("MM-dd-yyyy")

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
        {f"{self.using_user}": {"$exists": True}},
        {"$push": {f"{self.using_user}": {"$each": [new_expense], "$position": 0}}}
    )

        # if result.inserted_id:
        QMessageBox.information(self, "Success", "Expense saved successfully!")

        # # Thêm vào bảng giao diện
        row = self.category.table_expenses.rowCount()
        self.category.table_expenses.insertRow(row)
        pipeline = [
            {"$match": {self.using_user: {"$exists": True}}},  # Chỉ tìm document có key là username
            {"$project": {self.using_user: 1, "_id": 0}}  # Chỉ lấy dữ liệu của username đó
        ]
        document = list(self.expenses_collection.aggregate(pipeline))
        products = document[0][self.using_user]
        for product in products:
            self.category.table_expenses.setItem(row, 0, QTableWidgetItem(str(product["Categories"])))
            self.category.table_expenses.setItem(row, 1, QTableWidgetItem(str(product["Details"])))
            self.category.table_expenses.setItem(row, 2, QTableWidgetItem(str(product["Amount"])))
            self.category.table_expenses.setItem(row, 3, QTableWidgetItem(str(product["Date"])))

        # Xóa dữ liệu nhập sau khi lưu
        self.category.lineEdit_Details.clear()
        self.category.lineEdit_Amount.clear()
        self.category.dateEdit.setDateTime(datetime.now())

            # Cập nhật danh sách chi tiêu
        self.load_expense_history()

    def load_expense_history(self, categories_filter=None):
        """Đọc dữ liệu từ MongoDB và hiển thị trên bảng."""
        pipeline = [
            {"$match": {f"{self.using_user}": {"$exists": True}}},  # Tìm document có "Rent"
            {"$project": {
                "_id": 0,  # Ẩn _id
                f"{self.using_user}": {
                    "$filter": {
                        "input": f"${self.using_user}",
                        "as": "item",
                        "cond": {"$eq": ["$$item.Categories", categories_filter]}
                    }
                }
            }}
        ]

        result = list(self.expenses_collection.aggregate(pipeline))

        # Kiểm tra nếu kết quả rỗng
        if not result or f"{self.using_user}" not in result[0]:
            print("No matching data found.")
            self.category.table_expenses.setRowCount(0)  # Xóa hết dữ liệu cũ nếu không có dữ liệu mới
            return
        else:
            final_expenses=result[0][f"{self.using_user}"] #[{"_id":"","Username1":[{},{}}]}]
            self.category.table_expenses.setRowCount(len(final_expenses))
        for row, expense in enumerate(final_expenses):
            # print(row,expense)
            self.category.table_expenses.setItem(row, 0, QTableWidgetItem(str(expense["Categories"])))
            self.category.table_expenses.setItem(row, 1, QTableWidgetItem(expense["Details"]))
            self.category.table_expenses.setItem(row, 2, QTableWidgetItem(str(expense["Amount"])))
            self.category.table_expenses.setItem(row, 3, QTableWidgetItem(str(expense["Date"])))

    def filter_data(self, checked, category):
        """Lọc dữ liệu theo danh mục."""
        if checked:
            self.load_expense_history(categories_filter=category)
        else:
            self.load_expense_history()

    def update_income_saving(self):
        """Lấy income và saving từ MongoDB và cập nhật lên giao diện."""
        user_data = self.users_collection.find_one({"username": self.using_user}, {"income": 1, "_id": 0})

        if user_data:
            income = user_data.get("income", 0)

            self.category.label_setincome.setText(f"{income}")
        else:
            self.category.label_setincome.setText("Income: N/A")

    def update_total(self):
        """Tính tổng Amount của người dùng và cập nhật vào label_setexpense"""
        pipeline = [
            {"$unwind": f"${self.using_user}"},
            {"$group": {"_id": None, "total_expenses": {"$sum": f"${self.using_user}.Amount"}}}
        ]

        total_expenses = list(self.expenses_collection.aggregate(pipeline))

        if total_expenses:  # Kiểm tra xem có dữ liệu không
            total_expenses_value = total_expenses[0]["total_expenses"]
            self.category.label_setexpense.setText(f"{total_expenses_value}")  # Chuyển thành chuỗi trước khi setText
        else:
            self.category.label_setexpense.setText("0")  # Nếu không có dữ liệu, hiển thị 0
    def update_balance(self):
        """Tính Balance = Income - Expense và cập nhật vào label_setmybalance"""

        # Lấy giá trị từ label_setincome và label_setexpense, nếu rỗng thì mặc định là 0
        income_text = self.category.label_setincome.text().strip()
        expense_text = self.category.label_setexpense.text().strip()

        # Chuyển đổi sang số (mặc định là 0 nếu không hợp lệ)
        income = float(income_text) if income_text.replace('.', '', 1).isdigit() else 0
        expense = float(expense_text) if expense_text.replace('.', '', 1).isdigit() else 0

        # Tính toán Balance
        balance = income - expense

        # Cập nhật vào label_setmybalance
        self.category.label_setmybalance.setText(f"{balance}")



