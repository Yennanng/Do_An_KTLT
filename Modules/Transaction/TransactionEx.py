from PyQt6.QtCore import QDate, QTimer
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QApplication
from Modules.Transaction.Transaction import Ui_Transaction
from Api.MainAPI import API

class MainWindowEx_Transaction(QMainWindow, API):
    def __init__(self,using_user=None):
        super().__init__()
        self.connector()
        self.p_Transaction = Ui_Transaction()
        self.p_Transaction.setupUi(self)
        self.using_user = using_user
        self.API = API()
        self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction1)
        self.update_balance()
        self.update_income_saving()
        self.update_total()

        self.p_Transaction.pushButton_Transaction.clicked.connect(
            lambda: self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction1))
        self.p_Transaction.dateEdit.setDate(QDate.currentDate())
        self.p_Transaction.pushButton_Edit.setEnabled(False)
        self.p_Transaction.tableWidgetProduct.itemSelectionChanged.connect(self.enable_edit_button)
        self.p_Transaction.pushButton_Edit.clicked.connect(self.open_edit_page)
        self.p_Transaction.pushButton_Delete.clicked.connect(self.Delete)
        self.p_Transaction.pushButton_save_2.clicked.connect(self.process_update)
    def setupUi(self):
        self.p_Transaction.tableWidgetProduct.setColumnCount(4)
        self.p_Transaction.tableWidgetProduct.setHorizontalHeaderLabels(
            ["Categories", "Details", "Amount", "Date"])
        self.p_Transaction.tableWidgetProduct.setColumnWidth(0, 200)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(1, 200)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(2, 200)
        self.p_Transaction.tableWidgetProduct.setColumnWidth(3, 200)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)
        self.timer.start(5000)

        self.load_data()
    def update_all(self):
        """Gọi cả 3 hàm cập nhật cùng lúc"""
        self.update_income_saving()
        self.update_total()
        self.update_balance()
    def enable_edit_button(self):
        self.p_Transaction.pushButton_Edit.setEnabled(bool(self.p_Transaction.tableWidgetProduct.selectedItems()))

    def open_edit_page(self):
        current_row = self.p_Transaction.tableWidgetProduct.currentRow()
        if current_row >= 0:
            self.p_Transaction.lineEdit_Details.setText(
                self.p_Transaction.tableWidgetProduct.item(current_row, 1).text())
            self.p_Transaction.lineEdit_Amount.setText(
                self.p_Transaction.tableWidgetProduct.item(current_row, 2).text())
            self.p_Transaction.dateEdit.setDate(
                QDate.fromString(self.p_Transaction.tableWidgetProduct.item(current_row, 3).text(), "MM-dd-yyyy"))

            self.category = self.p_Transaction.tableWidgetProduct.item(current_row, 0).text().strip()
            self.set_category_radio(self.category)
            self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction2)

    def set_category_radio(self, category):
        category_map = {
            "Foods": self.p_Transaction.radioButton_Food,
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
        current_row = self.p_Transaction.tableWidgetProduct.currentRow()
        # global current_row
        if not self.category:
            QMessageBox.warning(self, "Warning", "Please select an item to update!")
            return

        new_details = self.p_Transaction.lineEdit_Details.text().strip()
        new_amount = self.p_Transaction.lineEdit_Amount.text().strip()
        new_date = self.p_Transaction.dateEdit.date().toString("MM-dd-yyyy")

        selected_category = None
        category_map = {
            "Foods": self.p_Transaction.radioButton_Food,
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

        self.expenses_collection.update_one(
            {f"{self.using_user}": {"$exists": True}},  # Điều kiện tìm kiếm
            {"$set": {f"{self.using_user}.{current_row}": {
                "Categories": selected_category,
                "Details": new_details,
                "Amount": amount,
                "Date": new_date
            }}}
        )

        self.load_data()
        QMessageBox.information(self, "Success", "Expense updated successfully!")
        self.p_Transaction.stackedWidget.setCurrentWidget(self.p_Transaction.page_Transaction1)

    def load_data(self):
        try:
            pipeline = [
                {"$match": {self.using_user: {"$exists": True}}},  # Chỉ tìm document có key là username
                {"$project": {self.using_user: 1, "_id": 0}}  # Chỉ lấy dữ liệu của username đó
            ]
            document = list(self.expenses_collection.aggregate(pipeline))
            products = document[0][self.using_user]

            self.p_Transaction.tableWidgetProduct.setRowCount(len(products))

            for row, product in enumerate(products):
                self.p_Transaction.tableWidgetProduct.setItem(row, 0, QTableWidgetItem(str(product["Categories"])))
                self.p_Transaction.tableWidgetProduct.setItem(row, 1, QTableWidgetItem(str(product["Details"])))
                self.p_Transaction.tableWidgetProduct.setItem(row, 2, QTableWidgetItem(str(product["Amount"])))
                self.p_Transaction.tableWidgetProduct.setItem(row, 3, QTableWidgetItem(str(product["Date"])))
        except:
            pass

    def Delete(self):
        current_row = self.p_Transaction.tableWidgetProduct.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, "Delete Confirmation", "Are you sure?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Biến 1 cái element trong array thành null
                self.expenses_collection.update_one(
                    {},
                    {"$unset": {f"{self.using_user}.{current_row}": 1}}
                )
                #Xoa cai null element đó
                self.expenses_collection.update_one(
                    {},
                    {"$pull": {f"{self.using_user}": None}}
                )
                # self.p_Transaction.tableWidgetProduct.removeRow(current_row)
                QMessageBox.information(self, "Success", "Product deleted successfully!")

                self.load_data()
        else:
            QMessageBox.warning(self, "Warning", "Please select a product to delete")

    def update_income_saving(self):
        """Lấy income và saving từ MongoDB và cập nhật lên giao diện."""
        user_data = self.users_collection.find_one({"username": self.using_user}, {"income": 1, "_id": 0})
        if user_data:
            income = user_data.get("income", 0)

            self.p_Transaction.label_setincome.setText(f"{income}")
        else:
            self.p_Transaction.label_setincome.setText("Income: N/A")

    def update_total(self):
        """Tính tổng Amount của người dùng và cập nhật vào label_setexpense"""
        pipeline = [
            {"$unwind": f"${self.using_user}"},
            {"$group": {"_id": None, "total_expenses": {"$sum": f"${self.using_user}.Amount"}}}
        ]

        total_expenses = list(self.expenses_collection.aggregate(pipeline))

        if total_expenses:
            total_expenses_value = total_expenses[0]["total_expenses"]
            self.p_Transaction.label_setexpense.setText(f"{total_expenses_value}")
        else:
            self.p_Transaction.label_setexpense.setText("0")

    def update_balance(self):
        """Tính Balance = Income - Expense và cập nhật vào label_setmybalance"""

        # Lấy giá trị từ label_setincome và label_setexpense, nếu rỗng thì mặc định là 0
        income_text = self.p_Transaction.label_setincome.text().strip()
        expense_text = self.p_Transaction.label_setexpense.text().strip()

        # Chuyển đổi sang số (mặc định là 0 nếu không hợp lệ)
        income = float(income_text) if income_text.replace('.', '', 1).isdigit() else 0
        expense = float(expense_text) if expense_text.replace('.', '', 1).isdigit() else 0

        # Tính toán Balance
        balance = income - expense

        # Cập nhật vào label_setmybalance
        self.p_Transaction.label_setmybalance.setText(f"{balance}")