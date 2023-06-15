"""
Script that loads a csv file using the strategy pattern
"""
import pathlib
import zipfile
from abc import ABC, abstractmethod
import pandas as pd


# Define paths
PARENT_PATH = pathlib.Path(__file__).parent
DATA_DIR = PARENT_PATH / 'data'

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
