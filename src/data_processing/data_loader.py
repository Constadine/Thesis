# src/data_processing/data_loader.py

import pandas as pd
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger

class DataLoader:
    """
    Responsible for loading bird and climate data.
    """

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def load_bird_data(self, bird_data_path):
        """
        Load bird population data from a CSV file.

        Args:
            bird_data_path (str): Path to the bird data CSV.

        Returns:
            pd.DataFrame: Bird population data.
        """
        try:
            self.logger.info(f"Loading bird data from {bird_data_path}...")
            bird_data = pd.read_csv(bird_data_path)
            self.logger.info("Bird data loaded successfully.")
            return bird_data
        except Exception as e:
            self.logger.error(f"Failed to load bird data: {e}")
            raise

    def load_climate_data(self, climate_data_path):
        """
        Load climate data from a CSV file.

        Args:
            climate_data_path (str): Path to the climate data CSV.

        Returns:
            pd.DataFrame: Climate data.
        """
        try:
            self.logger.info(f"Loading climate data from {climate_data_path}...")
            climate_data = pd.read_csv(climate_data_path)
            self.logger.info("Climate data loaded successfully.")
            return climate_data
        except Exception as e:
            self.logger.error(f"Failed to load climate data: {e}")
            raise
