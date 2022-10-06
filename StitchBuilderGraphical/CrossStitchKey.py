# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from KeyCreatorHeadless import KeyCreatorHeadless
from TextRectRenderer import TextRect
import StitchConstants

class CrossStitchKey(QtWidgets.QWidget):

  def __init__(self, parent=None):
    super().__init__(parent)
    self.keyCreator = None
    #self.scroll       = QtWidgets.QScrollArea(self)
    self.keyNoScroll  = CrossStitchKeyNoScroll(self)

    print("Size hint for key: %s" % self.sizeHint())

  def consumeImage(self, img_thread_array, bw=False):
    self.keyNoScroll.consumeImage(img_thread_array, bw)
    self.keyCreator = self.keyNoScroll.keyCreator
    
  def paintEvent(self, event):
    super().paintEvent(event)
    self.lastDesiredRect = event.rect()
    print("Resizing noscroll to desired rectangle %s" % self.lastDesiredRect)

class CrossStitchKeyEntry(QtWidgets.QWidget):
  """
  visually looks like:
  [s] Thread Display Name
  """

  def __init__(self, bw, font, squaresize, parent=None):
    super().__init__(parent)
    self.text = None
    self.renderWidget = None
    self.font = font
    self.bw = bw
    self.squaresize = squaresize

  @property
  def edge_margin(self):
    return int(self.squaresize / 12.0)

  @property
  def mid_margin(self):
    return int(self.squaresize / 6.0)
  
  def setEntry(self, threadentry, symbol, stitch_count):
    # TODO: display the stitch count somewhere
    # Determine text contents
    self.text = "%s (%s)" % (threadentry.DisplayNumStr, threadentry.DisplayName)
    self.statictext = QtGui.QStaticText(self.text)
    self.statictext.prepare(font=self.font)

    # Determine rectangles and top-left positions
    stsize = self.statictext.size()
    self.stwidth = stsize.width()
    self.stheight = stsize.height()

    tr_start_x = self.edge_margin
    tr_start_y = self.edge_margin
    tr_rect = QtCore.QRectF(tr_start_x, tr_start_y, self.squaresize, self.squaresize)
    st_start_x = tr_start_x + self.squaresize + self.mid_margin
    vert_extents = self.squaresize + 2 * self.edge_margin
    st_start_y = (vert_extents - self.stheight) / 2.0
    self.st_topleft = QtCore.QPoint(st_start_x, st_start_y)

    # Create TextRect
    self.renderTextRect = TextRect(tr_rect, symbol, threadentry, self.bw, self.font)

    # Save pen, brush for the static text
    self.pen = QtGui.QPen(QtCore.Qt.black)

  def minimumSizeHint(self):
    vert_extents = self.squaresize + 2 * self.edge_margin
    if self.text is not None:
      horiz_extents = self.edge_margin * 2 + self.mid_margin
      horiz_extents += self.stwidth
      horiz_extents += self.squaresize
      vert_extents = max(vert_extents, self.stheight)#probably won't be text taller than square
    else:
      horiz_extents = 48
    return QtCore.QSize(horiz_extents, vert_extents)

  def sizeHint(self):
    return self.minimumSizeHint()

  def paintEvent(self, event):
    super().paintEvent(event)
    painter = QtGui.QPainter(self)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text is not None:
      painter.setPen(self.pen)
      painter.setFont(self.font)
      painter.drawStaticText(self.st_topleft, self.statictext)
      self.renderTextRect.paint(painter)

class CrossStitchKeyNoScroll(QtWidgets.QWidget):

  def __init__(self, parent=None, sizefactor = 1.0):
    super().__init__(parent)
    self.keyCreator = None

    self.glayout = QtWidgets.QGridLayout()
    self.setLayout(self.glayout)

    self.setSizeFactor(sizefactor)

  def setSizeFactor(self, sizefactor):
    self.sizefactor = sizefactor

    fontsize_pt = int(round(StitchConstants.FONT_BASE_SIZE_PT * self.sizefactor))

    self.font = QtGui.QFont("sans-serif", pointSize=fontsize_pt)
    self.squaresize = int(round(StitchConstants.SQUARE_SIDE_LEN_PX * self.sizefactor))

  def clearOldContents(self):
    for i in reversed(range(self.glayout.rowCount())):
      for j in reversed(range(self.glayout.columnCount())):
        item = self.glayout.itemAtPosition(i, j)
        if item is not None:
          item.widget().deleteLater()
          self.glayout.removeWidget(item.widget())
    self.glayout.update()

  def consumeImage(self, img_thread_array, threadcount_dict, bw, columns = 4):
    self.gcols = columns
    # Clear our grid layout of anything that was in there previously
    self.clearOldContents()

    # Create our array of ThreadEntry objects to serve as our colors
    self.keyCreator = KeyCreatorHeadless(img_thread_array)
    threadlist = list(self.keyCreator.keys())
    white_entry = None
    white_list = [x for x in threadlist if x.dmc_num == "white"]
    if len(white_list):
      white_entry = white_list[0]
      threadlist = [x for x in threadlist if x.dmc_num != "white"]
    threads_sorted = sorted(threadlist, key=lambda x: int(x.dmc_num))
    if white_entry is not None:
      threads_sorted = [white_entry] + threads_sorted

    # Create and add widgets for each thread
    for i, t in enumerate(threads_sorted):
      entry_widget = CrossStitchKeyEntry(bw=bw, font=self.font, squaresize=self.squaresize)
      entry_widget.setEntry(t, self.keyCreator[t], threadcount_dict[t])
      col = i % self.gcols
      row = i / self.gcols
      self.glayout.addWidget(entry_widget, row, col)
    self.updateGeometry()
    self.repaint()


  def paintEvent(self, event):
    super().paintEvent(event)

