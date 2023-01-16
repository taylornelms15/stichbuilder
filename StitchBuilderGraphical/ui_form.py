# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from CrossStitchKey import CrossStitchKeyNoScroll
from CrossStitchPrintView import CrossStitchPrintView
from ImageLabel import ImageLabel

class Ui_StitchBuilderGraphical(object):
    def setupUi(self, StitchBuilderGraphical):
        if not StitchBuilderGraphical.objectName():
            StitchBuilderGraphical.setObjectName(u"StitchBuilderGraphical")
        StitchBuilderGraphical.resize(1385, 998)
        self.horizontalLayout = QHBoxLayout(StitchBuilderGraphical)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftHalfVertLayout = QVBoxLayout()
        self.leftHalfVertLayout.setObjectName(u"leftHalfVertLayout")
        self.topPic = ImageLabel(StitchBuilderGraphical)
        self.topPic.setObjectName(u"topPic")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topPic.sizePolicy().hasHeightForWidth())
        self.topPic.setSizePolicy(sizePolicy)
        self.topPic.setMinimumSize(QSize(200, 200))
        self.topPic.setAlignment(Qt.AlignCenter)

        self.leftHalfVertLayout.addWidget(self.topPic)

        self.line = QFrame(StitchBuilderGraphical)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.leftHalfVertLayout.addWidget(self.line)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setContentsMargins(10, -1, 10, -1)
        self.label = QLabel(StitchBuilderGraphical)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label.setMargin(5)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.filePathDisplay = QLineEdit(StitchBuilderGraphical)
        self.filePathDisplay.setObjectName(u"filePathDisplay")

        self.horizontalLayout_3.addWidget(self.filePathDisplay)

        self.filePathButton = QPushButton(StitchBuilderGraphical)
        self.filePathButton.setObjectName(u"filePathButton")

        self.horizontalLayout_3.addWidget(self.filePathButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_2 = QLabel(StitchBuilderGraphical)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2.setMargin(5)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.maxWSpinBox = QSpinBox(StitchBuilderGraphical)
        self.maxWSpinBox.setObjectName(u"maxWSpinBox")
        self.maxWSpinBox.setMinimum(15)
        self.maxWSpinBox.setMaximum(4096)
        self.maxWSpinBox.setValue(100)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.maxWSpinBox)

        self.label_3 = QLabel(StitchBuilderGraphical)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_3.setMargin(5)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.maxHSpinBox = QSpinBox(StitchBuilderGraphical)
        self.maxHSpinBox.setObjectName(u"maxHSpinBox")
        self.maxHSpinBox.setMinimum(15)
        self.maxHSpinBox.setMaximum(4096)
        self.maxHSpinBox.setValue(100)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.maxHSpinBox)

        self.label_4 = QLabel(StitchBuilderGraphical)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_4.setMargin(5)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.maxCSpinBox = QSpinBox(StitchBuilderGraphical)
        self.maxCSpinBox.setObjectName(u"maxCSpinBox")
        self.maxCSpinBox.setMinimum(3)
        self.maxCSpinBox.setMaximum(4096)
        self.maxCSpinBox.setValue(24)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.maxCSpinBox)

        self.label_5 = QLabel(StitchBuilderGraphical)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_5.setMargin(5)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.filterStrengthSlider = QSlider(StitchBuilderGraphical)
        self.filterStrengthSlider.setObjectName(u"filterStrengthSlider")
        self.filterStrengthSlider.setMaximum(20)
        self.filterStrengthSlider.setPageStep(2)
        self.filterStrengthSlider.setOrientation(Qt.Horizontal)
        self.filterStrengthSlider.setTickPosition(QSlider.TicksBelow)
        self.filterStrengthSlider.setTickInterval(2)

        self.horizontalLayout_5.addWidget(self.filterStrengthSlider)

        self.filterStrengthLabel = QLabel(StitchBuilderGraphical)
        self.filterStrengthLabel.setObjectName(u"filterStrengthLabel")
        self.filterStrengthLabel.setAlignment(Qt.AlignCenter)
        self.filterStrengthLabel.setMargin(5)

        self.horizontalLayout_5.addWidget(self.filterStrengthLabel)

        self.horizontalLayout_5.setStretch(0, 1)

        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_6 = QLabel(StitchBuilderGraphical)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_6.setMargin(5)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.ditherCheckBox = QCheckBox(StitchBuilderGraphical)
        self.ditherCheckBox.setObjectName(u"ditherCheckBox")
        self.ditherCheckBox.setMinimumSize(QSize(0, 30))
        self.ditherCheckBox.setMaximumSize(QSize(16777215, 30))
        self.ditherCheckBox.setChecked(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.ditherCheckBox)

        self.label_9 = QLabel(StitchBuilderGraphical)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_9)

        self.bwCheckBox = QCheckBox(StitchBuilderGraphical)
        self.bwCheckBox.setObjectName(u"bwCheckBox")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.bwCheckBox)


        self.leftHalfVertLayout.addLayout(self.formLayout)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.convertButton = QPushButton(StitchBuilderGraphical)
        self.convertButton.setObjectName(u"convertButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.convertButton.sizePolicy().hasHeightForWidth())
        self.convertButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.convertButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 4)
        self.horizontalLayout_8.setStretch(2, 1)

        self.leftHalfVertLayout.addLayout(self.horizontalLayout_8)

        self.line_2 = QFrame(StitchBuilderGraphical)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.leftHalfVertLayout.addWidget(self.line_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ThreadColorImageLabel = ImageLabel(StitchBuilderGraphical)
        self.ThreadColorImageLabel.setObjectName(u"ThreadColorImageLabel")
        sizePolicy.setHeightForWidth(self.ThreadColorImageLabel.sizePolicy().hasHeightForWidth())
        self.ThreadColorImageLabel.setSizePolicy(sizePolicy)
        self.ThreadColorImageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.ThreadColorImageLabel, 2, 1, 1, 1)

        self.ReducedColorspaceImageLabel = ImageLabel(StitchBuilderGraphical)
        self.ReducedColorspaceImageLabel.setObjectName(u"ReducedColorspaceImageLabel")
        sizePolicy.setHeightForWidth(self.ReducedColorspaceImageLabel.sizePolicy().hasHeightForWidth())
        self.ReducedColorspaceImageLabel.setSizePolicy(sizePolicy)
        self.ReducedColorspaceImageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.ReducedColorspaceImageLabel, 2, 0, 1, 1)

        self.label_14 = QLabel(StitchBuilderGraphical)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_14, 3, 1, 1, 1)

        self.label_7 = QLabel(StitchBuilderGraphical)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_11 = QLabel(StitchBuilderGraphical)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_11, 1, 1, 1, 1)

        self.label_8 = QLabel(StitchBuilderGraphical)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.OriginalImageLabel = ImageLabel(StitchBuilderGraphical)
        self.OriginalImageLabel.setObjectName(u"OriginalImageLabel")
        sizePolicy.setHeightForWidth(self.OriginalImageLabel.sizePolicy().hasHeightForWidth())
        self.OriginalImageLabel.setSizePolicy(sizePolicy)
        self.OriginalImageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.OriginalImageLabel, 0, 0, 1, 1)

        self.AfterFilterImageLabel = ImageLabel(StitchBuilderGraphical)
        self.AfterFilterImageLabel.setObjectName(u"AfterFilterImageLabel")
        sizePolicy.setHeightForWidth(self.AfterFilterImageLabel.sizePolicy().hasHeightForWidth())
        self.AfterFilterImageLabel.setSizePolicy(sizePolicy)
        self.AfterFilterImageLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.AfterFilterImageLabel, 0, 1, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)

        self.leftHalfVertLayout.addLayout(self.gridLayout_2)

        self.leftHalfVertLayout.setStretch(0, 1)
        self.leftHalfVertLayout.setStretch(5, 3)

        self.horizontalLayout.addLayout(self.leftHalfVertLayout)

        self.rightHalfVertLayout = QVBoxLayout()
        self.rightHalfVertLayout.setObjectName(u"rightHalfVertLayout")
        self.KeyLabel = QLabel(StitchBuilderGraphical)
        self.KeyLabel.setObjectName(u"KeyLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.KeyLabel.sizePolicy().hasHeightForWidth())
        self.KeyLabel.setSizePolicy(sizePolicy2)
        self.KeyLabel.setAlignment(Qt.AlignCenter)

        self.rightHalfVertLayout.addWidget(self.KeyLabel)

        self.crossStitchKey = CrossStitchKeyNoScroll(StitchBuilderGraphical)
        self.crossStitchKey.setObjectName(u"crossStitchKey")

        self.rightHalfVertLayout.addWidget(self.crossStitchKey)

        self.line_3 = QFrame(StitchBuilderGraphical)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.rightHalfVertLayout.addWidget(self.line_3)

        self.scrollArea = QScrollArea(StitchBuilderGraphical)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.RightSideScrollableContents = CrossStitchPrintView()
        self.RightSideScrollableContents.setObjectName(u"RightSideScrollableContents")
        self.RightSideScrollableContents.setGeometry(QRect(0, 0, 676, 752))
        self.scrollArea.setWidget(self.RightSideScrollableContents)

        self.rightHalfVertLayout.addWidget(self.scrollArea)

        self.savePdfButton = QPushButton(StitchBuilderGraphical)
        self.savePdfButton.setObjectName(u"savePdfButton")

        self.rightHalfVertLayout.addWidget(self.savePdfButton)

        self.rightHalfVertLayout.setStretch(1, 1)
        self.rightHalfVertLayout.setStretch(3, 5)

        self.horizontalLayout.addLayout(self.rightHalfVertLayout)


        self.retranslateUi(StitchBuilderGraphical)

        QMetaObject.connectSlotsByName(StitchBuilderGraphical)
    # setupUi

    def retranslateUi(self, StitchBuilderGraphical):
        StitchBuilderGraphical.setWindowTitle(QCoreApplication.translate("StitchBuilderGraphical", u"StitchBuilderGraphical", None))
        self.topPic.setText(QCoreApplication.translate("StitchBuilderGraphical", u"topPic", None))
        self.label.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Input Image", None))
        self.filePathButton.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Choose File...", None))
        self.label_2.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Max Width", None))
        self.label_3.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Max Height", None))
        self.label_4.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Max Number of Thread Colors", None))
        self.label_5.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Filter Strength", None))
        self.filterStrengthLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Off", None))
        self.label_6.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Dither", None))
        self.ditherCheckBox.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Dithering On", None))
        self.label_9.setText(QCoreApplication.translate("StitchBuilderGraphical", u"B&W", None))
        self.bwCheckBox.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Color Pattern Output", None))
        self.convertButton.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Convert", None))
        self.ThreadColorImageLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"ThreadColorImage", None))
        self.ReducedColorspaceImageLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"ReduceColorspaceImage", None))
        self.label_14.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Thread Colors", None))
        self.label_7.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Reduced Colorspace", None))
        self.label_11.setText(QCoreApplication.translate("StitchBuilderGraphical", u"After Filtering", None))
        self.label_8.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Original (Scaled)", None))
        self.OriginalImageLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"OriginalImage", None))
        self.AfterFilterImageLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"AfterFilterImage", None))
        self.KeyLabel.setText(QCoreApplication.translate("StitchBuilderGraphical", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">Key</span></p></body></html>", None))
        self.savePdfButton.setText(QCoreApplication.translate("StitchBuilderGraphical", u"Save PDF", None))
    # retranslateUi

