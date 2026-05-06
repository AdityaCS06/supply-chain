#!/usr/bin/env python
"""Download Store Item Demand Forecasting dataset from Kaggle"""

import os
import sys
from pathlib import Path
import zipfile
import shutil

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except ImportError:
    print("Error: kaggle package not installed")
    print("Run: pip install kaggle")
    sys.exit(1)


def download_dataset():
    project_root = Path(__file__).parent.parent.parent
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(exist_ok=True, parents=True)

    api = KaggleApi()
    api.authenticate()

    competition = "demand-forecasting-kernels-only"

    print(f"Downloading dataset from Kaggle competition: {competition}")

    api.competition_download_files(competition, path=raw_dir)

    zip_path = raw_dir / f"{competition}.zip"

    if zip_path.exists():
        print(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(raw_dir)

        zip_path.unlink()
        print("Dataset downloaded and extracted successfully!")

        for f in raw_dir.glob("*.csv"):
            print(f"  - {f.name}")
    else:
        print("Error: Download failed")
        sys.exit(1)


if __name__ == "__main__":
    download_dataset()