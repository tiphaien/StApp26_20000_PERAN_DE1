"""Dashboard: Tap water quality in France (2024).

Run: streamlit run app.py
"""
import streamlit as st

from sections import conclusions, deep_dives, intro, overview, quality
from utils.io import SOURCE, load_data, load_geojson
from utils.prep import taux

st.set_page_config(page_title="Tap Water Quality in France", page_icon="💧", layout="wide")

plv = load_data()
geojson = load_geojson()

# Title
st.title("💧 Is tap water safe everywhere in France? 💧")
st.caption(SOURCE)

# Filters
with st.sidebar:
    st.header("Filters")
    depts = st.multiselect("Departments (blank = the whole of France)", sorted(plv["dept"].unique()))
    mois = st.slider("Month", 1, 12, (1, 12))

donnees = plv[plv["mois"].between(mois[0], mois[1])]
if depts:
    donnees = donnees[donnees["dept"].isin(depts)]

if donnees.empty:
    st.error("No samples match the filters.")
    st.stop()

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Samples analyzed", f"{len(donnees):,}".replace(",", " "))
c2.metric("Non-compliant : bacteriology", f"{taux(donnees, 'Bactériologie'):.1f} %")
c3.metric("Non-compliant : chemistry", f"{taux(donnees, 'Chimie'):.1f} %")

# Tabs
onglet1, onglet2, onglet3, onglet4, onglet5 = st.tabs(
    ["1 · Context", "2 · Over time", "3 · Where?", "4 · Data quality", "5 · Conclusions"])

with onglet1:
    intro.render()
with onglet2:
    overview.render(donnees)
with onglet3:
    deep_dives.render(donnees, geojson)
with onglet4:
    quality.render(plv)
with onglet5:
    conclusions.render(plv)