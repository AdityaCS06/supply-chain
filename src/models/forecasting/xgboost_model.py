#!/usr/bin/env python
"""XGBoost Model for Demand Forecasting"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.logger import logger


class XGBoostForecaster:
    def __init__(self, params: dict = None):
        if params is None:
            params = {
                'n_estimators': 500,
                'max_depth': 6,
                'learning_rate': 0.05,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'min_child_weight': 3,
                'reg_alpha': 0.1,
                'reg_lambda': 1.0,
                'random_state': 42,
                'n_jobs': -1,
                'objective': 'reg:squarederror'
            }

        self.params = params
        self.model = None
        self.feature_names = []

    def calculate_mape(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        mask = y_true != 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    def calculate_wape(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100

    def prepare_data(self, df: pd.DataFrame, target_col: str = 'sales'):
        exclude_cols = ['date', target_col, 'store', 'item']
        feature_cols = [col for col in df.columns if col not in exclude_cols and not df[col].dtype == 'object']

        self.feature_names = feature_cols

        X = df[feature_cols].values
        y = df[target_col].values

        return X, y

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        logger.info(f"Training XGBoost model with {X_train.shape[0]} samples...")

        self.model = xgb.XGBRegressor(**self.params)
        self.model.fit(X_train, y_train, verbose=50)

        logger.info("XGBoost training complete!")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained yet!")
        return self.model.predict(X)

    def evaluate(self, X: np.ndarray, y_true: np.ndarray) -> dict:
        y_pred = self.predict(X)

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = self.calculate_mape(y_true, y_pred)
        wape = self.calculate_wape(y_true, y_pred)

        metrics = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'WAPE': wape
        }

        logger.info(f"XGBoost Evaluation: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%, WAPE={wape:.2f}%")

        return metrics

    def get_feature_importance(self) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("Model not trained yet!")

        importance = self.model.feature_importances_
        df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)

        return df

    def save_model(self, path: str):
        self.model.save_model(path)
        logger.info(f"XGBoost model saved to {path}")

        with open(f"{path}.params", 'wb') as f:
            pickle.dump(self.params, f)

    def load_model(self, path: str):
        self.model = xgb.XGBRegressor()
        self.model.load_model(path)

        with open(f"{path}.params", 'rb') as f:
            self.params = pickle.load(f)

        logger.info(f"XGBoost model loaded from {path}")


def train_xgboost_model(train_path: str, test_path: str = None):
    logger.info("Loading training data...")

    train_df = pd.read_csv(train_path)
    train_df = train_df.dropna()

    logger.info(f"Train shape: {train_df.shape}")

    forecaster = XGBoostForecaster()

    X_train, y_train = forecaster.prepare_data(train_df)

    logger.info(f"Features: {len(forecaster.feature_names)}")

    forecaster.train(X_train, y_train)

    importance = forecaster.get_feature_importance()
    logger.info("Top 10 features:")
    logger.info(importance.head(10).to_string())

    if test_path:
        logger.info("Evaluating on test data...")
        test_df = pd.read_csv(test_path)
        test_df = test_df.dropna()

        X_test, y_test = forecaster.prepare_data(test_df)
        metrics = forecaster.evaluate(X_test, y_test)
        logger.info(f"Test Metrics: {metrics}")

    Path("models/saved").mkdir(exist_ok=True, parents=True)
    forecaster.save_model("models/saved/xgboost_model.json")

    return forecaster


if __name__ == "__main__":
    print("=" * 60)
    print("XGBoost Demand Forecasting Model")
    print("=" * 60)

    model = train_xgboost_model("data/processed/train_processed.csv", "data/processed/test_processed.csv")

    print("\nModel training complete!")
    print("Saved to: models/saved/xgboost_model.json")