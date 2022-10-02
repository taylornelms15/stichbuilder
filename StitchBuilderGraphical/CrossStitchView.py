# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from KeyCreatorHeadless import KeyCreatorHeadless
from TextRectRenderer import TextRect
import StitchConstants

import numpy as np


class CrossStitchView(QtWidgets.QWidget):
  csFont = QtGui.QFont("sans-serif", pointSize=12)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.img_thread_array = None
    self.text_rects = None

  def minimumSizeHint(self):
    if self.text_rects is not None:
      return QtCore.QSize(StitchConstants.SQUARE_SIDE_LEN_PX * self.text_rects.shape[1], StitchConstants.SQUARE_SIDE_LEN_PX * self.text_rects.shape[0])
    else:
      return QtCore.QSize(200, 200)

  def consumeImage(self, img_thread_array, bw):
    self.img_thread_array = img_thread_array
    h, w = img_thread_array.shape

    self.keyCreator = KeyCreatorHeadless(img_thread_array)

    self.text_rects = np.zeros(img_thread_array.shape, dtype=object)
    for i, r in enumerate(img_thread_array):
      for j, entry in enumerate(r):
        left = j * StitchConstants.SQUARE_SIDE_LEN_PX
        top  = i * StitchConstants.SQUARE_SIDE_LEN_PX
        rect = QtCore.QRectF(left, top, StitchConstants.SQUARE_SIDE_LEN_PX, StitchConstants.SQUARE_SIDE_LEN_PX)
        try:
          text = self.keyCreator[entry]
        except KeyError as e:
          print("could not find %s among keys %s" % (entry, self.keyCreator.keys()))
          raise e
        tr = TextRect(rect, text, entry, bw, CrossStitchView.csFont)
        self.text_rects[i][j] = tr
    self.updateGeometry()
    self.repaint()

  def paintEvent(self, event):
    super().paintEvent(event)
    #TODO: bound this method to the region in event.rect()
    painter = QtGui.QPainter(self)

    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text_rects is not None:
      for i, r in enumerate(self.text_rects):
        for j, tr in enumerate(r):
          tr.paint(painter)

