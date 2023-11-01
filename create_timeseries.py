"""Module to create a timeseries based on linear response function csv files
"""

import os
from glob import glob
import pandas as pd
from lrf_calc import lrf_functions as lrf


CSV_PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/csv/"
PLOT_PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/plots/"


def find_name(csv):
    """Extract region name for plot title
    Args:
        csv (str): name of the csv file
        experiment (int): integer by which basal melt was increased by
    Returns name of the Antarctic region
    """
    name = os.path.splitext(os.path.basename(csv))[0]
    print(name)
    return name


def main(files, outpath):
    """Function which opens the csv files and plots a the LRF timeseries.
    Args:
        files (list): files for which a timeseries needs to be plotted
        outpath (str): path to where the plots should be stored
    Returns plots of LRF timeseries in .png format.
    """
    for file in files:
        name = find_name(file)
        lrf_df = pd.read_csv(file)
        lrf.lrf_ts(lrf_df, name, outpath)


if __name__ == "__main__":
    plot_files = glob(os.path.join(CSV_PATH, "total_*"))

    main(plot_files, PLOT_PATH)
