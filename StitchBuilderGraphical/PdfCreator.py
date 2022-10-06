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
  def getPrintRowsColumnsPerPage(print_area_px):
    """
    Gets the max number of rows and columns we can display per page. Assume no space taken up by key, etc (for now)
    """
    h_avail = print_area_px.height()
    w_avail = print_area_px.width()
    # remove the coordinate margin
    h_avail -= int(round(2.0 * StitchConstants.GRID_LABEL_MARGIN_BASE_PX * StitchConstants.PRINT_SIZEFACTOR))
    w_avail -= int(round(2.0 * StitchConstants.GRID_LABEL_MARGIN_BASE_PX * StitchConstants.PRINT_SIZEFACTOR))
    c_max   = int(w_avail) / int(round(StitchConstants.SQUARE_SIDE_LEN_PX * StitchConstants.PRINT_SIZEFACTOR))
    r_max   = int(h_avail) / int(round(StitchConstants.SQUARE_SIDE_LEN_PX * StitchConstants.PRINT_SIZEFACTOR))
    return (c_max, r_max)

  def renderThreadColorImage(self, painter, img_threadcolor, kheight, print_area_px):
    deadHeight = int(round(kheight + StitchConstants.PREVIEW_IMAGE_MARGIN_BASE_PX * StitchConstants.PRINT_SIZEFACTOR))
    avail_w = print_area_px.width()
    avail_h = print_area_px.height() - deadHeight
    # Scale image as big as we can reasonably get it
    max_scale_x = int(avail_w) / int(img_threadcolor.width())
    max_scale_y = int(avail_h) / int(img_threadcolor.height())
    scale = min(max_scale_x, max_scale_y)
    if scale == 0:
      # Indicates we're printing more threads than we have pixels available to us on the page
      # TODO: support such a terrible eventuality
      raise ValueError
    newsize = QtCore.QSize(img_threadcolor.width() * scale, img_threadcolor.height() * scale)
    img_to_render = img_threadcolor.scaled(newsize, mode = QtCore.Qt.FastTransformation)
    # Figure out where we're putting it
    iwidth = img_to_render.width()
    iheight = img_to_render.height()
    imargin_x_px = (avail_w - iwidth) / 2.0
    imargin_y_px = (avail_h - iheight) / 2.0 + deadHeight
    drawpoint = QtCore.QPointF(imargin_x_px, imargin_y_px)
    painter.drawImage(drawpoint, img_to_render)


  def printPageNumber(self, painter, page_num, total_pages, print_area_px):
    # Create StaticText
    fontsize = int(round(StitchConstants.FONT_BASE_SIZE_PT * StitchConstants.PRINT_SIZEFACTOR))
    pageNumFont = QtGui.QFont("sans-serif", pointSize = fontsize)
    pagenum_text = "Page %s of %s" % (page_num, total_pages)
    st =  QtGui.QStaticText(pagenum_text)
    st.prepare(font=pageNumFont)
    st_w = st.size().width()

    # Figure out where text is going
    tl_x = print_area_px.width() - st_w
    tl_h = print_area_px.height() #drawing just outside the margin for the page number
    drawpoint = QtCore.QPointF(tl_x, tl_h)

    # Draw StaticText
    painter.setPen(QtGui.QPen(QtCore.Qt.black))
    painter.setFont(pageNumFont)
    painter.drawStaticText(drawpoint, st)

  def consumeImage(self, threadarray, threadcount_dict, bw, img_threadcolor):
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
    keyWidget.consumeImage(threadarray, threadcount_dict, bw, print_area_px.width())

    # Determine rendering position based on sizehint
    kwidth  = keyWidget.sizeHint().width()
    kheight = keyWidget.sizeHint().height()
    kmargin_x_px = (print_area_px.width() - kwidth) / 2.0

    # Render key widget
    keyWidget.render(painter, QtCore.QPoint(kmargin_x_px, 0), renderFlags = PdfCreator.RENDER_FLAGS)
    print("Key widget total size width %s, height %s" % (kwidth, kheight))

    # Render Summary Thread Color Image
    self.renderThreadColorImage(painter, img_threadcolor, kheight, print_area_px)

    # Get the way we're going to split this PDF up
    c_max, r_max = PdfCreator.getPrintRowsColumnsPerPage(print_area_px)
    divisions = PrintDivider(threadarray.shape[1], threadarray.shape[0], c_max, r_max).getRectangles()
    divisions = divisions.ravel()
    for i, rect in enumerate(divisions):
      # Start new page
      writer.newPage()

      # Render page content
      csWidget = CrossStitchPrintView(parent = None, sizefactor = StitchConstants.PRINT_SIZEFACTOR)
      csWidget.consumeImage(threadarray, bw, rect)

      cwidth  = csWidget.sizeHint().width()
      cheight = csWidget.sizeHint().height()
      cmargin_x_px = (print_area_px.width() - cwidth) / 2.0
      cmargin_y_px = (print_area_px.height() - cheight) / 2.0

      csWidget.render(painter, QtCore.QPoint(cmargin_x_px, cmargin_y_px), renderFlags = PdfCreator.RENDER_FLAGS)

      self.printPageNumber(painter, i + 1, len(divisions), print_area_px)



    painter.end()
