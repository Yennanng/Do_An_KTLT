from PyQt6.QtWidgets import QApplication, QMainWindow
from Api.Transaction import MainWindowEx
# from Api.CategoryEx import MainWindowExt
app=QApplication([])
myWindow=MainWindowEx()
myWindow.setupUi()
myWindow.show()
app.exec()