#!/usr/bin/env python3

import numpy as np
import cv2
from ThreadTree import ThreadTree
from scipy.spatial import KDTree
import os.path

from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans

class ImageConverter(object):
  """
  Idea of class functionality:
  Class has one primary function, "convert(img)"
  The state it stores are effectively the arguments for that function
  The View allows a user to adjust those arguments, and then re-run the conversion
  Once the conversion is complete, the program then stores the various output products that can be queried.
  """
  CLUSTERING_ALGORITHM_CHOICES = ["KMEANS", "GMM"]
  COLORSPACE_CHOICES = ["RGB", "HSV", "LUV", "LAB"]

  def __init__(self):
    self.clustering_algorithm = "KMEANS"
    self.colorspace           = "LUV"
    self.ttree_path           = os.path.join("..", "data", "dmc_readable.parquet") 
    self.ttree                = ThreadTree(self.ttree_path)
    self.max_colors           = 30
    self.dither               = True
    self.filter_strength      = 0.0

  def setClusteringAlgorithm(self, alg):
    if alg not in self.CLUSTERING_ALGORITHM_CHOICES:
      raise ValueError("Invalid algorithm choice %s; valid choices are %s" % (alg, self.CLUSTERING_ALGORITHM_CHOICES))
    self.clustering_algorithm = alg

  def setColorspace(self, cs):
    if cs not in self.COLORSPACE_CHOICES:
      raise ValueError("Invalid colorspace choice %s; valid choices are %s" % (cs, self.COLORSPACE_CHOICES))
    self.colorspace = cs
    self.loadThreadTree(self.ttree_path)

  def loadThreadTree(self, dbpath):
    if not os.path.isfile(dbpath):
      raise ValueError("No ThreadTree db file found at %s" % dbpath)
    self.ttree_path = dbpath
    self.ttree = ThreadTree(self.ttree_path, self.colorspace)

  @staticmethod
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

  @staticmethod
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

  @staticmethod
  def ditherImage(img, img_color, used_entries, colorspace):
    """
    Applies floyd-steinberg dithering to help get rid of artifacts
    Returns img_threadcolor (dithered) and img_threads (array of ThreadEntry objects)
    """
    h, w, _ = img.shape
    entrylist = list(used_entries.keys())
    tree = KDTree(ImageConverter.getEntrylistDataForTree(entrylist, colorspace))
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
        
  @staticmethod
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

  def convert(self, img):
    """
    Converts the input image according to the parameters loaded into the class
    Expects an 8-bit BGR input image, as if just loaded by cv2.imread(path_to_image)
    """
    # Naming stuff
    mc                = self.max_colors
    ttree             = self.ttree
    colorspace        = self.colorspace

    # Structural parameters
    h, w, _ = img.shape
    conversion_forward, conversion_backward = self.getColorConversions(colorspace)

    # Converting to our relevant colorspace
    img_float = img.astype(np.float32) / 255.0 # go from 8-bit to float bgr image
    # Filter the image slightly, to fight some noise before we collapse the color space in a subsequent step
    if filter_strength > 0.0:
        img_float = cv2.bilateralFilter(img_float, 15, self.filter_strength, self.filter_strength)
    img_conv = cv2.cvtColor(img_float, conversion_forward)  # move to conversion colorspace
    img_conv_unrolled = img_conv.reshape([w * h, 3])        # unroll for clustering algorithm

    # Store source image and post-filtering image
    self.img              = img
    self.img_post_filter  = (img_float * 255.0).astype(np.uint8)

    # Apply clustering algorithm to determine simplified color space
    if self.clustering_algorithm == "GMM":
        gm = GaussianMixture(mc, n_init=3, max_iter=100)
        labels = gm.fit_predict(img_conv_unrolled)
        centers = gm.means_
    elif self.clustering_algorithm == "KMEANS":
        km = KMeans(mc, init="k-means++", n_init=3, max_iter=3000, tol=1.0e-5)
        labels = km.fit_predict(img_conv_unrolled)
        centers = km.cluster_centers_

    # Construct images from these centers
    labels = labels.reshape([h, w])
    self.img_reduced_colorspace = np.zeros([h, w, 3], dtype=np.float32)
    used_entries = {}
    for i, center in enumerate(centers):
      num_pixels = np.count_nonzero(labels == 1) # May be useful for debugging?
      _, entry = ttree.getClosestEntry(center)
      # Store the reduced-colorspace image
      self.img_reduced_colorspace[i == labels] = center
      if entry not in used_entries:
        used_entries[entry] = num_pixels

    if self.dither:
      self.img_thread_color, self.img_thread_array = ditherImage(img_conv, self.img_reduced_colorspace, used_entries, colorspace)
    else:
      self.img_thread_array = np.zeros([h, w], dtype=object)
      self.img_thread_color = np.zeros([h, w, 3], dtype=np.float32)
      for i, center in enumerate(centers):
        _, entry = ttree.getClosestEntry(center)
        self.img_thread_array[i == labels] = entry
        self.img_thread_color[i == labels] = entry.getColor(colorspace)

    # At this point, have stored self.img, self.img_post_filter, self.img_reduced_colorspace, self.img_thread_color, and self.img_thread_color
    # We'll convert the ones that aren't BGR 8-bit back to that space for the sake of consistency
    self.img_reduced_colorspace = (cv2.cvtColor(self.img_reduced_colorspace, conversion_backward) * 255.0).astype(np.uint8)
    self.img_thread_color = (cv2.cvtColor(self.img_thread_color, conversion_backward) * 255.0).astype(np.uint8)





