# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from UnicodeSymbols import UnicodeSymbols

import numpy as np

class TextRect(object):
  textDk = QtGui.QColor(0, 0, 0, 128)
  textLt = QtGui.QColor(255, 255, 255, 128)

  def __init__(self, rect, text, entry, flags):
    self.rect = rect
    self.text = text
    rgb = entry.getRGB()
    self.color = QtGui.QColor(rgb[0], rgb[1], rgb[2])
    self.pen = QtGui.QPen(QtCore.Qt.black)
    self.pen.setWidth(1)
    self.pen.setJoinStyle(QtCore.Qt.BevelJoin)
    self.brush = QtGui.QBrush(self.color)
    self.flags = flags
    if entry.getLightness() < 50:
      tcolor = TextRect.textLt
    else:
      tcolor = TextRect.textDk
    self.textpen = QtGui.QPen(tcolor)

  def paint(self, painter):
    painter.setPen(self.pen)
    painter.setBrush(self.brush)
    painter.drawRect(self.rect)
    painter.setPen(self.textpen)
    painter.drawText(self.rect, self.flags, self.text)


class CrossStitchView(QtWidgets.QWidget):
  csFont = QtGui.QFont("sans-serif", pointSize=12)
  csAlignmentFlags = (QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

  SQUARE_SIDE_LEN_PX = 24

  def __init__(self, parent=None):
    super().__init__(parent)
    print("Made my little widget")
    self.symbolDict = UnicodeSymbols()
    self.img_thread_array = None
    self.text_rects = None

  def minimumSizeHint(self):
    if self.text_rects is not None:
      return QtCore.QSize(CrossStitchView.SQUARE_SIDE_LEN_PX * self.text_rects.shape[1], CrossStitchView.SQUARE_SIDE_LEN_PX * self.text_rects.shape[0])
    else:
      return QtCore.QSize(200, 200)

  def consumeImage(self, img_thread_array):
    self.img_thread_array = img_thread_array
    h, w = img_thread_array.shape
    unique_elements, unique_inverse = np.unique(img_thread_array, return_inverse=True)
    unique_inverse = unique_inverse.reshape([h, w])
    #print("Unique elements: %s" % unique_elements)
    #print("Unique Inverse: %s" % unique_inverse)
    self.entryToUnicodeDict = self.symbolDict.constructMappingDict(unique_elements)
    print("Have mapping dict of len %s, and %s unique elements" % (len(self.entryToUnicodeDict), len(unique_elements)))

    self.text_rects = np.zeros(img_thread_array.shape, dtype=object)
    for i, r in enumerate(img_thread_array):
      for j, entry in enumerate(r):
        left = j * CrossStitchView.SQUARE_SIDE_LEN_PX
        top = i * CrossStitchView.SQUARE_SIDE_LEN_PX
        rect = QtCore.QRectF(left, top, CrossStitchView.SQUARE_SIDE_LEN_PX, CrossStitchView.SQUARE_SIDE_LEN_PX)
        try:
          text = self.entryToUnicodeDict[entry]
        except KeyError as e:
          print("could not find %s among keys %s" % (entry, self.entryToUnicodeDict.keys()))
          raise e
        tr = TextRect(rect, text, entry, CrossStitchView.csAlignmentFlags)
        self.text_rects[i][j] = tr
    self.updateGeometry()
    self.repaint()



  def paintEvent(self, event):
    super().paintEvent(event)
    painter = QtGui.QPainter(self)

    painter.setFont(CrossStitchView.csFont)

    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text_rects is not None:
      for i, r in enumerate(self.text_rects):
        for j, tr in enumerate(r):
          tr.paint(painter)
#    painter.setPen(QtCore.Qt.red)
#    painter.drawRect(5, 5, 80, 20)
#    painter.setBrush(QtCore.Qt.green)
#    painter.drawRect(10, 10, 20, 80)

