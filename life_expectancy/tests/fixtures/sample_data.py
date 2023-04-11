"""
Sample data created for testing purposes
"""


def raw_data() -> dict:
    """
    Raw data to mock

    :return: Dictionary with the raw data
    """
    data = {
        'unit,sex,age,geo\time': ['YR,F,Y1,AL','YR,F,Y1,AL','YR,F,Y1,PT'],
        '2021': ['79.4','79.6','79.6'],
        '2022': ['79.4','79.6','79.6'],
        '2023': ['83.2 ','79.6','79.6']
    }
    return data

def expected_result() -> dict:
    """
    Expected result to mock

    :return: Dictionary with the expected result
    """
    result = {
        'unit': ['YR','YR','YR'],
        'sex': ['F','F','F'],
        'age': ['Y1','Y1','Y1'],
        'region': ['PT','PT','PT'],
        'year': [2021,2022,2023],
        'value': [79.6,79.6,79.6]
    }
    return result
