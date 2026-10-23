import streamlit as st

from utils import viz
from utils.prep import INDICATEURS, taux, taux_par


def render(donnees, geojson):
    choix = st.radio("Indicator", list(INDICATEURS), horizontal=True)
    col_nc, col_eval = INDICATEURS[choix]
    par_dept = taux_par(donnees, "dept", choix)

    pire = par_dept.loc[par_dept["taux"].idxmax()]
    st.subheader(f"{choix}: the most affected département is {pire['dept']} "
                 f"({pire['taux']:.1f} % non-compliant samples)")
    st.plotly_chart(viz.carte(par_dept, geojson, col_eval), width="stretch")
    st.caption("Description: map of mainland France coloured by the percentage of non-compliant "
               "samples, from light (low) to dark (high). Hover over a département to see the figure.")

    st.divider()
    nb = st.slider("Number of departements to display", 5, 30, 15)
    moyenne = taux(donnees, choix)
    top = par_dept.sort_values("taux", ascending=False).head(nb)
    st.subheader(f"{choix}: the {nb} most affected départements, "
                 f"up to {top['taux'].max() / moyenne:.0f} times the average")
    st.plotly_chart(viz.classement(top, moyenne, col_nc, col_eval), width="stretch")
    st.caption("Description: ranking of départements by percentage of non-compliant samples. "
               "The orange dashed line shows the average.")