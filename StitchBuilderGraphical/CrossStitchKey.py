# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from KeyCreatorHeadless import KeyCreatorHeadless
from TextRectRenderer import TextRect

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
  EDGE_MARGIN         = 2
  MID_MARGIN          = 4
  SQUARE_SIDE_LEN_PX  = 24

  def __init__(self, bw, font, parent=None):
    super().__init__(parent)
    self.text = None
    self.renderWidget = None
    self.font = font
    self.bw = bw
  
  def setEntry(self, threadentry, symbol):
    # Determine text contents
    self.text = threadentry.DisplayName
    self.statictext = QtGui.QStaticText(self.text)

    # Determine rectangles and top-left positions
    stsize = self.statictext.size()
    self.stwidth = stsize.width()
    self.stheight = stsize.height()

    tr_start_x = CrossStitchKeyEntry.EDGE_MARGIN
    tr_start_y = CrossStitchKeyEntry.EDGE_MARGIN
    tr_rect = QtCore.QRectF(tr_start_x, tr_start_y, CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX, CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX)
    st_start_x = tr_start_x + CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX + CrossStitchKeyEntry.MID_MARGIN
    vert_extents = CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX + 2 * CrossStitchKeyEntry.EDGE_MARGIN 
    st_start_y = (vert_extents - self.stheight) / 2.0
    self.st_topleft = QtCore.QPoint(st_start_x, st_start_y)

    # Create TextRect
    self.renderTextRect = TextRect(tr_rect, symbol, threadentry, self.bw, self.font)

    # Save pen, brush for the static text
    self.pen = QtGui.QPen(QtCore.Qt.black)

  def minimumSizeHint(self):
    vert_extents = CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX + 2 * CrossStitchKeyEntry.EDGE_MARGIN 
    if self.text is not None:
      horiz_extents = CrossStitchKeyEntry.EDGE_MARGIN * 2 + CrossStitchKeyEntry.MID_MARGIN
      horiz_extents += self.stwidth
      horiz_extents += CrossStitchKeyEntry.SQUARE_SIDE_LEN_PX
      vert_extents = max(vert_extents, self.stheight)#probably won't be text taller than square
    else:
      horiz_extents = 48
    return QtCore.QSize(horiz_extents, vert_extents)

  def paintEvent(self, event):
    super().paintEvent(event)
    painter = QtGui.QPainter(self)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    if self.text is not None:
      painter.setPen(self.pen)
      painter.drawStaticText(self.st_topleft, self.statictext)
      self.renderTextRect.paint(painter)

class CrossStitchKeyNoScroll(QtWidgets.QWidget):
  csKeyFont = QtGui.QFont("sans-serif", pointSize=12)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.keyCreator = None
    self.gcols = 4

    self.glayout = QtWidgets.QGridLayout()
    self.setLayout(self.glayout)

    print("Size hint for noscroll: %s" % self.sizeHint())

  def minimumSizeHint(self):
    if self.keyCreator is not None:
      #TODO: actually find out the "size" of the widget
      return QtCore.QSize(200, 200)
    else:
      return QtCore.QSize(200, 200)

  def consumeImage(self, img_thread_array, bw=False):
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

     
    for i, t in enumerate(threads_sorted):
      entry_widget = CrossStitchKeyEntry(bw=False, font=CrossStitchKeyNoScroll.csKeyFont)
      entry_widget.setEntry(t, self.keyCreator[t])
      col = i % self.gcols
      row = i / self.gcols
      self.glayout.addWidget(entry_widget, col, row)
    self.updateGeometry()
    self.repaint()


  def paintEvent(self, event):
    super().paintEvent(event)
    print("Size hint for noscroll: %s\n\tevent rect %s event region %s" % (self.sizeHint(), event.rect(), event.region()))

