#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import os.path
import matplotlib.pyplot as plt

from ThreadTree import ThreadTree

CLUSTERING_ALGORITHM="KMEANS" # choices: "KMEANS", "GMM"

if CLUSTERING_ALGORITHM == "GMM":
    from sklearn.mixture import GaussianMixture
elif CLUSTERING_ALGORITHM == "KMEANS":
    from sklearn.cluster import KMeans


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
    parser.add_argument("-s", "--conversion-colorspace", type=str, required=False, default="LUV",
                        choices=["RGB", "HSV", "LUV", "LAB"],
                        help="Color space to use for thread matching and conversions; defaults to LUV space")
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
    return cv2.resize(img, [new_h, new_w], interpolation=cv2.INTER_AREA)

def construct_thread_array(img_luv, threadtree):
    """
    Takes in a BGR image of size (w, h), constructs an array of shape (w,h) representing which thread each goes to.
    Also provides a map of those thread colors.
    Basically, the end result is a 2d array of indexes into a second provided list of ThreadEntry objects
    """

    raise NotImplementedError
    return threadarray, threadkey

def getColorConversions(colorspace_name):
    """
    Gets the conversion to and from the colorspace, assuming a base space of BGR
    Return format is (conversion_to_space, conversion_from_space)
    """
    if colorspace_name == "RGB":
        return (cv2.COLOR_BGR2RGB, cv2.COLOR_RGB2BGR)
    if colorspace_name == "HSV":
        return (cv2.COLOR_BGR2HSV, cv2.COLOR_HSV2BGR)
    if colorspace_name == "LUV":
        return (cv2.COLOR_BGR2LUV, cv2.COLOR_LUV2BGR)
    if colorspace_name == "LAB":
        return (cv2.COLOR_BGR2LAB, cv2.COLOR_LAB2BGR)

def simplify_colors(img, max_colors, ttree, colorspace):
    """
    Function to squash the number of colors in the image.
    """
    # Some structural parameters
    w, h, _ = img.shape #TODO: fix this
    mc = max_colors
    if (mc == -1):
        mc = 12 #Test value for now
    conversion_forward, conversion_backward = getColorConversions(colorspace)

    # Converting to our relevant colorspace
    img_float = img.astype(np.float32) / 255.0 # go from 8-bit to float bgr image
    # Filter the image slightly, to fight some noise before we collapse the color space in a subsequent step
    img_float = cv2.bilateralFilter(img_float, 15, 0.3, 0.3)
    img_conv = cv2.cvtColor(img_float, conversion_forward)
    img_conv_unrolled = img_conv.reshape([w * h, 3])

    # Display post-filter image
    filter_debug_img = cv2.resize(img_float, [h * 2, w * 2], interpolation=cv2.INTER_NEAREST)
    cv2.imshow("Image after filtering", filter_debug_img)

    # Apply clustering algorithm to simplify color space
    if CLUSTERING_ALGORITHM == "GMM":
        gm = GaussianMixture(mc, n_init=3, max_iter=100)
        labels = gm.fit_predict(img_conv_unrolled)
        centers = gm.means_
    elif CLUSTERING_ALGORITHM == "KMEANS":
        #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
        #compactness, labels, centers = cv2.kmeans(img_conv_unrolled, mc, None, criteria, 100, cv2.KMEANS_PP_CENTERS)
        km = KMeans(mc, init="k-means++", n_init=5, max_iter=2000, tol=1.0e-5)
        labels = km.fit_predict(img_conv_unrolled)
        centers = km.cluster_centers_
        distances = km.transform(img_conv_unrolled)
        dists = distances.min(axis=1)
        dists = dists.reshape([w, h])
        distmax = np.max(dists)

    # Construct image from these centers
    labels = labels.reshape([w, h])
    retval_color = np.zeros([w, h, 3], dtype=np.float32)
    retval_tcolor = np.zeros([w, h, 3], dtype=np.uint8)
    retval_threadentry = np.zeros([w, h, 3], dtype=object)
    used_entries = []
    for i, center in enumerate(centers):
        print("Processing center %s, with %s matching pixels" % (center, np.count_nonzero(labels == i)))
        #color = np.rint(center).astype(np.uint8)
        color = center
        _, entry = ttree.getClosestEntry(color)
        tcolor = np.array(entry.getBGR())
        retval_color[i == labels] = color
        retval_tcolor[i == labels] = tcolor
        retval_threadentry[i == labels] = entry
        if entry not in used_entries:
            used_entries.append(entry)

    # Print thread color diagnostics
    for entry in used_entries:
        print("%s - %s" % (entry.DisplayNumStr, entry.DisplayName))
    print("Total thread colors: %s" % len(used_entries))

    # Create a "Distances" image
    #if CLUSTERING_ALGORITHM == "KMEANS":
    #    distimg = np.array((dists * 255.0 / distmax), dtype=np.uint8)
    #    cv2.imshow("IMG dists", distimg)
        

    # Convert back to BGR
    retval_color = cv2.cvtColor(retval_color, conversion_backward)

    return (retval_color, retval_threadentry, retval_tcolor)

def main():
    args = parse_args()
    print(args)

    # Read input image
    img = cv2.imread(args.infile[0], cv2.IMREAD_UNCHANGED)

    # Read in ThreadTree
    ttree = ThreadTree(args.datapath, args.conversion_colorspace)

    if (not args.keep_transparency) and (img.shape[2] > 3):
        # Convert transparency to white (for processing)
        trans_mask = 0 == img[:,:,3]
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Scale to match width/height, if any
    if (args.width is not None) or (args.height is not None):
        img = scale_image(img, args.width, args.height)

    # Reduce to smaller number of thread colors
    img_color, img_threads, img_threadcolors = simplify_colors(img, args.max_colors, ttree, args.conversion_colorspace)
    
    h, w, _ = img.shape
    up_w = w * 2
    up_h = h * 2
    #img_upscale = np.zeros([up_h, up_w, 3])
    #img_color_upscale = np.zeros([up_h, up_w, 3])
    #img_threadcolor_upscale = np.zeros([up_h, up_w, 3])
    img_upscale = cv2.resize(img, dsize=[up_w, up_h], interpolation=cv2.INTER_NEAREST)
    img_color_upscale = cv2.resize(img_color, dsize=[up_w, up_h], interpolation=cv2.INTER_NEAREST)
    img_threadcolors_upscale = cv2.resize(img_threadcolors, dsize=[up_w, up_h], interpolation=cv2.INTER_NEAREST)

    cv2.imshow("Input image", img_upscale)
    cv2.imshow("Output, simplified", img_color_upscale)
    cv2.imshow("Output, threaded", img_threadcolors_upscale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

