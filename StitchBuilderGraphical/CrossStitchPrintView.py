# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
import numpy as np

from KeyCreatorHeadless import KeyCreatorHeadless
from TextRectRenderer import TextRect
import StitchConstants

def createRectVectorized(x, y, w, h):
  """
  Create rectangles in a vectorized way for numpy
  """
  return QtCore.QRectF(x, y, w, h)

class CrossStitchPrintView(QtWidgets.QWidget):

  def __init__(self, parent = None, sizefactor = 1.0):
    super().__init__(parent)
    self.img_thread_array = None
    self.text_rects       = None
    self.staticTexts      = None
    self.sizefactor       = sizefactor

    # Set font sizes, square sizes
    self.squaresize = int(round(StitchConstants.SQUARE_SIDE_LEN_PX * self.sizefactor))
    self.marginsize = int(round(StitchConstants.GRID_LABEL_MARGIN_BASE_PX * self.sizefactor))
    self.fontsize   = int(round(StitchConstants.FONT_BASE_SIZE_PT * self.sizefactor))
    self.font       = QtGui.QFont("sans-serif", pointSize=self.fontsize)

  def minimumSizeHint(self):
    if self.text_rects is not None:
      w = self.squaresize * self.text_rects.shape[1]
      h = self.squaresize * self.text_rects.shape[0]
      w += self.marginsize * 2
      h += self.marginsize * 2
      return QtCore.QSize(w, h)
    else:
      return QtCore.QSize(200, 200)

  def sizeHint(self):
    return self.minimumSizeHint()

  def constructTextRectBounds(self, img_thread_array):
    """
    Gives the graphical coordinates for each ending rectangle
    Note: wants to use the sub-thread-array (the displayed section), not the whole image
    Doing this in a vectorized way for fun (and to avoid inefficient loops)
    """
    h, w    = img_thread_array.shape
    xx, yy  = np.meshgrid(np.arange(w), np.arange(h))
    xcoords = xx * self.squaresize
    ycoords = yy * self.squaresize
    xcoords += self.marginsize
    ycoords += self.marginsize
    bounds  = np.frompyfunc(createRectVectorized, 4, 1)(xcoords, ycoords, self.squaresize, self.squaresize)
    return bounds

  def constructStaticTexts(self, view_rect):
    """
    view_rect has tl_x(), tl_y(), width, and height
    we also have a GRID_NUM_INTERVAL
    want to create a horizontal label for each number in [tl_x():tl_x()+width] where number % GRID_NUM_INTERVAL == 0
    """
    # Predefine our return value list
    retval = []

    # Find out where conceptually we need to draw labels
    xvals = np.arange(view_rect.x(), view_rect.x() + view_rect.width())  #+ 1 # ADDING 1 FOR HUMAN INDEXING
    yvals = np.arange(view_rect.y(), view_rect.y() + view_rect.height()) #+ 1 # ADDING 1 FOR HUMAN INDEXING
    xidx_matches = np.logical_and(np.equal(0, np.mod(xvals, StitchConstants.GRID_NUM_INTERVAL)), np.greater(xvals, 0))
    yidx_matches = np.logical_and(np.equal(0, np.mod(yvals, StitchConstants.GRID_NUM_INTERVAL)), np.greater(yvals, 0))
    xlabel_offset_indices = np.where(xidx_matches)[0]
    ylabel_offset_indices = np.where(yidx_matches)[0]
    xlabel_numbers = xvals[xlabel_offset_indices]
    ylabel_numbers = yvals[ylabel_offset_indices]
    # Now we have (1) which square index in our grid gets a label, and (2) what its label is
    # Next step: figure out our "bottom center" point for each label (recall two points for each label)
    xlabel_positions_x = xlabel_offset_indices * self.squaresize + self.marginsize
    ylabel_positions_y = ylabel_offset_indices * self.squaresize + self.marginsize
    xlabel_position_y1 = self.marginsize
    xlabel_position_y2 = self.marginsize + view_rect.height() * self.squaresize
    ylabel_position_x1 = self.marginsize
    ylabel_position_x2 = self.marginsize + view_rect.width() * self.squaresize

    for i, number in enumerate(xlabel_numbers):
      p_x  = xlabel_positions_x[i]
      p_y1 = xlabel_position_y1
      p_y2 = xlabel_position_y2
      point1 = (p_x, p_y1)
      point2 = (p_x, p_y2)
      retval.append((QtGui.QStaticText("{:d}".format(number)), point1, "T"))
      retval.append((QtGui.QStaticText("{:d}".format(number)), point2, "B"))
    for i, number in enumerate(ylabel_numbers):
      p_y  = ylabel_positions_y[i]
      p_x1 = ylabel_position_x1
      p_x2 = ylabel_position_x2
      point1 = (p_x1, p_y)
      point2 = (p_x2, p_y)
      retval.append((QtGui.QStaticText("{:d}".format(number)), point1, "L"))
      retval.append((QtGui.QStaticText("{:d}".format(number)), point2, "R"))

    return retval

  def consumeImage(self, img_thread_array, bw, view_rect = None):
    """
    Parameters:
      img_thread_array (np.ndarray): 2-dimensional array of ThreadEntry objects describing the color to stitch
      bw (bool): Whether to render for B&W viewing/printing or color
      view_rect (Rect): object with x(), y(), topleft(), width(), and height() methods describing the sub-rectangle to render
    """
    if view_rect is None:
      view_rect = QtCore.QRect(0, 0, img_thread_array.shape[1], img_thread_array.shape[0])
    # Store info about display area
    self.rect = view_rect # represents sub-area of whole image (useful for coordinates)
    # store the sub-area we'll actually display
    self.img_thread_array = img_thread_array[view_rect.y():(view_rect.y() + view_rect.height()),
                                             view_rect.x():(view_rect.x() + view_rect.width())]
    # Create structures to hold created objects
    self.keyCreator = KeyCreatorHeadless(img_thread_array) # creating key from whole image to keep consistent color mapping
    self.text_rects = np.zeros(self.img_thread_array.shape, dtype=object)

    # Determine coordinates for ending display items
    trbounds = self.constructTextRectBounds(self.img_thread_array)

    # Construct the TextRect objects
    texts = np.zeros(self.img_thread_array.shape, dtype=object)
    for i, r in enumerate(self.img_thread_array): # okay fine one nested for loop
      for j, entry in enumerate(r):
        texts[i,j] = self.keyCreator[entry]
    self.text_rects = np.frompyfunc(TextRect.initPyFunc, 5, 1)(trbounds, texts, self.img_thread_array, bw, self.font)

    # Construct the StaticText objects for grid markings
    self.staticTexts = self.constructStaticTexts(view_rect)

    self.updateGeometry()
    self.repaint()

  @staticmethod
  def renderStaticText(painter, st, point, orientation, font):
    """
    New approach: try to apply a transform directly
    The parameter "point" is the "bottom center" of where we're drawing
    """
    st.prepare(font = font)
    fontwidth   = st.size().width()
    fontheight  = st.size().height()
    bc_to_tl = (-fontwidth / 2.0, -fontheight)
    if orientation == "T":
      rotation = 0
    elif orientation == "B":
      rotation = 0
      bc_to_tl = (-fontwidth / 2.0, 0.0)
    elif orientation == "L":
      rotation = 270
    elif orientation == "R":
      rotation = 90
    xform = QtGui.QTransform.fromTranslate(point[0], point[1])
    xform = xform.rotate(rotation)
    xform = xform.translate(bc_to_tl[0], bc_to_tl[1])
    painter.save()
    painter.setTransform(xform)
    painter.drawStaticText(QtCore.QPointF(0.0, 0.0), st)
    painter.restore()

  @staticmethod
  def renderStaticTexts(painter, staticTextTuples, font):
    painter.setFont(font)
    painter.setPen(QtGui.QPen(QtCore.Qt.black))
    for (st, point, orientation) in staticTextTuples:
      CrossStitchPrintView.renderStaticText(painter, st, point, orientation, font)

  def paintEvent(self, event):
    super().paintEvent(event)
    #TODO: bound this method to event.rect()
    painter = QtGui.QPainter(self)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text_rects is not None:
      for r in self.text_rects:
        for tr in r:
          tr.paint(painter)
    if self.staticTexts is not None:
      CrossStitchPrintView.renderStaticTexts(painter, self.staticTexts, self.font)
    painter.end()




