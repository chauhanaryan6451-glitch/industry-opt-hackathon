import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="FoodPulse AI", page_icon="⚡", layout="wide")

DATA = Path(__file__).resolve().parent / "data" / "food_factory_data.csv"
df = pd.read_csv(DATA, parse_dates=["timestamp"])

# Constants: clearly marked as prototype assumptions
TARIFF = 8.0
GRID_FACTOR = 0.70  # illustrative kg CO2e/kWh; replace with site/current factor for deployment
BASELINE_SEC = 2.50
OPTIMIZED_SEC = 2.18
TARGET_PRODUCTION = 5000

st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800;}
.sub {font-size: 18px; color: #666;}
.card {padding: 18px; border-radius: 12px; border: 1px solid #ddd; background: #fff;}
.alert {padding: 14px; border-radius: 10px; border: 1px solid #f0b429; background: #fff8e1;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ FoodPulse AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Smart Energy & Process Intelligence for Food-Processing SMEs</div>', unsafe_allow_html=True)
st.divider()

# KPIs based on illustrative optimized scenario
baseline_energy = TARGET_PRODUCTION * BASELINE_SEC
optimized_energy = TARGET_PRODUCTION * OPTIMIZED_SEC
saved_kwh = baseline_energy - optimized_energy
saved_rs = saved_kwh * TARIFF
saved_co2 = saved_kwh * GRID_FACTOR
reduction = saved_kwh / baseline_energy * 100

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Production", f"{TARGET_PRODUCTION:,.0f} kg/day")
c2.metric("Optimized SEC", f"{OPTIMIZED_SEC:.2f} kWh/kg", f"-{reduction:.1f}%")
c3.metric("Energy saved", f"{saved_kwh:,.0f} kWh/day")
c4.metric("Indicative saving", f"₹{saved_rs:,.0f}/day")
c5.metric("CO₂ avoided", f"{saved_co2:,.0f} kg/day")

st.caption("Prototype result: simulated representative SME scenario. Tariff and emissions factor are configurable assumptions, not a measured factory result.")

tab1, tab2, tab3, tab4 = st.tabs(["Live Energy", "Equipment Health", "AI Recommendations", "What-if Optimization"])

with tab1:
    recent = df.tail(96*3).copy()
    recent["rolling_energy"] = recent["total_energy_kwh"].rolling(8, min_periods=1).mean()
    fig = px.line(recent, x="timestamp", y="total_energy_kwh", title="15-minute total electricity consumption")
    fig.update_layout(height=420, yaxis_title="kWh / 15 min", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

    left,right = st.columns(2)
    with left:
        daily = df.groupby(df.timestamp.dt.date)["total_energy_kwh"].sum().reset_index()
        daily.columns=["date","energy_kwh"]
        fig2 = px.bar(daily, x="date", y="energy_kwh", title="Daily energy consumption")
        st.plotly_chart(fig2, use_container_width=True)
    with right:
        active = df[df.production_kg>0].copy()
        active["sec"] = active["total_energy_kwh"]/active["production_kg"]
        daily2 = active.groupby(active.timestamp.dt.date).agg(
            production_kg=("production_kg","sum"),
            energy_kwh=("total_energy_kwh","sum")
        ).reset_index()
        daily2["sec"] = daily2["energy_kwh"]/daily2["production_kg"]
        fig3 = px.line(daily2, x="timestamp", y="sec", title="Specific energy consumption trend")
        st.plotly_chart(fig3, use_container_width=True)

with tab2:
    health = pd.DataFrame({
        "Equipment":["Oven / Dryer","Compressor","Refrigeration","Motors / Conveyor","Pumps"],
        "Health":[94,68,54,92,89],
        "Status":["🟢 Normal","🟡 Watch","🔴 Attention","🟢 Normal","🟢 Normal"]
    })
    st.dataframe(health, use_container_width=True, hide_index=True)
    st.markdown("### Equipment signals")
    cols = st.columns(4)
    signals = [
        ("Compressor","Power +18%","Pressure -6%"),
        ("Refrigeration","Power +24%","Cold room +0.25°C"),
        ("Oven","Temperature +7°C","Energy +1.8 kWh/15m"),
        ("Motor","Load normal","No anomaly")
    ]
    for col,(name,a,b) in zip(cols,signals):
        with col:
            st.markdown(f"**{name}**")
            st.write(a)
            st.write(b)

with tab3:
    st.markdown("### 🔴 Priority recommendation — Compressor #1")
    st.error("Energy use is elevated while pressure delivery is falling.")
    st.write("**Evidence:** power +18%, pressure −6%, discharge temperature +7°C during the anomaly window.")
    st.write("**Recommended action:** inspect filter/air leakage and verify pressure set-point before replacing equipment.")
    st.metric("Estimated avoidable energy", "≈ 160 kWh/day")
    st.divider()
    st.markdown("### 🟡 Process recommendation — Oven")
    st.warning("The simulated oven is operating above the efficient temperature window.")
    st.write("Test **180°C instead of 185°C** while keeping the quality constraint ≥95%.")
    st.metric("Estimated SEC improvement", "≈ 0.12 kWh/kg")
    st.divider()
    st.markdown("### 🟡 Refrigeration")
    st.warning("Cooling load is elevated while product temperature remains within the acceptable range.")
    st.write("Inspect condenser condition and reduce unnecessary cycling during low-load periods.")

with tab4:
    st.markdown("### What-if: choose an operating point")
    temp = st.slider("Oven temperature (°C)", 175, 190, 180)
    production = st.slider("Production target (kg/day)", 4000, 6000, 5000, step=250)
    quality = 97 - 0.08*abs(temp-182)
    # simple demonstrator response curve
    sec = 2.05 + 0.0009*(temp-180)**2 + 0.00004*(production-5000)
    sec = max(sec, 2.05)
    energy = sec*production
    base_energy = BASELINE_SEC*production
    saving = max(0, base_energy-energy)
    saving_rs = saving*TARIFF
    co2 = saving*GRID_FACTOR

    a,b,c,d = st.columns(4)
    a.metric("Predicted SEC", f"{sec:.2f} kWh/kg")
    b.metric("Predicted energy", f"{energy:,.0f} kWh/day")
    c.metric("Quality score", f"{quality:.1f}%")
    d.metric("Saving vs baseline", f"₹{saving_rs:,.0f}/day")
    if quality >= 95:
        st.success("Operating point satisfies the prototype quality constraint (≥95%).")
    else:
        st.error("Operating point violates the prototype quality constraint.")
    st.caption("Optimization curve is a demonstrator model. A production deployment would learn the response surface from validated process and quality data.")

st.divider()
st.markdown("### How FoodPulse works")
st.write("Sensor/PLC data → edge gateway → time-series data → baseline prediction → anomaly detection → equipment/process diagnosis → constrained recommendation → savings verification.")
