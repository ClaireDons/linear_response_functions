import os
import pandas as pd
from glob import glob
from lrf_calc import amrstats_functions as amrstats
from lrf_calc import lrf_functions as lrf

path = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/data"
masks_path = r"/nobackup/users/donnelly/levermann-masks"
csv_path = r"/nobackup/users/donnelly/projects/LinearResponseFunctions/lrf_csv/"

filetoolsPath = "/usr/people/donnelly/bisicles/BISICLES/code/filetools/"
filetoolStats = "stats2d.Linux.64.g++.gfortran.DEBUG.ex"

experiment = "LRF8"
basal_melt = 8.0


def main(plot_files, masks):
    for mask in masks:
        key = os.path.splitext(os.path.basename(mask))[0][14:-3]
        name = csv_path + experiment + key + ".csv"
        print(name)
        if os.path.isfile(name) == True:
            df = pd.read_csv(name)
            if "SMA10" not in df.columns:
                df = lrf.lrf_calc(df, basal_melt)
                df.to_csv(name, index=False)
            elif "SMA10" in df.columns:
                df = lrf.lrf_calc(df, basal_melt)
                df.to_csv(name, index=False)
            else:
                print("Something odd happened")
        else:
            df = amrstats.AMRplot_DF(filetoolsPath, filetoolStats, plot_files, mask)
            df = lrf.lrf_calc(df, basal_melt)
            df.to_csv(name, index=False)


if __name__ == "__main__":
    files = glob(os.path.join(path, "plot.*"))
    mask_files = glob(os.path.join(masks_path, "*.2d.hdf5"))

    main(files, mask_files)
