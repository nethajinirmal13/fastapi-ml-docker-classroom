"""Classroom FastAPI service for a saved scikit-learn delivery-time model."""
from pathlib import Path
from typing import Literal

import joblib
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Delivery Time ML API in Docker", version="1.0")

# Load the model we trained into our own image. Never load untrusted joblib files.
artifact = joblib.load(Path(__file__).with_name("model.joblib"))
model = artifact["model"]
traffic_lookup = artifact["traffic_lookup"]


class DeliveryInput(BaseModel):
    distance_km: float = Field(gt=0, le=100, description="Delivery distance in kilometres")
    traffic: Literal["low", "medium", "high"]
    raining: bool
    orders_ahead: int = Field(ge=0, le=20)


@app.get("/")
def home():
    return {
        "message": "My FastAPI ML model is running inside Docker!",
        "test_get": "/predict-demo?distance_km=5&traffic=medium&raining=false&orders_ahead=2",
        "test_post": "/docs",
    }


@app.get("/model-info")
def model_info():
    return {
        "model": "LinearRegression",
        "features": artifact["feature_names"],
        "training_samples": artifact["training_samples"],
        "test_samples": artifact["test_samples"],
        "held_out_mae_minutes": artifact["mae_minutes"],
        "data_source": artifact["data_source"],
    }


def make_prediction(data: DeliveryInput):
    # Valid numeric input, but outside the business service area.
    if data.distance_km > 20:
        raise HTTPException(status_code=400, detail="Delivery not available beyond 20 km")

    row = [[
        data.distance_km,
        traffic_lookup[data.traffic],
        int(data.raining),
        data.orders_ahead,
    ]]
    estimate = round(max(float(model.predict(row)[0]), 1.0), 1)
    return {
        "estimated_minutes": estimate,
        "unit": "minutes",
        "note": "Illustrative prediction from synthetic training data",
    }


# Browser-friendly endpoint: query parameters in the URL
@app.get("/predict-demo")
def predict_demo(
    distance_km: float = Query(gt=0, le=100),
    traffic: Literal["low", "medium", "high"] = "medium",
    raining: bool = False,
    orders_ahead: int = Query(default=0, ge=0, le=20),
):
    return make_prediction(DeliveryInput(
        distance_km=distance_km, traffic=traffic,
        raining=raining, orders_ahead=orders_ahead,
    ))


# Real API-style request: POST a JSON body
@app.post("/predict")
def predict(data: DeliveryInput):
    return make_prediction(data)
