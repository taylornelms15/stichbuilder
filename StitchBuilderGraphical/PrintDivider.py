#!/usr/bin/env python3
from argparse import ArgumentParser, ArgumentTypeError

import numpy as np

class PrintDivider(object):
  MAX_ROWS_PER_PAGE = 20
  MAX_COLS_PER_PAGE = 20
  DEFAULT_OVERLAP   = 2

  def __init__(self, img_w, 
                     img_h, 
                     pagecols = PrintDivider.MAX_COLS_PER_PAGE, 
                     pagerows = PrintDivider.MAX_ROWS_PER_PAGE, 
                     overlap=PrintDivider.DEFAULT_OVERLAP):
    self.img_w = img_w
    self.img_h = img_h
    self.pagecols = pagecols
    self.pagerows = pagerows

    self.determineSplits()

  def determineSplits(self):
    """
    Goal is to determine how to split the cross stitch pattern presuming it won't fit onto one page
    Want to minimize "useless" pages in the printout
    We'll end up with a collection of boundaries for our output rectangles
    The "overlap" is used to duplicate boundary rows to make aligning patterns easier
    """
    # Trivial case
    if (self.img_w < self.pagecols) and (self.img_h < self.pagerows):
      self.rects
    pass

def valid_size_arg(s):
  msg = "{0!r}Not a valid dimension; expect size in the form of \"WxH\"".format(s)
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

if __name__ == "__main__":
  main()
