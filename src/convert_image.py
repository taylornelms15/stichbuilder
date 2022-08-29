#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import os.path
import matplotlib.pyplot as plt

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
    parser.add_argument("-c", "--max-colors", type=int, required=False, default=-1,
                        help="Maximum number of colors in the final image")
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

def construct_thread_array(img_luv, threadtree):
    """
    Takes in a BGR image of size (w, h), constructs an array of shape (w,h) representing which thread each goes to.
    Also provides a map of those thread colors.
    Basically, the end result is a 2d array of indexes into a second provided list of ThreadEntry objects
    """

    raise NotImplementedError
    return threadarray, threadkey

def simplify_colors(img, max_colors, ttree):
    """
    Function to squash the number of colors in the image.
    """
    w, h, _ = img.shape
    mc = max_colors
    if (mc == -1):
        mc = 12 #Test value for now
    img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    img_luv_unrolled = img_luv.reshape([w * h, 3]).astype(np.float32)

    # Apply k-means clustering to find color centers
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    compactness, labels, centers = cv2.kmeans(img_luv_unrolled, mc, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

    # Construct image from these centers
    labels = labels.reshape([w, h])
    retval_color = np.zeros([w, h, 3], dtype=np.uint8)
    retval_tcolor = np.zeros([w, h, 3], dtype=np.uint8)
    retval_tcolor_luv = np.zeros([w, h, 3], dtype=np.uint8)
    retval_threadentry = np.zeros([w, h, 3], dtype=object)
    for i, center in enumerate(centers):
        print("Processing center %s, with %s matching pixels" % (center, np.count_nonzero(labels == i)))
        color = np.rint(center).astype(np.uint8)
        _, entry = ttree.getClosestEntry(color)
        tcolor = np.array(entry.getBGR())
        tcolor_luv = np.array(entry.getLUV())
        retval_color[i == labels] = color
        retval_tcolor[i == labels] = tcolor
        retval_tcolor_luv[i == labels] = tcolor_luv
        retval_threadentry[i == labels] = entry
    

    # Convert back to BGR
    retval_color = cv2.cvtColor(retval_color, cv2.COLOR_LUV2BGR)
    cv2.imshow("TColor_luv", retval_tcolor_luv)
    cv2.imshow("TColor", retval_tcolor)
    cv2.imshow("retval_color", retval_color)
    cv2.imshow("retval_color_luv", cv2.cvtColor(retval_color, cv2.COLOR_BGR2LUV))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (retval_color, retval_threadentry, retval_tcolor)

def main():
    args = parse_args()
    print(args)

    # Read input image
    img = cv2.imread(args.infile[0], cv2.IMREAD_UNCHANGED)

    # Read in ThreadTree
    ttree = ThreadTree(args.datapath)

    if (not args.keep_transparency) and (img.shape[2] > 3):
        # Convert transparency to white (for processing)
        trans_mask = 0 == img[:,:,3]
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Scale to match width/height, if any
    if (args.width is not None) or (args.height is not None):
        img = scale_image(img, args.width, args.height)

    # Reduce to smaller number of thread colors
    img_color, img_threads, img_threadcolors = simplify_colors(img, args.max_colors, ttree)

    cv2.imshow("Input image", img)
    cv2.imshow("Output, simplified", img_color)
    cv2.imshow("Output, threaded", img_threadcolors)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

