from PyQt5 import QtWidgets
from view.view import Ui_MainWindow
from controller.foodManager import FoodManager
import sys

if __name__ == "__main__":
    model = FoodManager()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setModel(model)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

