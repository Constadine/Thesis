# scripts/validate_config.py

import sys
import os
import yaml
from src.configurations.config import Config
from pydantic import ValidationError

def main():
    # Ensure the script is run from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(project_root)
    
    config_path = 'config/config.yaml'
    
    with open(config_path, 'r') as f:
        try:
            config_dict = yaml.safe_load(f)
            config = Config(**config_dict)
            print("Configuration loaded successfully!")
        except ValidationError as e:
            print("Configuration validation error:", e)
        except Exception as e:
            print("Error loading configuration:", e)

if __name__ == "__main__":
    main()
