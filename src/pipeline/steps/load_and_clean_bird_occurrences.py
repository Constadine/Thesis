# src/pipeline/steps/load_and_clean_bird_occurrences.py

import pandas as pd
from src.configurations.config import Config
from src.utils.logger import setup_logger
import logging
from typing import Optional

class LoadAndCleanBirdOccurrences:
    """
    Loads and cleans the raw bird occurrence data.
    """

    def __init__(self, config: Config, logger: Optional['logging.Logger'] = None):
        self.config = config
        self.logger = logger or setup_logger('LoadAndCleanBirdOccurrences', self.config.log_file)

    def run(self, filename: str, nestlings: bool = False) -> pd.DataFrame:
        """
        Load and clean nestling data from the occurrence file.

        Args:
            filename (str): Path to the raw occurrence.txt file.
            nestlings (bool, optional): Whether to filter for nestling occurrences. Defaults to False.

        Returns:
            pd.DataFrame: Cleaned bird data.
        """
        self.logger.info(f"Loading raw bird data from {filename}...")
        ds = pd.read_csv(filename, sep="\t", on_bad_lines='skip')

        self.logger.info("Cleaning dataset...")
        ds.dropna(axis=1, how='all', inplace=True)

        col_to_drop1 = [
            'gbifID', 'occurrenceID', 'recordedBy', 'organismQuantity', 'taxonomicStatus', 'eventTime',
            'eventID', 'startDayOfYear', 'endDayOfYear', 'sampleSizeValue', 'locationID', 'county',
            'taxonID', 'scientificName', 'order', 'family', 'genus', 'genericName',
            'specificEpithet', 'infraspecificEpithet', 'taxonRank', 'vernacularName',
            'lastInterpreted', 'taxonKey', 'acceptedTaxonKey', 'orderKey', 'familyKey',
            'genusKey', 'speciesKey', 'species', 'acceptedScientificName', 'verbatimScientificName',
            'lastParsed', 'level0Gid', 'level0Name', 'level1Gid', 'level1Name',
            'level2Gid', 'year', 'month', 'day', 'level2Name', 'iucnRedListCategory'
        ]
        col_to_drop2 = [x for x in ds.columns if len(ds[x].unique()) == 1]
        ds.rename(columns={'decimalLatitude': 'lat', 'decimalLongitude': 'lon'}, inplace=True)

        ds.drop(columns=col_to_drop1 + col_to_drop2, inplace=True, errors='ignore')

        ds = ds[['eventDate', 'lifeStage', 'individualCount', 'lat', 'lon']]
        if nestlings:
            self.logger.info("Filtering for nestling life stage...")
            ds = ds[ds.lifeStage == 'Nestling']

        self.logger.info(f"Cleaned bird data shape: {ds.shape}")
        return ds
