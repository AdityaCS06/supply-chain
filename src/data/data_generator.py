#!/usr/bin/env python
"""Generate synthetic Store Item Demand Forecasting dataset"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys


def generate_store_item_demand_data(
    n_stores: int = 10,
    n_items: int = 50,
    start_date: str = "2013-01-01",
    end_date: str = "2017-12-31",
    output_dir: str = "data/raw"
) -> pd.DataFrame:
    """
    Generate synthetic store item demand data similar to Kaggle dataset.

    Columns: date, store, item, sales
    """

    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    stores = list(range(1, n_stores + 1))
    items = list(range(1, n_items + 1))

    print(f"Generating data for {len(stores)} stores x {len(items)} items x {len(dates)} days")

    records = []

    for store in stores:
        for item in items:
            base_demand = np.random.randint(20, 100)
            seasonal_factor = np.random.uniform(0.7, 1.3)

            for date in dates:
                day_of_week = date.dayofweek
                month = date.month
                year = date.year

                demand = base_demand * seasonal_factor

                if day_of_week in [5, 6]:
                    demand *= 1.3

                if month in [11, 12]:
                    demand *= 1.5

                if month in [6, 7, 8]:
                    demand *= 0.8

                if np.random.random() < 0.05:
                    demand *= np.random.uniform(2, 5)

                noise = np.random.normal(0, demand * 0.1)
                sales = max(0, int(demand + noise))

                records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'store': store,
                    'item': item,
                    'sales': sales
                })

    df = pd.DataFrame(records)

    output_path = Path(output_dir) / "train.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df):,} rows")
    print(f"Saved to: {output_path}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Stores: {df['store'].nunique()}, Items: {df['item'].nunique()}")

    return df


def generate_test_data(train_end_date: str = "2017-12-31", n_days: int = 90, output_dir: str = "data/raw") -> pd.DataFrame:
    """Generate test data (dates to forecast)"""

    start_date = pd.to_datetime(train_end_date) + timedelta(days=1)
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')

    test_records = []
    for store in range(1, 11):
        for item in range(1, 51):
            for date in dates:
                test_records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'store': store,
                    'item': item
                })

    df = pd.DataFrame(test_records)

    output_path = Path(output_dir) / "test.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated test data: {len(df):,} rows")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("Store Item Demand Data Generator")
    print("=" * 60)

    output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
    output_dir.mkdir(exist_ok=True, parents=True)

    print("\n[1/2] Generating training data...")
    train_df = generate_store_item_demand_data(output_dir=str(output_dir))

    print("\n[2/2] Generating test data...")
    test_df = generate_test_data(output_dir=str(output_dir))

    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)