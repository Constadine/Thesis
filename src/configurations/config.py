# src/configurations/config.py

from pydantic import BaseModel
from typing import List, Dict

class MetricsConfig(BaseModel):
    monthly_metric_name: str
    yearly_metric_name: str

class ClimateVariableMetrics(BaseModel):
    mean: MetricsConfig
    std: MetricsConfig

class ClimateVariableConfig(BaseModel):
    file_path_pattern: str
    skiprows: int
    usecols: List[int]
    delimiter: str
    column_names: List[str]
    date_column: str
    value_column: str
    distance_limit: float
    n_hours_for_mean_conc_diff: int
    value_threshold_for_conc_diff: float
    metrics: ClimateVariableMetrics

class PathsConfig(BaseModel):
    raw_occurrence_file: str
    cleaned_bird_data: str
    aggregated_bird_data: str
    paired_bird_climate_data: str
    climate_data_folder: str

class Config(BaseModel):
    paths: PathsConfig
    climate_variables: List[str]
    climate_configs: Dict[str, ClimateVariableConfig]
    log_file: str
