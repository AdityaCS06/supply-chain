#!/usr/bin/env python
"""Inventory Optimization Module - EOQ, Safety Stock, Reorder Point"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.logger import logger


class InventoryOptimizer:
    def __init__(self, service_level: float = 0.95):
        self.service_level = service_level
        self.z_score = self._get_z_score(service_level)

    def _get_z_score(self, service_level: float) -> float:
        z_scores = {
            0.90: 1.28,
            0.95: 1.65,
            0.99: 2.33
        }
        return z_scores.get(service_level, 1.65)

    def calculate_eoq(self, annual_demand: float, ordering_cost: float, holding_cost: float) -> float:
        eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
        logger.info(f"EOQ: {eoq:.2f} units")
        return eoq

    def calculate_safety_stock(self, demand_std: float, lead_time: float) -> float:
        safety_stock = self.z_score * demand_std * np.sqrt(lead_time)
        logger.info(f"Safety Stock: {safety_stock:.2f} units")
        return safety_stock

    def calculate_reorder_point(self, avg_daily_demand: float, lead_time: float, safety_stock: float) -> float:
        rop = (avg_daily_demand * lead_time) + safety_stock
        logger.info(f"Reorder Point: {rop:.2f} units")
        return rop

    def calculate_total_cost(self, eoq: float, annual_demand: float, ordering_cost: float, holding_cost: float) -> Dict[str, float]:
        ordering_cost_total = (annual_demand / eoq) * ordering_cost
        holding_cost_total = (eoq / 2) * holding_cost
        total_cost = ordering_cost_total + holding_cost_total

        return {
            'ordering_cost': ordering_cost_total,
            'holding_cost': holding_cost_total,
            'total_cost': total_cost,
            'eoq': eoq
        }

    def optimize_inventory(self, df: pd.DataFrame, product_id: str, unit_cost: float = 10.0,
                          ordering_cost: float = 50.0, holding_cost_rate: float = 0.2) -> Dict:
        product_data = df[df['item'] == product_id] if 'item' in df.columns else df.head(1)

        avg_daily_sales = product_data['sales'].mean()
        annual_demand = avg_daily_sales * 365
        demand_std = product_data['sales'].std()

        lead_time = 7

        holding_cost = unit_cost * holding_cost_rate

        eoq = self.calculate_eoq(annual_demand, ordering_cost, holding_cost)
        safety_stock = self.calculate_safety_stock(demand_std, lead_time)
        rop = self.calculate_reorder_point(avg_daily_sales, lead_time, safety_stock)
        costs = self.calculate_total_cost(eoq, annual_demand, ordering_cost, holding_cost)

        result = {
            'product_id': product_id,
            'avg_daily_demand': round(avg_daily_sales, 2),
            'annual_demand': round(annual_demand, 2),
            'demand_std': round(demand_std, 2),
            'lead_time_days': lead_time,
            'eoq': round(eoq, 2),
            'safety_stock': round(safety_stock, 2),
            'reorder_point': round(rop, 2),
            'ordering_cost_total': round(costs['ordering_cost'], 2),
            'holding_cost_total': round(costs['holding_cost'], 2),
            'total_inventory_cost': round(costs['total_cost'], 2),
            'service_level': self.service_level
        }

        return result

    def optimize_all_products(self, df: pd.DataFrame, unit_cost: float = 10.0,
                             ordering_cost: float = 50.0, holding_cost_rate: float = 0.2) -> pd.DataFrame:
        results = []

        items = df['item'].unique() if 'item' in df.columns else [1]

        logger.info(f"Optimizing inventory for {len(items)} products...")

        for item in items:
            try:
                result = self.optimize_inventory(df, item, unit_cost, ordering_cost, holding_cost_rate)
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to optimize product {item}: {e}")

        return pd.DataFrame(results)


def run_inventory_optimization(sales_path: str):
    logger.info("Loading sales data for inventory optimization...")

    df = pd.read_csv(sales_path)
    logger.info(f"Loaded {len(df)} sales records")

    optimizer = InventoryOptimizer(service_level=0.95)

    print("\n" + "=" * 60)
    print("Inventory Optimization Results")
    print("=" * 60)

    result = optimizer.optimize_all_products(df.head(100000))

    print(f"\nOptimized {len(result)} products:")
    print(result[['product_id', 'eoq', 'safety_stock', 'reorder_point', 'total_inventory_cost']].head(10))

    Path("data/processed").mkdir(exist_ok=True, parents=True)
    result.to_csv("data/processed/inventory_optimization.csv", index=False)
    logger.info("Saved optimization results to data/processed/inventory_optimization.csv")

    return optimizer, result


if __name__ == "__main__":
    run_inventory_optimization("data/raw/train.csv")