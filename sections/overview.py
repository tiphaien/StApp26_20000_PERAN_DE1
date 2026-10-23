# KPIs, high-level trends
import pandas as pd
import streamlit as st

from utils import viz
from utils.prep import INDICATEURS, MOIS, taux_par

# English labels shown in the legend (the keys stay as in INDICATEURS)
LIBELLES = {"Bacteriology": "Bacteriology", "Chemistry": "Chemistry"}


def render(donnees):
    exclure = st.toggle("Exclude Ardèche (07) and Lozère (48)",
                        help="These two départements were hit by severe floods in mid-October 2024.")
    if exclure:
        donnees = donnees[~donnees["dept"].isin(["07", "48"])]

    morceaux = []
    for indicateur in INDICATEURS:
        t = taux_par(donnees, "mois", indicateur)[["mois", "taux"]]
        t["Type of control"] = LIBELLES[indicateur]
        morceaux.append(t)
    graph = pd.concat(morceaux)

    bact = graph[graph["Type of control"] == "Bacteriology"].set_index("mois")["taux"]
    pire = bact.idxmax()
    st.subheader(f"The month most affected in bacteriology: {MOIS[pire - 1]} "
                 f"({bact[pire]:.1f} % of non-compliant samples)")

    st.plotly_chart(viz.courbe_mois(graph), width="stretch")
    st.caption("Description: curves of the percentage of non-compliant samples each month of 2024, "
               "in blue for bacteriology and in orange for chemistry. "
               "Hover over a point to see the exact value.")
    st.caption("Use the toggle to see how much of the October peak comes from Ardèche and Lozère alone. "
               "The timing coincides with the floods; the data does not prove they caused it.")