#!/usr/bin/env python3

import numpy as np
import cv2
from ThreadTree import ThreadTree
from scipy.spatial import KDTree

CLUSTERING_ALGORITHM="KMEANS" # choices: "KMEANS", "GMM"

class ImageConverter:

  def __init__(self):
    pass

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

