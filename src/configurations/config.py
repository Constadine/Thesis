# src/configurations/config.py

import yaml
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError


class Metrics(BaseModel):
    monthly_metric_name: str
    yearly_metric_name: str


class ClimateConfig(BaseModel):
    file_path_pattern: str
    skiprows: int
    usecols: List[int]
    delimiter: str
    column_names: List[str]
    date_column: str
    value_column: str
    distance_limit: int
    n_hours_for_mean_conc_diff: int
    value_threshold_for_conc_diff: int
    metrics: Dict[str, Metrics]


class Paths(BaseModel):
    raw_occurrence_file: str
    cleaned_bird_data: str
    aggregated_bird_data: str
    paired_bird_climate_data: str
    climate_data_folder: str
    correlation_data_path: str


class OutputDirs(BaseModel):
    heatmaps: str
    logs: str
    reports: Optional[str] = None  # Optional for future expansions


class Config(BaseModel):
    paths: Paths
    output: OutputDirs
    climate_variables: List[str]
    climate_configs: Dict[str, ClimateConfig]
    save_images_default: bool = False  # Default setting for saving images

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Config':
        """
        Loads the configuration from a YAML file.

        Args:
            yaml_path (str): Path to the YAML configuration file.

        Returns:
            Config: An instance of the Config class with loaded configurations.
        """
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)


class CorrelationConfig(BaseModel):
    data_file_path: str
    save_dir: str
    name_suffix: Optional[str] = ''
    save_images: bool = False
    show_plots: bool = True
    columns: List[str]
