import subprocess
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing


def run_statstool(path, driver, file, hdf5=""):
    """Function to run the BISICLES stats module
    and returns the output as plain text.
    path: path to driver
    driver: driver name
    file: plot file to be processed"""

    command = (
        path + driver + " " + file + " 918 1028 9.81 " + hdf5 + " | grep time"
    )
    output = subprocess.check_output(command, shell=True)
    output = output.decode("utf-8")
    return output


def create_series(output, df):
    """Function to take the BISICLES stats module
    output and turn it into a pandas data series.
    statsOutput: Output from the stats command
    df: a dataframe with the columns for the variables defined"""

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
    a_series = pd.Series(data, index=df.columns)
    return a_series


def stats_retrieve(path, driver, file, df, hdf5=""):
    """Function which calls the BISICLES stats module
    and returns a pandas data series.
    path: path to driver
    driver: driver name
    file: plot file to be processed
    df: a dataframe with the columns for the variables defined"""

    output = run_statstool(path, driver, file, hdf5)
    a_series = create_series(output, df)
    return a_series


def amrplot_df(path, driver, files, hdf5=""):
    """Function which runs the BISICLES stats module
    over multiple plot files in parallel.
    path: path to driver
    driver: driver name
    files: plot files to be processed"""

    num_jobs = multiprocessing.cpu_count()
    df = pd.DataFrame(
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
        delayed(stats_retrieve)(path, driver, i, df, hdf5) for i in files
    )
    df = df.append(series_list, ignore_index=True)
    df = df.sort_values(by=["time"])
    df = df.reset_index(drop=True)
    return df
