#!/usr/bin/env python3

from scipy.spatial import distance

DEFAULT_DISTANCE_COLORSPACE = "LUV"

class ColorSpace:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def getDistance(self, rh):
        ours = (self.x, self.y, self.z)
        theirs = (rh.x, rh.y, rh.z)
        return distance.euclidean(x, y, z)

    def getVals(self):
        return [self.x, self.y, self.z]

class RGB_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "RGB", x, y, z)
class HSV_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "HSV", x, y, z)
class LUV_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "LUV", x, y, z)
class LAB_CS(ColorSpace):
    def __init__(self, x, y, z):
        ColorSpace.__init__(self, "LAB", x, y, z)

class ThreadEntry:
    def __init__(self, DisplayName, DisplayNumStr, dmc_num, 
                rgb_r, rgb_g, rgb_b, 
                hsv_h, hsv_s, hsv_v,
                luv_l, luv_u, luv_v,
                lab_l, lab_a, lab_b):
        self.DisplayName = DisplayName
        self.DisplayNumStr = DisplayNumStr
        self.dmc_num = dmc_num
        self.rgb = RGB_CS(rgb_r, rgb_g, rgb_b)
        self.hsv = HSV_CS(hsv_h, hsv_s, hsv_v)
        self.luv = LUV_CS(luv_l, luv_u, luv_v)
        self.lab = LAB_CS(lab_l, lab_a, lab_b)
    
    def calcColorDistance(self, rh, colorspace=DEFAULT_DISTANCE_COLORSPACE):
        """
        Calculates the "distance" to the other color
        """
        # switch Colorspace
        if colorspace == "RGB":
            return self.rgb.distance(rh.rgb)
        elif colorspace == "HSV":
            return self.hsv.distance(rh.hsv)
        elif colorspace ==  "LUV":
            return self.luv.distance(rh.luv)
        elif colorspace == "LAB":
            return self.lab.distance(rh.lab)
        else:
            raise ValueError("Unsupported colorspace %s" % colorspace)

    def getRGBFloat(self):
        return self.rgb.getVals()
    def getRGB(self):
        rgbFloat = self.getRGBFloat()
        return [int(rgbFloat[0] * 255), int(rgbFloat[1] * 255), int(rgbFloat[2] * 255)]
    def getBGR(self):
        rgb = self.getRGB()
        return [rgb[2], rgb[1], rgb[0]]

    def getHSV(self):
        return self.hsv.getVals()
    def getLUV(self):
        return self.luv.getVals()
    def getLAB(self):
        return self.lab.getVals()

    def __str__(self):
        return "<Entry dmc=%s name=%s r=%s g=%s b=%s luv [%s %s %s]>" % (self.dmc_num, self.DisplayName, self.rgb.x, self.rgb.y, self.rgb.z, self.luv.x, self.luv.y, self.luv.z)

def plotEntries3D(entries):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting 

    xvals = np.array([x.luv.x for x in entries])
    yvals = np.array([x.luv.y for x in entries])
    zvals = np.array([x.luv.z for x in entries])
    cvals = np.array([x.getRGBFloat() for x in entries])
    names = [x.DisplayName for x in entries]

    fig = plt.figure()
    # Make 3d plot
    ax = fig.add_subplot(111, projection="3d")
    # Plot all our points (with their colors)
    ax.scatter(xvals, yvals, zvals, c=cvals)
    # Label each point 
    for i, name in enumerate(names):
        ax.text(xvals[i], yvals[i], zvals[i], name, size=4, zorder=1)
    # Change the background color
    ax.xaxis.pane.set_edgecolor("b")
    ax.yaxis.pane.set_edgecolor("b")
    ax.zaxis.pane.set_edgecolor("b")
    ax.set_xlabel("L Value")
    ax.set_ylabel("U Value")
    ax.set_zlabel("V Value")
    ax.patch.set_facecolor("gray")
    fig.patch.set_facecolor("gray")


    plt.show()

def main():
    """
    Meant for dev, not meant for production
    """
    import pandas as pd
    infile = "../data/dmc_readable.parquet"
    df = pd.read_parquet(infile)
    entries = []
    for index, row in df.iterrows():
        entry = ThreadEntry(row["DisplayName"], row["DisplayNumStr"], row["dmc_num"], 
                            row["rgb_r"], row["rgb_g"], row["rgb_b"], 
                            row["hsv_h"], row["hsv_s"], row["hsv_v"], 
                            row["luv_l"], row["luv_u"], row["luv_v"], 
                            row["lab_l"], row["lab_a"], row["lab_b"]) 
        entries.append(entry)
    plotEntries3D(entries)

if __name__ == "__main__":
    main()
