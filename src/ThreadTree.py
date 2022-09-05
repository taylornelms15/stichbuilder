#!/usr/bin/env python3

import pandas as pd
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

    def __init__(self, db_path):
        """
        TODO: allow for soft-overloading where we don't necessarily need a db path?
        Eventually will want to be able to cull the KD tree for "low-thread-SKU" lookups
        """
        self.df = pd.read_parquet(db_path) 
        self.entrylist = []
        for i, row in self.df.iterrows():
            entry = ThreadEntry(row["DisplayName"], row["DisplayNumStr"], row["dmc_num"], 
                                row["rgb_r"], row["rgb_g"], row["rgb_b"], 
                                row["hsv_h"], row["hsv_s"], row["hsv_v"], 
                                row["luv_l"], row["luv_u"], row["luv_v"], 
                                row["lab_l"], row["lab_a"], row["lab_b"]) 
            self.entrylist.append(entry)
        kdtree_data = np.array([x.getLUV() for x in self.entrylist]) 
        self.kdtree = KDTree(kdtree_data)
    
    def getClosestEntry(self, luv_tuple):
        """
        Queries the internal kdtree for the closest thread to the given LUV tuple
        Returns both the distance and the ThreadEntry that's closest
        """
        dist, idx = self.kdtree.query(luv_tuple)
        print("Query for data %s resulted in %s" % (luv_tuple, self.entrylist[idx]))
        return (dist, self.entrylist[idx])

def main():
    """
    Meant for dev, not meant for production
    """
    infile = "../data/dmc_readable.parquet"
    mytree = ThreadTree(infile)
    testColor = np.array([64, 80, 80])
    print("TestColor dist %s away from thread %s" % mytree.getClosestEntry(testColor))

if __name__ == "__main__":
    main()
