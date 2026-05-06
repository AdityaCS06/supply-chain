#!/usr/bin/env python
"""Data Loader for Supply Chain ML"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

from src.config import config
from src.logger import logger


class DataLoader:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = config.RAW_DATA_DIR

        logger.info(f"DataLoader initialized with data_dir: {self.data_dir}")

    def load_train_data(self) -> pd.DataFrame:
        train_path = self.data_dir / "train.csv"

        if not train_path.exists():
            raise FileNotFoundError(f"Train data not found: {train_path}")

        logger.info(f"Loading training data from {train_path}")
        df = pd.read_csv(train_path, parse_dates=['date'])

        logger.info(f"Loaded {len(df):,} rows, columns: {list(df.columns)}")
        return df

    def load_test_data(self) -> pd.DataFrame:
        test_path = self.data_dir / "test.csv"

        if not test_path.exists():
            logger.warning(f"Test data not found: {test_path}")
            return pd.DataFrame()

        logger.info(f"Loading test data from {test_path}")
        df = pd.read_csv(test_path, parse_dates=['date'])

        logger.info(f"Loaded {len(df):,} rows")
        return df

    def load_data(self, split: str = "train") -> pd.DataFrame:
        if split == "train":
            return self.load_train_data()
        elif split == "test":
            return self.load_test_data()
        else:
            raise ValueError(f"Invalid split: {split}. Use 'train' or 'test'")

    def get_store_item_data(self, store: int, item: int) -> pd.DataFrame:
        df = self.load_train_data()
        return df[(df['store'] == store) & (df['item'] == item)].copy()

    def get_date_range(self, split: str = "train") -> Tuple[str, str]:
        df = self.load_data(split)
        return df['date'].min().strftime('%Y-%m-%d'), df['date'].max().strftime('%Y-%m-%d')

    def get_summary(self) -> dict:
        df = self.load_train_data()

        summary = {
            "total_rows": len(df),
            "date_range": (df['date'].min(), df['date'].max()),
            "n_stores": df['store'].nunique(),
            "n_items": df['item'].nunique(),
            "total_sales": df['sales'].sum(),
            "avg_daily_sales": df['sales'].mean(),
            "columns": list(df.columns)
        }

        return summary


def load_data(split: str = "train") -> pd.DataFrame:
    loader = DataLoader()
    return loader.load_data(split)


def get_data_summary() -> dict:
    loader = DataLoader()
    return loader.get_summary()


if __name__ == "__main__":
    print("=" * 60)
    print("Data Summary")
    print("=" * 60)

    summary = get_data_summary()

    for key, value in summary.items():
        print(f"{key}: {value}")