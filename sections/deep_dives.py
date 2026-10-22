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
    st.subheader(f"{choix} : the department most affected is the {pire['dept']} "
                 f"({pire['taux']:.1f} % of non-conforming samples)")
    st.plotly_chart(viz.carte(par_dept, geojson, col_eval), use_container_width=True)
    st.caption(f"Description : map of metropolitan France where each department is colored according to "
               f"its percentage of non-conforming samples ({choix.lower()}), from light (low) to dark (high). Hover over a department to see the exact figure.")

    # Classement
    st.divider()
    nb = st.slider("Nombre de départements à afficher", 5, 30, 15)
    moyenne = taux(donnees, choix)
    top = par_dept.sort_values("taux", ascending=False).head(nb)
    st.subheader(f"{choix} : the {nb} most affected departments, "
                 f"up to {top['taux'].max() / moyenne:.0f} times the average")
    st.plotly_chart(viz.classement(top, moyenne, col_nc, col_eval), use_container_width=True)
    st.caption(f"Description : horizontal bars ranking the {nb} departments according to their percentage "
               f"of non-conforming samples ({choix.lower()}). The dotted orange line indicates the "
               "average of the selection. Hover over a bar to see the number of samples.")