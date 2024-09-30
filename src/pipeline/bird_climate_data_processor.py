# src/pipeline/bird_climate_data_processor.py

from src.configurations.config import Config
from src.utils.logger import setup_logger
from src.pipeline.steps.load_and_clean_bird_occurrences import LoadAndCleanBirdOccurrences
from src.pipeline.steps.aggregate_bird_populations import AggregateBirdPopulations
from src.pipeline.steps.pair_bird_data_with_climate_stations import PairBirdDataWithClimateStations
from src.pipeline.steps.prepare_correlation_data import PrepareCorrelationData
from src.utils.file_operations import save_dataframe
from typing import Optional
import logging


class BirdClimateDataProcessor:
    """
    Orchestrates the processing of bird and climate data from raw files to paired dataset and preparation for correlation analysis.
    """

    def __init__(self, config: Config, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or setup_logger('BirdClimateDataProcessor', self.config.output.logs, 'pipeline.log')

        # Initialize processing steps
        self.load_clean_step = LoadAndCleanBirdOccurrences(self.config, self.logger)
        self.aggregate_step = AggregateBirdPopulations(self.config, self.logger)
        self.pair_step = PairBirdDataWithClimateStations(self.config, self.logger)
        self.prepare_correlation_step = PrepareCorrelationData(self.config, self.logger)

    def run_pipeline(self, nestlings: bool = False) -> None:
        """
        Executes the entire data processing pipeline.

        Args:
            nestlings (bool, optional): Whether to filter for nestling occurrences. Defaults to False.
        """
        self.logger.info("Starting Bird-Climate Data Processing Pipeline...")

        # Step 1: Load and Clean Bird Occurrences
        raw_occurrence_file = self.config.paths.raw_occurrence_file
        cleaned_bird_csv = self.config.paths.cleaned_bird_data
        cleaned_bird_data = self.load_clean_step.run(raw_occurrence_file, nestlings=nestlings)
        save_dataframe(cleaned_bird_data, cleaned_bird_csv)
        self.logger.info(f"Cleaned bird data saved to '{cleaned_bird_csv}'.")

        # Step 2: Aggregate Bird Populations
        aggregated_bird_csv = self.config.paths.aggregated_bird_data
        self.aggregate_step.run(cleaned_bird_csv, aggregated_bird_csv)
        self.logger.info(f"Aggregated bird data saved to '{aggregated_bird_csv}'.")

        # Step 3: Pair Bird Data with Climate Stations
        paired_bird_climate_csv = self.config.paths.paired_bird_climate_data
        climate_data_folder = self.config.paths.climate_data_folder
        self.pair_step.run(aggregated_bird_csv, climate_data_folder, paired_bird_climate_csv)
        self.logger.info(f"Paired bird-climate data saved to '{paired_bird_climate_csv}'.")

        # Step 4: Prepare Correlation Data
        correlation_data_csv = self.config.paths.correlation_data_path
        self.prepare_correlation_step.run(paired_bird_climate_csv, correlation_data_csv)
        self.logger.info(f"Correlation data prepared and saved to '{correlation_data_csv}'.")

        self.logger.info("Bird-Climate Data Processing Pipeline Completed Successfully.")
