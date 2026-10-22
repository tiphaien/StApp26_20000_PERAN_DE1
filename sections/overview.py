# KPIs, high-level trends
import pandas as pd
import streamlit as st

from utils import viz
from utils.prep import MOIS, taux_par


def render(donnees):
    morceaux = []
    for indicateur in ["Bacteriologie", "Chemistry"]:
        t = taux_par(donnees, "mois", indicateur)[["mois", "taux"]]
        t["Type de contrôle"] = indicateur
        morceaux.append(t)
    graph = pd.concat(morceaux)

    bact = graph[graph["Type de contrôle"] == "Bacteriologie"].set_index("mois")["taux"]
    pire = bact.idxmax()
    st.subheader(f"The month most affected in bacteriology: {MOIS[pire - 1]} "
                 f"({bact[pire]:.1f} % of non-conforming samples)")

    st.plotly_chart(viz.courbe_mois(graph), use_container_width=True)
    st.caption("Description : curves of the percentage of non-conforming samples each month of 2024, "
               "in blue for bacteriology and in orange for chemistry. "
               "Hover over a point to see the exact value.")