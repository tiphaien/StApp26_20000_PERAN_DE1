"""Tableau de bord : qualité de l'eau du robinet en France (2024).

Lancer : streamlit run app.py
"""
import streamlit as st

from sections import conclusions, deep_dives, intro, overview, quality
from utils.io import SOURCE, load_data, load_geojson
from utils.prep import taux

st.set_page_config(page_title="Qualité de l'eau du robinet", page_icon="💧", layout="wide")

plv = load_data()
geojson = load_geojson()

# ---------- Titre ----------
st.title("💧 L'eau du robinet est-elle sûre partout en France ?")
st.caption(SOURCE)

# ---------- Filtres ----------
with st.sidebar:
    st.header("Filtres")
    depts = st.multiselect("Départements (vide = toute la France)", sorted(plv["dept"].unique()))
    mois = st.slider("Mois", 1, 12, (1, 12))

donnees = plv[plv["mois"].between(mois[0], mois[1])]
if depts:
    donnees = donnees[donnees["dept"].isin(depts)]

if donnees.empty:
    st.error("Aucun prélèvement ne correspond aux filtres.")
    st.stop()

# ---------- KPI ----------
c1, c2, c3 = st.columns(3)
c1.metric("Prélèvements analysés", f"{len(donnees):,}".replace(",", " "))
c2.metric("Non conformes : bactériologie", f"{taux(donnees, 'Bactériologie'):.1f} %")
c3.metric("Non conformes : chimie", f"{taux(donnees, 'Chimie'):.1f} %")

# ---------- Onglets ----------
onglet1, onglet2, onglet3, onglet4, onglet5 = st.tabs(
    ["1 · Contexte", "2 · Dans le temps", "3 · Où ?", "4 · Qualité des données", "5 · Conclusions"])

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