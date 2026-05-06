#!/usr/bin/env python
"""Risk Scoring Model for Supplier Risk Assessment"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.logger import logger


class RiskScorer:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_cols = []

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        categorical_cols = ['country', 'region', 'financial_stability']
        for col in categorical_cols:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
            self.encoders[col] = le

        self.feature_cols = [
            'on_time_delivery_rate', 'defect_rate', 'quality_rating',
            'credit_score', 'lead_time_days', 'min_order_quantity',
            'year_founded', 'employee_count',
            'country_encoded', 'region_encoded', 'financial_stability_encoded'
        ]

        return df

    def train(self, df: pd.DataFrame):
        logger.info("Training Risk Scoring Model...")

        df = self.prepare_features(df)

        X = df[self.feature_cols].values
        y_risk = df['overall_risk_score'].values

        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X, y_risk)

        logger.info("Risk Scoring Model trained successfully!")

        importance = pd.DataFrame({
            'feature': self.feature_cols,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        logger.info("Feature Importance:")
        logger.info(importance.to_string())

        return self

    def calculate_rule_based_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df['rule_delivery_risk'] = 100 - df['on_time_delivery_rate']
        df['rule_quality_risk'] = df['defect_rate'] * 10

        financial_risk_map = {'Low': 80, 'Medium': 50, 'High': 20}
        df['rule_financial_risk'] = df['financial_stability'].map(financial_risk_map)

        geo_risk_map = {'USA': 20, 'Germany': 20, 'UK': 20, 'Japan': 30,
                       'France': 30, 'Korea': 40, 'India': 60, 'China': 80,
                       'Brazil': 60, 'Mexico': 50}
        df['rule_geographic_risk'] = df['country'].map(geo_risk_map).fillna(40)

        df['rule_overall_risk'] = (
            df['rule_delivery_risk'] * 0.3 +
            df['rule_quality_risk'] * 0.25 +
            df['rule_financial_risk'] * 0.25 +
            df['rule_geographic_risk'] * 0.2
        )

        return df

    def get_risk_level(self, risk_score: float) -> str:
        if risk_score < 25:
            return 'Low'
        elif risk_score < 50:
            return 'Medium'
        elif risk_score < 75:
            return 'High'
        else:
            return 'Critical'

    def assess_suppliers(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df = self.calculate_rule_based_risk(df)

        if self.model is not None:
            df = self.prepare_features(df)
            ml_risk = self.model.predict(df[self.feature_cols].values)
            df['ml_risk_score'] = ml_risk
            df['overall_risk_score'] = df['rule_overall_risk'] * 0.7 + ml_risk * 0.3
        else:
            df['overall_risk_score'] = df['rule_overall_risk']

        df['risk_level'] = df['overall_risk_score'].apply(self.get_risk_level)

        return df

    def save_model(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'encoders': self.encoders,
                'feature_cols': self.feature_cols
            }, f)
        logger.info(f"Risk model saved to {path}")

    def load_model(self, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.encoders = data['encoders']
            self.feature_cols = data['feature_cols']
        logger.info(f"Risk model loaded from {path}")


def train_risk_model(supplier_path: str):
    logger.info("Loading supplier data...")

    df = pd.read_csv(supplier_path)

    logger.info(f"Loaded {len(df)} suppliers")

    scorer = RiskScorer()
    scorer.train(df)

    Path("models/saved").mkdir(exist_ok=True, parents=True)
    scorer.save_model("models/saved/risk_model.pkl")

    print("\n" + "=" * 60)
    print("Risk Scoring Model Complete")
    print("=" * 60)

    result = scorer.assess_suppliers(df)

    print("\nRisk Assessment Results:")
    print(result[['supplier_id', 'country', 'overall_risk_score', 'risk_level']].head(10))

    return scorer


if __name__ == "__main__":
    train_risk_model("data/raw/suppliers.csv")