"""Onglet « Qualité des données » : manquants, doublons, contrôles, nettoyage et limites."""
import pandas as pd
import streamlit as st


def render(plv):
    st.header("Qualité des données et limites")

    # 1. Chiffres clés
    nb_doublons = plv.duplicated().sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Prélèvements dans le fichier", f"{len(plv):,}".replace(",", " "))
    c2.metric("Lignes en double", int(nb_doublons))
    c3.metric("Départements couverts", plv["dept"].nunique())

    # 2. Valeurs manquantes par colonne
    st.subheader("Valeurs manquantes")
    colonnes_brutes = ["dateprel", "dept", "nomcommune", "plvconformitebacterio", "plvconformitechimique"]
    manquants = pd.DataFrame({
        "Colonne": colonnes_brutes,
        "Valeurs manquantes": [int(plv[c].isna().sum()) for c in colonnes_brutes],
        "% manquant": [round(plv[c].isna().mean() * 100, 3) for c in colonnes_brutes],
    })
    st.dataframe(manquants, hide_index=True)

    # 3. Répartition des codes de conformité (on voit les "S" exclus du calcul)
    st.subheader("Codes de conformité")
    codes = pd.DataFrame({
        "Bactériologie": plv["plvconformitebacterio"].value_counts(dropna=False),
        "Chimie": plv["plvconformitechimique"].value_counts(dropna=False),
    }).fillna(0).astype(int)
    st.dataframe(codes)
    st.caption("C = conforme, N = non conforme, S = sans objet (analyse non réalisée, exclue du calcul), "
               "D = conforme avec dérogation (chimie). Les taux sont calculés uniquement sur les "
               "prélèvements évalués.")

    # 4. Contrôles de validation
    st.subheader("Contrôles de validation")
    controles = pd.DataFrame({
        "Contrôle": [
            "Toutes les dates sont en 2024",
            "Aucune date manquante",
            "Codes conformité dans la liste attendue (C, N, S, D)",
            "Codes département au bon format (2 ou 3 caractères)",
        ],
        "Réussi": [
            bool((plv["dateprel"].dt.year == 2024).all()),
            bool(plv["dateprel"].notna().all()),
            bool(plv["plvconformitebacterio"].dropna().isin(["C", "N", "S", "D"]).all()
                 and plv["plvconformitechimique"].dropna().isin(["C", "N", "S", "D"]).all()),
            bool(plv["dept"].str.len().between(2, 3).all()),
        ],
    })
    controles["Réussi"] = controles["Réussi"].map({True: "✅ oui", False: "❌ non"})
    st.dataframe(controles, hide_index=True)

    # 5. Ce qui a été fait pendant le nettoyage + limites
    st.subheader("Nettoyage effectué et limites")
    st.markdown("""
**Nettoyage :**
- Sur les 6 fichiers fournis, seul `UDI_PLV` est utilisé : il concerne l'eau du robinet et contient déjà le verdict de conformité.
- 5 colonnes conservées sur 41.
- Codes département et commune lus comme du texte, pour conserver les zéros et les codes corses (2A, 2B).
- Codes département convertis de 3 à 2 caractères (`001` → `01`).
- Les codes `S` (sans objet) sont exclus du calcul des taux.

**Limites :**
- Une seule année (2024) : on observe des variations saisonnières, pas une tendance de long terme.
- Un prélèvement non conforme ne veut pas dire que toute la commune a bu une eau dangereuse : il s'agit d'un constat ponctuel.
- Les départements ne sont pas contrôlés au même rythme : un taux calculé sur peu de prélèvements est moins fiable.
- Les explications (relief, petits réseaux, pluies d'octobre) sont des hypothèses : les données montrent des coïncidences, pas des causes.
- Les coordonnées GPS du fichier sont incohérentes (projections mélangées, valeurs aberrantes) : la carte est donc faite par département.
""")