
import os, joblib, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from src.utils import load_data, add_features

DATA = "data/food_factory_data.csv"
OUT = "models/energy_model.joblib"

df = add_features(load_data(DATA))
features = ["production_kg","ambient_temp_c","humidity_pct","oven_temp_c",
            "compressor_pressure_bar","cold_room_temp_c","motor_load_pct","hour","day_of_week"]
target = "total_energy_kwh"

# Train on normal historical data only to establish a baseline
train = df[(df["anomaly_label"]=="normal") & (df["timestamp"] < "2026-09-19")].copy()
X, y = train[features], train[target]
model = RandomForestRegressor(n_estimators=180, random_state=42, min_samples_leaf=4, n_jobs=-1)
model.fit(X,y)
pred = model.predict(X)

print("Training MAE:", round(mean_absolute_error(y,pred),4))
print("Training R2 :", round(r2_score(y,pred),4))
joblib.dump({"model":model,"features":features}, OUT)
print("Saved:", OUT)
