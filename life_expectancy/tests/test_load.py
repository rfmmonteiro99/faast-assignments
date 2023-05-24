"""Tests for the load/save data code"""
from unittest.mock import patch, Mock
import pandas as pd

from life_expectancy.cleaning import LoadTSV, LoadJSON, save_data
from . import OUTPUT_DIR


@patch('life_expectancy.cleaning.pd.read_csv')
def test_load_data_tsv(read_table_mock: Mock, fixture_raw_data):
    """Run the `load_data` function for tsv files"""
    read_table_mock.return_value = fixture_raw_data
    load_class = LoadTSV()
    file_name = 'eu_life_expectancy_raw.tsv'
    results = load_class.load_data(OUTPUT_DIR / file_name)
    read_table_mock.assert_called_once()

    pd.testing.assert_frame_equal(results, fixture_raw_data)

@patch('life_expectancy.cleaning.pd.read_json')
def test_load_data_json(read_table_mock: Mock, fixture_json):
    """Run the `load_data` function for json files"""
    read_table_mock.return_value = fixture_json
    load_class = LoadJSON()
    file_name = 'eurostat_life_expec.zip'
    results = load_class.load_data(OUTPUT_DIR / file_name)
    read_table_mock.assert_called_once()

    pd.testing.assert_frame_equal(results, fixture_json)

def test_save_data(fixture_expected_result, capfd):
    """Run the `save_data` function"""

    with patch.object(fixture_expected_result, 'to_csv') as to_csv_mock:
        to_csv_mock.side_effect = print('Data saved', end='')
        file_name = 'pt_life_expectancy.csv'
        save_data(
            fixture_expected_result,
            OUTPUT_DIR / file_name
        )
        to_csv_mock.assert_called_once()

        out, _ = capfd.readouterr()
        assert out == 'Data saved'
