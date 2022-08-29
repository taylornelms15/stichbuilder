#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import os.path

from ThreadTree import ThreadTree

import pdb


def parse_args():
    parser = argparse.ArgumentParser("Utility to convert an image into a cross-stitch pattern")
    parser.add_argument("infile", nargs=1, type=str,
                        help="Path to input image")
    parser.add_argument("-t", "--keep-transparency", action="store_true",
                        help="Whether to keep transparency separate from white in the image (not currently supported")
    parser.add_argument("-w", "--width", type=int, choices=range(1, 2048), required=False, metavar="[1-2048]",
                        help="Max width of end image")
    parser.add_argument("-g", "--height", type=int, choices=range(1, 2048), required=False, metavar="[1-2048]",
                        help="Max height of end image")
    parser.add_argument("-d", "--datapath", type=str, default=os.path.join("..", "data", "dmc_readable.parquet"),
                        help="Path to database of possible threads")
    return parser.parse_args()

def scale_image(img, max_w, max_h):
    factor_x = 1.0
    factor_y = 1.0
    w, h, d = img.shape
    if (max_w is not None) and (max_w < w):
        factor_x = max_w * 1.0 / w
    if (max_h is not None) and (max_h < h):
        factor_y = max_h * 1.0 / h
    scale_factor = min(factor_x, factor_y)
    if (scale_factor == 1.0):
        # No scaling needed
        return img
    new_w = int(scale_factor * w)
    new_h = int(scale_factor * h)
    return cv2.resize(img, [new_w, new_h], interpolation=cv2.INTER_AREA)

def simplify_colors(img):
    """
    Function to squash the number of colors in the image.
    """
    raise NotImplementedError

def construct_thread_array(img, threadtree):
    """
    Takes in a BGR image of size (w, h), constructs an array of shape (w,h) representing which thread each goes to.
    Also provides a map of those thread colors.
    Basically, the end result is a 2d array of indexes into a second provided list of ThreadEntry objects
    """
    img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    raise NotImplementedError
    return threadarray, threadkey

def main():
    args = parse_args()
    print(args)

    # Read input image
    img = cv2.imread(args.infile[0], cv2.IMREAD_UNCHANGED)

    # Read in ThreadTree
    ttree = ThreadTree(args.datapath)

    if not args.keep_transparency:
        # Convert transparency to white (for processing)
        trans_mask = 0 == img[:,:,3]
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Scale to match width/height, if any
    if (args.width is not None) or (args.height is not None):
        img = scale_image(img, args.width, args.height)

    # Create thread array
    thread_array = construct_thread_array(img, ttree)

    pdb.set_trace()

    cv2.imshow("Input image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

