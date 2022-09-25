#!/usr/bin/env python

import numpy as np

from UnicodeSymbols import UnicodeSymbols

class KeyCreatorHeadless:
  def __init__(self, threadEntryArray):
    self.symbolDict = UnicodeSymbols()
    unique_elements = np.unique(threadEntryArray)
    self.entryToUnicodeDict = self.symbolDict.constructMappingDict(unique_elements)

  def __getitem__(self, key):
    return self.entryToUnicodeDict[key]

  def keys(self):
    return self.entryToUnicodeDict.keys()
