from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from Modules.Category.CategoryEx import MainWindowEx_Category
from Modules.Transaction.TransactionEx import MainWindowEx_Transaction
from Modules.Login.Sign_inEx import Login_EX
from Modules.Home.Home_Ex import HomeExt
from Modules.Account.Account_Ex import MainWindowEx_Account
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1080, 720)
        self.current_user = None

        # Tạo stackedWidget để quản lý các trang
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # # Khởi tạo cửa sổ đăng nhập trước
        self.login_window = Login_EX()
        self.stacked_widget.addWidget(self.login_window)
        self.open_login()
        if hasattr(self.login_window.p_Login, "pushLogin"):
            self.login_window.p_Login.pushLogin.clicked.connect(self.handle_login)

    def connect_navigation_buttons(self):
        # Kiểm tra nếu nút có tồn tại trước khi kết nối sự kiện
        if hasattr(self.home_window, "pushButton_Transaction"):
            self.home_window.pushButton_Transaction.clicked.connect(self.open_transaction)
        if hasattr(self.home_window, "pushButton_Account"):
            self.home_window.pushButton_Account.clicked.connect(self.open_account)
        if hasattr(self.home_window, "pushButton_Category"):
            self.home_window.pushButton_Category.clicked.connect(self.open_category)
        if hasattr(self.category_window.category, "pushButton_Transaction"):
            self.category_window.category.pushButton_Transaction.clicked.connect(self.open_transaction)
        if hasattr(self.category_window.category, "pushButton_Home"):
            self.category_window.category.pushButton_Home.clicked.connect(self.open_home)
        if hasattr(self.category_window.category, "pushButton_Account"):
            self.category_window.category.pushButton_Account.clicked.connect(self.open_account)
        if hasattr(self.transaction_window.p_Transaction, "pushButton_Home"):
            self.transaction_window.p_Transaction.pushButton_Home.clicked.connect(self.open_home)
        if hasattr(self.transaction_window.p_Transaction, "pushButton_Category"):
            self.transaction_window.p_Transaction.pushButton_Category.clicked.connect(self.open_category)
        if hasattr(self.transaction_window.p_Transaction, "pushButton_Account"):
            self.transaction_window.p_Transaction.pushButton_Account.clicked.connect(self.open_account)
        if hasattr(self.account_window.account, "pushButton_Transaction"):
            self.account_window.account.pushButton_Transaction.clicked.connect(self.open_transaction)
        if hasattr(self.account_window.account, "pushButton_Category"):
            self.account_window.account.pushButton_Category.clicked.connect(self.open_category)
        if hasattr(self.account_window.account, "pushButton_Home"):
            self.account_window.account.pushButton_Home.clicked.connect(self.open_home)


    def open_transaction(self):
        """ Chuyển sang trang Transaction """
        self.stacked_widget.setCurrentWidget(self.transaction_window) #mặc định cái bảng trước
        self.transaction_window.setupUi()

    def open_category(self):
        """ Chuyển về trang Category và chạy các chức năng """
        self.stacked_widget.setCurrentWidget(self.category_window)
        self.category_window.setupUi()

    def open_login(self):
        """ Chuyển về trang đăng nhập """
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.login_window.setupUi()

    def open_home(self):
        """ Chuyển sang trang Home và cập nhật thông tin người dùng """
        self.stacked_widget.setCurrentWidget(self.home_window)
    def open_account(self):
        self.stacked_widget.setCurrentWidget(self.account_window)

    def handle_login(self):
        """ Xử lý khi nút đăng nhập được bấm """
        username=self.login_window.p_Login.lineUserName.text().strip()
        if self.login_window.login() == username:
            self.current_user=username
            # Khởi tạo các trang chính kèm username
            self.home_window = HomeExt(self.current_user)
            self.transaction_window = MainWindowEx_Transaction(self.current_user)
            self.category_window = MainWindowEx_Category(self.current_user)
            self.account_window = MainWindowEx_Account(self.current_user)

            # Thêm vào stacked_widget
            self.stacked_widget.addWidget(self.home_window)
            self.stacked_widget.addWidget(self.transaction_window)
            self.stacked_widget.addWidget(self.category_window)
            self.stacked_widget.addWidget(self.account_window)

            # Gắn các nút điều hướng
            self.connect_navigation_buttons()
            self.open_home()

app=QApplication([])
myWindow=MainWindow()
myWindow.show()
app.exec()

