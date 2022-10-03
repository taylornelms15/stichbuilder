#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import os.path

from ThreadTree import ThreadTree
from scipy.spatial import KDTree

UPSCALE_FACTOR = 3
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
    parser.add_argument("--dither", action="store_true", default=False,
                        help="Enable dithering on image output")
    parser.add_argument("--filter-strength", type=float, default=0.0,
                        help="Strength of bilateral filtering, or 0.0 for no filtering")
    return parser.parse_args()

def getEntrylistDataForTree(entrylist, colorspace):
    if colorspace == "RGB":
        return np.array([x.getRGBFloat() for x in entrylist])
    elif colorspace == "HSV":
        return np.array([x.getHSV() for x in entrylist])
    elif colorspace == "LUV":
        return np.array([x.getLUV() for x in entrylist])
    elif colorspace == "LAB":
        return np.array([x.getLAB() for x in entrylist])
    else:
        raise ValueError("Unsupported color space %s" % colorspace)

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
    return cv2.resize(img, (new_h, new_w), interpolation=cv2.INTER_AREA)

def ditherImage(img, img_color, used_entries, colorspace):
    """
    Applies floyd-steinberg dithering to help get rid of artifacts
    Returns img_threadcolor (dithered) and img_threads (array of ThreadEntry objects)
    """
    h, w, _ = img.shape
    entrylist = list(used_entries.keys())
    tree = KDTree(getEntrylistDataForTree(entrylist, colorspace))
    img_threadcolor = np.zeros(img.shape, dtype=np.float32)
    img_threads = np.zeros([h, w], dtype=object)
    # I know we shouldn't do for loops on images in python, but the algorithm I'm working from really wants me to
    for i, r in enumerate(img_color):
        for j, c in enumerate(r):
            quant_error = img[i][j] - img_color[i][j]
            if j < w - 1:
                img_color[i][j + 1] = img_color[i][j + 1] + quant_error * 7.0/16
            if i < h - 1 and j > 0:
                img_color[i + 1][j - 1] = img_color[i + 1][j - 1] + quant_error * 3.0/16
            if i < h - 1:
                img_color[i + 1][j] = img_color[i + 1][j] + quant_error * 5.0/16
            if i < h - 1 and j < w - 1:
                img_color[i + 1][j + 1] = img_color[i + 1][j + 1] + quant_error * 1.0/16
    for i, r in enumerate(img_color):
        for j, c in enumerate(r):
            dist, idx = tree.query(img_color[i][j])
            matching_entry = entrylist[idx]
            img_threads[i][j] = matching_entry
            img_threadcolor[i][j] = matching_entry.getColor(colorspace)
    return (img_threadcolor, img_threads) 
            

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

def simplify_colors(img, max_colors, ttree, colorspace, dither, filter_strength):
    """
    Function to squash the number of colors in the image.
    """
    # Some structural parameters
    w, h, _ = img.shape #TODO: fix this (it's reversed)
    mc = max_colors
    if (mc == -1):
        mc = 12 #Test value for now
    conversion_forward, conversion_backward = getColorConversions(colorspace)

    # Converting to our relevant colorspace
    img_float = img.astype(np.float32) / 255.0 # go from 8-bit to float bgr image
    # Filter the image slightly, to fight some noise before we collapse the color space in a subsequent step
    if filter_strength > 0.0:
        img_float = cv2.bilateralFilter(img_float, 15, filter_strength, filter_strength)
    img_conv = cv2.cvtColor(img_float, conversion_forward)
    img_conv_unrolled = img_conv.reshape([w * h, 3])

    # Display post-filter image
    if filter_strength > 0.0:
        filter_debug_img = cv2.resize(img_float, (h * UPSCALE_FACTOR, w * UPSCALE_FACTOR), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Image after filtering", filter_debug_img)

    # Apply clustering algorithm to simplify color space
    if CLUSTERING_ALGORITHM == "GMM":
        gm = GaussianMixture(mc, n_init=3, max_iter=100)
        labels = gm.fit_predict(img_conv_unrolled)
        centers = gm.means_
    elif CLUSTERING_ALGORITHM == "KMEANS":
        #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
        #compactness, labels, centers = cv2.kmeans(img_conv_unrolled, mc, None, criteria, 100, cv2.KMEANS_PP_CENTERS)
        km = KMeans(mc, init="k-means++", n_init=3, max_iter=3000, tol=1.0e-5)
        labels = km.fit_predict(img_conv_unrolled)
        centers = km.cluster_centers_
        distances = km.transform(img_conv_unrolled)
        dists = distances.min(axis=1)
        dists = dists.reshape([w, h])
        distmax = np.max(dists)

    # Construct image from these centers
    labels = labels.reshape([w, h])
    retval_color = np.zeros([w, h, 3], dtype=np.float32)
    retval_tcolor = np.zeros([w, h, 3], dtype=np.float32)
    retval_tcolor = np.zeros([w, h], dtype=object)
    used_entries = {}
    for i, center in enumerate(centers):
        num_pixels = np.count_nonzero(labels == i)
        print("Processing center %s, with %s matching pixels" % (center, num_pixels))
        color = center
        _, entry = ttree.getClosestEntry(color)
        retval_color[i == labels] = color
        if entry not in used_entries:
            used_entries[entry] = num_pixels
        if not dither:
            retval_threadentry[i == labels] = entry
            retval_tcolor[i == labels] = entry.getColor(colorspace)
    if dither:
        retval_tcolor, retval_threadentry = ditherImage(img_conv, retval_color,  used_entries, colorspace)

    # Print thread color diagnostics
    for entry, pixels in used_entries.items():
        print("%s - %s: %d" % (entry.DisplayNumStr, entry.DisplayName, pixels))
    print("Total thread colors: %s" % len(used_entries))

    # Convert back to BGR
    retval_color = cv2.cvtColor(retval_color, conversion_backward)
    retval_tcolor = cv2.cvtColor(retval_tcolor, conversion_backward)

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
    img_color, img_threads, img_threadcolors = simplify_colors(img, args.max_colors, ttree, 
                                                    args.conversion_colorspace, args.dither, args.filter_strength)
    
    h, w, _ = img.shape
    up_w = w * UPSCALE_FACTOR
    up_h = h * UPSCALE_FACTOR
    #img_upscale = np.zeros([up_h, up_w, 3])
    #img_color_upscale = np.zeros([up_h, up_w, 3])
    #img_threadcolor_upscale = np.zeros([up_h, up_w, 3])
    img_upscale = cv2.resize(img, dsize=(up_w, up_h), interpolation=cv2.INTER_NEAREST)
    img_color_upscale = cv2.resize(img_color, dsize=(up_w, up_h), interpolation=cv2.INTER_NEAREST)
    img_threadcolors_upscale = cv2.resize(img_threadcolors, dsize=(up_w, up_h), interpolation=cv2.INTER_NEAREST)

    cv2.imshow("Input image", img_upscale)
    cv2.imshow("Output, simplified", img_color_upscale)
    cv2.imshow("Output, threaded", img_threadcolors_upscale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

