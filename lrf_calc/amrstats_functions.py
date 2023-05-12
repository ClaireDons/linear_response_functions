"""Module for functions that run stats tool from BISICLES and 
creating a pandas dataframe
"""

import subprocess
import multiprocessing
import pandas as pd
from joblib import Parallel, delayed


def run_statstool(driver, file, hdf5=""):
    """Function to run the BISICLES stats module
    and returns the output as plain text.
    Args:
        driver (str): path to stats tool driver
        file (str): plot file to be processed
        hdf5 (int): which amr level should be processed
    Returns plain text output summarising statistics
    """

    command = (
        driver + " " + file + " 918 1028 9.81 " + hdf5 + " | grep time"
    )
    output = subprocess.check_output(command, shell=True)
    output = output.decode("utf-8")
    return output


def create_series(output, stats_df):
    """Function to take the BISICLES stats module
    output and turn it into a pandas data series.
    Args:
        output (str): Output from the stats command
        stats_df (dataframe): name of df to output to
    Returns pandas series containing statistics
    """

    stats = output.split()
    data = [
        float(stats[2]),
        float(stats[5]),
        float(stats[8]),
        float(stats[11]),
        float(stats[14]),
        float(stats[17]),
        float(stats[20]),
    ]
    a_series = pd.Series(data, index=stats_df.columns)
    return a_series


def stats_retrieve(driver, file, stats_df, hdf5=""):
    """Function which calls the BISICLES stats module
    and returns a pandas data series.
    Args:
        driver (str): path to stats tool driver
        file (str): plot file to be processed
        stats_df (str): a dataframe with the columns for the variables defined
        hdf5 (int): which amr level should be processed
    Returns pandas series containing statistics
    """

    output = run_statstool(driver, file, hdf5)
    a_series = create_series(output, stats_df)
    return a_series


def amrplot_df(driver, files, hdf5=""):
    """Function which runs the BISICLES stats module
    over multiple plot files in parallel.
    Args:
        driver (str): path to stats tool driver
        files (list): lis of plot files to be processed
        hdf5 (int): which amr level should be processed
    Returns pandas dataframe containing summary statistics
    for each plot file in files
    """

    num_jobs = multiprocessing.cpu_count()
    stats_df = pd.DataFrame(
        columns=[
            "time",
            "volumeAll",
            "volumeAbove",
            "groundedArea",
            "floatingArea",
            "totalArea",
            "groundedPlusLand",
        ]
    )
    series_list = Parallel(n_jobs=num_jobs)(
        delayed(stats_retrieve)(driver, i, stats_df, hdf5) for i in files
    )
    stats_df = stats_df.append(series_list, ignore_index=True)
    stats_df = stats_df.sort_values(by=["time"])
    stats_df = stats_df.reset_index(drop=True)
    return stats_df
