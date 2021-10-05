from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QTextEdit, QPushButton, QScrollArea, \
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QRect


class SimulationOutputTab(QWidget):
    """
    Creates the contents of a tab which displays all kinds of useful outputs from the simulation or simulations
    """
    def __init__(self):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.scrollArea.setVisible(True)

        self.tableWidget = QTableWidget(4,3)
        self.data = {'col1': ['1', '2', '3', '4'],
                'col2': ['1', '2', '1', '3'],
                'col3': ['1', '1', '2', '1']}

        self.setData()
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.show()
        self.gridLayout = QGridLayout(self.scrollArea)
        self.gridLayout.addWidget(self.tableWidget)

        self.tabLayout = QHBoxLayout()
        self.tabLayout.addWidget(self.scrollArea)
        self.setLayout(self.tabLayout)

    def setData(self):
        # loops through all data in the dictionary and adds it to the tabel widget, sets the horizontal headers to the titles of each dictionary key
        horizontalHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horizontalHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.tableWidget.setItem(m, n, newitem)
        self.tableWidget.setHorizontalHeaderLabels(horizontalHeaders)