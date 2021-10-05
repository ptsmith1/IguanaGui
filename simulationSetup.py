import os
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QTextEdit, QPushButton, QScrollArea, \
    QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QRect
import json


class InputTab(QWidget):
    """
    Create the data input tab for the simulation
    """
    def __init__(self, mainWindow):
        super().__init__()
        # tab structure --> tab --> horizontal layout --> QScrollArea (scrollArea) --> QWidget (scrollAreaWidgetContents) --> QGridLayout --> 4 QGridLayouts + save button --> labels + textEdits in each of the 4 sub grid layouts
        self.scrollArea = QScrollArea()
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

        self.saveButton = QPushButton()
        self.saveButton.setText("Save")
        self.saveButton.setMaximumWidth(100)
        self.HeadingFont()

        # these 4 methods generate the four settings categories and labels/Textedits for each category
        self.GeneralSettings()
        self.CostingSettings()
        self.AnalysisSettings()
        self.VisualiserSettings()
        self.saveButton.clicked.connect(lambda: self.SaveSettings(mainWindow))

        # sets layouts parent to be the scrollAreaWidget
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        # adds the 4 layouts for the 4 sections
        self.gridLayout.addLayout(self.generalGridLayout, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.costingGridLayout, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.analysisGridLayout, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.visualiserGridLayout, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.saveButton,2,1,alignment=Qt.AlignRight)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabLayout = QHBoxLayout()
        self.tabLayout.addWidget(self.scrollArea)
        self.setLayout(self.tabLayout)

    def GeneralSettings(self):
        self.generalGridLayout = QGridLayout()
        self.generalGridLayout.setContentsMargins(0,0,0,10)
        # heading label for the section
        headingLabel = QLabel(self.scrollAreaWidgetContents)
        headingLabel.setText("General Settings")
        headingLabel.setFont(self.headingFont)

        # these store the label/textEdit objects
        self.generalSettingsLabels = []
        self.generalSettingsEdits = []
        # stores the text for the labels
        self.generalSettingsLabelNames = ['Version number:','Memory allocation:','Multicore enabled:','Something else:']
        # generates a textEdit and label for each named label
        for i in range(len(self.generalSettingsLabelNames)):
            self.generalSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.generalSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.generalSettingsEdits[i].setMaximumSize(100, 25)
            self.generalSettingsLabels[i].setText(self.generalSettingsLabelNames[i])
            self.generalGridLayout.addWidget(self.generalSettingsLabels[i], i+1, 0)
            self.generalGridLayout.addWidget(self.generalSettingsEdits[i], i+1, 1)
        # adds the heading label and a spacer to force the labels to the top of the section
        self.generalGridLayout.addWidget(headingLabel,0,0)
        self.generalGridLayout.addItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding))

    def CostingSettings(self):
        self.costingGridLayout = QGridLayout()
        headingLabel = QLabel(self.scrollAreaWidgetContents)
        headingLabel.setText("Costing Settings")
        headingLabel.setFont(self.headingFont)

        self.costingSettingsLabels = []
        self.costingSettingsEdits = []
        self.costingSettingsLabelNames = ['Cost threshold:','Evolution limit:','Nodes limit:','Nodes per evolution limit:']

        for i in range(len(self.costingSettingsLabelNames)):
            self.costingSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.costingSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.costingSettingsEdits[i].setMaximumSize(100, 25)
            self.costingSettingsLabels[i].setText(self.costingSettingsLabelNames[i])
            self.costingGridLayout.addWidget(self.costingSettingsLabels[i], i+1, 0)
            self.costingGridLayout.addWidget(self.costingSettingsEdits[i], i+1, 1)

        self.costingGridLayout.addWidget(headingLabel,0,0)
        self.costingGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def AnalysisSettings(self):
        self.analysisGridLayout = QGridLayout()
        self.analysisGridLayout.setContentsMargins(30,0,0,10)

        headingLabel = QLabel(self.scrollAreaWidgetContents)
        headingLabel.setText("Analysis Settings")
        headingLabel.setFont(self.headingFont)

        self.analysisSettingsLabels = []
        self.analysisSettingsEdits = []
        self.analysisSettingsLabelNames = ['All match value:','Negatives match value:','Positives match value:','Same sign value:','All values value:','All nones value:','Same order mag value:']

        for i in range(len(self.analysisSettingsLabelNames)):
            self.analysisSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.analysisSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.analysisSettingsEdits[i].setMaximumSize(100, 25)
            self.analysisSettingsLabels[i].setText(self.analysisSettingsLabelNames[i])
            self.analysisGridLayout.addWidget(self.analysisSettingsLabels[i], i+1, 0)
            self.analysisGridLayout.addWidget(self.analysisSettingsEdits[i], i+1, 1)

        self.analysisGridLayout.addWidget(headingLabel,0,0)
        self.analysisGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def VisualiserSettings(self):
        self.visualiserGridLayout = QGridLayout()
        self.visualiserGridLayout.setContentsMargins(30,0,0,0)
        headingLabel = QLabel(self.scrollAreaWidgetContents)
        headingLabel.setText("Visualiser Settings")
        headingLabel.setFont(self.headingFont)

        self.visualiserSettingsLabels = []
        self.visualiserSettingsEdits = []
        self.visualiserSettingsLabelNames = ['Visualiser on:','Task view:','Evolution view:','Max nodes to visualise:']
        for i in range(len(self.visualiserSettingsLabelNames)):
            self.visualiserSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.visualiserSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.visualiserSettingsEdits[i].setMaximumSize(100, 25)
            self.visualiserSettingsLabels[i].setText(self.visualiserSettingsLabelNames[i])
            self.visualiserGridLayout.addWidget(self.visualiserSettingsLabels[i], i+1, 0, 1, 1)
            self.visualiserGridLayout.addWidget(self.visualiserSettingsEdits[i], i+1, 1, 1, 1)
        self.visualiserGridLayout.addWidget(headingLabel,0,0,1,1)
        self.visualiserGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def HeadingFont(self):
        self.headingFont = QFont('Arial', 12)
        self.headingFont.setUnderline(True)

    def SaveSettings(self, mainWindow):
        data = {}
        data['general'] = []
        data['costing'] = []
        data['analysis'] = []
        data['visualiser'] = []

        for i, textValue in enumerate(self.generalSettingsEdits):
            data['general'].append({self.generalSettingsLabelNames[i]:textValue.toPlainText()})

        for i, textValue in enumerate(self.costingSettingsEdits):
            data['costing'].append({self.costingSettingsLabelNames[i]:textValue.toPlainText()})

        for i, textValue in enumerate(self.analysisSettingsEdits):
            data['analysis'].append({self.analysisSettingsLabelNames[i]:textValue.toPlainText()})

        for i, textValue in enumerate(self.visualiserSettingsEdits):
            data['visualiser'].append({self.visualiserSettingsLabelNames[i]:textValue.toPlainText()})

        with open('data.txt','w') as outFile:
            json.dump(data,outFile)
            mainWindow.textBrowser.append("Save Successful")