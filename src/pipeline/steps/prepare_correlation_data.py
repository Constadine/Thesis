# src/pipeline/steps/prepare_correlation_data.py

import pandas as pd
from src.configurations.config import Config
from src.utils.logger import setup_logger
from src.utils.file_operations import save_dataframe
from typing import Optional
import logging


class PrepareCorrelationData:
    """
    Prepares data for correlation analysis by merging bird and climate data.
    """

    def __init__(self, config: Config, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or setup_logger('PrepareCorrelationData', self.config.log_file)

    def run(self, input_csv: str, output_csv: str) -> None:
        """
        Processes bird and climate data to generate a dataset suitable for correlation analysis.

        Args:
            input_csv (str): Path to the paired bird-climate data CSV.
            output_csv (str): Path to save the processed data CSV.
        """
        self.logger.info(f"Loading paired bird-climate data from '{input_csv}'...")
        bird_data = pd.read_csv(input_csv)

        # Extract 'Year' from 'Date' column
        # This is done to make it easier to group climate data later
        self.logger.info("Extracting 'Year' from 'Date' column...")
        bird_data['Year'] = pd.to_datetime(bird_data['Date']).dt.year

        # Initialize list to hold processed data frames
        self.logger.info("Initializing list to hold processed data frames...")
        bird_data_list = []

        # Process each climate variable
        climate_variables = self.config.climate_variables
        climate_files = [f"{var}.csv" for var in climate_variables]

        # Process each climate variable
        self.logger.info("Processing each climate variable to calculate yearly means...")
        for variable, file_name in zip(climate_variables, climate_files):
            # Load climate data
            climate_data_path = self.config.paths.climate_data_folder  # Assuming processed climate data is here
            climate_data_path = f"{climate_data_path}/{file_name}"
            climate_data = pd.read_csv(climate_data_path)

            # Extract column names for station and value
            station_column = f"{variable}_nearest_station"
            value_column = f"{variable}_values"

            # If station column exists in bird data, process climate data
            if station_column in bird_data.columns:
                # Get valid stations from bird data
                valid_stations = bird_data[station_column].dropna().unique()
                valid_stations = [station for station in valid_stations if station in climate_data.columns]

                # If there are valid stations, calculate yearly means
                if valid_stations:

                    # Ensure Date column is in datetime format
                    climate_data['Date'] = pd.to_datetime(climate_data['Date'], errors='coerce')

                    # Extract the year from the Date column
                    climate_data['Year'] = climate_data['Date'].dt.year

                    yearly_mean = climate_data.groupby('Year')[valid_stations].mean(numeric_only=True).reset_index()
                    yearly_mean_melted = yearly_mean.melt(
                        id_vars='Year',
                        var_name=f"{variable}_station",
                        value_name=value_column
                    )

                    # Merge climate data with bird data
                    bird_data_temp = bird_data.merge(
                        yearly_mean_melted,
                        left_on=['Year', station_column],
                        right_on=['Year', f"{variable}_station"],
                        how='left'
                    )

                    # If there are no values for a particular year, fill with -1
                    bird_data_temp[value_column] = bird_data_temp[value_column].fillna(-1)
                    bird_data_list.append(bird_data_temp)
                else:
                    self.logger.warning(f"No valid stations found for '{variable}'. Skipping.")
            else:
                self.logger.warning(f"Column '{station_column}' not found in bird data. Skipping '{variable}'.")

        # If there are processed data frames, concatenate them
        if bird_data_list:
            final_bird_data = pd.concat(bird_data_list, ignore_index=True)

            # Drop unnecessary station and distance columns
            self.logger.info("Dropping unnecessary station and distance columns...")
            columns_to_drop = [
                f"{var}_nearest_station" for var in climate_variables
            ] + [
                f"{var}_nearest_distance" for var in climate_variables
            ]
            final_bird_data = final_bird_data.drop(columns=columns_to_drop, errors='ignore')

            # Reorder columns for clarity
            self.logger.info("Reordering columns for clarity...")
            new_column_order = [
                'Year', 'lat', 'lon', 'total_population'
            ] + [f"{var}_values" for var in climate_variables]
            final_bird_data = final_bird_data[new_column_order]

            # Save processed data for correlation analysis
            self.logger.info("Saving processed data for correlation analysis...")
            save_dataframe(final_bird_data, output_csv)

            self.logger.info(f"Data preparation complete. Saved to '{output_csv}'.")
        else:
            self.logger.error("No data processed. Exiting pipeline.")
