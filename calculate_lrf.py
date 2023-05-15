"""Module to calculate the Linear Response Function for BISICLES
"""

import os
from glob import glob
import pandas as pd
from lrf_calc import amrstats_functions as amrstats
from lrf_calc import lrf_functions as lrf

PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/data"
MASK_PATH = r"/nobackup/users/donnelly/levermann-masks"
CSV_PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/csv/"
STATS_TOOL = r"/usr/people/donnelly/bisicles/BISICLES/code/filetools/stats2d.Linux.64.g++.gfortran.DEBUG.ex"

EXPERIMENT = 8


def find_name(mask, outpath, experiment):
    """Create the name for the csv file
    Args:
        mask (str): name of mask of antarctica region
        outpath (str): path to where csv will be output
        experiment (int): integer by which basal melt was increased by
    Returns name of csv file that will be created
    """
    key = os.path.splitext(os.path.basename(mask))[0][9:-5]
    name =  "LRF" + str(experiment) + key
    csv_name = outpath + name + ".csv"
    print(name)
    return name, csv_name


def main(plot_files, masks, experiment, outpath, driver):
    """Check if csv of linear response functions exists and if not calculates it
    Args:
        plot_files (list): list of BISICLES plot files
        masks (list): list of Antarctica mask files
        experiment (int): number by which basal melt was increased by
        outpath (str): path to where csv will be output
        driver (str): BISICLES stats tool path and name
    returns csv files containing statistics of plot files
    """
    for mask in masks:
        name, csv_name = find_name(mask, outpath, experiment)
        if os.path.isfile(name) is True:
            lrf_df = pd.read_csv(csv_name)
            if "SMA10" not in lrf_df.columns:
                lrf_df = lrf.lrf_calc(lrf_df, float(experiment))
                lrf_df.to_csv(csv_name, index=False)
                lrf.lrf_ts(lrf_df, name, outpath)
            else:
                print("csv already calculated")
        else:
            lrf_df = amrstats.amrplot_df(driver, plot_files, mask)
            lrf_df = lrf.lrf_calc(lrf_df, float(experiment))
            lrf_df.to_csv(csv_name, index=False)
            lrf.lrf_ts(lrf_df, name, outpath)


if __name__ == "__main__":
    files = glob(os.path.join(PATH, "plot.*"))
    mask_files = glob(os.path.join(MASK_PATH, "*.2d.hdf5"))

    main(files, mask_files, EXPERIMENT, CSV_PATH, STATS_TOOL)
