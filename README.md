# Supply Chain Management with Machine Learning

MTech Thesis Project

## Project Overview

An intelligent supply chain management system using machine learning that addresses:
- **Demand Forecasting** - Predict future product demand with high precision using ensemble ML models (XGBoost + LSTM)
- **Risk Prediction** - Identify potential supply chain disruptions and supplier risks
- **Inventory Optimization** - Calculate optimal stock levels, reorder points, and replenishment quantities

## Dataset

**Store Item Demand Forecasting** (Kaggle)
- 5 years of daily sales data (2013-2017)
- 10 stores, 50 items
- ~913,000 rows
- Goal: Forecast 3 months of sales

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| ML Models | XGBoost, LightGBM, scikit-learn |
| Deep Learning | TensorFlow, Keras (LSTM) |
| API | FastAPI |
| Dashboard | Streamlit |
| Optimization | SciPy, PuLP |

## Project Structure

```
supply_chain_ml/
├── config/              # Configuration files
├── data/
│   ├── raw/             # Raw data (train.csv, test.csv)
│   ├── processed/       # Processed data
│   └── features/        # Feature engineered data
├── src/
│   ├── data/            # Data loading and EDA
│   ├── features/        # Feature engineering
│   ├── models/          # ML models
│   │   ├── forecasting/ # XGBoost, LSTM, Ensemble
│   │   ├── risk/        # Risk scoring, anomaly detection
│   │   └── inventory/   # Optimization algorithms
│   ├── api/             # FastAPI endpoints
│   ├── dashboard/       # Streamlit dashboard
│   └── utils/           # Utilities
├── models/              # Saved models
├── notebooks/           # Jupyter notebooks
├── tests/               # Unit tests
└── docs/                # Documentation
```

## Installation

```bash
# Create virtual environment
conda create -n supply_chain python=3.10
conda activate supply_chain

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Data Loading
```python
from src.data.data_loader import load_data

train_df = load_data('train')
test_df = load_data('test')
```

### Run EDA
```python
python src/data/eda.py
```

## Progress

| Phase | Status |
|-------|--------|
| Phase 1: Project Setup | ✅ Complete |
| Phase 2: Data Pipeline | ⏳ Pending |
| Phase 3: Forecasting | ⏳ Pending |
| Phase 4: Risk | ⏳ Pending |
| Phase 5: Inventory | ⏳ Pending |
| Phase 6: API & Dashboard | ⏳ Pending |
| Phase 7: Documentation | ⏳ Pending |

## Documentation

- `test.md` - Full project documentation
- `implementation.md` - Implementation plan and progress

---

*Author: MTech Thesis Student*
*Version: 1.0.0*