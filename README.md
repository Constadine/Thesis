# Project Title: Viability of Coastal Bird Breeding in Western Coastal Regions of Sweden

## Project Objective:

The primary objective of this research project is to conduct a comprehensive assessment of the viability of coastal bird breeding in the western coastal regions of Sweden. The central focus of this study revolves around the thorough analysis of the temporal dynamics of wave activity in these coastal areas, with a particular emphasis on ascertaining its potential deleterious effects on the avian breeding process.

## Scientific Inquiries:

This investigation encompasses an intricate examination of climatic variables intricately associated with wave activity, including wind speed and direction, atmospheric pressure, temperature, wave speed, and wave direction. The overarching aim is to elucidate the predominant climatic factor driving variations in coastal conditions, thereby contributing to a deeper understanding of the evolving climate dynamics.

## Data Sources:

- **Bird data:** [GBIF](https://www.gbif.org)
- **Climate observations:** [SMHI](https://www.smhi.se)
- **Reanalysis data:** [Copernicus](https://www.copernicus.eu)

## Code Overview

This project includes several Python scripts designed to process and analyze the bird and climate data. The primary scripts are:

### 1. `process_paired_data.py`

This script processes bird and climate data, offering options to filter for specific periods and to calculate lagged population data for correlation analysis.

### Usage:

- **To filter data for April to June only:**

  ```bash
  python process_paired_data.py --apr_jun
  ```

To add lagged population data only:

```bash
python process_paired_data.py --lagged
```

- **To apply both April-June filtering and add lagged population data:**

```bash
python process_paired_data.py --apr_jun --lagged
```

- **To display help information:**

```bash
python process_paired_data.py --help
```
### Flags:

   - `--apr_jun`: Filters the climate data to include only the months of April, May, and June.
   - `--lagged`: Adds a column for lagged_population, which represents the population in the following year.

### Output Files:

The script generates output files based on the flags provided:

   - No Flags: data_for_correlation.csv
   - With `--apr_jun`: data_for_correlation_apr_jun.csv
   - With `--lagged`: data_for_correlation_with_lag.csv
   - With Both Flags: data_for_correlation_apr_jun_with_lag.csv

### 2. visualize_paired_data.py

This script visualizes the processed bird and climate data on a map using the Folium library. It highlights bird breeding locations and the nearest climate stations.
Usage:

```bash
    python visualize_paired_data.py
```

### 3. analysis.py

This script generates heatmaps for Pearson, Spearman, and Kendall Tau correlations from your bird and climate data.

### Usage:

- **Generate heatmaps for a specific dataset:**

```bash
    python heatmap_script.py --data_path data/final_datasets/data_for_correlation_apr_jun.csv --suffix apr_jun
```
- **Customize the save directory for heatmaps:**

```bash
    python heatmap_script.py --data_path data/final_datasets/data_for_correlation_apr_jun.csv --suffix apr_jun --save_dir /path/to/save
```

- **Display help information:**

```bash
    python heatmap_script.py --help
```

### Script Arguments:

    `--data_path`: Path to the CSV file containing the data for correlation analysis (required).
    `--suffix`: Optional suffix for the output heatmap filenames (default: empty).
    `--save_dir`: Directory where the heatmaps will be saved (default: /home/kotikos/Education/UoG/Earth Science Master/Thesis/results/heatmaps).

### Output:

The script generates three heatmaps (Pearson, Spearman, and Kendall Tau) and saves them in the specified directory with the specified suffix. The filenames follow this format:

    `pearson_correlation_heatmap_<suffix>.png`
    `spearman_correlation_heatmap_<suffix>.png`
    `kendall_correlation_heatmap_<suffix>.png`

### Notes:

Ensure all paths to data sources are correctly specified in the scripts before running. The climate data should be organized by variable, with each file named according to its variable (e.g., air_pressure.csv).

### Installation and Dependencies
Required Libraries:

    Pandas
    Numpy
    Polars
    Folium
    Matplotlib
    Seaborn

### Installation:

You can install the required libraries using pip:

```bash
    pip install requirements.txt
```

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements

We thank the following sources for their invaluable data:

    GBIF
    SMHI
    Copernicus
