import subprocess
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing


def statsRun(path, driver, file, hdf5=""):
    '''Function to run the BISICLES stats module 
    and returns the output as plain text.
    path: path to driver
    driver: driver name
    file: plot file to be processed'''
    
    statsCommand = path + driver + ' ' + file + ' 918 1028 9.81 ' + hdf5 + ' | grep time'
    statsOutput = subprocess.check_output(statsCommand,shell=True)
    statsOutput = statsOutput.decode('utf-8')
    return statsOutput


def statsSeries(statsOutput, df):
    '''Function to take the BISICLES stats module 
    output and turn it into a pandas data series.
    statsOutput: Output from the stats command
    df: a dataframe with the columns for the variables defined'''
    
    stats = statsOutput.split()
    data = [float(stats[2]),float(stats[5]),float(stats[8]),float(stats[11]),
            float(stats[14]),float(stats[17]),float(stats[20])]
    a_series = pd.Series(data, index = df.columns)
    return a_series


def statsRetrieve(path, driver, file, df, hdf5=""):
    '''Function which calls the BISICLES stats module 
    and returns a pandas data series.
    path: path to driver
    driver: driver name
    file: plot file to be processed
    df: a dataframe with the columns for the variables defined'''
    
    statsOutput = statsRun(path,driver,file,hdf5)
    a_series= statsSeries(statsOutput, df)
    return a_series


def AMRplot_DF(path, driver, files,hdf5=""):
    '''Function which runs the BISICLES stats module 
    over multiple plot files in parallel.
    path: path to driver
    driver: driver name
    files: plot files to be processed'''
    
    num_jobs = multiprocessing.cpu_count()
    df = pd.DataFrame(columns = 
                      ["time", "volumeAll", "volumeAbove", "groundedArea", 
                       "floatingArea", "totalArea", "groundedPlusLand"])  
    series_list = Parallel(n_jobs=num_jobs)(delayed(statsRetrieve)
                                            (path,driver,i,df,hdf5)
                                            for i in files) 
    df = df.append(series_list, ignore_index=True)
    df = df.sort_values(by=['time'])
    df = df.reset_index(drop =True)
    return df