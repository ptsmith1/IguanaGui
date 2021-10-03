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
    def __init__(self):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.scrollArea.setVisible(True)
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setSizePolicy(self.sizePolicy)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.scrollAreaWidgetContents.setSizePolicy(self.sizePolicy1)

        self.saveButton = QPushButton()
        self.saveButton.setText("Save")
        self.saveButton.setMaximumWidth(100)
        self.saveButton.clicked.connect(self.SaveSettings)

        self.SubheadingFont()
        self.GeneralSettings()
        self.CostingSettings()
        self.AnalysisSettings()
        self.VisualiserSettings()

        # sets layouts parent to be the scrollAreaWidget
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
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
        self.generalSettingsLabel = QLabel(self.scrollAreaWidgetContents)
        self.generalSettingsLabel.setText("General Settings")
        self.generalSettingsLabel.setFont(self.subheadingFont)
        self.generalSettingsLabel.setMaximumHeight(25)

        self.generalSettingsLabels = []
        self.generalSettingsEdits = []
        self.generalSettingsLabelNames = ['Version number:','Memory allocation:','Multicore enabled:','Something else:']
        for i in range(len(self.generalSettingsLabelNames)):
            self.generalSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.generalSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.generalSettingsEdits[i].setMaximumSize(100, 25)
            self.generalSettingsLabels[i].setText(self.generalSettingsLabelNames[i])
            self.generalGridLayout.addWidget(self.generalSettingsLabels[i], i+1, 0)
            self.generalGridLayout.addWidget(self.generalSettingsEdits[i], i+1, 1)
        self.generalGridLayout.addWidget(self.generalSettingsLabel,0,0)
        self.generalGridLayout.addItem(QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding))

    def CostingSettings(self):
        self.costingGridLayout = QGridLayout()

        self.costSettingsLabel = QLabel(self.scrollAreaWidgetContents)
        self.costSettingsLabel.setText("Cost Settings")
        self.costSettingsLabel.setFont(self.subheadingFont)
        self.costThresholdLabel = QLabel(self.scrollAreaWidgetContents)
        self.costThresholdLabel.setText("Cost threshold:")
        self.evolutionLimitLabel = QLabel(self.scrollAreaWidgetContents)
        self.evolutionLimitLabel.setText("Evolution limit:")
        self.nodesLimitLabel = QLabel(self.scrollAreaWidgetContents)
        self.nodesLimitLabel.setText("Nodes limit:")
        self.nodesPerEvoLabel = QLabel(self.scrollAreaWidgetContents)
        self.nodesPerEvoLabel.setText("Nodes per evolution limit:")

        self.costThresholdEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.costThresholdEdit.setMaximumSize(100,25)
        self.evolutionLimitEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.evolutionLimitEdit.setMaximumSize(100,25)
        self.nodesLimitEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.nodesLimitEdit.setMaximumSize(100,25)
        self.nodesPerEvoEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.nodesPerEvoEdit.setMaximumSize(100,25)

        self.costingGridLayout.addWidget(self.costSettingsLabel, 0, 0, 1, 1)
        self.costingGridLayout.addWidget(self.costThresholdLabel, 1, 0, 1, 1)
        self.costingGridLayout.addWidget(self.evolutionLimitLabel, 2, 0, 1, 1)
        self.costingGridLayout.addWidget(self.nodesLimitLabel, 3, 0, 1, 1)
        self.costingGridLayout.addWidget(self.nodesPerEvoLabel, 4, 0, 1, 1)

        self.costingGridLayout.addWidget(self.costThresholdEdit, 1, 1, 1, 1)
        self.costingGridLayout.addWidget(self.evolutionLimitEdit, 2, 1, 1, 1)
        self.costingGridLayout.addWidget(self.nodesLimitEdit, 3, 1, 1, 1)
        self.costingGridLayout.addWidget(self.nodesPerEvoEdit, 4, 1, 1, 1)

        self.costingGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def AnalysisSettings(self):
        self.analysisGridLayout = QGridLayout()
        self.analysisGridLayout.setContentsMargins(30,0,0,10)

        self.analysisSettingsLabel = QLabel(self.scrollAreaWidgetContents)
        self.analysisSettingsLabel.setText("Analysis Settings")
        self.analysisSettingsLabel.setFont(self.subheadingFont)
        self.analysisSettingsLabel.setMaximumHeight(50)
        self.allMatchLabel = QLabel(self.scrollAreaWidgetContents)
        self.allMatchLabel.setText("All match value:")
        self.negativesMatchLabel = QLabel(self.scrollAreaWidgetContents)
        self.negativesMatchLabel.setText("Negatives match value:")
        self.positivesMatchLabel = QLabel(self.scrollAreaWidgetContents)
        self.positivesMatchLabel.setText("Positives match value:")
        self.sameSignLabel = QLabel(self.scrollAreaWidgetContents)
        self.sameSignLabel.setText("Same sign value:")
        self.allValuesLabel = QLabel(self.scrollAreaWidgetContents)
        self.allValuesLabel.setText("All values value:")
        self.allNonesLabel = QLabel(self.scrollAreaWidgetContents)
        self.allNonesLabel.setText("All nones value:")
        self.sameOrderMagLabel = QLabel(self.scrollAreaWidgetContents)
        self.sameOrderMagLabel.setText("Same order mag value:")

        self.allMatchEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.allMatchEdit.setMaximumSize(100, 25)
        self.negativesMatchEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.negativesMatchEdit.setMaximumSize(100, 25)
        self.positivesMatchEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.positivesMatchEdit.setMaximumSize(100, 25)
        self.sameSignEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.sameSignEdit.setMaximumSize(100, 25)
        self.allValuesEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.allValuesEdit.setMaximumSize(100, 25)
        self.allNonesEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.allNonesEdit.setMaximumSize(100, 25)
        self.sameOrderMagEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.sameOrderMagEdit.setMaximumSize(100, 25)


        self.analysisGridLayout.addWidget(self.analysisSettingsLabel, 0, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.allMatchLabel, 1, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.negativesMatchLabel, 2, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.positivesMatchLabel, 3, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.sameSignLabel, 4, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.allValuesLabel, 5, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.allNonesLabel, 6, 0, 1, 1)
        self.analysisGridLayout.addWidget(self.sameOrderMagLabel, 7, 0, 1, 1)

        self.analysisGridLayout.addWidget(self.allMatchEdit, 1, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.negativesMatchEdit, 2, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.positivesMatchEdit, 3, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.sameSignEdit, 4, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.allValuesEdit, 5, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.allNonesEdit, 6, 1, 1, 1)
        self.analysisGridLayout.addWidget(self.sameOrderMagEdit, 7, 1, 1, 1)

        self.analysisGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def VisualiserSettings(self):
        self.visualiserGridLayout = QGridLayout()
        self.visualiserGridLayout.setContentsMargins(30,0,0,0)
        self.visualiserSettingsLabel = QLabel(self.scrollAreaWidgetContents)
        self.visualiserSettingsLabel.setText("Visualiser Settings")
        self.visualiserSettingsLabel.setFont(self.subheadingFont)

        self.visualiserSettingsLabels = []
        self.visualiserSettingsEdits = []
        self.visualiserSettingsLabelNames = ['Visualiser on:','Task view:','Evolution view:','Max nodes to visualise:']
        for i in range(len(self.generalSettingsLabelNames)):
            self.visualiserSettingsLabels.append(QLabel(self.scrollAreaWidgetContents))
            self.visualiserSettingsEdits.append(QTextEdit(self.scrollAreaWidgetContents))
            self.visualiserSettingsEdits[i].setMaximumSize(100, 25)
            self.visualiserSettingsLabels[i].setText(self.visualiserSettingsLabelNames[i])
            self.visualiserGridLayout.addWidget(self.visualiserSettingsLabels[i], i+1, 0, 1, 1)
            self.visualiserGridLayout.addWidget(self.visualiserSettingsEdits[i], i+1, 1, 1, 1)
        self.visualiserGridLayout.addWidget(self.visualiserSettingsLabel,0,0,1,1)
        self.visualiserGridLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def SubheadingFont(self):
        self.subheadingFont = QFont('Arial',12)
        self.subheadingFont.setUnderline(True)

    def SaveSettings(self):
        data = {}
        data['costing'] = []
        data['costing'].append({'cost_threshold':self.costThresholdEdit.toPlainText(),
                                'evolution_limit':self.evolutionLimitEdit.toPlainText(),
                                'nodes_limit':self.nodesLimitEdit.toPlainText(),
                                'max_nodes_per_evo':self.nodesPerEvoEdit.toPlainText(),})
        data['analysis'] = []
        data['analysis'].append({'all_match': self.allMatchEdit.toPlainText(),
                                'negatives_match: ': self.negativesMatchEdit.toPlainText(),
                                'positives_match': self.positivesMatchEdit.toPlainText(),
                                'same_sign': self.sameSignEdit.toPlainText(),
                                'all_values': self.allValuesEdit.toPlainText(),
                                'all_nones': self.allNonesEdit.toPlainText(),
                                'same_order_mag': self.sameOrderMagEdit.toPlainText()})
        with open('data.txt','w') as outFile:
            json.dump(data,outFile)