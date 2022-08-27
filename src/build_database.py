#!/usr/bin/env python3

import json
import argparse
import pandas as pd
import numpy as np

import pdb

COL_NAMES=["DisplayName", "DisplayNumStr", "dmc_num", "anchor_num", "red", "grn", "blu", "hue", "sat", "val"]
COL_TYPES=["str",         "str",           "str",     "str",        "int", "int", "int", "int", "int", "int"]
COL_DICT=dict(zip(COL_NAMES, [pd.Series(dtype=x) for x in COL_TYPES]))


def parse_args():
    parser = argparse.ArgumentParser(description="Builds a database object from the json input of DMC floss")
    parser.add_argument("input_file", type=argparse.FileType('r'), nargs="+",
                        help="One or more file paths for json objects to use")
    args = parser.parse_args()
    return args

def getColorValsFromHex(hexcode):
    return (0, 0, 0, 0, 0, 0)

def addDMCEntryToDataframe(df, line):
    dmc_num = line["number"]
    name = line["readableName"]
    hexcode = line["hex"]

    pdb.set_trace()

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



if __name__ == "__main__":
    main()
