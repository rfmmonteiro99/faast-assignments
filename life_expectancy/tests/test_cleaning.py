"""Tests for the cleaning module"""
from unittest.mock import patch, Mock
import pandas as pd

from life_expectancy.cleaning import load_data, clean_data, save_data, main
from . import OUTPUT_DIR


@patch('life_expectancy.cleaning.pd.read_csv')
def test_load_data(read_table_mock: Mock, fixture_raw_data):
    """Run the `load_data` function"""
    read_table_mock.return_value = fixture_raw_data
    file_name = 'eu_life_expectancy_raw.tsv'
    results = load_data(OUTPUT_DIR / file_name)
    read_table_mock.assert_called_once()

    pd.testing.assert_frame_equal(results, fixture_raw_data)

def test_clean_data(fixture_raw_data, fixture_expect):
    """Run the `clean_data` function and compare the output to the expected output"""
    pt_life_expectancy_data = clean_data(
        eu_life_expectancy=fixture_raw_data,
        region='PT'
    ).reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_data, fixture_expect
    )

def test_save_data(fixture_expect, capfd):
    """Run the `save_data` function"""
    
    with patch.object(fixture_expect, 'to_csv') as to_csv_mock:
        to_csv_mock.side_effect = print('Data saved', end='')
        file_name = 'pt_life_expectancy.csv'
        save_data(
            fixture_expect,
            OUTPUT_DIR / file_name
        )
        to_csv_mock.assert_called_once()

        out, _ = capfd.readouterr()
        assert out == 'Data saved'

@patch("life_expectancy.cleaning.load_data")
def test_main(load_mock: Mock, fixture_raw_data, fixture_expect):
    """Run the `main` function and compare the output to the expected output"""
    load_mock.return_value = fixture_raw_data
    pt_life_expectancy_data = main('PT').reset_index(drop=True)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_data, fixture_expect
    )
