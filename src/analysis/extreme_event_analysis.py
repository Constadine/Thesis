import argparse
import sys
import yaml
import pandas as pd
import numpy as np

def load_data(data_path, population_path):
    # Load datasets and return as dataframes
    data = pd.read_csv(data_path)
    population = pd.read_csv(population_path)
    return data, population

def identify_extreme_events(data, threshold=0.95):
    # Identify and flag extreme events
    data_long = pd.melt(data, id_vars=['Date'], var_name='Station', value_name='Temperature')
    extreme_threshold = data_long['Temperature'].quantile(threshold)
    data_long['Extreme_Event'] = data_long['Temperature'] > extreme_threshold
    return data_long

def summarize_extreme_events(data_long):
    # Summarize the extreme events
    summary = data_long.groupby(data_long['Date'].dt.year)['Extreme_Event'].sum().reset_index()
    summary.columns = ['Year', 'Extreme_Events']
    return summary

def correlate_with_population(extreme_summary, population_data):
    # Correlate extreme events with bird population data
    merged_data = pd.merge(extreme_summary, population_data, on='Year')
    correlation = merged_data.corr()
    return correlation

def main(data_path, population_path, threshold=0.95):
    data, population = load_data(data_path, population_path)
    extreme_events = identify_extreme_events(data, threshold)
    extreme_summary = summarize_extreme_events(extreme_events)
    correlation_results = correlate_with_population(extreme_summary, population)
    
    # Save or display results
    print("Correlation between extreme events and bird population:")
    print(correlation_results)
    extreme_summary.to_csv('extreme_event_summary.csv', index=False)
    print("Results saved to 'extreme_event_summary.csv'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run extreme event impact analysis.')
    parser.add_argument('--config', type=str, help='Path to the configuration YAML file.')
    parser.add_argument('--data_path', type=str, help='Path to the temperature data CSV file.')
    parser.add_argument('--population_path', type=str, help='Path to the bird population data CSV file.')
    parser.add_argument('--threshold', type=float, default=0.95, help='Percentile threshold for defining extreme events.')

    args = parser.parse_args()

    # Load configuration if a config file is provided
    if args.config:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
        data_path = config.get('data_path')
        population_path = config.get('population_path')
        threshold = config.get('threshold', 0.95)
    else:
        # If running in Spyder or without a config file
        if len(sys.argv) == 1:
            print("No command-line arguments detected, using default values.")
            args = parser.parse_args([
                '--data_path', '/home/kotikos/Education/UoG/Earth Science Master/Thesis/data/SMHI/air_temperature.csv',
                '--population_path', '/path/to/default/population.csv',
                '--threshold', '0.95'
            ])
        data_path = args.data_path
        population_path = args.population_path
        threshold = args.threshold

    main(data_path=data_path, population_path=population_path, threshold=threshold)
