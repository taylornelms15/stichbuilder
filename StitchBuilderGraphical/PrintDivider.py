#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentTypeError
import numpy as np

"""
Simple data container for a rectangle
"""
class Rect(object):
  def __init__(self, x, y, w, h):
    self.tlx  = x
    self.tly  = y
    self.w    = w
    self.h    = h

  def __repr__(self):
    return "<Rect x[%s, %s] y[%s, %s]>" % (self.x(), self.x() + self.w, self.y(), self.y() + self.h)
  def __str__(self):
    return self.__repr__()
  
  @property
  def shape(self):
    return (self.h, self.w)

  def width(self):
    return self.w
  def height(self):
    return self.h
  def x(self):
    return self.tlx
  def y(self):
    return self.tly
  def topLeft(self):
    return (self.tlx, self.tly)

def myCeil(n):
    return int(-1 * n // 1 * -1)

class PrintDivider(object):
  MAX_ROWS_PER_PAGE = 20 #NOTE: may go over this number with more overlap
  MAX_COLS_PER_PAGE = 20 #NOTE: may go over this number with more overlap
  DEFAULT_OVERLAP   = 3

  def __init__(self, img_w, 
                     img_h, 
                     pagecols = MAX_COLS_PER_PAGE, 
                     pagerows = MAX_ROWS_PER_PAGE, 
                     overlap  = DEFAULT_OVERLAP):
    self.img_w    = img_w
    self.img_h    = img_h
    self.pagecols = pagecols
    self.pagerows = pagerows
    self.overlap  = overlap

    self.rects = None # This will end up being a 2d numpy array containing Rect objects
    self.determineSplits()

  def getRectangles(self):
    return self.rects

  @staticmethod
  def getSplitsOneDimension(pagecols, img_w, overlap):
    # Determine some split characteristics
    pages_x_float = float(img_w) / pagecols
    pages_x = int(myCeil(pages_x_float))
    splits_x = pages_x - 1
    width_with_overlaps = img_w + overlap * splits_x
    cols_per_page_float = width_with_overlaps / float(pages_x)

    # Get the widths of each section
    widths = np.zeros([pages_x], dtype=int)
    for i in range(len(widths)):
      widths[i] = int((i + 1) * cols_per_page_float) - int(i * cols_per_page_float)

    # Get the indexes each section starts at
    tl_x = np.zeros([pages_x], dtype=int)
    for i in range(len(widths)):
      unoverlapped = sum(widths[:i])
      index_x = unoverlapped - (i * overlap) 
      tl_x[i] = index_x

    return (tl_x, widths)

  def determineSplits(self):
    """
    Goal is to determine how to split the cross stitch pattern presuming it won't fit onto one page
    Want to minimize "useless" pages in the printout
    We'll end up with a collection of boundaries for our output rectangles
    The "overlap" is used to duplicate boundary rows to make aligning patterns easier
    """
    # Trivial case (for testing output)
    if (self.img_w < self.pagecols) and (self.img_h < self.pagerows):
      rect = Rect(0, 0, self.img_w, self.img_h)
      self.rects = np.array([[rect]], dtype=object)

    tl_corners_x, widths = PrintDivider.getSplitsOneDimension(self.pagecols, self.img_w, self.overlap)
    tl_corners_y, heights = PrintDivider.getSplitsOneDimension(self.pagerows, self.img_h, self.overlap)

    num_pages_x = len(widths)
    num_pages_y = len(heights)
    retval = np.zeros([num_pages_y, num_pages_x], dtype=object)
    for i in range(num_pages_y):
      tl_corner_y = tl_corners_y[i]
      height      = heights[i]
      for j in range(num_pages_x):
        tl_corner_x = tl_corners_x[j]
        width       = widths[j]
        retval[i][j] = Rect(tl_corner_x, tl_corner_y, width, height)

    self.rects = retval


def valid_size_arg(s):
  msg = "\"{0!r}\" Not a valid dimension; expect size in the form of \"WxH\"".format(s)
  words = s.split("x")
  if len(words) != 2:
    raise ArgumentTypeError(msg)
  try:
    w = int(words[0])
    h = int(words[1])
  except ValueError:
    raise ArgumentTypeError(msg)
  return (w, h)

def parse_args():
  parser = ArgumentParser("Quick utility to figure out how to split up a large pattern across multiple pages")
  parser.add_argument("-s", "--size", type=valid_size_arg, required=True,
                      help="Input image size in the form of \"WxH\"")
  parser.add_argument("-r", "--rows", type=int, required=False,
                      default = PrintDivider.MAX_ROWS_PER_PAGE,
                      help="Number of rows max on a page")
  parser.add_argument("-c", "--cols", type=int, required=False,
                      default = PrintDivider.MAX_COLS_PER_PAGE,
                      help="Number of columns max on a page")
  parser.add_argument("-o", "--overlap", type=int, required=False,
                      default = PrintDivider.DEFAULT_OVERLAP,
                      help="How much overlap to supply for each page")

  args = parser.parse_args()
  args.width  = args.size[0]
  args.height = args.size[1]
  return args

def main():
  args = parse_args()

  divider = PrintDivider(args.width, args.height, args.cols, args.rows, args.overlap)
  print(divider.getRectangles())

if __name__ == "__main__":
  main()
