#!/usr/bin/env python
"""FastAPI Application for Supply Chain ML"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys
import xgboost as xgb

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.logger import logger
from src.config import config

app = FastAPI(
    title="Supply Chain ML API",
    description="API for Demand Forecasting, Risk Assessment, and Inventory Optimization",
    version="1.0.0"
)

xgb_model = None
risk_scorer = None


class ForecastRequest(BaseModel):
    product_ids: List[int]
    store_ids: List[int]
    horizon_days: int = 30
    confidence_level: float = 0.95


class RiskRequest(BaseModel):
    supplier_ids: List[str]
    assessment_date: Optional[str] = None


class InventoryRequest(BaseModel):
    product_ids: List[int]
    target_service_level: float = 0.95
    budget_constraint: Optional[float] = None


@app.on_event("startup")
async def startup_event():
    global xgb_model, risk_scorer

    logger.info("Loading models...")

    try:
        xgb_model = xgb.XGBRegressor()
        xgb_model.load_model("models/saved/xgboost_model.json")
        logger.info("XGBoost model loaded")
    except Exception as e:
        logger.warning(f"XGBoost model not loaded: {e}")

    try:
        import pickle
        with open("models/saved/risk_model.pkl", 'rb') as f:
            risk_scorer = pickle.load(f)
        logger.info("Risk model loaded")
    except Exception as e:
        logger.warning(f"Risk model not loaded: {e}")

    logger.info("API startup complete")


@app.get("/")
async def root():
    return {
        "message": "Supply Chain ML API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/forecast",
            "/risk/assessment",
            "/inventory/optimize"
        ]
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": {
            "xgboost": xgb_model is not None,
            "risk": risk_scorer is not None
        }
    }


@app.post("/forecast")
async def forecast_demand(request: ForecastRequest):
    if xgb_model is None:
        raise HTTPException(status_code=503, detail="XGBoost model not loaded")

    try:
        df = pd.read_csv("data/features/train_features.csv")
        df = df.dropna()

        exclude_cols = ['date', 'sales', 'store', 'item']
        feature_cols = [col for col in df.columns if col not in exclude_cols]

        predictions = []
        for store in request.store_ids:
            for product in request.product_ids:
                product_data = df[(df['store'] == store) & (df['item'] == product)]
                if len(product_data) > 0:
                    X = product_data[feature_cols].iloc[-1:].values
                    pred = xgb_model.predict(X)[0]
                    predictions.append({
                        "store_id": store,
                        "product_id": product,
                        "predicted_demand": round(pred, 2),
                        "horizon_days": request.horizon_days
                    })

        return {
            "forecasts": predictions,
            "model_used": "xgboost",
            "created_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/risk/assessment")
async def assess_risk(request: RiskRequest):
    try:
        df = pd.read_csv("data/raw/suppliers.csv")

        result = risk_scorer.assess_suppliers(df)

        filtered = result[result['supplier_id'].isin(request.supplier_ids)]

        risk_scores = []
        for _, row in filtered.iterrows():
            risk_scores.append({
                "supplier_id": row['supplier_id'],
                "country": row['country'],
                "overall_risk_score": round(row['overall_risk_score'], 2),
                "delivery_risk": round(row['delivery_risk'], 2),
                "quality_risk": round(row['quality_risk'], 2),
                "financial_risk": round(row['financial_risk'], 2),
                "geographic_risk": round(row['geographic_risk'], 2),
                "risk_level": row['risk_level']
            })

        return {
            "risk_scores": risk_scores,
            "created_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Risk assessment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inventory/optimize")
async def optimize_inventory(request: InventoryRequest):
    try:
        from src.models.inventory.optimizer import InventoryOptimizer

        df = pd.read_csv("data/raw/train.csv")

        optimizer = InventoryOptimizer(service_level=request.target_service_level)

        results = []
        for product_id in request.product_ids:
            result = optimizer.optimize_inventory(df, product_id)
            results.append(result)

        return {
            "recommendations": results,
            "created_at": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Inventory optimization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)