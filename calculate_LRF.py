import os
from glob import glob
from amrstats_functions import *
from LRF_functions import *

path = r'/nobackup/users/donnelly/Antarctica/LRF8'
files = glob(os.path.join(path, "plot.*"))

masks_path = r'/nobackup/users/donnelly/levermann-masks'
mask_files = glob(os.path.join(masks_path, "*.2d.hdf5"))

filetoolsPath = '/usr/people/donnelly/bisicles/BISICLES/code/filetools/'
filetoolStats = 'stats2d.Linux.64.g++.gfortran.DEBUG.ex'
csv_path = r'/nobackup/users/donnelly/LRF_csv/'
experiment = "LRF8"
bm = 8.0

for mask in mask_files:
    key = os.path.splitext(os.path.basename(mask))[0][14:-3]
    name = csv_path + experiment + key + ".csv"
    print(name)
    if os.path.isfile(name) == True:
        df = pd.read_csv(name)
        if 'SMA10' not in df.columns:
            df = LRF_calc(df,bm)
            df.to_csv(name,index = False)
        elif 'SMA10' in df.columns:
            #df = df.drop(columns=['ice_mass','SLE','SLEm','difference','LRF','SMA10'])
            df = LRF_calc(df,bm)
            df.to_csv(name,index = False)
        else:
            print("Something odd happened")
    else:
        df = AMRplot_DF(filetoolsPath,filetoolStats,files,mask)
        df = LRF_calc(df,bm)
        df.to_csv(name,index = False)