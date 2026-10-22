# KPIs, high-level trends
import pandas as pd
import streamlit as st

from utils import viz
from utils.prep import MOIS, taux_par


def render(donnees):
    # Un tableau par type de contrôle, puis on les empile
    morceaux = []
    for indicateur in ["Bactériologie", "Chimie"]:
        t = taux_par(donnees, "mois", indicateur)[["mois", "taux"]]
        t["Type de contrôle"] = indicateur
        morceaux.append(t)
    graph = pd.concat(morceaux)

    bact = graph[graph["Type de contrôle"] == "Bactériologie"].set_index("mois")["taux"]
    pire = bact.idxmax()
    st.subheader(f"Le mois le plus touché en bactériologie : {MOIS[pire - 1]} "
                 f"({bact[pire]:.1f} % de prélèvements non conformes)")

    st.plotly_chart(viz.courbe_mois(graph), use_container_width=True)
    st.caption("Description : courbes du pourcentage de prélèvements non conformes chaque mois de 2024, "
               "en bleu pour la bactériologie et en orange pour la chimie. "
               "Survolez un point pour voir la valeur exacte.")