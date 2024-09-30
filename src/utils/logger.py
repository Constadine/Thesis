# src/utils/logger.py

import logging
import os
from typing import Optional


def setup_logger(name: str, log_dir: str, log_filename: str = 'pipeline.log', level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with a FileHandler and StreamHandler.

    Args:
        name (str): Name of the logger.
        log_dir (str): Directory where the log file will be saved.
        log_filename (str, optional): Name of the log file. Defaults to 'pipeline.log'.
        level (int, optional): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    # Define the full log file path
    log_file_path = os.path.join(log_dir, log_filename)

    # Avoid adding multiple handlers if the logger already has them
    if not logger.handlers:
        # File Handler
        f_handler = logging.FileHandler(log_file_path)
        f_handler.setLevel(level)
        f_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_formatter)
        logger.addHandler(f_handler)

        # Stream Handler (console)
        s_handler = logging.StreamHandler()
        s_handler.setLevel(level)
        s_formatter = logging.Formatter('%(levelname)s - %(message)s')
        s_handler.setFormatter(s_formatter)
        logger.addHandler(s_handler)

    return logger
