
import joblib, pandas as pd, numpy as np
from src.utils import load_data, add_features

df = add_features(load_data())
bundle = joblib.load("models/energy_model.joblib")
model, features = bundle["model"], bundle["features"]

df["expected_energy_kwh"] = model.predict(df[features])
df["deviation_pct"] = (df["total_energy_kwh"]-df["expected_energy_kwh"]) / df["expected_energy_kwh"] * 100
df["energy_anomaly"] = df["deviation_pct"] > 12

df.to_csv("data/scored_factory_data.csv", index=False)
print("Anomalies:", int(df["energy_anomaly"].sum()))
