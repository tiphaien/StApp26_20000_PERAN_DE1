# load_data(), fetch_and_cache(), license text

"""Chargement des données et informations de source."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

RACINE = Path(__file__).parent.parent
FICHIER_DONNEES = RACINE / "data" / "processed" / "prelevements_2024.parquet"
FICHIER_CARTE = RACINE / "assets" / "departements.geojson"

URL_JEU = "https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet"
SOURCE = ("Source : Résultats du contrôle sanitaire de l'eau du robinet, 2024 — "
          "Ministère de la Santé — data.gouv.fr — Licence Ouverte")


@st.cache_data
def load_data():
    return pd.read_parquet(FICHIER_DONNEES)


@st.cache_data
def load_geojson():
    with open(FICHIER_CARTE, encoding="utf-8") as f:
        return json.load(f)