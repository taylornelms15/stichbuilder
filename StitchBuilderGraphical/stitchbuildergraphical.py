# This Python file uses the following encoding: utf-8
import sys
import os.path
import cv2
import numpy as np

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QImageReader, QPainter

from ImageConverter import ImageConverter, ImageConverterResultImages
from PdfCreator import PdfCreator
import StitchConstants

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_StitchBuilderGraphical

GRID_COLUMN_COUNT = 6

# Filter Slider parameters
FILTER_SLIDER_MAX_REAL_VAL = 2.0

# Some text constants
SAVE_PDF_BUTTON_TEXT_NORMAL   = "Save PDF"
SAVE_PDF_BUTTON_TEXT_WORKING  = "Saving..."

class StitchBuilderArgs(object):
  def __init__(self):
    self.filterStrength = 0.0
    self.maxW = ImageConverter.ABSOLUTE_MAX_W
    self.maxH = ImageConverter.ABSOLUTE_MAX_H
    self.maxC = ImageConverter.ABSOLUTE_MAX_C
    self.dithering  = True
    self.bw         = False
    self.imgpath    = None
    self.img        = None

class ImageConverterWorker(QtCore.QObject):
  finished =  QtCore.Signal(ImageConverterResultImages)
  scalingDone = QtCore.Signal(np.ndarray)
  filterDone = QtCore.Signal(np.ndarray)

  def __init__(self, converter, img, parent=None):
    super().__init__(parent)
    self.convert = converter
    self.img = img

  def run(self):
    print("Conversion starting")
    results = self.convert.convert(self.img, [self.scalingDoneCallback, self.filterDoneCallback])
    print("Conversion ending")
    self.finished.emit(results)

  def scalingDoneCallback(self, img):
    self.scalingDone.emit(img)
  def filterDoneCallback(self, img):
    self.filterDone.emit(img)

class PdfCreatorWorker(QtCore.QObject):
  finished = QtCore.Signal(str)
  def __init__(self, filename, img_threadcolor, threadarray, bw, parent=None):
    super().__init__(parent)
    self.filename = filename
    self.pdfCreator = PdfCreator(filename)
    self.img_threadcolor = img_threadcolor
    self.threadarray = threadarray
    self.bw = bw

  def run(self):
    print("Starting to write pdf")
    self.pdfCreator.consumeImage(self.threadarray, self.bw, self.img_threadcolor)
    print("Finished writing PDF")
    self.finished.emit(self.filename)

