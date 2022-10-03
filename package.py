#!/usr/bin/env python3

import PyInstaller.__main__
import nuitka.__main__
#import argparse
import os.path
import StitchBuilderGraphical.StitchConstants

def main():
  #parser = argparse.ArgumentParser("Script to run PyInstaller")
  #parser.add_argument("--os", type=str, required=True,
  #                  choices=["mac", "windows", "linux"])
  #args = parser.parse_args()

  upx_path = os.path.join(os.path.expanduser("~"), "upx-3.96-win64")
  installer_arguments = [os.path.join("StitchBuilderGraphical", "stitchbuildergraphical.py"),
                        #"--onefile",
                        "--onedir",
                        "--nowindowed",
                        #"--windowed",
                        "--noconfirm",
                        "--add-data=%s;data" % os.path.join("data", "dmc_readable.parquet"),
                        "--add-data=%s;data" % os.path.join("data", "InputAnImage.png"),
                        '--name=%s' % StitchBuilderGraphical.StitchConstants.PROGRAM_NAME,
                        "--upx-dir=%s" % upx_path,
                        ]
  nuitka_arguments = ["--follow-imports",
                      "--include-data-files=%s=%s" % (os.path.join("data", "dmc_readable.parquet"), os.path.join("data", "dmc_readable.parquet")),
                      "--include-data-files=%s=%s" % (os.path.join("data", "InputAnImage.png"), os.path.join("data", "InputAnImage.png")),
                      os.path.join("StitchBuilderGraphical", "stitchbuildergraphical.py")]

  #PyInstaller.__main__.run(installer_arguments)
  nuitka.__main__.main(nuitka_arguments)

if __name__ == "__main__":
  main()
