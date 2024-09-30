# src/utils/config_loader.py

import yaml
import os

class ConfigLoader:
    """
    Loads configuration from a YAML file.
    """

    def __init__(self, config_path: str = 'config/config.yaml') -> None:
        """
        Loads configuration from a YAML file.

        Args:
            config_path (str): Path to the YAML configuration file. Defaults to 'config/config.yaml'.

        Returns:
            None
        """
        self.config_path: str = config_path
        self.config: dict = self.load_config()

    def load_config(self) -> dict:
        """
        Load the YAML configuration file.

        Returns:
            dict: Configuration parameters.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

        with open(self.config_path, 'r') as file:
            try:
                config: dict = yaml.safe_load(file)
                return config
            except yaml.YAMLError as e:
                raise Exception(f"Error parsing YAML file: {e}")
