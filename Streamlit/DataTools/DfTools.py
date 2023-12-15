import pandas as pd


class CustomDf(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super(CustomDf, self).__init__(*args, **kwargs)

    def custom_method(self, target_column, reference_column):
        print("This is a Custom method")


def calculate_difference_from_min(df, target_column, reference_column):
    """
    Calculate the difference between values in a target column and the minimum value of a reference column.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the columns.
    - target_column (str): The name of the target column.
    - reference_column (str): The name of the reference column.

    Returns:
    - pd.Series: A Series containing the calculated differences.
    """
    min_index = df[reference_column].idxmin()
    return df[target_column] - df[target_column][min_index]


if __name__ == "__main__":
    filepath = r"C:\Users\nikhilp\Desktop\2023-12-12T11-36_export.csv"
    df = pd.read_csv(filepath)
    df = CustomDf(df)
