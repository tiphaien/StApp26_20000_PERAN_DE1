# insights, implications, next steps

import streamlit as st

from utils.prep import taux, taux_par


def render(plv):
    nat_bact = taux(plv, "Bacteriology")
    nat_chim = taux(plv, "Chemistry")
    pires = taux_par(plv, "dept", "Bacteriology").sort_values("taux", ascending=False).head(3)
    m = taux_par(plv, "mois", "Bacteriology")

    st.subheader("Key takeaways")
    st.success(f"""
    1. **Tap water is mostly compliant**: {nat_bact:.1f}% of samples were non-compliant
       for bacteriology and {nat_chim:.1f}% for chemistry in 2024.
    2. **Bacteriological problems are highly concentrated**: the most affected departments
       ({", ".join(pires["dept"])}) reach up to {pires["taux"].max():.0f}% — particularly mountainous
       and rural areas.
    3. **There is a seasonal effect**: rates range from {m["taux"].min():.1f}% in the calmest month to
       {m["taux"].max():.1f}% in the most affected month (October), a peak that coincides with flooding
       during the Cévenol storm episode.
    """)

    st.subheader("Implications and next steps")
    st.markdown("""
      - **Prioritize action** on small water systems in mountainous areas, where non-compliance is concentrated.
      - **Strengthen monitoring** after periods of heavy rainfall.
      - **Next steps**: add several years of data (2020–2024) to distinguish an isolated event
         from a trend, and compare results with system size to test the small-system hypothesis.
    """)