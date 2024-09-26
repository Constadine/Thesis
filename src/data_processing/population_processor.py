# src/data_processing/population_processor.py

import pandas as pd
from typing import List
class PopulationProcessor:
    """
    Responsible for processing population data, such as adding lagged population figures.
    """

    def __init__(self, logger):
        self.logger = logger

    def add_lagged_population(
        self,
        df: pd.DataFrame,
        group_keys: List[str] = ['lat', 'lon'],
        lag: int = -1
    ) -> pd.DataFrame:
        """
        Add a lagged population column to the DataFrame.

        Args:
            df (pd.DataFrame): DataFrame with population data.
            group_keys (List[str], optional): Columns to group by before applying the lag. Defaults to ['lat', 'lon'].
            lag (int, optional): Number of periods to lag. Defaults to -1 (next period).

        Returns:
            pd.DataFrame: DataFrame with the lagged population column added.
        """
        self.logger.info(f"Adding lagged population data with lag={lag}...")
        df['lagged_population'] = df.groupby(group_keys)['total_population'].shift(lag)
        initial_shape = df.shape
        df = df.dropna(subset=['lagged_population'])
        self.logger.info(f"Lagged population added. Records reduced from {initial_shape[0]} to {df.shape[0]}.")
        return df
