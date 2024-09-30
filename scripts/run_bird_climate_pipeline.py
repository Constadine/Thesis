# scripts/run_bird_climate_pipeline.py

import sys
import os

# Add the project root to sys.path to recognize 'src' as a module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
from src.main import load_config  # Import the corrected load_config function
from src.pipeline.bird_climate_data_processor import BirdClimateDataProcessor
from pydantic import ValidationError

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Run the Bird-Climate Data Processing Pipeline.',
        epilog='Example usage: python run_bird_climate_pipeline.py --nestlings'
    )
    parser.add_argument('--nestlings', action='store_true', help='Filter data for nestling occurrences.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Load configuration using the corrected load_config function
    config_path = 'config/config.yaml'
    try:
        config = load_config(config_path)
    except ValidationError as e:
        print("Configuration validation error:", e)
        sys.exit(1)
    except Exception as e:
        print("Error loading configuration:", e)
        sys.exit(1)

    # Initialize and run the pipeline
    processor = BirdClimateDataProcessor(config)
    processor.run_pipeline(nestlings=args.nestlings)

if __name__ == "__main__":
    main()
