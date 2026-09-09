import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file into a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df

    except Exception as e:
        raise ValueError(f"Unable to load CSV file: {e}")