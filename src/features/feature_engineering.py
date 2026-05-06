#!/usr/bin/env python
"""Feature Engineering for Demand Forecasting"""

import pandas as pd
import numpy as np
from typing import List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.logger import logger


class FeatureEngineer:
    def __init__(self):
        self.features_created = []

    def create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Creating time-based features...")

        df = df.copy()

        df['date'] = pd.to_datetime(df['date'])

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
        df['quarter'] = df['date'].dt.quarter

        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
        df['is_month_end'] = df['date'].dt.is_month_end.astype(int)

        df['is_q1'] = (df['quarter'] == 1).astype(int)
        df['is_q2'] = (df['quarter'] == 2).astype(int)
        df['is_q3'] = (df['quarter'] == 3).astype(int)
        df['is_q4'] = (df['quarter'] == 4).astype(int)

        self.features_created.extend([
            'year', 'month', 'day', 'day_of_week', 'day_of_year',
            'week_of_year', 'quarter', 'is_weekend', 'is_month_start',
            'is_month_end', 'is_q1', 'is_q2', 'is_q3', 'is_q4'
        ])

        return df

    def create_lag_features(self, df: pd.DataFrame, lags: List[int] = None) -> pd.DataFrame:
        if lags is None:
            lags = [1, 7, 14, 28, 60, 90, 365]

        logger.info(f"Creating lag features for lags: {lags}")

        df = df.copy()

        lag_features = []
        for lag in lags:
            col_name = f'sales_lag_{lag}'
            df[col_name] = df.groupby(['store', 'item'])['sales'].shift(lag)
            lag_features.append(col_name)

        self.features_created.extend(lag_features)
        return df

    def create_rolling_features(self, df: pd.DataFrame, windows: List[int] = None) -> pd.DataFrame:
        if windows is None:
            windows = [7, 14, 30, 60, 90]

        logger.info(f"Creating rolling features for windows: {windows}")

        df = df.copy()

        for window in windows:
            df[f'rolling_mean_{window}'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).mean()
            )
            df[f'rolling_std_{window}'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).std()
            )
            df[f'rolling_min_{window}'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).min()
            )
            df[f'rolling_max_{window}'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).max()
            )

        self.features_created.extend([
            f'rolling_mean_{w}' for w in windows
        ] + [
            f'rolling_std_{w}' for w in windows
        ] + [
            f'rolling_min_{w}' for w in windows
        ] + [
            f'rolling_max_{w}' for w in windows
        ])

        return df

    def create_expanding_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Creating expanding features...")

        df = df.copy()

        df['expanding_mean'] = df.groupby(['store', 'item'])['sales'].transform(
            lambda x: x.shift(1).expanding().mean()
        )
        df['expanding_std'] = df.groupby(['store', 'item'])['sales'].transform(
            lambda x: x.shift(1).expanding().std()
        )

        self.features_created.extend(['expanding_mean', 'expanding_std'])
        return df

    def create_ewm_features(self, df: pd.DataFrame, spans: List[int] = None) -> pd.DataFrame:
        if spans is None:
            spans = [7, 14, 30]

        logger.info(f"Creating EWM features for spans: {spans}")

        df = df.copy()

        for span in spans:
            df[f'ewm_mean_{span}'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).ewm(span=span, min_periods=1).mean()
            )

        self.features_created.extend([f'ewm_mean_{s}' for s in spans])
        return df

    def create_store_item_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Creating store-item features...")

        df = df.copy()

        store_item_stats = df.groupby(['store', 'item'])['sales'].agg(['mean', 'std', 'min', 'max']).reset_index()
        store_item_stats.columns = ['store', 'item', 'store_item_mean', 'store_item_std', 'store_item_min', 'store_item_max']

        df = df.merge(store_item_stats, on=['store', 'item'], how='left')

        store_stats = df.groupby('store')['sales'].agg(['mean', 'std']).reset_index()
        store_stats.columns = ['store', 'store_mean', 'store_std']
        df = df.merge(store_stats, on='store', how='left')

        item_stats = df.groupby('item')['sales'].agg(['mean', 'std']).reset_index()
        item_stats.columns = ['item', 'item_mean', 'item_std']
        df = df.merge(item_stats, on='item', how='left')

        self.features_created.extend([
            'store_item_mean', 'store_item_std', 'store_item_min', 'store_item_max',
            'store_mean', 'store_std', 'item_mean', 'item_std'
        ])

        return df

    def create_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Creating all features...")

        df = self.create_time_features(df)
        df = self.create_lag_features(df)
        df = self.create_rolling_features(df)
        df = self.create_expanding_features(df)
        df = self.create_ewm_features(df)
        df = self.create_store_item_features(df)

        logger.info(f"Total features created: {len(self.features_created)}")
        logger.info(f"Features: {self.features_created}")

        return df

    def get_feature_list(self) -> List[str]:
        return self.features_created


def engineer_features(input_path: str, output_path: str = None):
    logger.info(f"Loading data from {input_path}")

    df = pd.read_csv(input_path)

    logger.info(f"Original shape: {df.shape}")

    engineer = FeatureEngineer()
    df_features = engineer.create_all_features(df)

    logger.info(f"Final shape: {df_features.shape}")

    if output_path:
        df_features.to_csv(output_path, index=False)
        logger.info(f"Saved to {output_path}")

    return df_features


if __name__ == "__main__":
    input_file = "data/raw/train.csv"
    output_file = "data/features/train_features.csv"

    print("=" * 60)
    print("Feature Engineering")
    print("=" * 60)

    Path("data/features").mkdir(exist_ok=True)

    df = engineer_features(input_file, output_file)

    print(f"\nFeatures created: {len(df.columns)}")
    print(f"Sample columns: {df.columns.tolist()[:20]}")