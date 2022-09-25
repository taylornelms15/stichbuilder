# This Python file uses the following encoding: utf-8
import sys
import os.path
import cv2
import numpy as np

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PySide6.QtGui import QImage, QImageReader, QPainter

#from UnicodeSymbols import UnicodeSymbols
from ImageConverter import ImageConverter, ImageConverterResultImages

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_StitchBuilderGraphical

GRID_COLUMN_COUNT = 6

# Filter Slider parameters
FILTER_SLIDER_MAX_REAL_VAL = 2.0

class StitchBuilderArgs(object):
  def __init__(self):
    self.filterStrength = 0.0
    self.maxW = ImageConverter.ABSOLUTE_MAX_W
    self.maxH = ImageConverter.ABSOLUTE_MAX_H
    self.maxC = ImageConverter.ABSOLUTE_MAX_C
    self.dithering = True
    self.imgpath = None
    self.img = None

class ImageConverterWorker(QtCore.QObject):
  finished =  QtCore.Signal(ImageConverterResultImages)

  def __init__(self, converter, img, parent=None):
    super().__init__(parent)
    self.convert = converter
    self.img = img

  def run(self):
    print("Conversion starting")
    results = self.convert.convert(self.img)
    print("Conversion ending")
    self.finished.emit(results)

class StitchBuilderGraphical(QWidget):
  def __init__(self, parent=None):
    # Initialization
    super().__init__(parent)
    self.ui = Ui_StitchBuilderGraphical()
    self.ui.setupUi(self)

    # Internal Model
    self.imageConverter = ImageConverter()
    self.args           = StitchBuilderArgs()

    # Images
    img = self.loadTestImage()
    h, w, _ = img.shape
    self.ui.topPic.setImage(QImage(img, w, h, QImage.Format_BGR888))
    #TODO: put a better top pic here?

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
    self.initSpinBoxes()

    # Convert Button
    cButton = self.ui.convertButton
    cButton.setEnabled(False)#initially no filepath, so set to disabled
    cButton.clicked.connect(self.onConvertButton)

    # Conversion Results
    self.ui.OriginalImageLabel.setHidden(True)
    self.ui.AfterFilterImageLabel.setHidden(True)
    self.ui.ReducedColorspaceImageLabel.setHidden(True)
    self.ui.ThreadColorImageLabel.setHidden(True)

  def initSpinBoxes(self):
    wbox = self.ui.maxWSpinBox
    hbox = self.ui.maxHSpinBox
    cbox = self.ui.maxCSpinBox
    wbox.setMinimum(ImageConverter.ABSOLUTE_MIN_W)
    hbox.setMinimum(ImageConverter.ABSOLUTE_MIN_H)
    cbox.setMinimum(ImageConverter.ABSOLUTE_MIN_C)
    wbox.setMaximum(ImageConverter.ABSOLUTE_MAX_W)
    hbox.setMaximum(ImageConverter.ABSOLUTE_MAX_H)
    cbox.setMaximum(ImageConverter.ABSOLUTE_MAX_C)
    wbox.valueChanged.connect(self.onWValueChanged)
    hbox.valueChanged.connect(self.onHValueChanged)
    cbox.valueChanged.connect(self.onCValueChanged)
    self.args.maxW = wbox.value()
    self.args.maxH = hbox.value()
    self.args.maxC = cbox.value()

  def loadArgsIntoConverter(self):
    self.imageConverter.setMaxH(self.args.maxH)
    self.imageConverter.setMaxW(self.args.maxW)
    self.imageConverter.setMaxC(self.args.maxC)
    self.imageConverter.setFilterStrength(self.args.filterStrength)
    self.imageConverter.setDither(self.args.dithering)

  def onConvertButton(self):
    """
    Should collect the relevant args, put them into an ImageConverter, and start its thread running
    """
    self.loadArgsIntoConverter()
    img = self.args.img
    # Create a QThread object
    self.thread = QtCore.QThread()
    # Step 3: Create a worker object
    self.worker = ImageConverterWorker(self.imageConverter, img)
    # Step 4: Move worker to the thread
    self.worker.moveToThread(self.thread)
    # Step 5: Connect signals and slots
    self.thread.started.connect(self.worker.run)
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(self.thread.deleteLater)
    self.worker.finished.connect(self.onConversionFinished)
    # Step 6: Start the thread
    self.thread.start()

  def onConversionFinished(self, resultobj):
    h, w, _ = resultobj.img_scaled.shape
    print("Resulting h, w are %s, %s" % (h, w))
    img_scaled              = QImage(resultobj.img_scaled, w, h, QImage.Format_BGR888)
    after_filter            = QImage(resultobj.img_post_filter,  w, h, QImage.Format_BGR888)
    img_reduced_colorspace  = QImage(resultobj.img_reduced_colorspace,  w, h, QImage.Format_BGR888)
    img_thread_color        = QImage(resultobj.img_thread_color,  w, h, QImage.Format_BGR888)
    self.ui.OriginalImageLabel.setHidden(False)
    self.ui.OriginalImageLabel.setImage(img_scaled)
    self.ui.AfterFilterImageLabel.setHidden(False)
    self.ui.AfterFilterImageLabel.setImage(after_filter)
    self.ui.ReducedColorspaceImageLabel.setHidden(False)
    self.ui.ReducedColorspaceImageLabel.setImage(img_reduced_colorspace)
    self.ui.ThreadColorImageLabel.setHidden(False)
    self.ui.ThreadColorImageLabel.setImage(img_thread_color)

    self.ui.RightSideScrollableContents.consumeImage(resultobj.img_thread_array, bw=False)
    self.ui.crossStitchKey.consumeImage(resultobj.img_thread_array, bw=False)
    self.repaint()

  @staticmethod
  def convertQImageToMat(img):
    h = img.height()
    w = img.width()
    img = img.convertToFormat(QImage.Format_RGBA8888)
    bytesperline = img.bytesPerLine()
    img_array = np.asarray(img.constBits())
    print("orig h=%s, w=%s, bytesperline %s, asarray size: %s" % (h, w, bytesperline, img_array.shape))
    img_array = np.copy(img_array)
    img_array.resize([h, w, 4])
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    return img_array

  def onFilePathButton(self):
    supportedFormats = QImageReader.supportedImageFormats()
    text_filter = "Images ({})".format(" ".join(["*.{}".format(fo.data().decode()) for fo in supportedFormats]))
    filename, _ = QFileDialog.getOpenFileName(self, "Open Image", dir=os.path.join("..", "data"), filter=text_filter)
    if len(filename) == 0:
      # User likely picked "cancel", don't change anything
      return
    self.ui.filePathDisplay.setText(filename)
    self.args.imgpath = filename
    loaded_image      = QImage(filename, format=QImage.Format_BGR888)
    if (loaded_image.hasAlphaChannel()):
      print("Found an alpha channel, drawing it onto white background")
      tmp = QImage(loaded_image.width(), loaded_image.height(), QImage.Format_BGR888)
      tmp.fill(QtCore.Qt.white)
      painter = QPainter(tmp)
      painter.drawImage(QtCore.QPoint(0,0), loaded_image)
      del painter
      loaded_image = tmp.convertToFormat(QImage.Format_BGR888)
    self.ui.topPic.setImage(loaded_image)
    self.args.img = self.convertQImageToMat(loaded_image)
    self.ui.convertButton.setEnabled(True)

  def onWValueChanged(self, val):
    self.args.maxW = val

  def onHValueChanged(self, val):
    self.args.maxH = val

  def onCValueChanged(self, val):
    self.args.maxC = val

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
    """
    Currently unused, but a good reference for some of the unicode symbol things
    """
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
