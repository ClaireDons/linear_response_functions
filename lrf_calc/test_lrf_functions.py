""" Tests for functions in the lrf_functions module"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def test_df():
    """Create test dataframe"""

    data = [0, -10, np.nan]
    test_df = pd.DataFrame(data, columns=["volumeAbove"])
    return test_df


def test_sle_calc(test_df):
    """Test if sea level equivalent function is working and can deal
    with NaNs and negative numbers
    """

    from lrf_calc.lrf_functions import sle_calc

    test = sle_calc(test_df.volumeAbove)
    exp_dat = [0.0, -2.5345e-11, np.nan]
    expected = pd.Series(exp_dat, name="volumeAbove")

    pd.testing.assert_series_equal(test, expected, check_dtype=False)


def test_lrf_calc():
    """Test that linear response function calculation is working"""
    from lrf_calc.lrf_functions import lrf_calc

    bm = 8
    data = [1000, 2000, 4000]
    df = pd.DataFrame(data, columns=["SLE"])
    exp_dat = [np.nan, -0.125, -0.25]
    expected = pd.Series(exp_dat, name="SLE")

    test = lrf_calc(df.SLE, bm)
    pd.testing.assert_series_equal(test, expected, check_dtype=False)


def test_add_lrf(test_df):
    """Test that the columns are correctly added to the statistics dataframe"""
    from lrf_calc.lrf_functions import add_lrf

    bm = 8
    df = add_lrf(test_df, bm)
    assert "SLE" in df.columns
    assert "LRF" in df.columns
    assert "rollmean" in df.columns
