"""Tests for the main function code"""
from unittest.mock import patch, Mock
import pandas as pd

from life_expectancy import main
from life_expectancy.region import Region


@patch("life_expectancy.loading.pd.read_csv")
def test_main_tsv(load_mock: Mock, fixture_raw_data, fixture_expected_result):
    """Run the `main` function and compare the output to the expected output for tsv files"""
    load_mock.return_value = fixture_raw_data
    pt_life_expectancy_data = (
        main('eu_life_expectancy_raw.tsv', Region.PT.value)
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(pt_life_expectancy_data, fixture_expected_result)

@patch("life_expectancy.loading.pd.read_json")
def test_main_json(load_mock: Mock, fixture_json, fixture_expected_result_json):
    """Run the `main` function and compare the output to the expected output for json files"""
    load_mock.return_value = fixture_json
    pt_life_expectancy_data = (
        main('eurostat_life_expec.zip', Region.PT.value)
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(pt_life_expectancy_data, fixture_expected_result_json)
