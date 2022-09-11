# This Python file uses the following encoding: utf-8
import sys
import os.path
import cv2

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PySide6.QtGui import QImage, QPixmap, QImageReader

#from UnicodeSymbols import UnicodeSymbols
from ImageConverter import ImageConverter

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_StitchBuilderGraphical

GRID_COLUMN_COUNT = 6

# Filter Slider parameters
FILTER_SLIDER_MAX_REAL_VAL = 3.0

class StitchBuilderArgs(object):
  def __init__(self):
    self.filterStrength = 0.0
    self.maxW = ImageConverter.ABSOLUTE_MAX_W
    self.maxH = ImageConverter.ABSOLUTE_MAX_H
    self.dithering = True
    self.imgpath = None

class StitchBuilderGraphical(QWidget):
  def __init__(self, parent=None):
    # Initialization
    super().__init__(parent)
    self.ui = Ui_StitchBuilderGraphical()
    self.ui.setupUi(self)
    self.setLayout(self.ui.verticalLayout)

    # Internal Model
    self.imageConverter = ImageConverter()
    self.args           = StitchBuilderArgs()

    # Images
    img = self.loadTestImage()
    h, w, _ = img.shape
    self.ui.topPic.setPixmap(QPixmap(QImage(img, w, h, QImage.Format_BGR888)))

    # File Path
    fileDisplay = self.ui.filePathDisplay
    fileButton  = self.ui.filePathButton
    fileDisplay.setReadOnly(True)
    fileButton.clicked.connect(self.onFilePathButton)

    # Filter Strength
    slider = self.ui.filterStrengthSlider
    slider.valueChanged.connect(self.onFilterValueChanged)
    self.filterStep = FILTER_SLIDER_MAX_REAL_VAL / slider.maximum()

    # Dithering
    checkbox = self.ui.ditherCheckBox
    checkbox.toggled.connect(self.onDitherBoxChecked)

    # Spin Boxes (maxW, maxH, maxC)
    wbox = self.ui.maxWSpinBox
    hbox = self.ui.maxHSpinBox
    cbox = self.ui.maxCSpinBox
    wbox.setMinimum(ImageConverter.ABSOLUTE_MIN_W)
    hbox.setMinimum(ImageConverter.ABSOLUTE_MIN_H)
    cbox.setMinimum(ImageConverter.ABSOLUTE_MIN_C)
    wbox.setMaximum(ImageConverter.ABSOLUTE_MAX_W)
    hbox.setMaximum(ImageConverter.ABSOLUTE_MAX_H)
    cbox.setMaximum(ImageConverter.ABSOLUTE_MAX_C)

    # Convert Button
    cButton = self.ui.convertButton
    cButton.setEnabled(False)#initially no filepath, so set to disabled

  def onFilePathButton(self):
    supportedFormats = QImageReader.supportedImageFormats()
    text_filter = "Images ({})".format(" ".join(["*.{}".format(fo.data().decode()) for fo in supportedFormats]))
    filename, _ = QFileDialog.getOpenFileName(self, "Open Image", filter=text_filter)
    if len(filename) == 0:
      # User likely picked "cancel", don't change anything
      return
    self.ui.filePathDisplay.setText(filename)
    self.args.imgpath = filename
    loaded_image      = QImage(filename, format=QImage.Format_BGR888)
    #TODO: load this into the top image
    self.args.img = loaded_image

  def onFilterValueChanged(self, val):
    if (val == 0):
      self.ui.filterStrengthLabel.setText("Off")
      self.args.filterStrength = 0.0
    else:
      scaledVal = val * self.filterStep
      scaledValText = "{:4.1f}".format(scaledVal)
      self.ui.filterStrengthLabel.setText(scaledValText)
      self.args.filterStrength = scaledVal

  def onDitherBoxChecked(self, val):
    print("Dither checkbox val: %s" % val)
    if (val):
      self.ui.ditherCheckBox.setText("Dithering On")
      self.args.dithering = True
    else:
      self.ui.ditherCheckBox.setText("Dithering Off")
      self.args.dithering = False

  def loadTestImage(self):
    test_path = os.path.join("..", "data", "zirda.webp")
    img = cv2.imread(test_path, cv2.IMREAD_UNCHANGED)
    if (img.shape[2] > 3):
      trans_mask = (0 == img[:,:,3])
      img[trans_mask] = [255, 255, 255, 255]
      img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    return img

  def createCharLabel(self, character):
    font_size = 18
    labeltext = "<html><head/><body><p align=\"center\"><span style=\" font-size:{0}pt;\">{1}</span></p></body></html>".format(font_size, character)
    twidget = QLabel(character,alignment=QtCore.Qt.AlignCenter)
    twidget.setText(labeltext)
    return twidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = StitchBuilderGraphical()
    widget.show()
    sys.exit(app.exec())
