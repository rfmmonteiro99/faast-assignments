"""Tests for the region enum"""
import numpy as np

from life_expectancy.region import Region


def test_regions_list(fixture_expected_countries: list):
    """Run the `list_all_countries` function"""
    region_list = Region.list_all_countries()

    np.testing.assert_array_equal(region_list, fixture_expected_countries)
