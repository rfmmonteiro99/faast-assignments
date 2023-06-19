"""Tests for the cleaning code"""
import pandas as pd

from life_expectancy.cleaning import CleanTSV, CleanJSON
from life_expectancy.region import Region


def test_clean_data_tsv(fixture_raw_data, fixture_expected_result):
    """Run the `clean_data` function and compare the output to the expected output for tsv files"""
    clean_class = CleanTSV()
    pt_life_expectancy_data = clean_class.clean_data(
        eu_life_expectancy=fixture_raw_data,
        region=Region.PT.value
    ).reset_index(drop=True)

    pd.testing.assert_frame_equal(pt_life_expectancy_data, fixture_expected_result)

def test_clean_data_json(fixture_json, fixture_expected_result_json):
    """Run the `clean_data` function and compare the output to the expected output for json files"""
    clean_class = CleanJSON()
    pt_life_expectancy_data = clean_class.clean_data(
        eu_life_expectancy=fixture_json, # Acho que tenho de mudar esta fixture?
        region=Region.PT.value
    ).reset_index(drop=True)

    pd.testing.assert_frame_equal(pt_life_expectancy_data, fixture_expected_result_json)
