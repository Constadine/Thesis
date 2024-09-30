# src/pipeline/steps/pair_bird_data_with_climate_stations.py

import polars as pl
import numpy as np
from src.configurations.config import Config
from src.utils.logger import setup_logger
from typing import Optional
import logging
import time
import os

class PairBirdDataWithClimateStations:
    """
    Pairs bird population data with nearest climate station data.
    """

    def __init__(self, config: Config, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or setup_logger('PairBirdDataWithClimateStations', self.config.log_file)

    @staticmethod
    def haversine(lon1: np.ndarray, lat1: np.ndarray, lon2: np.ndarray, lat2: np.ndarray) -> np.ndarray:
        """
        Calculate the great-circle distance between each bird location and all climate stations.
        
        Args:
            lon1 (np.ndarray): Longitudes of bird locations (1D array).
            lat1 (np.ndarray): Latitudes of bird locations (1D array).
            lon2 (np.ndarray): Longitudes of climate stations (1D array).
            lat2 (np.ndarray): Latitudes of climate stations (1D array).
        
        Returns:
            np.ndarray: 2D array of distances in kilometers. Shape will be (num_bird_locations, num_climate_stations).
        """
        R = 6371.0  # Radius of the Earth in kilometers
        
        # Convert degrees to radians
        lat1 = np.radians(lat1)[:, np.newaxis]  # Shape (num_bird_locations, 1)
        lon1 = np.radians(lon1)[:, np.newaxis]  # Shape (num_bird_locations, 1)
        lat2 = np.radians(lat2)  # Shape (num_climate_stations,)
        lon2 = np.radians(lon2)  # Shape (num_climate_stations,)
        
        # Calculate the differences between bird locations and all climate stations
        dlon = lon2 - lon1  # Broadcasting: Shape (num_bird_locations, num_climate_stations)
        dlat = lat2 - lat1  # Broadcasting: Shape (num_bird_locations, num_climate_stations)
        
        # Haversine formula
        a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        # Distance in kilometers
        distance = R * c  # Shape (num_bird_locations, num_climate_stations)
        
        return distance


    def run(self, paired_bird_csv: str, climate_data_folder: str, output_csv: str) -> None:
        """
        Pairs bird data with climate data based on nearest stations.

        Args:
            paired_bird_csv (str): Path to the aggregated bird data CSV.
            climate_data_folder (str): Path to the climate data folder.
            output_csv (str): Path to save the paired data CSV.
        """
        start_time = time.time()
        self.logger.info(f"Loading paired bird data from {paired_bird_csv} using Polars...")
        bird_data = pl.read_csv(paired_bird_csv)

        self.logger.info("Converting 'eventDate' column to datetime and renaming to 'Date'...")
        bird_data = bird_data.with_columns([
            pl.col("eventDate")
            .str.to_date("%Y-%m-%d", strict=False)
            .alias("Date")
        ])

        # Log and check if there are any invalid dates
        invalid_dates = bird_data.filter(pl.col("Date").is_null()).shape[0]
        if invalid_dates > 0:
            self.logger.warning(f"{invalid_dates} rows have invalid or missing date values.")


        # Removed redundant renaming

        self.logger.info("Extracting unique bird coordinates...")
        bird_coords = bird_data.select(['lat', 'lon']).unique().to_numpy()

        self.logger.info("Initializing combined bird data...")
        combined_bird_data = bird_data

        CLIMATE_VARIABLES = self.config.climate_variables

        for variable in CLIMATE_VARIABLES:
            self.logger.info(f"Processing climate variable: {variable}...")
            climate_data_path = os.path.join(climate_data_folder, f"{variable}.csv")

            if not os.path.exists(climate_data_path):
                self.logger.warning(f"Climate data file {climate_data_path} does not exist. Skipping.")
                continue

            self.logger.info(f"Loading climate data from {climate_data_path}...")
            climate_data = pl.read_csv(climate_data_path)
            config = self.config.climate_configs[variable]

            self.logger.info(f"Converting 'Date' column to datetime for {variable}...")
            climate_data = climate_data.with_columns([
                pl.col("Date")
                .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
                .alias("Date")
            ])


            self.logger.info("Extracting station coordinates from column names...")
            # Assuming column names are in 'lat_lon_variable' format
            # Adjust this parsing based on your actual column naming convention
            station_columns = [col for col in climate_data.columns if col != 'Date']
            station_coords = np.array([
                tuple(map(float, col.split('_')[:2])) for col in station_columns
            ])

            self.logger.info("Calculating distances using Haversine formula...")
            # For each bird location, calculate distance to all stations
            # Then find the nearest station
            # This can be computationally intensive for large datasets

            distances = self.haversine(
                lon1=bird_coords[:, 1],
                lat1=bird_coords[:, 0],
                lon2=station_coords[:, 1],
                lat2=station_coords[:, 0]
            )

            self.logger.info("Identifying nearest stations for each bird location...")
            nearest_station_indices = np.argmin(distances, axis=1)
            nearest_stations = station_coords[nearest_station_indices]
            nearest_distances = distances[np.arange(distances.shape[0]), nearest_station_indices]

            nearest_stations_str = [f"{lat}_{lon}" for lat, lon in nearest_stations]

            self.logger.info("Creating DataFrame for nearest station information...")
            bird_coords_df = pl.DataFrame({
                'lat': bird_coords[:, 0],
                'lon': bird_coords[:, 1],
                f'{variable}_nearest_station': nearest_stations_str,
                f'{variable}_nearest_distance': nearest_distances
            })

            distance_limit = config.distance_limit
            self.logger.info(f"Filtering stations with distance <= {distance_limit} km...")
            bird_coords_df = bird_coords_df.filter(pl.col(f'{variable}_nearest_distance') <= distance_limit)

            self.logger.info("Merging nearest station information with bird data...")
            combined_bird_data = combined_bird_data.join(
                bird_coords_df,
                on=['lat', 'lon'],
                how='left'
            )

        self.logger.info(f"Saving paired bird and climate data to {output_csv}...")
        combined_bird_data.write_csv(output_csv)

        end_time = time.time()
        self.logger.info(f"Pairing completed in {end_time - start_time:.2f} seconds.")
