# src/main.py

from src.configurations.config import Config
from pydantic import ValidationError
import yaml
import logging

def load_config(config_path: str) -> Config:
    with open(config_path, 'r') as file:
        try:
            config_dict = yaml.safe_load(file)
            config = Config(**config_dict)
            return config
        except ValidationError as e:
            print("Configuration validation error:", e)
            raise
        except Exception as e:
            print("Error loading configuration:", e)
            raise
