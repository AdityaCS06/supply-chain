#!/usr/bin/env python
"""LSTM Model for Demand Forecasting"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
import pickle
from pathlib import Path
import sys
import warnings

warnings.filterwarnings('ignore')
tf.get_logger().setLevel('ERROR')

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.logger import logger


class LSTMForecaster:
    def __init__(self, sequence_length: int = 30, n_features: int = None):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        self.scaler = MinMaxScaler()
        self.feature_cols = []

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

        self.feature_cols = feature_cols
        self.n_features = len(feature_cols)

        X_data = df[feature_cols].values
        y_data = df[target_col].values

        X_scaled = self.scaler.fit_transform(X_data)
        y_scaled = self.scaler.fit_transform(y_data.reshape(-1, 1))

        X, y = [], []
        for i in range(self.sequence_length, len(X_scaled)):
            X.append(X_scaled[i - self.sequence_length:i])
            y.append(y_scaled[i, 0])

        return np.array(X), np.array(y)

    def prepare_predict_data(self, df: pd.DataFrame):
        data = df[self.feature_cols + ['sales']].values
        scaled_data = self.scaler.transform(data)

        X = []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i - self.sequence_length:i])

        return np.array(X)

    def build_model(self):
        logger.info(f"Building LSTM model: {self.sequence_length} timesteps, {self.n_features} features")

        self.model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(1)
        ])

        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )

        logger.info("LSTM model built successfully")
        self.model.summary(print_fn=logger.info)

    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 20, batch_size: int = 64):
        logger.info(f"Training LSTM: {X_train.shape[0]} samples, epochs={epochs}, batch_size={batch_size}")

        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )

        logger.info("LSTM training complete!")
        return history

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not trained yet!")

        predictions = self.model.predict(X, verbose=0)
        predictions_inv = self.scaler.inverse_transform(predictions.reshape(-1, 1))

        return predictions_inv.flatten()

    def evaluate(self, X: np.ndarray, y_true: np.ndarray) -> dict:
        y_pred = self.predict(X)
        y_true_inv = self.scaler.inverse_transform(y_true.reshape(-1, 1)).flatten()

        mae = mean_absolute_error(y_true_inv, y_pred)
        rmse = np.sqrt(np.mean((y_true_inv - y_pred) ** 2))
        mape = self.calculate_mape(y_true_inv, y_pred)
        wape = self.calculate_wape(y_true_inv, y_pred)

        metrics = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'WAPE': wape
        }

        logger.info(f"LSTM Evaluation: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%, WAPE={wape:.2f}%")

        return metrics

    def save_model(self, path: str):
        self.model.save(path)
        logger.info(f"LSTM model saved to {path}")

        with open(f"{path}.scaler", 'wb') as f:
            pickle.dump(self.scaler, f)

        with open(f"{path}.info", 'wb') as f:
            pickle.dump({'sequence_length': self.sequence_length, 'n_features': self.n_features}, f)

    def load_model(self, path: str):
        self.model = keras.models.load_model(path)

        with open(f"{path}.scaler", 'rb') as f:
            self.scaler = pickle.load(f)

        with open(f"{path}.info", 'rb') as f:
            info = pickle.load(f)
            self.sequence_length = info['sequence_length']
            self.n_features = info['n_features']

        logger.info(f"LSTM model loaded from {path}")


def train_lstm_model(train_path: str, test_path: str = None, sequence_length: int = 30, sample_size: int = 50000):
    logger.info("Loading training data for LSTM...")

    train_df = pd.read_csv(train_path)
    train_df = train_df.dropna()

    if len(train_df) > sample_size:
        logger.info(f"Sampling {sample_size} rows for LSTM training (original: {len(train_df)})")
        train_df = train_df.sample(n=sample_size, random_state=42)

    logger.info(f"Train shape: {train_df.shape}")

    forecaster = LSTMForecaster(sequence_length=sequence_length)

    X_train, y_train = forecaster.prepare_data(train_df)

    logger.info(f"LSTM input shape: {X_train.shape}")

    forecaster.build_model()
    forecaster.train(X_train, y_train, epochs=20, batch_size=64)

    if test_path:
        logger.info("Evaluating on test data...")
        test_df = pd.read_csv(test_path)
        test_df = test_df.dropna()

        X_test, y_test = forecaster.prepare_data(test_df)
        metrics = forecaster.evaluate(X_test, y_test)
        logger.info(f"Test Metrics: {metrics}")

    Path("models/saved").mkdir(exist_ok=True, parents=True)
    forecaster.save_model("models/saved/lstm_model.keras")

    return forecaster


if __name__ == "__main__":
    print("=" * 60)
    print("LSTM Demand Forecasting Model")
    print("=" * 60)

    model = train_lstm_model("data/processed/train_processed.csv", "data/processed/test_processed.csv")

    print("\nLSTM model training complete!")
    print("Saved to: models/saved/lstm_model.keras")