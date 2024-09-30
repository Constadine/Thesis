# src/pipeline/steps/aggregate_bird_populations.py

import polars as pl
from src.configurations.config import Config
from src.utils.logger import setup_logger
from src.utils.file_operations import save_dataframe
import logging
from typing import Optional

class AggregateBirdPopulations:
    """
    Aggregates bird data by event date and location.
    """

    def __init__(self, config: Config, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or setup_logger('AggregateBirdPopulations', self.config.log_file)

    def run(self, input_csv: str, output_csv: str) -> None:
        """
        Aggregates and sorts bird data.

        Args:
            input_csv (str): Path to the cleaned bird data CSV.
            output_csv (str): Path to save the aggregated data CSV.
        """
        self.logger.info(f"Loading bird data from {input_csv} using Polars...")
        bird_data = pl.read_csv(input_csv)

        self.logger.info("Aggregating individual counts by eventDate, lat, and lon...")
        aggregated_data = bird_data.group_by(['eventDate', 'lat', 'lon']).agg(
            pl.col('individualCount').sum().alias('total_population')
        )

        self.logger.info("Sorting aggregated data by lat, lon, and eventDate...")
        sorted_data = aggregated_data.sort(['lat', 'lon', 'eventDate'])

        self.logger.info(f"Saving aggregated bird data to {output_csv}...")
        sorted_data.write_csv(output_csv)

        self.logger.info("Aggregation and sorting complete.")
