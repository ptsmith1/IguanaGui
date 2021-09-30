import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
    def keyPressEvent(self, event):
        print("hiya")

app = QApplication(sys.argv)
demo = MainWindow()
demo.show()
sys.exit(app.exec_())