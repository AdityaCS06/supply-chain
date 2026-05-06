#!/usr/bin/env python
"""Data Transformations and Preprocessing"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from typing import Tuple, List, Optional
from pathlib import Path
import sys
import pickle

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.logger import logger


class DataTransformer:
    def __init__(self):
        self.scaler = None
        self.encoders = {}
        self.feature_cols = []

    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'forward') -> pd.DataFrame:
        logger.info(f"Handling missing values with strategy: {strategy}")

        df = df.copy()

        if strategy == 'forward':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].ffill()
            df[numeric_cols] = df[numeric_cols].bfill()
        elif strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'zero':
            df = df.fillna(0)

        return df

    def remove_outliers(self, df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
        logger.info(f"Removing outliers from column: {column}")

        df = df.copy()

        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        df = df[z_scores < threshold]

        logger.info(f"Removed {len(df)} rows with outliers")
        return df

    def split_train_test(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info(f"Splitting data with test_size: {test_size}")

        df = df.sort_values('date').reset_index(drop=True)
        split_idx = int(len(df) * (1 - test_size))

        train = df.iloc[:split_idx].copy()
        test = df.iloc[split_idx:].copy()

        logger.info(f"Train size: {len(train)}, Test size: {len(test)}")
        return train, test

    def temporal_split(self, df: pd.DataFrame, train_end: str = '2017-06-30') -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info(f"Splitting data temporally: train until {train_end}")

        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])

        train = df[df['date'] <= train_end].copy()
        test = df[df['date'] > train_end].copy()

        logger.info(f"Train size: {len(train)}, Test size: {len(test)}")
        return train, test

    def prepare_features(self, df: pd.DataFrame, target_col: str = 'sales') -> Tuple[np.ndarray, np.ndarray]:
        exclude_cols = ['date', target_col, 'store', 'item']
        feature_cols = [col for col in df.columns if col not in exclude_cols]

        self.feature_cols = feature_cols

        X = df[feature_cols].values
        y = df[target_col].values

        return X, y

    def scale_features(self, X_train: np.ndarray, X_test: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, np.ndarray]:
        logger.info(f"Scaling features with method: {method}")

        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled

    def inverse_scale(self, X: np.ndarray) -> np.ndarray:
        return self.scaler.inverse_transform(X)

    def save_scaler(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.scaler, f)
        logger.info(f"Saved scaler to {path}")

    def load_scaler(self, path: str):
        with open(path, 'rb') as f:
            self.scaler = pickle.load(f)
        logger.info(f"Loaded scaler from {path}")


class TimeSeriesSplitter:
    def __init__(self, n_splits: int = 5):
        self.n_splits = n_splits
        self.tscv = TimeSeriesSplit(n_splits=n_splits)

    def get_splits(self, X: np.ndarray, y: np.ndarray):
        splits = []
        for train_idx, val_idx in self.tscv.split(X):
            splits.append((train_idx, val_idx))
        return splits


def preprocess_data(input_path: str, output_dir: str = "data/processed"):
    logger.info(f"Loading data from {input_path}")

    df = pd.read_csv(input_path)

    logger.info(f"Original shape: {df.shape}")

    transformer = DataTransformer()

    df = transformer.handle_missing_values(df, strategy='forward')

    train, test = transformer.temporal_split(df, train_end='2017-06-30')

    Path(output_dir).mkdir(exist_ok=True)

    train.to_csv(f"{output_dir}/train_processed.csv", index=False)
    test.to_csv(f"{output_dir}/test_processed.csv", index=False)

    logger.info(f"Saved train ({len(train)}) and test ({len(test)}) to {output_dir}")

    return train, test, transformer


if __name__ == "__main__":
    print("=" * 60)
    print("Data Preprocessing")
    print("=" * 60)

    train, test, transformer = preprocess_data("data/features/train_features.csv")

    print(f"\nTrain shape: {train.shape}")
    print(f"Test shape: {test.shape}")
    print(f"Features: {transformer.feature_cols[:10]}...")