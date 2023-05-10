# -*- coding: utf-8 -*-
import subprocess
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing

def statsRun(path, driver, file):
    '''Function to run the BISICLES stats module and returns the output as plain text.
    path: path to driver
    driver: driver name
    file: plot file to be processed'''
    
    statsCommand = path + driver + ' ' + file + ' 918 1028 9.81 | grep time'
    statsOutput = subprocess.check_output(statsCommand,shell=True)
    statsOutput = statsOutput.decode('utf-8')
    return statsOutput

def statsSeries(statsOutput, df):
    '''Function to take the BISICLES stats module output and turn it into a pandas data series.
    statsOutput: Output from the stats command
    df: a dataframe with the columns for the variables defined'''
    
    stats = statsOutput.split()
    data = [float(stats[2]),stats[5],stats[8],stats[11],stats[14],stats[17],stats[20]]
    a_series = pd.Series(data, index = df.columns)
    return a_series

def statsRetrieve(path, driver, file, df):
    '''Function which calls the BISICLES stats module and returns a pandas data series
    path: path to driver
    driver: driver name
    file: plot file to be processed
    df: a dataframe with the columns for the variables defined'''
    
    statsOutput = statsRun(filetoolsPath, filetoolStats,file)
    a_series= statsSeries(statsOutput, df)
    return a_series

def AMRplot_DF(path, driver, files):
    '''Function which runs the BISICLES stats module over multiple plot files in parallel
    path: path to driver
    driver: driver name
    files: plot files to be processed'''
    
    num_jobs = multiprocessing.cpu_count()
    df = pd.DataFrame(columns = 
                      ["time", "volumeAll", "volumeAbove", "groundedArea", 
                       "floatingArea", "totalArea", "groundedPlusLand"])  
    series_list = Parallel(n_jobs=num_jobs)(delayed(statsRetrieve)
                                            (filetoolsPath,filetoolStats,i,df)
                                            for i in files) 
    df = df.append(series_list, ignore_index=True)
    df = df.sort_values(by=['time'])
    df = df.reset_index(drop =True)
    return df

if __name__ == '__main__':
    import os
    from glob import glob
    path = r'/nobackup/users/donnelly/Antarctica/LRF4'
    files = glob(os.path.join(path, "plot.*"))
    filetoolsPath = '/usr/people/donnelly/bisicles/BISICLES/code/filetools/'
    filetoolStats = 'stats2d.Linux.64.g++.gfortran.DEBUG.ex'
    
    df = AMRplot_DF(filetoolsPath,filetoolStats,files)
    print(df)
    df.to_csv("stats_test.csv",index = False)