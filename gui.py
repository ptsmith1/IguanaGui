from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QTextBrowser, QHBoxLayout, QVBoxLayout, QTabWidget, QMenu, QAction, QFileDialog,\
    QSizePolicy, QMessageBox, QScrollArea, QTextEdit, QStyle, QListWidget
from PyQt5.QtCore import QSize, QEvent
from PyQt5.QtGui import QPixmap, QImage, QPalette, QIcon, QTextLayout, QFont
from PyQt5.Qt import Qt
import sys
from simulationSetup import InputTab
from simulationOutputTab import SimulationOutputTab


class MainWindow(QMainWindow):
    """
    This is the main class for the UI
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Iguana")
        self.resize(760,600)
        self.shiftDown = False

        # create menu

        self.createActions()
        self.createMenus()

        # create widgets

        self.button = QPushButton()
        self.button.setText("Run Iguana")
        self.button.clicked.connect(self.runIguana)
        self.button2 = QPushButton()
        self.button2.setText("Placeholder1")
        self.button3 = QPushButton()
        self.button3.setText("Placeholder2")
        self.button4 = QPushButton()
        self.button4.setText("Placeholder3")
        self.textBrowser = QTextEdit()
        self.textBrowser.setMinimumSize(QSize(100, 100))
        self.textBrowser.setMaximumSize(QSize(16777215, 150))

        self.tabWidget = QTabWidget()
        self.tabList = [InputTab(self)]
        self.tabWidget.installEventFilter(self)
        self.tabWidget.addTab(self.tabList[0], "Simulation Setup")

        # create layouts and add widgets to them

        self.topLeftLayout = QVBoxLayout()
        self.topLeftLayout.addWidget(self.button, 0)
        self.topLeftLayout.addWidget(self.button2, 1)
        self.topLeftLayout.addWidget(self.button3, 2)
        self.topLeftLayout.addWidget(self.button4, 3)

        self.topLayout = QHBoxLayout()
        self.topLayout.addLayout(self.topLeftLayout)
        self.topLayout.addWidget(self.tabWidget)

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.topLayout, 0, 0, 2, 1)
        self.mainLayout.addWidget(self.textBrowser, 2, 0, 1, 1)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shiftDown = True
            self.tabList[self.tabWidget.currentIndex()].scrollArea.verticalScrollBar().setEnabled(False)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shiftDown = False
            self.tabList[self.tabWidget.currentIndex()].scrollArea.verticalScrollBar().setEnabled(True)

    def wheelEvent(self, event):
        # if the shift is held down then when the wheel event triggers, zoom is increased/decreased
        if self.shiftDown:
            mouseInput = event.angleDelta().y()
            if mouseInput != abs(mouseInput):
                self.tabList[self.tabWidget.currentIndex()].scaleFactor *= 0.8
            else:
                self.tabList[self.tabWidget.currentIndex()].scaleFactor *= 1.25

            self.tabList[self.tabWidget.currentIndex()].imageLabel.resize(self.tabList[self.tabWidget.currentIndex()].scaleFactor * self.tabList[self.tabWidget.currentIndex()].imageLabel.pixmap().size())

    def eventFilter(self, source, event):
        # adds the right click context menu
        if event.type() == QEvent.ContextMenu and source is self.tabWidget:
            menu = QMenu()
            deleteAction = menu.addAction('Delete Tab')
            helpAction = menu.addAction('Help')
            action = menu.exec_(self.mapToGlobal(event.pos()))
            currentTab = self.tabWidget.currentIndex()
            if action == deleteAction and currentTab != 0:
                self.tabWidget.removeTab(currentTab)
                del self.tabList[currentTab]

            return True

        return super().eventFilter(source, event)

    def createActions(self):
        self.openImageTabAct = QAction("&Image Tab", self, shortcut="Ctrl+O", triggered=self.loadImageAct)
        self.choosePathsAct = QAction("&Simulation Paths...", self, shortcut="Ctrl+1", triggered=self.chooseSimulationPaths)
        self.openInputTabAct = QAction("&Outputs Tab", self, shortcut="Ctrl+2", triggered=self.loadOutputsTab)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.choosePathsAct)

        self.newMenu = QMenu('&New', self)
        self.newMenu.addAction(self.openImageTabAct)
        self.newMenu.addAction(self.openInputTabAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.newMenu)

    def loadImageAct(self):
        # creates a new image tab and then gets and loads an image into it
        self.newImageTab()
        self.loadImage(self.getImagePath())

    def getImagePath(self):
        # returns the path to an image
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        return fileName

    def loadImage(self, fileName):
        # takes an image path and loads that image into the newly created image tab
        if fileName:
            image = QImage(fileName)
            self.tabList[-1].imageLabel.setPixmap(QPixmap.fromImage(image))
            self.tabList[-1].imageLabel.adjustSize()
            if image.isNull():
                self.textBrowser.append("Image filepath invalid")

    def chooseSimulationPaths(self):
        # calls the class which generates a menu allowing the user to input simulation paths
        self.simulationPathWindow = SystemPathWindow(self)
        self.simulationPathWindow.show()

    def loadOutputsTab(self):
        self.tabList.append(SimulationOutputTab())
        self.tabWidget.addTab(self.tabList[-1], "Output Tab")

    def newImageTab(self):
        self.tabList.append(NewImageTab())
        self.tabWidget.addTab(self.tabList[-1], "Image Tab ")

    def runIguana(self):
        self.textBrowser.append("Iguana running!")
        # this will be where iguana will be run from
        self.getLog()
        self.newImageTab()
        self.loadImage('chicken.jpg')

    def getLog(self):
        path = 'C:\\Users\\Philip\\Desktop\\Iguana\\PycharmProjects\\Iguana\\log.log'
        text = open(path).read()
        self.textBrowser.append(text)

class SystemPathWindow(QWidget):
    """
    This creates a window allowing the user select paths for the simulation paths
    This should probably in its own file.
    """
    def __init__(self, mainWindow):
        super().__init__()
        self.resize(500,150)
        mainLayout = QGridLayout()

        openIcon = self.style().standardIcon(getattr(QStyle,'SP_DirLinkIcon'))
        self.modellingButton = QPushButton()
        self.modellingButton.setIcon(openIcon)
        self.blenderButton = QPushButton()
        self.blenderButton.setIcon(openIcon)
        self.loggingButton = QPushButton()
        self.loggingButton.setIcon(openIcon)

        self.modellingTextBox = QTextEdit()
        self.modellingTextBox.setPlaceholderText("This should be the path to Iguana/Modelling")
        self.modellingTextBox.setText("C:\\Users\\Philip\\Desktop\\Iguana\\Modelling")
        self.modellingTextBox.setMaximumHeight(25)
        self.blenderTextBox = QTextEdit()
        self.blenderTextBox.setText("C:\\Program Files\\Blender Foundation\\Blender 2.90\\blender.exe")
        self.blenderTextBox.setPlaceholderText("This should be the path to blender.exe")
        self.blenderTextBox.setMaximumHeight(25)
        self.loggingTextBox = QTextEdit()
        self.loggingTextBox.setText("C:\\Users\\Philip\\Desktop\\log.log")
        self.loggingTextBox.setPlaceholderText("This should be the path to where Iguana will place the output log")
        self.loggingTextBox.setMaximumHeight(25)

        self.saveButton = QPushButton()
        self.saveButton.setText("Save")

        self.modellingButton.clicked.connect(lambda: self.getGenericPath('modellingButton'))
        self.blenderButton.clicked.connect(lambda: self.getGenericPath('blenderButton'))
        self.loggingButton.clicked.connect(lambda: self.getGenericPath('loggingButton'))
        self.saveButton.clicked.connect(lambda: self.checkValidPaths(mainWindow))

        mainLayout.addWidget(self.modellingButton,0,0)
        mainLayout.addWidget(self.blenderButton,1,0)
        mainLayout.addWidget(self.loggingButton,2,0)
        mainLayout.addWidget(self.saveButton,3,0)

        mainLayout.addWidget(self.modellingTextBox,0,1)
        mainLayout.addWidget(self.blenderTextBox,1,1)
        mainLayout.addWidget(self.loggingTextBox,2,1)

        self.setLayout(mainLayout)

    def getGenericPath(self, name):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  '', options=options)
        if name == 'modellingButton':
             self.modellingTextBox.setText(fileName)
        if name == 'blenderButton':
             self.blenderTextBox.setText(fileName)
        if name == 'loggingButton':
             self.loggingTextBox.setText(fileName)

    def checkValidPaths(self, mainWindow):
        self.close()
        mainWindow.textBrowser.append("Save Successful")
        #this will somehow check if the blender and Iguana paths are valid


class NewImageTab(QWidget):
    """
    Create a new image tab
    This should be moved to its own file
    """
    def __init__(self):
        super().__init__()
        self.scaleFactor = 1

        # imageLabel will hold the image which is currently loaded in in the mainMenu class but should realy be loaded in here
        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)

        self.tabLayout = QHBoxLayout()
        self.tabLayout.addWidget(self.scrollArea)
        self.setLayout(self.tabLayout)