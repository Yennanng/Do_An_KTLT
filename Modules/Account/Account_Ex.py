from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from Api.MainAPI import API
from Modules.Account.Account import Ui_Account

class MainWindowEx_Account(QMainWindow, API):
    def __init__(self, using_user=None, category_window=None):
        super().__init__()
        self.account = Ui_Account()
        self.account.setupUi(self)
        self.using_user = using_user
        self.API = API()
        self.category_window = category_window  # Tham chiếu đến cửa sổ Category

        self.account.label_username.setText(using_user)
        self.account.label_nameaccount.setText(using_user)

        # Kết nối nút Save
        self.account.pushButton_Save.clicked.connect(self.save)
        self.account.pushButton_Exit.clicked.connect(self.exit)


    def save(self):
        """Lưu thông tin income vào MongoDB và cập nhật giao diện"""
        income = self.account.lineEdit_month_income.text().strip()
        saving = self.account.lineEdit_target_saving.text().strip()
        birthday = self.account.dateEdit_Birthday.date().toString("MM-dd-yyyy")

        # Kiểm tra birthday có đúng định dạng mm-dd-yyy không
        try:
            datetime.strptime(birthday, "%m-%d-%Y")  # Nếu lỗi, sẽ vào except
        except ValueError:
            QMessageBox.warning(self, "Error", "Birthday must be in mm-dd-yyyy format!")
            return  # Dừng hàm nếu ngày sinh không hợp lệ


        # Kiểm tra income và saving có phải số hợp lệ không
        if not (income.replace(".", "", 1).isdigit() and saving.replace(".", "", 1).isdigit()):
            QMessageBox.warning(self, "Lỗi", "Income và Saving must be valid number!")
            return  # Dừng hàm nếu dữ liệu không hợp lệ

        # Chuyển về kiểu số
        income = float(income)
        saving = float(saving)

        # Cập nhật vào MongoDB
        self.users_collection.update_one(
            {"username": self.using_user},  # Điều kiện tìm kiếm
            {"$set": {
                "income": income,
                "birthday": birthday,
                "saving": saving
            }}
        )

        QMessageBox.information(self, "Success", "Data updated successfully!")

    def exit(self):
        confirm = QMessageBox.question(
            self, "Exit", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()
