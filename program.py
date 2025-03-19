import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from Modules.Login.Sign_inEx import Sign_inEX

app=QApplication([])
myWindow=Sign_inEX()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()

# app = QApplication(sys.argv)
# MainWindow = Sign_inEX()
# MainWindow.show()
# sys.exit(app.exec())