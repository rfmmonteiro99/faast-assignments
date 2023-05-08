"""Pytest configuration file"""
import pandas as pd
import pytest

from life_expectancy.tests.fixtures.sample_data import raw_data, expected_result


@pytest.fixture
def fixture_raw_data():
    """Load raw data"""
    return pd.DataFrame(raw_data())

@pytest.fixture
def fixture_expect():
    """Load expected result"""
    return pd.DataFrame(expected_result())
