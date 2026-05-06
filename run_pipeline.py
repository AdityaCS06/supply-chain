#!/usr/bin/env python
"""
Data Pipeline Script
Generates all processed CSV files from raw data with a single command.

Usage:
    python run_pipeline.py

Requirements:
    - data/raw/train.csv (from Kaggle)
    - data/raw/test.csv (from Kaggle)
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.logger import logger


def run_step(name: str, command: list) -> bool:
    """Run a pipeline step and return success status"""
    try:
        print(f"Running: {name}...")
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  [OK] {name} completed")
            return True
        else:
            print(f"  [FAIL] {name}")
            print(f"  Error: {result.stderr[:200] if result.stderr else 'Unknown'}")
            return False
    except Exception as e:
        print(f"  [ERROR] {name}: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("SUPPLY CHAIN ML - DATA PIPELINE")
    print("=" * 60)
    print()

    steps = [
        ("Generate Suppliers", ["python", "src/data/supplier_generator.py"]),
        ("Feature Engineering", ["python", "src/features/feature_engineering.py"]),
        ("Data Transformations", ["python", "src/features/transformations.py"]),
        ("Inventory Optimization", ["python", "src/models/inventory/optimizer.py"]),
    ]

    results = {}
    for name, command in steps:
        results[name] = run_step(name, command)
        print()

    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    for name, success in results.items():
        status = "[OK]" if success else "[FAIL]"
        print(f"  {status} - {name}")

    print()
    print("Generated files:")
    print("  - data/raw/suppliers.csv")
    print("  - data/features/train_features.csv")
    print("  - data/processed/train_processed.csv")
    print("  - data/processed/test_processed.csv")
    print("  - data/processed/inventory_optimization.csv")
    print()
    print("Now run: streamlit run src/dashboard/home.py")
    print("=" * 60)


if __name__ == "__main__":
    main()