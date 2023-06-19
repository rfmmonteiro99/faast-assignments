"""
Script that loads, cleans, and saves data
"""
import pathlib
import argparse
import pandas as pd
from life_expectancy.region import Region
from life_expectancy.loading import LoadTSV, LoadJSON
from life_expectancy.cleaning import CleanTSV, CleanJSON


# Define paths
PARENT_PATH = pathlib.Path(__file__).parent
DATA_DIR = PARENT_PATH / 'data'
OUTPUT_FILE_NAME = 'pt_life_expectancy.csv'
OUTPUT_FILE_PATH = DATA_DIR / OUTPUT_FILE_NAME

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
