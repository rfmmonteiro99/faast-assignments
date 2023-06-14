"""
Script that loads a csv file, cleans its data, and saves it - using the strategy pattern
"""
import pathlib
import argparse
import zipfile
from abc import ABC, abstractmethod
import pandas as pd
from life_expectancy.region import Region


# Define paths
PARENT_PATH = pathlib.Path(__file__).parent
DATA_DIR = PARENT_PATH / 'data'
OUTPUT_FILE_NAME = 'pt_life_expectancy.csv'
OUTPUT_FILE_PATH = DATA_DIR / OUTPUT_FILE_NAME

class LoadData(ABC): # pylint: disable=too-few-public-methods
    """Abstract class for loading data"""

    @abstractmethod
    def load_data(
            self,
            file_path: str) -> pd.DataFrame:
        """Abstract method to load data"""

class LoadTSV(LoadData): # pylint: disable=too-few-public-methods
    """Class to load data with a tsv format"""
    def load_data(
            self,
            file_path: str) -> pd.DataFrame:
        """
        Loads file from its folder as a pandas DataFrame
        :param file_path: Path to the file

        :return: Pandas DataFrame with the loaded data
        """
        data = pd.read_csv(
            file_path,
            sep = '\t'
        )

        return data

class LoadJSON(LoadData): # pylint: disable=too-few-public-methods
    """Class to load json data inside a zipped folder"""
    def load_data(
            self,
            file_path: str) -> pd.DataFrame:
        """
        Loads file from its folder as a pandas DataFrame
        :param file_path: Path to the file

        :return: Pandas DataFrame with the loaded data
        """
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)

            data = pd.read_json(file_path)

        return data

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

def save_data(
        data_to_save: pd.DataFrame,
        file_path: str):
    """
    Save the clean DataFrame to a specified folder
    :param data_to_save: Pandas DataFrame with the data to be saved
    :param file_path: Path to the file
    """
    data_to_save.to_csv(
        file_path,
        index=False
    )

def main(
        input_file_name: str,
        region: Region) -> pd.DataFrame:
    """
    Steps: Load the data, clean it, and export it
    :param input_file_name: The file name that serves as input to the pipeline
    :param region: Region to select data from

    :return: Pandas DataFrame after performing the cleaning process
    """
    file_format = input_file_name.rsplit('.', maxsplit=1)[-1]

    if file_format == 'zip':
        load_class = LoadJSON()
        clean_class = CleanJSON()

    elif file_format == 'tsv':
        load_class = LoadTSV()
        clean_class = CleanTSV()

    input_file_path = DATA_DIR / input_file_name
    loaded_data = load_class.load_data(input_file_path)

    cleaned_data = clean_class.clean_data(loaded_data, region)

    save_data(cleaned_data, OUTPUT_FILE_PATH)

    return cleaned_data


if __name__ == "__main__": # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument('region')
    args = parser.parse_args()

    main('eurostat_life_expec.zip', Region(args.region).value) # 'eu_life_expectancy_raw.tsv'
