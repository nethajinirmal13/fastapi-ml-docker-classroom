"""Run after: python train_model.py ; pytest -q"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "Docker" in r.json()["message"]


def test_model_info():
    r = client.get("/model-info")
    assert r.status_code == 200
    assert r.json()["model"] == "LinearRegression"


def test_prediction_post():
    r = client.post("/predict", json={
        "distance_km": 7, "traffic": "high",
        "raining": True, "orders_ahead": 3,
    })
    assert r.status_code == 200
    assert r.json()["estimated_minutes"] > 0


def test_prediction_get():
    r = client.get("/predict-demo?distance_km=5&traffic=medium&raining=false&orders_ahead=2")
    assert r.status_code == 200


def test_negative_distance():
    assert client.post("/predict", json={
        "distance_km": -1, "traffic": "low", "raining": False, "orders_ahead": 0,
    }).status_code == 422


def test_business_rule():
    assert client.post("/predict", json={
        "distance_km": 25, "traffic": "low", "raining": False, "orders_ahead": 0,
    }).status_code == 400


def test_invalid_traffic():
    assert client.post("/predict", json={
        "distance_km": 3, "traffic": "extreme", "raining": False, "orders_ahead": 0,
    }).status_code == 422
