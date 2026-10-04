# FoodPulse AI — Smart Energy & Process Optimization for Food-Processing SMEs

## What this prototype demonstrates
FoodPulse monitors representative food-processing energy/process variables, establishes an expected energy baseline, detects abnormal consumption, surfaces equipment/process issues, and demonstrates constrained optimization while holding production and quality constant.

### Submission headline
**12.8% simulated reduction in specific energy consumption (SEC), from 2.50 to 2.18 kWh/kg, while production remains 5,000 kg/day and simulated quality remains 96%.**

This is a representative simulation, NOT a measured factory result.

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Optional ML scripts
```bash
python src/train_energy_model.py
python src/score_anomalies.py
python src/optimization.py
```

## Project structure
- `app.py` — Streamlit dashboard/demo
- `data/food_factory_data.csv` — synthetic 30-day, 15-minute factory dataset
- `src/train_energy_model.py` — baseline energy model
- `src/score_anomalies.py` — anomaly scoring
- `src/optimization.py` — quantified optimization scenario
- `docs/solution_writeup.pdf` — submission-ready write-up
- `docs/architecture.png` — architecture diagram
- `docs/data_model.png` — data model
- `docs/deployment_plan.png` — deployment/business model schematic

## Important assumptions
- Representative food-processing SME, not a real customer site.
- Electricity tariff used for the prototype: ₹8/kWh; replace with actual DISCOM tariff during a pilot.
- Illustrative grid factor: 0.70 kgCO2e/kWh; replace with the current approved/project-specific factor for formal reporting.
- Quality constraint in simulation: >=95%.
- Production target: 5,000 kg/day.
- Baseline SEC: 2.50 kWh/kg.
- Optimized SEC: 2.18 kWh/kg.

## India SME fit
BEE currently includes food processing in its MSME energy-efficiency work and ADEETIE support. The product is therefore designed as a retrofit-first, low-capex monitoring and optimization layer rather than requiring replacement of existing machinery.
