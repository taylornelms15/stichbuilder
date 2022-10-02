# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget

import numpy as np


MARGINSIZE_IN       = 0.5
RESOLUTION_DPI      = 600
DISPLAY_SIZEFACTOR  = RESOLUTION_DPI / 96 #96 conceptual pixels per inch for accurate font rendering

import PdfKeyHeader

class PdfCreator:

  def __init__(self, filename):
    self.filename = filename

  def consumeImage(self, threadarray, bw):
    # Set up PdfWriter with paper size, orientation, margins, etc
    writer = QtGui.QPdfWriter(self.filename)
    writer.setResolution(RESOLUTION_DPI)
    writer.setPageSize(QtGui.QPageSize.Letter)
    writer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)
    writer.setPageMargins(QtCore.QMarginsF(MARGINSIZE_IN, MARGINSIZE_IN, MARGINSIZE_IN, MARGINSIZE_IN),
            QtGui.QPageLayout.Inch)

    # Compute rendering space available given page layout
    pagelayout = writer.pageLayout()
    print_area_px = pagelayout.paintRectPixels(writer.logicalDpiX())
    print("Pixels of paint area: %s" % (print_area_px,))

    # Create painter with which to render onto pages
    painter = QtGui.QPainter(writer)

    # Create header key widget
    keyWidget = PdfKeyHeader.PdfKeyHeader()
    keyWidget.consumeImage(threadarray, bw, print_area_px.width())

    # Determine rendering position based on sizehint
    kwidth  = keyWidget.sizeHint().width()
    kheight = keyWidget.sizeHint().height()
    margin_x_px = (print_area_px.width() - kwidth) / 2.0

    print("Key widget total size width %s, height %s" % (kwidth, kheight))

    keyWidget.render(painter, QtCore.QPoint(margin_x_px, 0), renderFlags=QWidget.RenderFlags(QWidget.RenderFlag.DrawChildren))

    painter.end()
