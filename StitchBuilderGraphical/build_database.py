#!/usr/bin/env python3

import json
import argparse
import pandas as pd
import numpy as np
import cv2
import os.path

COL_NAMES=["DisplayName", "DisplayNumStr", "dmc_num", 
            "red", "grn", "blu", 
            "rgb_r", "rgb_g", "rgb_b",
            "hsv_h", "hsv_s", "hsv_v",
            "luv_l", "luv_u", "luv_v",
            "lab_l", "lab_a", "lab_b"]
COL_TYPES=["str", "str", "str",
            "int", "int", "int",
            "float64", "float64", "float64",
            "float64", "float64", "float64",
            "float64", "float64", "float64",
            "float64", "float64", "float64"]
COL_DICT=dict(zip(COL_NAMES, [pd.Series(dtype=x) for x in COL_TYPES]))


def parse_args():
    parser = argparse.ArgumentParser(description="Builds a database object from the json input of DMC floss")
    parser.add_argument("input_file", type=argparse.FileType('r'), nargs="+",
                        help="One or more file paths for json objects to use")
    args = parser.parse_args()
    return args

def getColorValsFromHex(hexcode):
    """
    Returns (r, g, b, r_f, g_f, b_f, h, s, v, l, u, v, l, a, b)
    """
    rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
    # Create a numpy array for a single-pixel image
    bgrPix = np.zeros([1, 1, 3], dtype="uint8")
    bgrPix[:,:,0] = rgb[2]
    bgrPix[:,:,1] = rgb[1]
    bgrPix[:,:,2] = rgb[0]
    # Create the same, but in floating point
    bgrF = bgrPix.astype(np.float32) / 255.0
    hsvF = np.zeros([1, 1, 3], dtype=np.float32)
    luvF = np.zeros([1, 1, 3], dtype=np.float32)
    labF = np.zeros([1, 1, 3], dtype=np.float32)
    # Use OpenCV to convert color spaces
    hsvF = cv2.cvtColor(bgrF, cv2.COLOR_BGR2HSV)
    luvF = cv2.cvtColor(bgrF, cv2.COLOR_BGR2LUV)
    labF = cv2.cvtColor(bgrF, cv2.COLOR_BGR2LAB)
    
    return (bgrPix[0,0,2], bgrPix[0,0,1], bgrPix[0,0,0],
            bgrF[0,0,2], bgrF[0,0,1], bgrF[0,0,0],
            hsvF[0,0,0], hsvF[0,0,1], hsvF[0,0,2],
            luvF[0,0,0], luvF[0,0,1], luvF[0,0,2],
            labF[0,0,0], labF[0,0,1], labF[0,0,2])

def addDMCEntryToDataframe(df, line):
    dmc_num = line["number"]
    name = line["readableName"]
    hexcode = line["hex"]
    cval = getColorValsFromHex(hexcode)
    rowvals = [name, "dmc-%s" % dmc_num, dmc_num, 
               cval[0], cval[1], cval[2], 
               cval[3], cval[4], cval[5], 
               cval[6], cval[7], cval[8],
               cval[9], cval[10], cval[11],
               cval[12], cval[13], cval[14]]
    df.loc[df.shape[0]] = rowvals

def addJsonToDataframe(df, infile):
    """
    Currently only supporting the one DMC json file I have
    """
    try:
        jobj = json.loads(infile.read())
    except:
        print("Error parsing json file %s; skipping", infile)
        return
    for k, v in jobj.items():
        if k not in ["noFlossMatch", "blanc"]:
            addDMCEntryToDataframe(df, v)
    

def main():
    args = parse_args()
    input_file_list = args.input_file
    df = pd.DataFrame(COL_DICT)
    for infile in input_file_list:
        addJsonToDataframe(df, infile)
    print(df)
    # By default, create output filename by changing extension of final input filename
    infile_name = infile.name
    outfile_name = os.path.splitext(infile_name)[0] + ".parquet"
    df.to_parquet(outfile_name)


if __name__ == "__main__":
    main()
