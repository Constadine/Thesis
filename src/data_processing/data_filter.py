# src/data_processing/data_filter.py

import pandas as pd
from typing import List
class DataFilter:
    """
    Responsible for filtering datasets based on specified criteria.
    """

    def __init__(self, logger):
        self.logger = logger

    def filter_april_to_june(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data for the months of April, May, and June.

        Args:
            df (pd.DataFrame): DataFrame with a 'Date' column.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        self.logger.info("Filtering data for April to June...")
        df['Month'] = pd.to_datetime(df['Date']).dt.month  
        filtered_df = df[df['Month'].isin([4, 5, 6])]  # type: pd.DataFrame
        self.logger.info(f"Data filtered: {filtered_df.shape[0]} records retained.")
        return filtered_df

    def fill_missing_values(
        self,
        df: pd.DataFrame,
        columns: List[str],
        fill_value: int = -1
    ) -> pd.DataFrame:
        """
        Fill missing values in specified columns with a given value.

        Args:
            df (pd.DataFrame): DataFrame to process.
            columns (List[str]): List of column names to fill.
            fill_value (int, optional): Value to fill missing entries. Defaults to -1.

        Returns:
            pd.DataFrame: DataFrame with filled values.
        """
        self.logger.info(
            f"Filling missing values in columns: {columns} with {fill_value}...")
        df[columns] = df[columns].fillna(fill_value)
        self.logger.info("Missing values filled.")
        return df
