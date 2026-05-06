#!/usr/bin/env python
"""Anomaly Detection for Supply Chain"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.logger import logger


class AnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.model = None
        self.scaler = StandardScaler()
        self.feature_cols = []

    def prepare_features(self, df: pd.DataFrame, is_training: bool = True) -> np.ndarray:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])

        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

        if 'sales' in df.columns:
            df['rolling_mean_7'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(7, min_periods=1).mean()
            )
            df['rolling_std_7'] = df.groupby(['store', 'item'])['sales'].transform(
                lambda x: x.shift(1).rolling(7, min_periods=1).std()
            )
            df['lag_1'] = df.groupby(['store', 'item'])['sales'].shift(1)

        feature_cols = ['sales', 'day_of_week', 'month', 'is_weekend',
                       'rolling_mean_7', 'rolling_std_7', 'lag_1']

        self.feature_cols = [f for f in feature_cols if f in df.columns]
        X = df[self.feature_cols].fillna(0).values

        if is_training:
            X = self.scaler.fit_transform(X)
        else:
            X = self.scaler.transform(X)

        return X

    def train(self, df: pd.DataFrame):
        logger.info("Training Anomaly Detection Model...")

        X = self.prepare_features(df, is_training=True)

        self.model = IsolationForest(
            n_estimators=100,
            contamination=self.contamination,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X)

        logger.info("Anomaly Detection Model trained successfully!")

        return self

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained yet!")

        X = self.prepare_features(df, is_training=False)

        predictions = self.model.predict(X)

        scores = self.model.score_samples(X)

        return predictions, scores

    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        predictions, scores = self.predict(df)

        df['is_anomaly'] = predictions == -1
        df['anomaly_score'] = -scores

        df['anomaly_type'] = 'Normal'
        df.loc[df['is_anomaly'], 'anomaly_type'] = 'Anomaly'

        return df

    def save_model(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_cols': self.feature_cols,
                'contamination': self.contamination
            }, f)
        logger.info(f"Anomaly model saved to {path}")

    def load_model(self, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_cols = data['feature_cols']
            self.contamination = data['contamination']
        logger.info(f"Anomaly model loaded from {path}")


def train_anomaly_model(sales_path: str, supplier_path: str = None):
    logger.info("Loading sales data for anomaly detection...")

    sales_df = pd.read_csv(sales_path)
    logger.info(f"Loaded {len(sales_df)} sales records")

    detector = AnomalyDetector(contamination=0.05)
    detector.train(sales_df)

    result = detector.detect_anomalies(sales_df.head(10000))

    anomaly_count = result['is_anomaly'].sum()
    logger.info(f"Detected {anomaly_count} anomalies in sample of {len(result)} records")

    Path("models/saved").mkdir(exist_ok=True, parents=True)
    detector.save_model("models/saved/anomaly_model.pkl")

    print("\n" + "=" * 60)
    print("Anomaly Detection Complete")
    print("=" * 60)
    print(f"Total records analyzed: {len(result)}")
    print(f"Anomalies detected: {anomaly_count} ({anomaly_count/len(result)*100:.2f}%)")
    print(f"\nAnomaly Score Distribution:")
    print(result[result['is_anomaly']][['store', 'item', 'anomaly_score']].head(10))

    return detector


if __name__ == "__main__":
    train_anomaly_model("data/raw/train.csv")