# Project Title: Viability of Coastal Bird Breeding in Coastal Regions of Sweden

## Project Objective:

The primary objective of this research project is to conduct a comprehensive assessment of the viability of coastal bird breeding in the western coastal regions of Sweden. The central focus of this study revolves around the thorough analysis of the temporal dynamics of wave activity in these coastal areas, with a particular emphasis on ascertaining its potential deleterious effects on the avian breeding process.

## Scientific Inquiries:

This investigation encompasses an intricate examination of climatic variables intricately associated with wave activity, including wind speed and direction, atmospheric pressure, temperature, wave speed, and wave direction. The overarching aim is to elucidate the predominant climatic factor driving variations in coastal conditions, thereby contributing to a deeper understanding of the evolving climate dynamics.

## Table of Contents

- [Data Sources](#data-sources)
- [Project Overview](#project-overview)
- [Data Processing Pipeline](#data-processing-pipeline)
  - [Purpose](#purpose)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Output](#output)
  - [Logging](#logging)
- [Correlational Analysis](#correlational-analysis)
- [Workflow](#workflow)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Data Sources:

- **Bird data:** [GBIF](https://www.gbif.org)
- **Climate observations:** [SMHI](https://www.smhi.se)
- **Reanalysis data:** [Copernicus](https://www.copernicus.eu)


## Project Overview

The project is divided into several key components:

1. **Data Acquisition:** Gathering raw bird occurrence data and climate station data.
2. **Data Processing Pipeline:** Cleaning and preparing the data, and pairing bird locations with the nearest climate stations.
3. **Correlational Analysis:** Conducting statistical analyses to identify correlations between climate variables and bird populations.
4. **Reporting:** Compiling findings into comprehensive reports and visualizations.

## Description of Key Directories and Files

- **`config/`**
  - `config.yaml`: Configuration file containing paths and settings for the data processing pipeline.

- **`data/`**
  - **`bird_data/`**
    - `raw/`: Contains raw bird occurrence data (`occurrence.txt`).
    - `processed/`: Stores processed bird data, including cleaned, aggregated, and paired datasets.
  - **`climate_data/`**
    - `raw/`: Contains raw climate data CSV files for various climate variables.
    - `processed/`: Reserved for any further processed climate data if needed.

- **`logs/`**
  - `pipeline.log`: Log file capturing detailed information about the pipeline's execution.

- **`scripts/`**
  - `run_bird_climate_pipeline.py`: Executable script to run the entire data processing pipeline.
  - `validate_config.py`: Script to validate the configuration file against the Pydantic model.

- **`src/`**
  - **`configurations/`**
    - `config.py`: Pydantic models defining the structure of the configuration.
  - **`pipeline/`**
    - `bird_climate_data_processor.py`: Orchestrates the execution of various pipeline steps.
    - **`steps/`**
      - `pair_bird_data_with_climate_stations.py`: Handles the pairing of bird data with nearest climate stations.
  - **`utils/`**
    - `file_operations.py`: Utility functions for file reading and writing.
    - `logger.py`: Configures and sets up logging.

- **`requirements.txt`**
  - Lists all Python dependencies required to run the pipeline.

- **`README.md`**
  - This documentation file.

## Data Processing Pipeline

### Purpose

The **Data Processing Pipeline** is designed to prepare and integrate bird occurrence data with relevant climate station data. This integration is essential for conducting meaningful correlational analyses between bird populations and climate variables.

### Installation

#### Prerequisites

- **Python 3.10** or higher.
- **pip** package manager.

#### Steps

1. **Clone the Repository**

```
git clone https://github.com/Constadine/Thesis.git
cd Thesis
```

2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```
python3 -m venv venv
```

3. Activate the Virtual Environment

On Unix or MacOS:

```
source venv/bin/activate
```
On Windows:

```
venv\Scripts\activate
```
4. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration
The pipeline is configured using the config.yaml file located in the config/ directory. This file defines paths to data files, climate variables, and logging settings.

Example config.yaml
```
paths:
  raw_occurrence_file: 'data/bird_data/raw/occurrence.txt'
  cleaned_bird_data: 'data/bird_data/processed/all_nestlings_cleaned.csv'
  aggregated_bird_data: 'data/bird_data/processed/aggregated_bird_data_sorted.csv'
  paired_bird_climate_data: 'data/bird_data/processed/paired_birds_all_climate_data.csv'
  climate_data_folder: 'data/climate_data/raw'

climate_variables:
  - air_pressure
  - air_temperature
  - seawater_level
  - sea_temp
  - wave_height
  - wind

climate_configs:
  air_pressure:
    file_path_pattern: 'air_pressure.csv'
    skiprows: 10
    usecols: [0, 2]
    delimiter: ';'
    column_names: ['Date', 'Air Pressure']
    date_column: 'Date'
    value_column: 'Air Pressure'
    distance_limit: 20
    n_hours_for_mean_conc_diff: 12
    value_threshold_for_conc_diff: 40
    metrics:
      mean:
        monthly_metric_name: 'Monthly Mean Air Pressure'
        yearly_metric_name: 'Yearly Mean Air Pressure'
      std:
        monthly_metric_name: 'Monthly Std Dev Air Pressure'
        yearly_metric_name: 'Yearly Std Dev Air Pressure'

  # Add configurations for other climate variables similarly

log_file: 'logs/pipeline.log'
```
#### Key Configuration Sections

- paths
    - Defines file paths for raw and processed data, as well as the climate data folder.
- climate_variables
    - Lists all climate variables to be processed.
- climate_configs
    - Detailed configurations for each climate variable, including file patterns, data parsing settings, and distance limits for pairing.
- log_file
    - Specifies the path to the log file.


### Usage

#### Running the Pipeline
Execute the pipeline using the run_bird_climate_pipeline.py script located in the scripts/ directory.

```
python scripts/run_bird_climate_pipeline.py [--nestlings]
```

#### Command-Line Arguments
- `--nestlings`: (Optional) If provided, the pipeline will filter data for nestling occurrences.

Example
To run the pipeline with the nestlings filter:
```
python scripts/run_bird_climate_pipeline.py --nestlings
```
### Output
The processed and paired data will be saved to the path specified in config.yaml under paths.paired_bird_climate_data. For example:

```
data/bird_data/processed/paired_birds_all_climate_data.csv
```
Output File Details
- File: paired_birds_all_climate_data.csv
- Contents: Combined dataset containing bird occurrence information along with corresponding climate station data, including nearest station identifiers and distances.


### Logging
Comprehensive logging is implemented to track the pipeline's execution and aid in troubleshooting.

- Log File: logs/pipeline.log
- Log Details:
    - Start and completion of each pipeline step.
    - Information about data loading, processing, and saving.
    - Warnings for missing climate data files or invalid data entries.
    - Errors encountered during execution.


#### Viewing Logs
You can view the log file using standard command-line tools or any text editor.

```
cat logs/pipeline.log
```
Or, for real-time monitoring:

```
tail -f logs/pipeline.log
```



