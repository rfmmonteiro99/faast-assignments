"""
Script that cleans data using the strategy pattern
"""
from abc import ABC, abstractmethod
import pandas as pd
from life_expectancy.region import Region


class CleanData(ABC): # pylint: disable=too-few-public-methods
    """Abstract class to clean data"""

    @abstractmethod
    def clean_data(
            self,
            eu_life_expectancy: pd.DataFrame,
            region: Region) -> pd.DataFrame:
        """Abstract method to clean the data"""

class CleanTSV(CleanData): # pylint: disable=too-few-public-methods
    """Class to clean data coming from a tsv file"""

    def clean_data(
            self,
            eu_life_expectancy: pd.DataFrame,
            region: str = 'PT') -> pd.DataFrame:
        """
        Clean the previously imported DataFrame
        :param eu_life_expectancy: Pandas DataFrame with life expectancy data
        :param region: Region to select data from

        :return: Pandas DataFrame after performing the cleaning process
        """
        # The first column has issues
        bad_columns = eu_life_expectancy.columns[0]

        # Fix issue where multiple column names needed to be split by ','
        updated_columns = bad_columns.split(',')

        # Update the dataframe to split the data columns and update the column names
        eu_life_expectancy[updated_columns] = (
            eu_life_expectancy[bad_columns].str.split(',', expand=True)
        )

        # Drop dirty columns
        eu_life_expectancy.drop(columns=bad_columns, inplace=True)

        # Unpivot
        eu_life_expectancy_pivot = eu_life_expectancy.melt(
            updated_columns,
            var_name='year',
            value_name='value'
        )

        # Change column name
        eu_life_expectancy_pivot = (
            eu_life_expectancy_pivot.rename(columns={eu_life_expectancy_pivot.columns[3]: 'region'})
        )

        # Change year's data type
        eu_life_expectancy_pivot = eu_life_expectancy_pivot.astype({'year': int})

        # Get only the float numbers in the 'value' column and set the data type
        eu_life_expectancy_pivot['value'] = (
            eu_life_expectancy_pivot['value'].str.extract(r'([0-9]+\.?[0-9])').astype('float')
        )

        # Drop missing values
        eu_life_expectancy_final = eu_life_expectancy_pivot[
            ~eu_life_expectancy_pivot['value'].isna()
        ]

        # Filter the data for `region`
        eu_life_expectancy_final = eu_life_expectancy_final[
            eu_life_expectancy_final['region'] == region
        ]

        return eu_life_expectancy_final

class CleanJSON(CleanData): # pylint: disable=too-few-public-methods
    """Class to clean data coming from a json file"""

    def clean_data(
            self,
            eu_life_expectancy: pd.DataFrame,
            region: Region) -> pd.DataFrame:
        """
        Clean the previously imported DataFrame
        :param eu_life_expectancy: Pandas DataFrame with life expectancy data
        :param region: Region to select data from

        :return: Pandas DataFrame after performing the cleaning process
        """
        # Drop columns that are not in the list we want
        drop_cols = ['flag', 'flag_detail']
        eu_life_expectancy = eu_life_expectancy.drop(columns=drop_cols, axis=1)

        # Rename columns
        rename_dict = {'country': 'region', 'life_expectancy': 'value'}
        eu_life_expectancy = eu_life_expectancy.rename(columns=rename_dict)

        # Filter by region
        eu_life_expectancy_final = eu_life_expectancy[eu_life_expectancy['region'] == region]

        return eu_life_expectancy_final
