"""Functions for calculating Linear response function
based on statistics dataframe and plotting a timeseries.
"""
import matplotlib.pyplot as plt


def sle_calc(vol_above):
    """Function to calculate sea level equivalent based on stats output from BISICLES
    Args:
        vol_above (pd Series): Dataframe column of volume above flotation
    Returns pandas series containing sea level equivalent values
    """
    sea_area = 361.8
    rho_i = 0.917

    ice_mass = vol_above / (10**9) * rho_i
    sle = ice_mass * (1 / sea_area)
    print(sle)
    return sle


def lrf_calc(sle, bm):
    """Function to calculate a Linear Response Function from
    Levermann et al. (2020) based on stats output from BISICLES
    Args:
        sle (pd Series): dataframe containing summary statistics
        bm (float): basal melt anomaly
    Returns pandas series with LRF values
    """
    slem = -(sle) / 1000
    difference = slem.diff()
    lrf = difference / bm
    return lrf


def add_lrf(df, bm):
    """Function to calculate a Linear Response Function from
    Levermann et al. (2020) based on stats output from BISICLES
    Args:
        df (dataframe): dataframe containing summary statistics
        bm (float): basal melt anomaly
    Returns dataframe with additional columns for LRF and running mean
    """

    df["SLE"] = sle_calc(df["volumeAbove"])
    df["LRF"] = lrf_calc(df["SLE"], bm)
    df["rollmean"] = df.LRF.rolling(10).mean()

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
    plt.plot(df["time"], df["rollmean"])
    plt.xlabel("Time (years)")
    plt.title(key)
    plt.savefig(plot_path + key + ".png")
    plt.clf()
    return plot
