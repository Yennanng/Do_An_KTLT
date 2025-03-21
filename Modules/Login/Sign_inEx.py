import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit
from Api.Login_API import LoginAPI
from Api.Signup_API import SignupAPI
from Modules.Login.Sign_in import Ui_Login
from Modules.Transaction.Transaction import Ui_Transaction

class Login_EX(QMainWindow):
    def __init__(self):
        super().__init__()
        self.p_Login = Ui_Login()
        self.p_Login.setupUi(self)
        self.LoginAPI = LoginAPI()
        self.SignupAPI = SignupAPI()
        self.p_Transaction = Ui_Transaction()

    def setupUi(self):
        self.p_Login.pushLogin.clicked.connect(self.login)
        self.p_Login.checkShowPassword.stateChanged.connect(self.show_password)
        self.p_Login.pushSignup.clicked.connect(self.open_signup)
        self.p_Login.stackedWidget.setCurrentWidget(self.p_Login.page_Signin)
        self.p_Login.checkShowPassword_3.stateChanged.connect(self.show_password2)
        self.p_Login.pushRegister_2.clicked.connect(self.register)

    def login(self):
        """ Xử lý đăng nhập """
        username = self.p_Login.lineUserName.text().strip()
        password = self.p_Login.linePassWord.text().strip()

        login_signal = self.LoginAPI.check_user_login(username=username, password=password)

        match login_signal:
            case 1:
                QMessageBox.warning(self, "Error", "Error 1: Username or password is empty")
            case 2:
                QMessageBox.warning(self, "Error", "Error 2: User not found")
            case 3:
                QMessageBox.warning(self, "Error", "Error 3: Incorrect Username or Password")
            case 0:
                QMessageBox.information(self, "Success", "Login successful!")

    def show_password(self):
        """ Hiển thị hoặc ẩn mật khẩu """
        if self.p_Login.checkShowPassword.isChecked():
            self.p_Login.linePassWord.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.p_Login.linePassWord.setEchoMode(QLineEdit.EchoMode.Password)

    def open_signup(self):
        """ Chuyển sang trang đăng ký """
        self.p_Login.stackedWidget.setCurrentWidget(self.p_Login.page_Signup)

    def show_password2(self):
        """ Hiển thị hoặc ẩn mật khẩu trên trang đăng ký """
        if self.p_Login.checkShowPassword_3.isChecked():
            self.p_Login.linePassword_2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.p_Login.lineConfirm_2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.p_Login.linePassword_2.setEchoMode(QLineEdit.EchoMode.Password)
            self.p_Login.lineConfirm_2.setEchoMode(QLineEdit.EchoMode.Password)

    def register(self):
        """ Xử lý đăng ký """
        username = self.p_Login.lineUserName_3.text().strip()
        password = self.p_Login.linePassword_2.text().strip()
        confirm_password = self.p_Login.lineConfirm_2.text().strip()

        # Sử dụng SignupAPI để kiểm tra đăng ký
        signup_signal = self.SignupAPI.check_user_signup(username=username, password=password, repassword=confirm_password)

        match signup_signal:
            case 1:
                QMessageBox.warning(self, "Error", "Error 1: Username or password is empty")
            case 2:
                QMessageBox.warning(self, "Error", "Error 2: Passwords do not match")
            case 3:
                QMessageBox.warning(self, "Error", "Error 3: Username already exists")
            case 0:
                QMessageBox.information(self, "Success", "Registration successful!")
                self.p_Login.stackedWidget.setCurrentWidget(self.p_Login.page_Signin)  # Quay về trang đăng nhập sau khi đăng ký thành công

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login_window = Login_EX()
    login_window.setupUi()
    login_window.show()
    sys.exit(app.exec())
