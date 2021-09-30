from Gui.gui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    print("hi")