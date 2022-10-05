#!/usr/bin/env python3

#from pandas import read_parquet
"""
NOTE: removing pandas dependency to hopefully cut down on executable size/scope
"""
import duckdb
from scipy.spatial import KDTree
import numpy as np

from ThreadEntry import ThreadEntry

class ThreadTree:
    """
    The collection of our different thread options
    Stores the following:
        DataFrame containing all our thread data
        List of ThreadEntry objects, containing the same data
        KDTree containing the threads, spatially organized based on spatial relations
    """
    def getEntrylistDataForTree(self, colorspace):
        if colorspace == "RGB":
            return np.array([x.getRGBFloat() for x in self.entrylist])
        elif colorspace == "HSV":
            return np.array([x.getHSV() for x in self.entrylist])
        elif colorspace == "LUV":
            return np.array([x.getLUV() for x in self.entrylist])
        elif colorspace == "LAB":
            return np.array([x.getLAB() for x in self.entrylist])
        else:
            raise ValueError("Unsupported color space %s" % colorspace)

    def __init__(self, db_path, colorspace = "LUV"):
        """
        TODO: allow for soft-overloading where we don't necessarily need a db path?
        Eventually will want to be able to cull the KD tree for "low-thread-SKU" lookups
        """
        #self.df = read_parquet(db_path)
        cursor = duckdb.connect()
        cursor.execute("SELECT * FROM read_parquet('%s')" % db_path)
        self.entrylist = []
        #for i, row in self.df.iterrows():
        for i, row in enumerate(cursor.fetchall()):
            #entry = ThreadEntry(row["DisplayName"], row["DisplayNumStr"], row["dmc_num"],
            #                    row["rgb_r"], row["rgb_g"], row["rgb_b"],
            #                    row["hsv_h"], row["hsv_s"], row["hsv_v"],
            #                    row["luv_l"], row["luv_u"], row["luv_v"],
            #                    row["lab_l"], row["lab_a"], row["lab_b"])
            """
            COL_NAMES=["DisplayName", "DisplayNumStr", "dmc_num",
                        "red", "grn", "blu",
                        "rgb_r", "rgb_g", "rgb_b",
                        "hsv_h", "hsv_s", "hsv_v",
                        "luv_l", "luv_u", "luv_v",
                        "lab_l", "lab_a", "lab_b"]
            """
            entry = ThreadEntry(row[0], row[1], row[2],
                                row[6], row[7], row[8],
                                row[9], row[10], row[11],
                                row[12], row[13], row[14],
                                row[15], row[16], row[17])
            self.entrylist.append(entry)
        self.colorspace = colorspace
        kdtree_data = self.getEntrylistDataForTree(colorspace)
        self.kdtree = KDTree(kdtree_data)
    
    def getClosestEntry(self, cs_tuple):
        """
        Queries the internal kdtree for the closest thread to the given in-colorspace tuple
        Returns both the distance and the ThreadEntry that's closest
        """
        dist, idx = self.kdtree.query(cs_tuple)
        return (dist, self.entrylist[idx])
