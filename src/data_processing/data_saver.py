# src/data_processing/data_saver.py

import pandas as pd

class DataSaver:
    """
    Responsible for saving DataFrames to CSV files.
    """

    def __init__(self, logger):
        self.logger = logger

    def save_to_csv(self, df, output_path):
        """
        Save the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame to save.
            output_path (str): Path to save the CSV file.
        """
        try:
            self.logger.info(f"Saving DataFrame to {output_path}...")
            df.to_csv(output_path, index=False)
            self.logger.info("DataFrame saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save DataFrame: {e}")
            raise
