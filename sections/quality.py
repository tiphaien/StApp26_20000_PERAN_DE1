"""Onglet « Qualité des données » : manquants, doublons, contrôles, nettoyage et limites."""
import pandas as pd
import streamlit as st


def render(plv):
    st.header("Qualité des données et limites")

    # 1. key numbers
    nb_doublons = plv.duplicated().sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Extracts from the file", f"{len(plv):,}".replace(",", " "))
    c2.metric("Duplicate lines", int(nb_doublons))
    c3.metric("Departments covered", plv["dept"].nunique())

    # 2. missing values for each row
    st.subheader("Missing values")
    colonnes_brutes = ["dateprel", "dept", "nomcommune", "plvconformitebacterio", "plvconformitechimique"]
    manquants = pd.DataFrame({
        "Column": colonnes_brutes,
        "Missing values": [int(plv[c].isna().sum()) for c in colonnes_brutes],
        "% missing": [round(plv[c].isna().mean() * 100, 3) for c in colonnes_brutes],
    })
    st.dataframe(manquants, hide_index=True)

    # 3. Breakdown of compliance codes (note that the ‘S’ codes are excluded from the calculation)
    st.subheader("Compliance codes")
    codes = pd.DataFrame({
        "Bacteriology": plv["plvconformitebacterio"].value_counts(dropna=False),
        "Chemistry": plv["plvconformitechimique"].value_counts(dropna=False),
    }).fillna(0).astype(int)
    st.dataframe(codes)
    st.caption("C = compliant, N = non-compliant, S = not applicable (analysis not carried out, excluded from the calculation), "
               "D = compliant with a derogation (chemistry). The rates are calculated solely on the basis of the "
               "samples assessed.")

    # 4. validation checks
    st.subheader("Validation checks")
    controles = pd.DataFrame({
        "Controle": [
            "All dates are in 2024",
            "No missing dates",
            "Compliance codes in the expected list (C, N, S, D)",
            "Department codes in the correct format (2 or 3 characters)",
        ],
        "Réussi": [
            bool((plv["dateprel"].dt.year == 2024).all()),
            bool(plv["dateprel"].notna().all()),
            bool(plv["plvconformitebacterio"].dropna().isin(["C", "N", "S", "D"]).all()
                 and plv["plvconformitechimique"].dropna().isin(["C", "N", "S", "D"]).all()),
            bool(plv["dept"].str.len().between(2, 3).all()),
        ],
    })
    controles["Réussi"] = controles["Réussi"].map({True: "yes", False: "no"})
    st.dataframe(controles, hide_index=True)

    # 5. what was done to clean the data and what are the limitations of this analysis
    st.subheader("Cleaning carried out and limitations")
    st.markdown("""
**Data cleaning:**
- Of the 6 files provided, only `UDI_PLV` is used: this relates to tap water and already contains the compliance result.
- 5 columns retained out of 41.
- Department and municipality codes treated as text, to preserve leading zeros and Corsican codes (2A, 2B).
- Department codes converted from 3 to 2 characters (`001` → `01`).
- `S` codes (not applicable) are excluded from the calculation of rates.

**Limitations:**
- A single year (2024): seasonal variations are observed, not a long-term trend.
- A non-compliant sample does not mean that the entire municipality drank unsafe water: this is a one-off finding.
- Departments are not monitored at the same frequency: a rate calculated from a small number of samples is less reliable.
- The explanations (topography, small distribution networks, October rainfall) are hypotheses: the data show correlations, not causes.
- The GPS coordinates in the file are inconsistent (mixed projections, outliers): the map is therefore drawn up by department.
""")