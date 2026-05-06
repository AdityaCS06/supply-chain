#!/usr/bin/env python
"""Exploratory Data Analysis for Supply Chain ML"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.data_loader import DataLoader
from src.logger import logger


class EDA:
    def __init__(self, data_loader: DataLoader = None):
        self.loader = data_loader or DataLoader()
        self.df = None
        self.output_dir = Path("notebooks")

    def load_data(self):
        logger.info("Loading data for EDA...")
        self.df = self.loader.load_train_data()
        return self

    def basic_info(self) -> Dict[str, Any]:
        info = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "memory_usage_mb": self.df.memory_usage(deep=True).sum() / 1024 / 1024,
            "null_counts": self.df.isnull().sum().to_dict()
        }

        logger.info(f"Dataset shape: {info['shape']}")
        logger.info(f"Columns: {info['columns']}")
        logger.info(f"Missing values: {info['null_counts']}")

        return info

    def statistical_summary(self) -> pd.DataFrame:
        summary = self.df.describe()
        print("\n" + "=" * 60)
        print("Statistical Summary")
        print("=" * 60)
        print(summary)

        return summary

    def sales_by_store(self) -> pd.DataFrame:
        store_sales = self.df.groupby('store')['sales'].agg(['sum', 'mean', 'std']).round(2)
        store_sales.columns = ['total_sales', 'avg_sales', 'std_sales']
        store_sales = store_sales.sort_values('total_sales', ascending=False)

        print("\n" + "=" * 60)
        print("Sales by Store")
        print("=" * 60)
        print(store_sales)

        return store_sales

    def sales_by_item(self) -> pd.DataFrame:
        item_sales = self.df.groupby('item')['sales'].agg(['sum', 'mean', 'std']).round(2)
        item_sales.columns = ['total_sales', 'avg_sales', 'std_sales']
        item_sales = item_sales.sort_values('total_sales', ascending=False)

        print("\n" + "=" * 60)
        print("Top 10 Items by Sales")
        print("=" * 60)
        print(item_sales.head(10))

        return item_sales

    def time_series_analysis(self) -> Dict[str, Any]:
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['day_of_week'] = self.df['date'].dt.dayofweek

        yearly_sales = self.df.groupby('year')['sales'].sum()
        monthly_sales = self.df.groupby('month')['sales'].mean()
        dow_sales = self.df.groupby('day_of_week')['sales'].mean()

        print("\n" + "=" * 60)
        print("Yearly Sales")
        print("=" * 60)
        print(yearly_sales)

        print("\n" + "=" * 60)
        print("Monthly Average Sales")
        print("=" * 60)
        print(monthly_sales)

        print("\n" + "=" * 60)
        print("Day of Week Average Sales (0=Mon, 6=Sun)")
        print("=" * 60)
        print(dow_sales)

        return {
            "yearly_sales": yearly_sales.to_dict(),
            "monthly_sales": monthly_sales.to_dict(),
            "dow_sales": dow_sales.to_dict()
        }

    def distribution_analysis(self) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("Sales Distribution")
        print("=" * 60)

        stats = {
            "min": self.df['sales'].min(),
            "max": self.df['sales'].max(),
            "mean": self.df['sales'].mean(),
            "median": self.df['sales'].median(),
            "std": self.df['sales'].std(),
            "skewness": self.df['sales'].skew(),
            "kurtosis": self.df['sales'].kurtosis()
        }

        for key, value in stats.items():
            print(f"{key}: {value:.2f}")

        return stats

    def run_full_eda(self):
        print("=" * 60)
        print("EXPLORATORY DATA ANALYSIS")
        print("=" * 60)

        self.load_data()
        self.basic_info()
        self.statistical_summary()
        self.sales_by_store()
        self.sales_by_item()
        self.time_series_analysis()
        self.distribution_analysis()

        print("\n" + "=" * 60)
        print("EDA Complete!")
        print("=" * 60)


if __name__ == "__main__":
    eda = EDA()
    eda.run_full_eda()