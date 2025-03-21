import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
# from Modules.Login.Sign_inEx import Sign_inEX
from Modules.Home.Home_Ex import HomeExt

app=QApplication([])
myWindow=HomeExt()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()

# app = QApplication(sys.argv)
# MainWindow = Sign_inEX()
# MainWindow.show()
# sys.exit(app.exec())