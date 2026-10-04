
import pandas as pd
import numpy as np

def load_data(path="data/food_factory_data.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df

def add_features(df):
    x = df.copy()
    x["hour"] = x["timestamp"].dt.hour + x["timestamp"].dt.minute/60
    x["day_of_week"] = x["timestamp"].dt.dayofweek
    x["is_active"] = (x["production_kg"] > 0).astype(int)
    x["energy_intensity"] = x["total_energy_kwh"] / x["production_kg"].replace(0, np.nan)
    x["energy_intensity"] = x["energy_intensity"].replace([np.inf,-np.inf], np.nan).fillna(0)
    return x
