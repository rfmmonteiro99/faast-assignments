"""Tests for the cleaning module"""
import pytest
from unittest.mock import patch, Mock
import pandas as pd

from life_expectancy.tests.fixtures.sample_data import raw_data, expected_result
from life_expectancy.cleaning import load_data, clean_data, save_data
from . import OUTPUT_DIR


@pytest.fixture
def fixture_raw_data():
    """Load raw data"""
    return pd.DataFrame(raw_data())

@pytest.fixture
def fixture_expect():
    """Load expected result"""
    return pd.DataFrame(expected_result())

@patch('life_expectancy.cleaning.pd.read_csv')
def test_load_data(read_table_mock: Mock, fixture_raw_data):
    """Run the `load_data` function"""
    read_table_mock.return_value = fixture_raw_data
    results = load_data(OUTPUT_DIR, 'eu_life_expectancy_raw.tsv')
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
        save_data(
            fixture_expect,
            OUTPUT_DIR,
            'pt_life_expectancy.csv'
        )
        to_csv_mock.assert_called_once()

        out, _ = capfd.readouterr()
        assert out == 'Data saved'
