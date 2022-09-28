# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from KeyCreatorHeadless import KeyCreatorHeadless
from TextRectRenderer import TextRect

import numpy as np


class CrossStitchView(QtWidgets.QWidget):
  csFont = QtGui.QFont("sans-serif", pointSize=12)

  SQUARE_SIDE_LEN_PX = 24

  def __init__(self, parent=None):
    super().__init__(parent)
    self.img_thread_array = None
    self.text_rects = None

  def minimumSizeHint(self):
    if self.text_rects is not None:
      return QtCore.QSize(CrossStitchView.SQUARE_SIDE_LEN_PX * self.text_rects.shape[1], CrossStitchView.SQUARE_SIDE_LEN_PX * self.text_rects.shape[0])
    else:
      return QtCore.QSize(200, 200)

  def createTestPdf(self):
    writer = QtGui.QPdfWriter("test.pdf")
    writer.setPageSize(QtGui.QPageSize.Letter)
    writer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)
    pen = QtGui.QPen(QtCore.Qt.black)
    painter = QtGui.QPainter(writer)
    painter.setPen(pen)
    for i in range(10):
      for j in range(20):
        painter.drawRect(i * 24, j * 24, 24, 24)
    painter.end()

  def consumeImage(self, img_thread_array, bw):
    self.img_thread_array = img_thread_array
    h, w = img_thread_array.shape

    self.keyCreator = KeyCreatorHeadless(img_thread_array)

    self.text_rects = np.zeros(img_thread_array.shape, dtype=object)
    for i, r in enumerate(img_thread_array):
      for j, entry in enumerate(r):
        left = j * CrossStitchView.SQUARE_SIDE_LEN_PX
        top = i * CrossStitchView.SQUARE_SIDE_LEN_PX
        rect = QtCore.QRectF(left, top, CrossStitchView.SQUARE_SIDE_LEN_PX, CrossStitchView.SQUARE_SIDE_LEN_PX)
        try:
          text = self.keyCreator[entry]
        except KeyError as e:
          print("could not find %s among keys %s" % (entry, self.keyCreator.keys()))
          raise e
        tr = TextRect(rect, text, entry, bw, CrossStitchView.csFont)
        self.text_rects[i][j] = tr
    self.updateGeometry()
    self.repaint()

    #self.createTestPdf()



  def paintEvent(self, event):
    super().paintEvent(event)
    painter = QtGui.QPainter(self)

    #painter.setFont(CrossStitchView.csFont)

    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text_rects is not None:
      for i, r in enumerate(self.text_rects):
        for j, tr in enumerate(r):
          tr.paint(painter)

