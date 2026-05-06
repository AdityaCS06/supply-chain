#!/usr/bin/env python
"""Generate synthetic supplier data for Risk Prediction module"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.logger import logger


def generate_supplier_data(n_suppliers: int = 20):
    """Generate synthetic supplier data with risk metrics"""

    logger.info(f"Generating {n_suppliers} supplier records...")

    countries = ['USA', 'China', 'Germany', 'Japan', 'India', 'Brazil', 'Mexico', 'UK', 'France', 'Korea']
    regions = ['North America', 'Asia', 'Europe', 'Latin America']
    financial_stability = ['Low', 'Medium', 'High']

    records = []

    for i in range(1, n_suppliers + 1):
        country = np.random.choice(countries)
        region = 'Asia' if country in ['China', 'Japan', 'Korea', 'India'] else \
                 'Europe' if country in ['Germany', 'UK', 'France'] else \
                 'North America' if country in ['USA', 'Mexico'] else 'Latin America'

        on_time_rate = np.random.uniform(70, 99)
        defect_rate = np.random.uniform(0.5, 8)
        quality_rating = np.random.uniform(3.0, 5.0)
        credit_score = np.random.randint(40, 100)
        financial = np.random.choice(financial_stability, p=[0.2, 0.5, 0.3])

        delivery_risk = max(0, 100 - on_time_rate)
        quality_risk = defect_rate * 10
        financial_risk = 100 - credit_score if financial == 'Low' else \
                         50 - credit_score / 2 if financial == 'Medium' else 20

        geographic_risk = 80 if country in ['China'] else \
                          60 if country in ['India', 'Brazil'] else \
                          40 if country in ['Mexico'] else 20

        overall_risk = (delivery_risk * 0.3 + quality_risk * 0.25 +
                       financial_risk * 0.25 + geographic_risk * 0.2)

        if overall_risk < 25:
            risk_level = 'Low'
        elif overall_risk < 50:
            risk_level = 'Medium'
        elif overall_risk < 75:
            risk_level = 'High'
        else:
            risk_level = 'Critical'

        records.append({
            'supplier_id': f'SUP{i:03d}',
            'supplier_name': f'Supplier Company {i}',
            'country': country,
            'region': region,
            'on_time_delivery_rate': round(on_time_rate, 2),
            'defect_rate': round(defect_rate, 2),
            'quality_rating': round(quality_rating, 2),
            'credit_score': credit_score,
            'financial_stability': financial,
            'lead_time_days': np.random.randint(7, 60),
            'min_order_quantity': np.random.randint(50, 500),
            'year_founded': np.random.randint(1990, 2020),
            'employee_count': np.random.randint(50, 5000),
            'delivery_risk': round(delivery_risk, 2),
            'quality_risk': round(quality_risk, 2),
            'financial_risk': round(financial_risk, 2),
            'geographic_risk': round(geographic_risk, 2),
            'overall_risk_score': round(overall_risk, 2),
            'risk_level': risk_level
        })

    df = pd.DataFrame(records)

    output_path = Path("data/raw") / "suppliers.csv"
    df.to_csv(output_path, index=False)

    logger.info(f"Generated {len(df)} suppliers")
    logger.info(f"Saved to: {output_path}")

    print("\n" + "=" * 60)
    print("Supplier Data Summary")
    print("=" * 60)
    print(f"Total suppliers: {len(df)}")
    print(f"\nRisk Level Distribution:")
    print(df['risk_level'].value_counts())
    print(f"\nAverage Risk Scores:")
    print(f"  Delivery Risk: {df['delivery_risk'].mean():.2f}")
    print(f"  Quality Risk: {df['quality_risk'].mean():.2f}")
    print(f"  Financial Risk: {df['financial_risk'].mean():.2f}")
    print(f"  Geographic Risk: {df['geographic_risk'].mean():.2f}")
    print(f"  Overall Risk: {df['overall_risk_score'].mean():.2f}")

    return df


if __name__ == "__main__":
    generate_supplier_data(20)