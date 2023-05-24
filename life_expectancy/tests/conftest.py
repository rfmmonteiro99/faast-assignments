"""Pytest configuration file"""
import pandas as pd
import pytest

from life_expectancy.tests.fixtures.sample_data import raw_data, expected_result
from . import FIXTURES_DIR


@pytest.fixture
def fixture_raw_data() -> pd.DataFrame:
    """Load raw data"""
    return pd.DataFrame(raw_data())

@pytest.fixture
def fixture_expected_result() -> pd.DataFrame:
    """Load expected result"""
    return pd.DataFrame(expected_result())

@pytest.fixture
def fixture_json() -> pd.DataFrame:
    """Load eu_life_expectancy_fixture.json"""
    return pd.read_json(FIXTURES_DIR / 'eu_life_expectancy_fixture.json')

# @pytest.fixture
# def fixture_pandas_from_json() -> pd.DataFrame:
#     """Create a pd df from the data in the json file"""
#     return pd.read_json(FIXTURES_DIR / 'eu_life_expectancy_fixture.json')

@pytest.fixture
def fixture_expected_result_json() -> pd.DataFrame:
    """Load pt_life_expectancy_fixture.csv"""
    return pd.read_csv(FIXTURES_DIR / 'pt_life_expectancy_fixture.csv')

@pytest.fixture
def fixture_expected_countries() -> list:
    """Retrieve the list of expected countries"""
    countries_list = [
        'AT','BE','BG','CH','CY','CZ','DK','EE','EL','ES','FI','FR','HR','HU',
        'IS','IT','LI','LT','LU','LV','MT','NL','NO','PL','PT','RO','SE', 'SI',
        'SK','DE','DE_TOT','AL','IE','ME','MK','RS','AM','AZ','GE','TR','UA',
        'BY','UK','XK','FX','MD','SM','RU'
    ]

    return countries_list
