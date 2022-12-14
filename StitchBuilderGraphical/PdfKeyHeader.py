# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFrame

import numpy as np

from CrossStitchKey import CrossStitchKeyNoScroll
import StitchConstants

class PdfKeyHeader(QFrame):
  MAX_COL_COUNT       = 8

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    self.setLineWidth(4 * StitchConstants.PRINT_SIZEFACTOR)
    self.keyWidget = None

    # Construct layout
    self.vlayout = QtWidgets.QVBoxLayout()

    # Construct "Key" label
    self.klabel = QtWidgets.QLabel("Key", self)
    fontsize = int(round(16 * StitchConstants.PRINT_SIZEFACTOR))
    self.klabel.setText('<html><head/><body><p align="center"><span style=" font-size:{fontsize:d}pt; font-weight:700;">{text:s}</span></p></body></html>'.format(fontsize = fontsize, text="Key"))
    self.vlayout.addWidget(self.klabel, alignment=QtCore.Qt.AlignCenter)


    self.setLayout(self.vlayout)

  def clearOldKeyWidget(self):
    self.vlayout.removeWidget(self.keyWidget)
    self.keyWidget.deleteLater()
    self.keyWidget = None

  def consumeImage(self, threadarray, threadcount_dict, bw, maxWidth):
    if self.keyWidget is not None:
      self.clearOldKeyWidget()
    unique_elements = np.unique(threadarray)
    columns = min(PdfKeyHeader.MAX_COL_COUNT, len(unique_elements))
    # Size key to available size
    found_col_count = False
    while not found_col_count:
      # need to remake the keyWidget, otherwise deletions don't happen correctly before rendering and everything goes to hell
      keyWidget = CrossStitchKeyNoScroll(sizefactor=StitchConstants.PRINT_SIZEFACTOR)
      keyWidget.consumeImage(threadarray, threadcount_dict, bw, columns=columns)
      print("Trying column count %s, keyWidget width %s of print_size_pixels width %s" % (columns, keyWidget.sizeHint().width(), maxWidth))
      if keyWidget.sizeHint().width() < maxWidth:
        found_col_count = True
      else:
        columns -= 1
    self.keyWidget = keyWidget

    self.vlayout.addWidget(self.keyWidget)

    self.updateGeometry()
