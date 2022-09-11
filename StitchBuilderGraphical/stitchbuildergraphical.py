# This Python file uses the following encoding: utf-8
import sys
import os.path
import cv2

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QImage, QPixmap


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

class StitchBuilderGraphical(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.ui = Ui_StitchBuilderGraphical()
    self.ui.setupUi(self)
    self.setLayout(self.ui.verticalLayout)

    self.imageConverter = ImageConverter()
    img = self.loadTestImage()
    h, w, _ = img.shape
    self.ui.topPic.setPixmap(QPixmap(QImage(img, w, h, QImage.Format_BGR888)))

    # File Path
    self.ui.filePathDisplay.setReadOnly(True)

    # Filter Strength
    slider = self.ui.filterStrengthSlider
    slider.valueChanged.connect(self.onFilterValueChanged)
    self.filterStep = FILTER_SLIDER_MAX_REAL_VAL / slider.maximum()

    # Dithering
    checkbox = self.ui.ditherCheckBox
    checkbox.toggled.connect(self.onDitherBoxChecked)


  def onFilterValueChanged(self, val):
    if (val == 0):
      self.ui.filterStrengthLabel.setText("Off")
    else:
      scaledVal = val * self.filterStep
      scaledValText = "{:4.1f}".format(scaledVal)
      self.ui.filterStrengthLabel.setText(scaledValText)

  def onDitherBoxChecked(self, val):
    print("Dither checkbox val: %s" % val)
    if (val):
      self.ui.ditherCheckBox.setText("Dithering On")
    else:
      self.ui.ditherCheckBox.setText("Dithering Off")

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