class StitchBuilderGraphical(QWidget):
  def __init__(self, parent=None):
    # Initialization
    super().__init__(parent)
    self.ui = Ui_StitchBuilderGraphical()
    self.ui.setupUi(self)
    self.setWindowTitle(StitchConstants.PROGRAM_NAME)

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

    # B&W
    checkbox = self.ui.bwCheckBox
    checkbox.toggled.connect(self.onBWBoxChecked)

    # Spin Boxes (maxW, maxH, maxC)
    self.initSpinBoxes()

    # Convert Button
    cButton = self.ui.convertButton
    cButton.setEnabled(False)#initially no filepath, so set to disabled
    cButton.clicked.connect(self.onConvertButton)

    # Conversion Results
    self.threadarray_results = None
    self.ui.OriginalImageLabel.setHidden(True)
    self.ui.AfterFilterImageLabel.setHidden(True)
    self.ui.ReducedColorspaceImageLabel.setHidden(True)
    self.ui.ThreadColorImageLabel.setHidden(True)

    # PDF Button
    self.ui.savePdfButton.setText(SAVE_PDF_BUTTON_TEXT_NORMAL)
    self.ui.savePdfButton.setHidden(True)
    self.ui.savePdfButton.clicked.connect(self.onSavePdfButton)

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
    self.worker.scalingDone.connect(self.onImageScalingFinished)
    self.worker.filterDone.connect(self.onImageFilteringFinished)
    # Step 5.5: disable the button to avoid multi-click
    self.ui.convertButton.setEnabled(False)
    # Step 6: Start the thread
    self.thread.start()

  def onSavePdfButton(self):
    threadarray = self.threadarray_results
    if threadarray is None:
      # Should not happen
      return
    fileName, _ = QFileDialog.getSaveFileName(self, caption="Save Pdf",
                               filter="PDF (*.pdf)")
    # Create a QThread object
    self.pdf_thread = QtCore.QThread()
    # Step 3: Create a worker object
    self.pdf_worker = PdfCreatorWorker(fileName, self.img_thread_color, threadarray, self.args.bw)
    # Step 4: Move worker to the thread
    self.pdf_worker.moveToThread(self.pdf_thread)
    # Step 5: Connect signals and slots
    self.pdf_thread.started.connect(self.pdf_worker.run)
    self.pdf_worker.finished.connect(self.pdf_thread.quit)
    self.pdf_worker.finished.connect(self.pdf_worker.deleteLater)
    self.pdf_thread.finished.connect(self.pdf_thread.deleteLater)
    self.pdf_worker.finished.connect(self.onSavePdfFinished)
    # Step 5.5: Disable the button, change text as indicator of progress
    self.ui.savePdfButton.setEnabled(False)
    self.ui.savePdfButton.setText(SAVE_PDF_BUTTON_TEXT_WORKING)
    # Step 6: Start the thread
    self.pdf_thread.start()

  def onImageScalingFinished(self, img_scaled):
    h, w, _ = img_scaled.shape
    img_scaled              = QImage(img_scaled, w, h, QImage.Format_RGBA8888)
    self.ui.OriginalImageLabel.setHidden(False)
    self.ui.OriginalImageLabel.setImage(img_scaled)

  def onImageFilteringFinished(self, img_post_filter):
    h, w, _ = img_post_filter.shape
    after_filter            = QImage(img_post_filter,  w, h, QImage.Format_RGBA8888)
    self.ui.AfterFilterImageLabel.setHidden(False)
    self.ui.AfterFilterImageLabel.setImage(after_filter)

  def onConversionFinished(self, resultobj):
    self.ui.convertButton.setEnabled(True)
    # Get results
    h, w, _ = resultobj.img_scaled.shape
    img_reduced_colorspace  = QImage(resultobj.img_reduced_colorspace,  w, h, QImage.Format_RGBA8888)
    img_thread_color        = QImage(resultobj.img_thread_color,  w, h, QImage.Format_RGBA8888)

    # Save results
    self.threadarray_results = resultobj.img_thread_array
    self.img_thread_color    = img_thread_color

    # Change UI elements now that we have results
    self.ui.ReducedColorspaceImageLabel.setHidden(False)
    self.ui.ReducedColorspaceImageLabel.setImage(img_reduced_colorspace)
    self.ui.ThreadColorImageLabel.setHidden(False)
    self.ui.ThreadColorImageLabel.setImage(img_thread_color)
    self.ui.savePdfButton.setHidden(False)

    self.ui.crossStitchKey.consumeImage(resultobj.img_thread_array, bw=self.args.bw)
    self.ui.RightSideScrollableContents.consumeImage(resultobj.img_thread_array, bw=self.args.bw)
    self.repaint()

  def onSavePdfFinished(self, filename):
    self.ui.savePdfButton.setEnabled(True)
    self.ui.savePdfButton.setText(SAVE_PDF_BUTTON_TEXT_NORMAL)
    displayText = "Saved pdf to %s" % filename
    QMessageBox.information(self, "Save Complete", displayText)

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
    filename, _ = QFileDialog.getOpenFileName(self, "Open Image", filter=text_filter)
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

  def onBWBoxChecked(self, val):
    if (val):
      self.ui.bwCheckBox.setText("Black and White Pattern Output")
      self.args.bw = True
    else:
      self.ui.bwCheckBox.setText("Color Pattern Output")
      self.args.bw = False


  def onDitherBoxChecked(self, val):
    if (val):
      self.ui.ditherCheckBox.setText("Dithering On")
      self.args.dithering = True
    else:
      self.ui.ditherCheckBox.setText("Dithering Off")
      self.args.dithering = False

  def loadTestImage(self):
    if StitchConstants.FROZEN:
      test_path = os.path.join(os.path.dirname(__file__), "data", "InputAnImage.png")
    else:
      test_path = os.path.join("..", "data", "InputAnImage.png")
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
