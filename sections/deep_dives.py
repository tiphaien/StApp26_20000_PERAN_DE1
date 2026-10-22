# comparisons, distributions, drilldowns

import streamlit as st

from utils import viz
from utils.prep import INDICATEURS, taux, taux_par


def render(donnees, geojson):
    choix = st.radio("Indicateur", list(INDICATEURS), horizontal=True)
    col_nc, col_eval = INDICATEURS[choix]
    par_dept = taux_par(donnees, "dept", choix)

    # Carte
    pire = par_dept.loc[par_dept["taux"].idxmax()]
    st.subheader(f"{choix} : le département le plus touché est le {pire['dept']} "
                 f"({pire['taux']:.1f} % de non-conformités)")
    st.plotly_chart(viz.carte(par_dept, geojson, col_eval), use_container_width=True)
    st.caption(f"Description : carte de France métropolitaine où chaque département est coloré selon "
               f"son pourcentage de prélèvements non conformes ({choix.lower()}), du plus clair (faible) "
               "au plus foncé (élevé). Survolez un département pour voir le chiffre exact.")

    # Classement
    st.divider()
    nb = st.slider("Nombre de départements à afficher", 5, 30, 15)
    moyenne = taux(donnees, choix)
    top = par_dept.sort_values("taux", ascending=False).head(nb)
    st.subheader(f"{choix} : les {nb} départements les plus touchés, "
                 f"jusqu'à {top['taux'].max() / moyenne:.0f} fois la moyenne")
    st.plotly_chart(viz.classement(top, moyenne, col_nc, col_eval), use_container_width=True)
    st.caption(f"Description : barres horizontales classant les {nb} départements selon leur pourcentage "
               f"de prélèvements non conformes ({choix.lower()}). La ligne pointillée orange indique la "
               "moyenne de la sélection. Survolez une barre pour voir le nombre de prélèvements.")