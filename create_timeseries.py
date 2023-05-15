"""Module to calculate the Linear Response Function for BISICLES
"""

import os
from glob import glob
import pandas as pd
from lrf_calc import lrf_functions as lrf


CSV_PATH = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/csv/"

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
    for file in files:
        name = find_name(file)
        lrf_df = pd.read_csv(file)
        lrf.lrf_ts(lrf_df, name, outpath)

if __name__ == "__main__":
    files = glob(os.path.join(CSV_PATH, "*.csv"))

    main(files, CSV_PATH)
