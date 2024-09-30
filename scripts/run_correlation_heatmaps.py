# scripts/run_correlation_heatmaps.py

from dotenv import load_dotenv
load_dotenv()

import argparse
import sys
import pandas as pd
import os
from src.configurations.config import Config, CorrelationConfig
from src.analysis.correlation_heatmaps import CorrelationHeatmapGenerator


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate and save correlation heatmaps for Pearson, Spearman, and Kendall Tau correlations.',
        epilog='Example usage: python run_correlation_heatmaps.py --config config/config.yaml'
    )
    parser.add_argument('--config', type=str, default='config/config.yaml',
                        help='Path to the configuration YAML file.')
    parser.add_argument('--data_path', type=str,
                        help='Path to the CSV file containing the data. Overrides config.')
    parser.add_argument('--save_dir', type=str,
                        help='Directory where the heatmaps will be saved. Overrides config.')
    parser.add_argument('--name_suffix', type=str, default='',
                        help='Optional suffix for the output heatmap filenames.')
    parser.add_argument('--save_images', action='store_true',
                        help='Include this flag to save the heatmaps as PNG files.')
    parser.add_argument('--no_show', action='store_true',
                        help='Include this flag to suppress showing the plots.')
    parser.add_argument('--columns', type=str, nargs='+',
                        help='List of columns to include in the correlation.')
    parser.add_argument('--list_columns', action='store_true',
                        help='List available columns from the dataset and exit.')

    return parser.parse_args()


def list_columns(config: Config) -> None:
    """Load the dataset and print available columns."""
    try:
        data_path = config.paths.correlation_data_path
        if not os.path.isfile(data_path):
            # Handle if data_path is a directory with multiple CSVs
            if os.path.isdir(data_path):
                csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
                if not csv_files:
                    print(f"No CSV files found in directory: {data_path}")
                    sys.exit(1)
                df = pd.concat([pd.read_csv(os.path.join(data_path, f)) for f in csv_files])
            else:
                print(f"Data path '{data_path}' is neither a file nor a directory.")
                sys.exit(1)
        else:
            df = pd.read_csv(data_path)
        columns = df.columns.tolist()
        print("\nAvailable columns in the dataset:")
        for col in columns:
            print(f" - {col}")
    except Exception as e:
        print(f"Error loading the dataset: {e}")
        sys.exit(1)


def main():
    """Main function to run correlation heatmaps."""
    args = parse_arguments()

    # Load configuration using Pydantic
    try:
        config = Config.from_yaml(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # If --list_columns is passed, list the columns and exit
    if args.list_columns:
        list_columns(config)
        sys.exit(0)

    # Override config with command-line arguments if provided
    data_file_path = args.data_path if args.data_path else config.paths.correlation_data_path
    save_dir = args.save_dir if args.save_dir else config.output.heatmaps
    name_suffix = args.name_suffix
    save_images = args.save_images or False  # Default to False unless specified
    show_plots = not args.no_show
    columns = args.columns if args.columns else config.climate_variables

    if not data_file_path:
        print("Error: Data file path must be specified either via --data_path or in the configuration file.")
        sys.exit(1)

    # Validate that the provided columns exist in the dataset
    try:
        if os.path.isfile(data_file_path):
            df = pd.read_csv(data_file_path)
        elif os.path.isdir(data_file_path):
            csv_files = [f for f in os.listdir(data_file_path) if f.endswith('.csv')]
            if not csv_files:
                print(f"No CSV files found in directory: {data_file_path}")
                sys.exit(1)
            df = pd.concat([pd.read_csv(os.path.join(data_file_path, f)) for f in csv_files])
        else:
            print(f"Data path '{data_file_path}' is neither a file nor a directory.")
            sys.exit(1)
        available_columns = df.columns.tolist()
        invalid_columns = [col for col in columns if col not in available_columns]
        if invalid_columns:
            print(f"Error: The following columns are not present in the dataset: {invalid_columns}")
            print("Use --list_columns to see available options.")
            sys.exit(1)
    except Exception as e:
        print(f"Error reading data file: {e}")
        sys.exit(1)

    # Initialize CorrelationConfig dataclass
    correlation_config = CorrelationConfig(
        data_file_path=data_file_path,
        save_dir=save_dir,
        name_suffix=name_suffix,
        save_images=save_images,
        show_plots=show_plots,
        columns=columns
    )

    # Initialize and run the heatmap generator
    try:
        heatmap_generator = CorrelationHeatmapGenerator(correlation_config)
        heatmap_generator.run()
    except Exception as e:
        print(f"An error occurred during heatmap generation: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
