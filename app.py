"""Dashboard: Tap water quality in France (2024).

Run: streamlit run app.py
"""
import plotly.express as px
import streamlit as st

from pathlib import Path
from sections import conclusions, deep_dives, intro, overview, quality
from utils.io import SOURCE, load_data, load_geojson
from utils.prep import INDICATEURS, taux

st.set_page_config(page_title="Tap Water Quality in France", page_icon="💧", layout="wide")

plv = load_data()
geojson = load_geojson()

@st.cache_data
def liste_communes(plv):
    """Commune names with their département, e.g. 'ANNECY (74)'."""
    return sorted((plv["nomcommune"] + " (" + plv["dept"] + ")").dropna().unique())


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


# Author & course info
LOGO = Path(__file__).parent / "assets" / "efrei_logo.png"

with st.sidebar:
    st.divider()
    if LOGO.exists():
        st.image(str(LOGO), width=160)

    st.markdown("""
**Tiphaine PERAN**
[Data Engineering Program] · [i2] · Group DE1

📧 [tiphaine.peran@efrei.net](mailto:tiphaine.peran@efrei.net)
🔗 [LinkedIn](https://www.linkedin.com/in/tiphaine-peran/)
💻 [GitHub](https://github.com/tiphaien)

---

**Course:** Data Analysis & Visualization
**Project proposed by:** Prof. Mano Joseph Mathew
[mano.mathew@efrei.fr](mailto:mano.mathew@efrei.fr)
""")




# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Samples analyzed", f"{len(donnees):,}".replace(",", " "))
c2.metric("Non-compliant : bacteriology", f"{taux(donnees, 'Bactériologie'):.1f} %")
c3.metric("Non-compliant : chemistry", f"{taux(donnees, 'Chimie'):.1f} %")


# Check your town
with st.expander("Check your town: how did your tap water do in 2024?"):
    choix = st.selectbox("Type the name of your commune", liste_communes(plv),
                         index=None, placeholder="e.g. ANNECY (74)")
    if choix is None:
        st.info("Start typing a commune name in the box above.")
    else:
        nom, dept = choix.rsplit(" (", 1)
        ville = plv[(plv["nomcommune"] == nom) & (plv["dept"] == dept.rstrip(")"))]
        bact, chim = list(INDICATEURS)
        non_conformes = ville[ville["bacterio_nc"] | ville["chimique_nc"]]

        t1, t2, t3 = st.columns(3)
        t1.metric("Samples tested in 2024", len(ville))
        t2.metric("Non-compliant samples", len(non_conformes))
        t3.metric("Bacteriology non-compliance", f"{taux(ville, bact):.1f} %",
                  f"{taux(ville, bact) - taux(plv, bact):+.1f} pt vs France", delta_color="inverse")

        if non_conformes.empty:
            st.success(f"All {len(ville)} samples taken in {nom} in 2024 were compliant.")
        else:
            st.warning(f"{len(non_conformes)} of {len(ville)} samples were non-compliant in {nom} in 2024.")

        t = ville.assign(Result=(ville["bacterio_nc"] | ville["chimique_nc"]).map(
            {True: "Non-compliant", False: "Compliant"}))
        fig = px.strip(t, x="dateprel", y="Result", color="Result",
                       color_discrete_map={"Compliant": "#2a78d6", "Non-compliant": "#eb6834"},
                       labels={"dateprel": "Sample date (2024)", "Result": ""})
        fig.update_layout(height=250, showlegend=False)
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Description: each dot is one tap water sample taken in {nom} in 2024, placed by date. "
                   "Blue dots are compliant, orange dots are non-compliant. "
                   "A non-compliant sample is a one-off finding that triggers corrective action; "
                   "it does not mean the water was unsafe all year.")
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