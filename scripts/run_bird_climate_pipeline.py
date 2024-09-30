# scripts/run_bird_climate_pipeline.py

import argparse
import sys
from src.configurations.config import Config
from src.pipeline.bird_climate_data_processor import BirdClimateDataProcessor
from dotenv import load_dotenv
from pydantic import ValidationError

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Run Bird-Climate Data Processing Pipeline.')
    parser.add_argument('--config', type=str, default='config/config.yaml', help='Path to the configuration YAML file.')
    parser.add_argument('--nestlings', action='store_true', help='Filter for nestling life stage.')
    return parser.parse_args()

def main():
    """Main function to execute the data processing pipeline."""
    # Load environment variables from .env
    load_dotenv()

    args = parse_arguments()

    # Load configuration using Pydantic
    try:
        config = Config.from_yaml(args.config)
    except ValidationError as e:
        print(f"Configuration validation error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Configuration file not found: {args.config}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # Initialize and run the pipeline
    processor = BirdClimateDataProcessor(config)
    processor.run_pipeline(nestlings=args.nestlings)

if __name__ == '__main__':
    main()
