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
    return sle


def tot_lrf_calc(total_volume, basal_melt):
    """Function to calculate sea level equivalent based on stats output from BISICLES
    Args:
        vol_above (pd Series): Dataframe column of volume above flotation
    Returns pandas series containing sea level equivalent values
    """
    rho_i = 0.917

    ice_mass = -total_volume / (10**9) * rho_i
    diff_mass = ice_mass.diff()
    lrf = diff_mass / basal_melt
    return lrf



def lrf_calc(sle, basal_melt):
    """Function to calculate a Linear Response Function from
    Levermann et al. (2020) based on stats output from BISICLES
    Args:
        sle (pd Series): dataframe containing summary statistics
        basal_melt (float): basal melt anomaly
    Returns pandas series with LRF values
    """
    slem = -(sle) / 1000
    difference = slem.diff()
    lrf = difference / basal_melt
    return lrf


def add_lrf(lrf_df, basal_melt):
    """Function to calculate a Linear Response Function from
    Levermann et al. (2020) based on stats output from BISICLES
    Args:
        lrf_df (dataframe): dataframe containing summary statistics
        basal_melt (float): basal melt anomaly
    Returns dataframe with additional columns for LRF and running mean
    """

    lrf_df["SLE"] = sle_calc(lrf_df["volumeAbove"])
    sle = - lrf_df.SLE
    #totsle = tot_sle_calc(lrf_df["volumeAll"])
    lrf_df["diffsle"] = sle.diff(1)
    lrf_df["cumsle"] = lrf_df.diffsle.cumsum()
    lrf_df["LRF"] = lrf_calc(lrf_df["SLE"], basal_melt)
    lrf_df["rollmean"] = lrf_df.LRF.rolling(10).mean()
    lrf_df["totLRF"] = tot_lrf_calc(lrf_df["volumeAll"], basal_melt)
    lrf_df["tot_rollmean"] = lrf_df.totLRF.rolling(10).mean()

    return lrf_df


def lrf_ts(lrf_df, key, plot_path):
    """Function to plot LRF from Levermann et al. (2020) based on
    dataframe created in LRF_calc.
    Args:
        lrf_df (dataframe): dataframe containing summary statistics
        key (str): name of region
        plot_path (str): path to where plots are saved
    Returns a plot with LRF and 10 year running mean"""

    plot = plt.plot(lrf_df["time"], lrf_df["LRF"])
    plt.plot(lrf_df["time"], lrf_df["rollmean"])
    plt.xlabel("Time (years)")
    plt.ylabel("LRF")
    #plt.title(key)
    plt.savefig(plot_path + key + ".png")
    plt.clf()
    return plot
