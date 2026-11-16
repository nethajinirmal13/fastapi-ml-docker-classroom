"""Train and package a tiny classroom delivery-time regression model.
Synthetic data: not suitable for production predictions.
"""
import random
from pathlib import Path

import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

rng = random.Random(42)
traffic_names = ["low", "medium", "high"]
traffic_lookup = {"low": 0, "medium": 1, "high": 2}

X, y = [], []
for _ in range(400):
    distance = round(rng.uniform(1, 20), 2)
    traffic_name = rng.choice(traffic_names)
    raining = rng.choice([False, True])
    orders_ahead = rng.randint(0, 8)

    X.append([distance, traffic_lookup[traffic_name], int(raining), orders_ahead])
    # Classroom simulation: longer routes, congestion, and rain add minutes.
    minutes = (
        8 + 3.5 * distance + 6 * traffic_lookup[traffic_name]
        + 5 * int(raining) + 2 * orders_ahead + rng.uniform(-2, 2)
    )
    y.append(minutes)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LinearRegression().fit(X_train, y_train)
mae = mean_absolute_error(y_test, model.predict(X_test))

artifact = {
    "model": model,
    "feature_names": ["distance_km", "traffic_score", "raining", "orders_ahead"],
    "traffic_lookup": traffic_lookup,
    "mae_minutes": round(float(mae), 2),
    "training_samples": len(X_train),
    "test_samples": len(X_test),
    "data_source": "Synthetic classroom data",
}
output = Path(__file__).with_name("model.joblib")
joblib.dump(artifact, output)
print(f"Model trained; saved {output.name}; held-out MAE = {mae:.2f} min")
