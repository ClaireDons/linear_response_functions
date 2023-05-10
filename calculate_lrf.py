"""Module to calculate the Linear Response Function for BISICLES
"""

import os
from glob import glob
import pandas as pd
from lrf_calc import amrstats_functions as amrstats
from lrf_calc import lrf_functions as lrf

PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/data"
MASK_PATH = r"/nobackup/users/donnelly/levermann-masks"
CSV_PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/lrf_csv/"

FILETOOLS_PATH = "/usr/people/donnelly/bisicles/BISICLES/code/filetools/"
STATS_TOOL = "stats2d.Linux.64.g++.gfortran.DEBUG.ex"

EXPERIMENT = "LRF8"
BASAL_MELT = 8.0


def main(plot_files, masks, outpath, filetools, driver):
    """Check if csv of linear response functions exists and if not calculates it
    """
    for mask in masks:
        key = os.path.splitext(os.path.basename(mask))[0][14:-3]
        name = outpath + EXPERIMENT + key + ".csv"
        print(name)
        if os.path.isfile(name) is True:
            lrf_df = pd.read_csv(name)
            if "SMA10" not in lrf_df.columns:
                lrf_df = lrf.lrf_calc(lrf_df, BASAL_MELT)
                lrf_df.to_csv(name, index=False)
            elif "SMA10" in lrf_df.columns:
                lrf_df = lrf.lrf_calc(lrf_df, BASAL_MELT)
                lrf_df.to_csv(name, index=False)
            else:
                print("Something odd happened")
        else:
            lrf_df = amrstats.amrplot_df(filetools, driver, plot_files, mask)
            lrf_df = lrf.lrf_calc(lrf_df, BASAL_MELT)
            lrf_df.to_csv(name, index=False)


if __name__ == "__main__":
    files = glob(os.path.join(PATH, "plot.*"))
    mask_files = glob(os.path.join(MASK_PATH, "*.2d.hdf5"))

    main(files, mask_files, CSV_PATH, FILETOOLS_PATH, STATS_TOOL)
