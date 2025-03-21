from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from Modules.Category.CategoryEx import MainWindowEx_Category
from Modules.Transaction.TransactionEx import MainWindowEx_Transaction
from Modules.Login.Sign_inEx import Login_EX
from Modules.Home.Home_Ex import HomeExt
from Modules.Account.Account_Ex import MainWindowEx_Account

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1080, 720)

        # Tạo stackedWidget để quản lý các trang
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Khởi tạo cửa sổ danh mục, giao dịch và đăng nhập
        self.login_window = Login_EX()
        self.category_window = MainWindowEx_Category()
        self.transaction_window = MainWindowEx_Transaction()
        self.home_window = HomeExt()
        self.account_window = MainWindowEx_Account()

        # Thêm vào stackedWidget
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.category_window)
        self.stacked_widget.addWidget(self.transaction_window)
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.addWidget(self.account_window)
        # Mặc định hiển thị trang đăng nhập
        self.stacked_widget.setCurrentWidget(self.login_window)
        if hasattr(self.login_window.p_Login, "page_Signin"):
            self.login_window.p_Login.stackedWidget.setCurrentWidget(self.login_window.p_Login.page_Signin)

        # Gọi hàm open_login sau khi mở trang đăng nhập
        self.open_login()

        # Kiểm tra nếu nút có tồn tại trước khi kết nối sự kiện
        if hasattr(self.home_window, "pushButton_Transaction_2"):
            self.home_window.pushButton_Transaction_2.clicked.connect(self.open_transaction)
        if hasattr(self.home_window, "pushButton_Account"):
            self.home_window.pushButton_Account.clicked.connect(self.open_account)
        if hasattr(self.home_window, "pushButton_Category"):
            self.home_window.pushButton_Category.clicked.connect(self.open_category)
        if hasattr(self.category_window.category, "pushButton_Transaction"):
            self.category_window.category.pushButton_Transaction.clicked.connect(self.open_transaction)
        if hasattr(self.category_window.category, "pushButton_Home"):
            self.category_window.category.pushButton_Home.clicked.connect(self.open_home)
        if hasattr(self.category_window.category, "pushButton_Home"):
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
        if hasattr(self.login_window.p_Login, "pushLogin"):
            self.login_window.p_Login.pushLogin.clicked.connect(self.open_home)

    def open_transaction(self):
        """ Chuyển sang trang Transaction """
        self.stacked_widget.setCurrentWidget(self.transaction_window)
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
        self.stacked_widget.setCurrentWidget(self.home_window)

    def open_account(self):
        self.stacked_widget.setCurrentWidget(self.account_window)

    def handle_login(self):
        """ Xử lý khi nút đăng nhập được bấm """
        login_signal = self.login_window.p_Login.login()

        if login_signal == 0:
            self.open_home()


app=QApplication([])
myWindow=MainWindow()
myWindow.show()
app.exec()

