"""
Script that loads a csv file, cleans its data, and saves it 
"""
import argparse
import pandas as pd


def clean_data(
    file_path: str,
    region: str = 'PT'
):
    """
    Load file as a pandas DataFrame and clean the data
    :param file_path: Name of the file to be loaded
    :param region: Region to select data from
    """
    # Load the eu_life_expectancy_raw.tsv data from the data folder
    eu_life_expectancy = pd.read_csv(file_path, sep='\t')

    # The first column has issues
    bad_columns = eu_life_expectancy.columns[0]

    # Fix issue where multiple column names needed to be split by ','
    updated_columns = bad_columns.split(',')

    # Update the dataframe to split the data columns and update the column names
    eu_life_expectancy[updated_columns] = eu_life_expectancy[bad_columns]\
        .str\
        .split(',', expand=True)

    # Drop dirty columns
    eu_life_expectancy.drop(columns=bad_columns, inplace=True)

    # Unpivot
    eu_life_expectancy_pivot = eu_life_expectancy.melt(
        updated_columns,
        var_name='year',
        value_name='value'
    )

    # Change column name
    eu_life_expectancy_pivot = eu_life_expectancy_pivot\
        .rename(columns={eu_life_expectancy_pivot.columns[3]: 'region'})

    # Change year's data type
    eu_life_expectancy_pivot = eu_life_expectancy_pivot.astype({'year': int})

    # Get only the float numbers in the 'value' column and set the correspondent data type
    eu_life_expectancy_pivot['value'] = eu_life_expectancy_pivot['value']\
        .str\
        .extract(r'([0-9]+\.?[0-9])')\
        .astype('float')

    # Drop missing values
    eu_life_expectancy_final = eu_life_expectancy_pivot[~eu_life_expectancy_pivot['value'].isna()]

    # Filter the data where region equal to PT (Portugal)
    eu_life_expectancy_final = eu_life_expectancy_final[
        eu_life_expectancy_final['region'] == region
    ]

    # Save the resulting dataframe to the data folder
    eu_life_expectancy_final.to_csv('life_expectancy/data/pt_life_expectancy.csv', index=False)

if __name__ == "__main__": # pragma: no cover

    # Parse arguments passed through the CL
    parser = argparse.ArgumentParser()
    parser.add_argument('region')
    args = parser.parse_args()

    clean_data(
        file_path='life_expectancy/data/eu_life_expectancy_raw.tsv',
        region=args.region
    )
