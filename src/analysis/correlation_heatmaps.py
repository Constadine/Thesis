# src/analysis/correlation_heatmaps.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from typing import List
from src.configurations.config import CorrelationConfig
import logging


class CorrelationHeatmapGenerator:
    """
    Generates and saves correlation heatmaps based on the provided configuration.
    """

    def __init__(self, config: CorrelationConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    def setup_logging(self):
        """Sets up logging configuration."""
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def run(self):
        """Executes the heatmap generation process."""
        self.logger.info("Starting correlation heatmap generation.")
        self.generate_heatmaps()
        self.logger.info("Correlation heatmap generation completed.")

    def generate_heatmaps(self):
        """Generates correlation heatmaps for the specified columns."""
        # Load data
        try:
            self.logger.info(f"Loading data from {self.config.data_file_path}")
            df = pd.read_csv(self.config.data_file_path)
            self.validate_columns(df)
            self.logger.info("Data loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            raise ValueError(f"Failed to load data from {self.config.data_file_path}: {e}")

        # Compute correlation matrix
        try:
            self.logger.info("Computing correlation matrix.")
            corr_matrix = df[self.config.columns].corr()
            self.logger.info("Correlation matrix computed successfully.")
        except KeyError as e:
            self.logger.error(f"One or more specified columns do not exist: {e}")
            raise ValueError(f"One or more specified columns do not exist in the dataset: {e}")

        # Create heatmap
        self.logger.info("Generating heatmap.")
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Heatmap')

        # Prepare save directory
        save_dir = self.config.save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.logger.info(f"Heatmaps will be saved to {save_dir}")

        # Prepare filename
        suffix = self.config.name_suffix
        filename = f"correlation_heatmap{suffix}.png" if self.config.save_images else "correlation_heatmap.png"
        save_path = os.path.join(save_dir, filename)

        # Save the heatmap
        if self.config.save_images:
            self.logger.info(f"Saving heatmap to {save_path}")
            plt.savefig(save_path)
            self.logger.info(f"Heatmap saved to {save_path}")

        # Show plot
        if self.config.show_plots:
            self.logger.info("Displaying heatmap plot.")
            plt.show()
        else:
            self.logger.info("Displaying heatmap plot is suppressed.")
            plt.close()

    def validate_columns(self, df: pd.DataFrame):
        """Validates that all specified columns exist in the DataFrame."""
        missing_columns = [col for col in self.config.columns if col not in df.columns]
        if missing_columns:
            self.logger.error(f"The following columns are missing in the dataset: {missing_columns}")
            raise ValueError(f"The following columns are missing in the dataset: {missing_columns}")
