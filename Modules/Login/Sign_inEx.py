from Modules.Login.Sign_in import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit, QLabel, QPushButton, QVBoxLayout, QDialog
from Api.Login_API import LoginAPI
from Modules.Sign_up.Sign_upEX import Sign_upEx

class Sign_inEX(Ui_MainWindow,LoginAPI):
    # def __init__(self,LoginAPI):
    #     super().__init__()
    #     self.LoginAPI = LoginAPI
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.Sign_up=Sign_upEx()
        self.pushLogin.clicked.connect(self.Login)
        self.checkShowPassword.stateChanged.connect(self.show_password)
        self.pushSignup.clicked.connect(self.open_Signup)

    def Login(self):
        username = self.lineUserName.text()
        password = self.linePassWord.text()

        login_signal= self.check_user_login(username=username,password=password)
        match login_signal:
            case  1:
                QMessageBox.warning(self.MainWindow,"Error","Error 1: Username or password is empty")
            case 2:
                QMessageBox.warning(self.MainWindow,"Error","Error 2: User not found")
            case 3:
                QMessageBox.warning(self.MainWindow,"Error","Error 3: Incorrect Username or Password")
            case _:
                pass #chỗ này sẽ kết nối tiếp vào trang Home
        
    def show_password(self):
        if self.checkShowPassword.isChecked():
            self.linePassWord.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.linePassWord.setEchoMode(QLineEdit.EchoMode.Password)

    def open_Signup(self):
        self.Sign_up_Window = QMainWindow()
        self.Sign_up.setupUi(self.Sign_up_Window)
        self.Sign_up_Window.show()
        self.MainWindow.hide()

    def show(self):
        self.MainWindow.show()

