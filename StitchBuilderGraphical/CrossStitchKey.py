# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui

class CrossStitchKey(QtWidgets.QtWidget):

  def __init__(self, parent=None):
    super().__init__(parent)
    self.img_thread_array = None

  def minimumSizeHint(self):
    if self.text_rects is not None:
      return QtCore.QSize(200, 200)
    else:
      return QtCore.QSize(200, 200)
