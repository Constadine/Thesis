# src/utils/file_operations.py

import pandas as pd
from typing import Any

def save_dataframe(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """
    Saves a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        path (str): Destination path for the CSV.
        index (bool, optional): Whether to include the DataFrame index. Defaults to False.
    """
    df.to_csv(path, index=index)
