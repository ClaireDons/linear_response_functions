"""Functions for calculating Linear response function
based on statistics dataframe and plotting a timeseries.
"""
import matplotlib.pyplot as plt


def lrf_calc(df, bm):
    """Function to calculate a Linear Response Function from
    Levermann et al. (2020) based on stats output from BISICLES
    Args:
        df (dataframe): dataframe containing summary statistics
        bm (float): basal melt anomaly
    Returns dataframe with additional columns for LRF and running mean
    """

    sea_area = 361.8
    rho_i = 0.917

    df["ice_mass"] = (df.volumeAbove / (10**9)) * rho_i
    df["SLE"] = df.ice_mass * (1 / sea_area)
    df["SLEm"] = -(df.SLE) / 1000
    df["difference"] = df.SLEm.diff()
    df["LRF"] = df.difference / bm
    df["SMA10"] = df.LRF.rolling(10).mean()
    return df


def lrf_ts(df, key, plot_path):
    """Function to plot LRF from Levermann et al. (2020) based on
    dataframe created in LRF_calc.
    Args:
        df: df (dataframe): dataframe containing summary statistics
        key (str): name of region
        plot_path (str): path to where plots are saved
    Returns a plot with LRF and 10 year running mean"""

    plot = plt.plot(df["time"], df["LRF"])
    plt.plot(df["time"], df["SMA10"])
    plt.xlabel("Time (years)")
    plt.title(key)
    plt.show()
    plt.savefig(plot_path + key + ".jpg")
    plt.clf()
    return plot
