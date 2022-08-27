#!/usr/bin/env python3

from scipy.spatial import distance

import pdb

class ThreadEntry:
    def __init__(self, DisplayName, DisplayNumStr, dmc_num, red, grn, blu, hue, sat, val, l, u, v):
        self.DisplayName = DisplayName
        self.DisplayNumStr = DisplayNumStr
        self.dmc_num = dmc_num
        self.red = red
        self.grn = grn
        self.blu = blu
        self.hue = hue
        self.sat = sat
        self.val = val
        self.l   = l
        self.u   = u
        self.v   = v
    
    def calcColorDistance(self, rh):
        """
        Calculates the "distance" to the other color
        """
        ours = (self.l, self.u, self.v)
        theirs = (rh.l, rh.u, rh.v)
        return distance.euclidean(ours, theirs)

    def getRGB(self):
        return [self.red, self.grn, self.blu]
    def getRGBFloat(self):
        rgb = self.getRGB()
        return [rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0]

    def __str__(self):
        return "<Entry dmc=%s name=%s r=%s g=%s b=%s>" % (self.dmc_num, self.DisplayName, self.red, self.grn, self.blu)

def plotEntries3D(entries):
    import numpy as np
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt

    xvals = np.array([x.l for x in entries])
    yvals = np.array([x.u for x in entries])
    zvals = np.array([x.v for x in entries])
    cvals = np.array([x.getRGBFloat() for x in entries])
    names = [x.DisplayName for x in entries]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(xvals, yvals, zvals, c=cvals)
    for i, name in enumerate(names):
        ax.text(xvals[i], yvals[i], zvals[i], name, size=10, zorder=1)
        #ax.annotate(name, (xvals[i], yvals[i], zvals[i]))


    plt.show()

def main():
    """
    Meant for dev, not meant for production
    """
    import pandas as pd
    import argparse
    infile = "../data/dmc_readable.parquet"
    df = pd.read_parquet(infile)
    entries = []
    for index, row in df.iterrows():
        entry = ThreadEntry(row["DisplayName"], row["DisplayNumStr"], row["dmc_num"], 
                            row["red"], row["grn"], row["blu"], 
                            row["hue"], row["sat"], row["val"], 
                            row["l"], row["u"], row["v"])
        print(entry)
        entries.append(entry)
    plotEntries3D(entries)

if __name__ == "__main__":
    main()
