# src/data_processing/data_merger.py

import pandas as pd
from typing import List
class DataMerger:
    """
    Responsible for merging bird and climate datasets.
    """

    def __init__(self, logger):
        self.logger = logger

    def merge_datasets(
        self,
        bird_df: pd.DataFrame,
        climate_df: pd.DataFrame,
        on_keys: List[str],
        how: str = 'left'
    ) -> pd.DataFrame:
        """
        Merge two DataFrames based on specified keys.

        Args:
            bird_df (pd.DataFrame): Bird population DataFrame.
            climate_df (pd.DataFrame): Climate DataFrame.
            on_keys (List[str]): List of column names to merge on.
            how (str, optional): Type of merge. Defaults to 'left'.

        Returns:
            pd.DataFrame: Merged DataFrame.
        """
        self.logger.info(
            f"Merging datasets on keys: {on_keys} with method '{how}'..."
        )
        merged_df: pd.DataFrame = pd.merge(
            bird_df, climate_df, on=on_keys, how=how
        )
        self.logger.info(f"Merged dataset shape: {merged_df.shape}")
        return merged_df
