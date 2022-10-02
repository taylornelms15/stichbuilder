# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget

from CrossStitchPrintView import CrossStitchPrintView
from PdfKeyHeader import PdfKeyHeader
from PrintDivider import PrintDivider
import StitchConstants

MARGINSIZE_IN       = 0.5
RESOLUTION_DPI      = 600
DISPLAY_SIZEFACTOR  = RESOLUTION_DPI / 96 #96 conceptual pixels per inch for accurate font rendering


class PdfCreator:
  RENDER_FLAGS = QWidget.RenderFlags(QWidget.RenderFlag.DrawChildren)

  def __init__(self, filename):
    self.filename = filename

  @staticmethod
  def getPrintRowsColumnsPerPage(print_area_px, kwidth, kheight):
    """
    Gets the max number of rows and columns we can display per page, given the space taken up by the key
    """
    h_avail = print_area_px.height() - kheight
    w_avail = print_area_px.width()
    # remove the coordinate margin
    h_avail -= int(round(2.0 * StitchConstants.GRID_LABEL_MARGIN_BASE_PX * StitchConstants.PRINT_SIZEFACTOR))
    w_avail -= int(round(2.0 * StitchConstants.GRID_LABEL_MARGIN_BASE_PX * StitchConstants.PRINT_SIZEFACTOR))
    c_max   = int(w_avail) / int(round(StitchConstants.SQUARE_SIDE_LEN_PX * StitchConstants.PRINT_SIZEFACTOR))
    r_max   = int(h_avail) / int(round(StitchConstants.SQUARE_SIDE_LEN_PX * StitchConstants.PRINT_SIZEFACTOR))
    return (c_max, r_max)

  def consumeImage(self, threadarray, bw, img_threadcolor):
    # Set up PdfWriter with paper size, orientation, margins, etc
    writer = QtGui.QPdfWriter(self.filename)
    writer.setResolution(StitchConstants.RESOLUTION_DPI)
    writer.setPageSize(QtGui.QPageSize.Letter)
    writer.setPageOrientation(QtGui.QPageLayout.Orientation.Landscape)
    writer.setPageMargins(QtCore.QMarginsF(StitchConstants.MARGINSIZE_IN,
                                           StitchConstants.MARGINSIZE_IN,
                                           StitchConstants.MARGINSIZE_IN,
                                           StitchConstants.MARGINSIZE_IN),
                          QtGui.QPageLayout.Inch)

    # Compute rendering space available given page layout
    pagelayout = writer.pageLayout()
    print_area_px = pagelayout.paintRectPixels(writer.logicalDpiX())
    print("Pixels of paint area: %s" % (print_area_px,))

    # Create painter with which to render onto pages
    painter = QtGui.QPainter(writer)

    # Create header key widget
    keyWidget = PdfKeyHeader()
    keyWidget.consumeImage(threadarray, bw, print_area_px.width())

    # Determine rendering position based on sizehint
    kwidth  = keyWidget.sizeHint().width()
    kheight = keyWidget.sizeHint().height()
    kmargin_x_px = (print_area_px.width() - kwidth) / 2.0

    print("Key widget total size width %s, height %s" % (kwidth, kheight))

    # Get the way we're going to split this PDF up
    c_max, r_max = PdfCreator.getPrintRowsColumnsPerPage(print_area_px, kwidth, kheight)
    divisions = PrintDivider(threadarray.shape[1], threadarray.shape[0], c_max, r_max).getRectangles()
    divisions = divisions.ravel()
    print(divisions)
    for i, rect in enumerate(divisions):
      # Make new page if we're past the first page
      if i > 0:
        writer.newPage()

      # Render key widget
      keyWidget.render(painter, QtCore.QPoint(kmargin_x_px, 0), renderFlags = PdfCreator.RENDER_FLAGS)

      # Render page content
      csWidget = CrossStitchPrintView(parent = None, sizefactor = StitchConstants.PRINT_SIZEFACTOR)
      csWidget.consumeImage(threadarray, bw, rect)

      cwidth  = csWidget.sizeHint().width()
      cheight = csWidget.sizeHint().height()
      cmargin_x_px = (print_area_px.width() - cwidth) / 2.0
      cmargin_y_px = (print_area_px.height() - kheight - cheight) / 2.0 + kheight

      csWidget.render(painter, QtCore.QPoint(cmargin_x_px, cmargin_y_px), renderFlags = PdfCreator.RENDER_FLAGS)



    painter.end()
