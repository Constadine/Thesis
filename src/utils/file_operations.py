# src/utils/file_operations.py

import pandas as pd
from typing import Optional
import logging

def save_dataframe(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        path (str): Path to the output CSV file.
        index (bool, optional): Whether to include the index. Defaults to False.
    """
    try:
        df.to_csv(path, index=index)
        logging.getLogger(__name__).info(f"DataFrame saved to '{path}'.")
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to save DataFrame to '{path}': {e}")
        raise
