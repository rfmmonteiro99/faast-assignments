"""
Script that loads a csv file, cleans its data, and saves it 
"""
import argparse
import pandas as pd


def load_data(
        file_path: str) -> pd.DataFrame:
    """
    Loads file from its folder as a pandas DataFrame
    :param file_name: Name of the file to be loaded

    :return: Pandas DataFrame with the loaded data
    """
    data = pd.read_csv(
        file_path,
        sep='\t'
    )

    return data

def clean_data(
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

    # Get only the float numbers in the 'value' column and set the correspondent data type
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

def save_data(
        data_to_save: pd.DataFrame,
        file_name: str):
    """
    Save the clean DataFrame to a specified folder
    :param data_to_save: Pandas DataFrame with the data to be saved
    :param file_name: Name for the created file
    """
    data_to_save.to_csv(
        file_name,
        index=False
    )

def main(
        input_filename: str,
        region: str,
        output_filename: str):
    """
    Steps: Load the data, clean it, and export it
    :param input_filename: 
    :param region: 
    :param output_filename: 
    """
    loaded_data = load_data(
        file_path=input_filename
    )

    cleaned_data = clean_data(
        eu_life_expectancy=loaded_data,
        region=region
    )

    save_data(
        cleaned_data,
        output_filename
    )


if __name__ == "__main__": # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument('region')
    args = parser.parse_args()

    main(
        'life_expectancy/data/eu_life_expectancy_raw.tsv',
        args.region,
        'life_expectancy/data/pt_life_expectancy.csv'
    )
