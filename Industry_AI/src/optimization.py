
import pandas as pd

BASELINE_SEC = 2.50
OPTIMIZED_SEC = 2.18
PRODUCTION_KG_DAY = 5000
TARIFF_RS_PER_KWH = 8.0

baseline_energy = BASELINE_SEC * PRODUCTION_KG_DAY
optimized_energy = OPTIMIZED_SEC * PRODUCTION_KG_DAY
saving_kwh = baseline_energy - optimized_energy
saving_rs_day = saving_kwh * TARIFF_RS_PER_KWH
reduction_pct = saving_kwh / baseline_energy * 100

result = pd.DataFrame([{
    "production_kg_day": PRODUCTION_KG_DAY,
    "baseline_energy_kwh_day": baseline_energy,
    "optimized_energy_kwh_day": optimized_energy,
    "baseline_sec_kwh_per_kg": BASELINE_SEC,
    "optimized_sec_kwh_per_kg": OPTIMIZED_SEC,
    "energy_reduction_pct": reduction_pct,
    "energy_saved_kwh_day": saving_kwh,
    "indicative_saving_rs_day": saving_rs_day,
    "quality_baseline_pct": 96.0,
    "quality_optimized_pct": 96.0
}])
result.to_csv("data/optimization_result.csv", index=False)
print(result.to_string(index=False))
