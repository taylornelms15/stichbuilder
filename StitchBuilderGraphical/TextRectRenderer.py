# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtGui

class TextRect(object):
  textDk = QtGui.QColor(0, 0, 0, 128)
  textLt = QtGui.QColor(255, 255, 255, 128)
  textBw = QtCore.Qt.black

  def __init__(self, rect, text, entry, bw, font):
    self.rect = rect
    self.text = text
    self.bw   = bw
    self.font = font
    rgb = entry.getRGB()
    self.color = QtGui.QColor(rgb[0], rgb[1], rgb[2])
    self.pen = QtGui.QPen(QtCore.Qt.black)
    self.pen.setWidth(1)
    self.pen.setJoinStyle(QtCore.Qt.BevelJoin)
    if (self.bw):
      self.brush = QtGui.QBrush(QtCore.Qt.white)
    else:
      self.brush = QtGui.QBrush(self.color)
    if (self.bw):
      tcolor = TextRect.textBw
    elif entry.getLightness() < 50:
      tcolor = TextRect.textLt
    else:
      tcolor = TextRect.textDk
    self.textpen = QtGui.QPen(tcolor)
    self.statictext = QtGui.QStaticText(self.text)
    self.statictext.prepare(font = self.font)

    # Find the top-left corner for the text (as opposed to the rectangle)
    stsize = self.statictext.size()
    add_x = (self.rect.width() - stsize.width()) / 2.0
    add_y = (self.rect.height() - stsize.height()) / 2.0
    self.st_left_top = self.rect.topLeft()
    self.st_left_top.setX(self.st_left_top.x() + add_x)
    self.st_left_top.setY(self.st_left_top.y() + add_y)

  def paint(self, painter):
    painter.setPen(self.pen)
    painter.setBrush(self.brush)
    painter.drawRect(self.rect)
    painter.setPen(self.textpen)
    painter.setFont(self.font)
    painter.drawStaticText(self.st_left_top, self.statictext)
