# Supply Chain Management with Machine Learning

MTech Thesis Project

## Project Overview

An intelligent supply chain management system leveraging machine learning to address critical supply chain challenges:

- **Demand Forecasting** — Predict future product demand with high precision using ensemble ML models (XGBoost + LSTM hybrid approach)
- **Risk Prediction** — Identify potential supply chain disruptions and supplier risks through predictive analytics
- **Inventory Optimization** — Calculate optimal stock levels, reorder points, and replenishment quantities using mathematical optimization

## Dataset

**Store Item Demand Forecasting** (Kaggle Dataset)

- 5 years of daily sales data (2013-2017)
- 10 stores, 50 items per store
- ~913,000 total records
- Objective: Forecast 3 months of daily sales

> **Note**: Place `train.csv` and `test.csv` in `data/raw/` directory before running the pipeline.

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| ML Models | XGBoost, LightGBM, scikit-learn |
| Deep Learning | TensorFlow, Keras (LSTM) |
| API | FastAPI |
| Dashboard | Streamlit |
| Optimization | SciPy, PuLP |
| Logging | Custom logger module |

## Project Structure

```
supply_chain/
├── config/                  # Configuration files and settings
├── data/
│   ├── raw/                 # Raw data (train.csv, test.csv from Kaggle)
│   ├── processed/           # Transformed and processed datasets
│   └── features/            # Feature engineered datasets
├── src/
│   ├── data/                # Data loading, generation, and EDA
│   ├── features/            # Feature engineering and transformations
│   ├── models/
│   │   ├── forecasting/     # XGBoost, LSTM, Ensemble models
│   │   ├── risk/            # Risk scoring and anomaly detection
│   │   └── inventory/       # Optimization algorithms
│   ├── api/                 # FastAPI REST endpoints
│   ├── dashboard/           # Streamlit web dashboard
│   ├── logger.py           # Custom logging configuration
│   └── utils/               # Utility functions
├── models/                  # Saved trained models
├── notebooks/               # Jupyter notebooks for exploration
├── tests/                   # Unit and integration tests
├── docs/                    # Additional documentation
├── run_pipeline.py          # Main pipeline execution script
└── requirements.txt         # Python dependencies
```

## Prerequisites

- Python 3.10 or higher
- pip or conda package manager
- Kaggle account (for dataset download)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd supply-chain
```

### 2. Create Virtual Environment

**Using venv (recommended):**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

**Using conda:**

```bash
conda create -n supply_chain python=3.10
conda activate supply_chain
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Dataset

1. Visit [Store Item Demand Forecasting Challenge](https://www.kaggle.com/competitions/demand-forecasting-kernels) on Kaggle
2. Download `train.csv` and `test.csv`
3. Place files in `data/raw/` directory

## Usage

### Running the Data Pipeline

Execute all data processing steps in sequence:

```bash
python run_pipeline.py
```

This will:
- Generate supplier data (`data/raw/suppliers.csv`)
- Create engineered features (`data/features/train_features.csv`)
- Process transformations (`data/processed/train_processed.csv`, `test_processed.csv`)
- Generate inventory optimization results (`data/processed/inventory_optimization.csv`)

### Running Individual Components

**Data Generation:**
```bash
python src/data/supplier_generator.py
```

**Feature Engineering:**
```bash
python src/features/feature_engineering.py
```

**Data Transformations:**
```bash
python src/features/transformations.py
```

**Inventory Optimization:**
```bash
python src/models/inventory/optimizer.py
```

### Running the Dashboard

Launch the Streamlit web interface:

```bash
streamlit run src/dashboard/home.py
```

The dashboard will open at `http://localhost:8501`

### Running the FastAPI Server

Launch the FastAPI REST API server:

```bash
uvicorn src.api.main:app --reload
```

Or alternatively:

```bash
fastapi dev src/api/main.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Using Data in Your Code

```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load data
from src.data.data_loader import load_data

train_df = load_data('train')
test_df = load_data('test')
```

## Running EDA (Exploratory Data Analysis)

```bash
python src/data/eda.py
```

## Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1: Project Setup | ✅ Complete | Environment, dependencies, structure |
| Phase 2: Data Pipeline | ✅ Complete | Data loading, generation, transformations |
| Phase 3: Forecasting | ✅ Complete | XGBoost, LSTM, Ensemble models implemented |
| Phase 4: Risk Prediction | ✅ Complete | Risk scoring, anomaly detection models |
| Phase 5: Inventory Optimization | ✅ Complete | Optimization algorithms implemented |
| Phase 6: API & Dashboard | ✅ Complete | FastAPI endpoints, Streamlit UI complete |
| Phase 7: Testing & Documentation | 🔄 In Progress | Unit tests, final documentation |

## Configuration

- Modify `config/` files to adjust model parameters
- Update `src/logger.py` to configure logging levels
- Edit `requirements.txt` to add/remove dependencies

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_data_loader.py

# Run with coverage
pytest --cov=src tests/
```

## Logging

The project uses a custom logging module (`src/logger.py`) configured to:
- Log to both console and file
- Capture INFO, WARNING, and ERROR levels
- Store logs in `logs/` directory

## Documentation

Additional documentation available in `docs/`:
- `test.md` — Comprehensive project documentation
- `implementation.md` — Implementation plan and progress tracking

## Troubleshooting

**Module Not Found Error:**
Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

**Dataset Not Found:**
Verify `train.csv` and `test.csv` exist in `data/raw/`

**Port Already in Use:**
Dashboard uses port 8501 by default. To change:
```bash
streamlit run src/dashboard/home.py --server.port 8502
```

## License

This project is for academic purposes as part of MTech Thesis.

---

**Author:** Aditya Sharma  
**Project:** MTech Thesis — Supply Chain Management with Machine Learning  
**Version:** 1.0.0  
**Last Updated:** May 2026