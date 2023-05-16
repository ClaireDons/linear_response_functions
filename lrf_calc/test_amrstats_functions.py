""" Tests for functions in the amrstats_functions module"""

import pytest
import pandas as pd


@pytest.fixture
def test_df():
    """Create test dataframe"""
    test_df = pd.DataFrame(
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
    return test_df


def test_run_statstool():
    """Test that subprocess calls driver and greps time, 
    and stores output correctly
    """
    from lrf_calc.amrstats_functions import run_statstool

    test_driver = "./mock_driver.sh"
    output = run_statstool(test_driver, "file")
    test_output = str(output)
    expected_output = "time = 1 iceVolumeAll = 2  iceVolumeAbove = 3  groundedArea = 4  floatingArea = 5  totalArea = 6  groundedPlusOpenLandArea = 7  iceMassAll = 8  iceMassAbove = 9  sector = 10\n"
    assert test_output == expected_output


def test_create_series(test_df):
    """Test pandas Series creation based on string output"""
    from lrf_calc.amrstats_functions import create_series

    test_output = "time = 1 iceVolumeAll = 2  iceVolumeAbove = 3  groundedArea = 4  floatingArea = 5  totalArea = 6  groundedPlusOpenLandArea = 7  iceMassAll = 8  iceMassAbove = 9  sector = 10\n"
    data = [1, 2, 3, 4, 5, 6, 7]
    expected = pd.Series(data, index=test_df.columns)

    test_series = create_series(test_output, test_df)
    pd.testing.assert_series_equal(test_series, expected, check_dtype=False)


def test_stats_retrieve(test_df):
    """Test that calling driver to series creation works"""
    from lrf_calc.amrstats_functions import stats_retrieve

    test_driver = "./mock_driver.sh"
    data = [1, 2, 3, 4, 5, 6, 7]
    expected = pd.Series(data, index=test_df.columns)

    test = stats_retrieve(test_driver, "file", test_df)
    pd.testing.assert_series_equal(test, expected, check_dtype=False)


def test_amrplot_df(test_df):
    from lrf_calc.amrstats_functions import amrplot_df

    test_driver = "./mock_driver.sh"
    test_files = ["file1, file2"]
    test = amrplot_df(test_driver, test_files)

    data = [[1, 2, 3, 4, 5, 6, 7]]
    expected = pd.DataFrame(data, columns=test_df.columns)

    pd.testing.assert_frame_equal(test, expected, check_dtype=False)