import argparse
from analysis.extreme_event_analysis import load_data, identify_extreme_events, summarize_extreme_events, correlate_with_population

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run extreme event impact analysis.')
    parser.add_argument('--data_path', type=str, required=True, help='Path to the temperature data CSV file.')
    parser.add_argument('--population_path', type=str, required=True, help='Path to the bird population data CSV file.')
    parser.add_argument('--threshold', type=float, default=0.95, help='Percentile threshold for defining extreme events.')

    args = parser.parse_args()

    # Load the data
    temperature_data = load_data(args.data_path)
    population_data = load_data(args.population_path)

    # Identify and summarize extreme events
    extreme_events = identify_extreme_events(temperature_data, threshold=args.threshold)
    extreme_summary = summarize_extreme_events(extreme_events)

    # Correlate with bird population data
    correlation_results = correlate_with_population(extreme_summary, population_data)

    # Output the results
    print("Correlation between extreme events and bird population:")
    print(correlation_results)
