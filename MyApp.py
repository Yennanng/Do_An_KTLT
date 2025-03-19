from PyQt6.QtWidgets import QApplication, QMainWindow

from Modules.Category.CategoryEx import MainWindowEx_Category
from Modules.Transaction.TransactionEx import MainWindowEx_Transaction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1080, 720)

        # Khởi tạo cửa sổ quản lý danh mục (Category)
        self.category_window = MainWindowEx_Category()
        self.category_window.setupUi()
        self.setCentralWidget(self.category_window.category)

        # Kết nối sự kiện chuyển qua trang Transaction
        self.category_window.category.pushButton_Transaction.clicked.connect(self.open_transaction)

    def open_transaction(self):
        # Mở cửa sổ giao dịch (Transaction) với đầy đủ chức năng
        self.transaction_window = MainWindowEx_Transaction()
        self.transaction_window.setupUi()
        self.transaction_window.show()
        self.hide()  # Ẩn cửa sổ hiện tại (Category)

app=QApplication([])
myWindow=MainWindowEx_Transaction()
myWindow.setupUi()
myWindow.show()
app.exec()
