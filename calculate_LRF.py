import os
import pandas as pd
from glob import glob
from lrf_calc import amrstats_functions as amrstats
from lrf_calc import lrf_functions as lrf

path = r'/nobackup/users/donnelly/projects/LinearResponseFunctions/data'
files = glob(os.path.join(path, "plot.*"))

masks_path = r'/nobackup/users/donnelly/levermann-masks'
mask_files = glob(os.path.join(masks_path, "*.2d.hdf5"))

filetoolsPath = '/usr/people/donnelly/bisicles/BISICLES/code/filetools/'
filetoolStats = 'stats2d.Linux.64.g++.gfortran.DEBUG.ex'
csv_path = r'/nobackup/users/donnelly/projects/LinearResponseFunctions/lrf_csv/'
experiment = "LRF8"
bm = 8.0

for mask in mask_files:
    key = os.path.splitext(os.path.basename(mask))[0][14:-3]
    name = csv_path + experiment + key + ".csv"
    print(name)
    if os.path.isfile(name) == True:
        df = pd.read_csv(name)
        if 'SMA10' not in df.columns:
            df = lrf.LRF_calc(df,bm)
            df.to_csv(name,index = False)
        elif 'SMA10' in df.columns:
            df = lrf.LRF_calc(df,bm)
            df.to_csv(name,index = False)
        else:
            print("Something odd happened")
    else:
        df = amrstats.AMRplot_DF(filetoolsPath,filetoolStats,files,mask)
        df = lrf.LRF_calc(df,bm)
        df.to_csv(name,index = False)