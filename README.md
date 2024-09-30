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

Example `config.yaml`:
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


# TO FIX

#### Viewing Logs
You can view the log file using standard command-line tools or any text editor.

```
cat logs/pipeline.log
```
Or, for real-time monitoring:

```
tail -f logs/pipeline.log
```

Correlational Analysis
Purpose
The Correlational Analysis aims to identify and quantify the relationships between coastal bird populations and various climatic variables. By generating correlation heatmaps, we can visually assess the strength and direction of these relationships, which is crucial for understanding the impact of climatic factors on the viability of coastal bird breeding.

Analysis Pipeline
The analysis involves the following steps:

Data Preparation: Utilize the processed data from the data processing pipeline.
Configuration: Set up analysis parameters in the configuration file.
Running the Analysis Script: Execute the script to generate correlation heatmaps.
Interpreting Results: Analyze the generated heatmaps to draw meaningful conclusions.
Configuration
The analysis parameters are set in the same config.yaml file under the output section and other relevant sections. Ensure your config.yaml includes the necessary configurations for the analysis.

Example config.yaml (additional relevant sections):

yaml
Copy code
paths:
  raw_occurrence_file: 'data/bird_data/raw/occurrence.txt'
  cleaned_bird_data: 'data/bird_data/processed/all_nestlings_cleaned.csv'
  aggregated_bird_data: 'data/bird_data/processed/aggregated_bird_data_sorted.csv'
  paired_bird_climate_data: 'data/bird_data/processed/paired_birds_all_climate_data.csv'
  climate_data_folder: 'data/climate_data/processed'
  correlation_data_path: 'data/final_datasets/data_for_correlation.csv'

output:
  heatmaps: 'results/heatmaps'
  logs: 'logs'
  reports: 'results/reports'

save_images_default: false  # Default setting for saving images unless overridden
Key Configuration Sections for Analysis
paths.correlation_data_path: Specifies the path to the data file used for correlation analysis.
output.heatmaps: Directory where the generated heatmaps will be saved.
save_images_default: Default behavior for saving images when running analysis scripts.
Usage
Running the Correlation Heatmap Script
The correlation heatmaps can be generated using the run_correlation_heatmaps.py script located in the scripts/ directory.

Basic Command
bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --columns total_population sea_temp_values
Command-Line Arguments
--config: Path to the configuration YAML file. Defaults to config/config.yaml if not specified.
--columns: List of columns to include in the correlation analysis.
--save_images: Include this flag to save the heatmaps as PNG files.
--no_show: Include this flag to suppress displaying the plots interactively.
--save_dir: (Optional) Specify a different directory to save the heatmaps. Overrides the output.heatmaps setting in the configuration.
--list_columns: Include this flag to list all available columns in the dataset and exit.
Examples
List Available Columns

To display all the columns available for analysis:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --list_columns
Expected Output:

markdown
Copy code
Available columns in the dataset:
 - Year
 - lat
 - lon
 - total_population
 - air_pressure_values
 - air_temperature_values
 - wind_values
 - sea_temp_values
 - seawater_level_values
 - wave_height_values
 ...
Generate Heatmap with Specified Columns

To generate a correlation heatmap for specific columns and save the image:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --columns total_population sea_temp_values --save_images
Suppress Plot Display

If you want to run the script without displaying the plots interactively:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --columns total_population sea_temp_values --save_images --no_show
Specify a Custom Save Directory

To save the heatmaps to a different directory:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --columns total_population sea_temp_values --save_images --save_dir 'custom/heatmaps'
Output
The generated heatmaps will be saved in the directory specified by output.heatmaps in the configuration file, unless overridden by the --save_dir argument.

Default Save Directory: results/heatmaps/
File Naming Convention: Heatmaps are saved with the filename correlation_heatmap.png or with an optional suffix if provided using --name_suffix.
Interpreting the Heatmaps
The correlation heatmaps display the correlation coefficients between the selected variables:

Correlation Coefficients:
+1.0: Perfect positive correlation.
0.0: No correlation.
-1.0: Perfect negative correlation.
By examining the heatmap, you can identify which climate variables have significant correlations with bird populations, aiding in understanding the climatic influences on coastal bird breeding.

Dependencies
Ensure the following Python packages are installed (already included in requirements.txt):

pandas
numpy
seaborn
matplotlib
pydantic
pyyaml
Example Workflow
Prepare the Data:

Run the data processing pipeline to generate the data_for_correlation.csv file:

bash
Copy code
python scripts/run_bird_climate_pipeline.py --config config/config.yaml
List Available Columns:

Check which columns are available for correlation analysis:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --list_columns
Generate Heatmap:

Create a correlation heatmap using selected variables:

bash
Copy code
python scripts/run_correlation_heatmaps.py --config config/config.yaml --columns total_population wind_values sea_temp_values --save_images
Review Output:

Heatmaps are saved in results/heatmaps/.
Review the heatmap to interpret the correlations.
Visualization
Purpose
Visual representations, such as heatmaps, are crucial for interpreting complex data relationships. They provide intuitive insights into how different variables interact with each other.

Customization
You can customize the visualizations by:

Selecting Different Variables: Use the --columns argument.
Adjusting Aesthetics: Modify the script to change color schemes or annotations.
Adding Name Suffixes: Use the --name_suffix argument to differentiate between multiple heatmaps.
Additional Visualizations
Beyond heatmaps, consider creating:

Scatter Plots: To visualize relationships between two variables.
Time Series Plots: To observe trends over time.
Box Plots: To analyze the distribution of a variable.


