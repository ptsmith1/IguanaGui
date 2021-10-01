from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QTextBrowser, QHBoxLayout, QVBoxLayout, QTabWidget, QMenu, QAction, QFileDialog,\
    QSizePolicy, QMessageBox, QScrollArea, QTextEdit, QStyle
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QPalette, QIcon
from PyQt5.Qt import Qt
import sys


class MainWindow(QMainWindow):
    """
    This is the main class for the UI
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Iguana")
        self.resize(760,600)
        self.scaleFactor = 1
        self.shiftDown = False
        self.tabCount= 2

        # create widgets
        self.button = QPushButton()
        self.button.setText("one")
        self.button.clicked.connect(self.runIguana)
        self.button2 = QPushButton()
        self.button2.setText("two")
        self.button3 = QPushButton()
        self.button3.setText("three")
        self.button4 = QPushButton()
        self.button4.setText("four")

        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setMinimumSize(300,200)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)

        self.tabWidget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.textBrowser = QTextEdit()
        self.textBrowser.setMinimumSize(QSize(0, 50))
        self.textBrowser.setMaximumSize(QSize(16777215, 150))

        # create layouts and add widgets to them
        self.tab2Layout = QHBoxLayout()
        self.tab2Layout.addWidget(self.scrollArea)
        self.tab2.setLayout(self.tab2Layout)
        self.tabWidget.addTab(self.tab1, "SimulationSetup")
        self.tabWidget.addTab(self.tab2, "ImageViewer")

        self.topLeftLayout = QVBoxLayout()
        self.topLeftLayout.addWidget(self.button, 0)
        self.topLeftLayout.addWidget(self.button2, 1)
        self.topLeftLayout.addWidget(self.button3, 2)
        self.topLeftLayout.addWidget(self.button4, 3)

        self.topLayout = QHBoxLayout()
        self.topLayout.addLayout(self.topLeftLayout)
        self.topLayout.addWidget(self.tabWidget)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.textBrowser, 2, 0, 1, 1)
        self.mainLayout.addLayout(self.topLayout, 0, 0, 2, 1)
        # something
        self.createActions()
        self.createMenus()
        # to see anything you have to make one main widget which you add your main layout to which is then set as the
        # centralWidget of the mainWindow
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def keyPressEvent(self, event2):
        if event2.key() == Qt.Key_Shift:
            self.shiftDown = True
            self.scrollArea.verticalScrollBar().setEnabled(False)

    def keyReleaseEvent(self, event3):
        if event3.key() == Qt.Key_Shift:
            self.shiftDown = False
            self.scrollArea.verticalScrollBar().setEnabled(True)

    def wheelEvent(self, event):
        # if the shift is held down then when the wheel event triggers, zoom is increased/decreased
        if self.shiftDown:
            mouseInput = event.angleDelta().y()
            if mouseInput != abs(mouseInput):
                self.scaleFactor *= 0.8
            else:
                self.scaleFactor *= 1.25
            print(self.scaleFactor)

            self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

    def createActions(self):
        self.openImageAct = QAction("&Image Tab", self, shortcut="Ctrl+O", triggered=self.loadImageAct)
        self.choosePathsAct = QAction("&Simulation Paths...", self, shortcut="Ctrl+1", triggered=self.chooseSimulationPaths)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.choosePathsAct)

        self.newMenu = QMenu('&New', self)
        self.newMenu.addAction(self.openImageAct)
        self.newMenu.setEnabled(False)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.newMenu)

    def chooseSimulationPaths(self):
        self.simulationPathWindow = SystemPathWindow(self)
        self.simulationPathWindow.show()

    def loadImageAct(self):
        self.loadImage(self.getImagePath())
        self.newImageTab()

    def loadImage(self, fileName):
        if fileName:
            image = QImage(fileName)
            self.imageLabel = QLabel()
            self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.imageLabel.setScaledContents(True)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.imageLabel.adjustSize()
            if image.isNull():
                self.textBrowser.append("Image filepath invalid")

    def newImageTab(self):
        self.scrollArea = QScrollArea()
        self.scrollArea.setMinimumSize(300, 200)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)
        newTab = QWidget()
        newTabLayout = QHBoxLayout()
        newTabLayout.addWidget(self.scrollArea)
        newTab.setLayout(newTabLayout)
        self.tabCount += 1
        self.tabWidget.addTab(newTab, "Image Tab " + str(self.tabCount))

    def getImagePath(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        return fileName


    def runIguana(self):
        self.textBrowser.append("Iguana running!")
        # this will be where iguana will be run from
        self.getLog()
        self.imageLabel.setPixmap(QPixmap.fromImage(QImage('chicken.jpg')))
        self.imageLabel.adjustSize()
        self.newMenu.setEnabled(True)

    def getLog(self):
        path = 'C:\\Users\\Philip\\Desktop\\Iguana\\PycharmProjects\\Iguana\\log.log'
        text = open(path).read()
        self.textBrowser.append(text)

class SystemPathWindow(QWidget):
    """
    This creates a window allowing the user select paths for the simulation paths
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


