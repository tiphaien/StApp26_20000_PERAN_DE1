# context, objectives, data caveats
import streamlit as st

from utils.io import URL_JEU


def render():
    st.subheader("Pourquoi c'est important")
    st.markdown("""
    L'eau du robinet est l'aliment le plus contrôlé en France : des centaines de milliers de prélèvements
    sont analysés chaque année par les Agences régionales de santé. **Mais cette eau est-elle de la même
    qualité partout, et à toutes les saisons ?**

    **Public visé :** habitants, élus locaux et services des eaux qui veulent savoir où agir en priorité.

    **Les questions de ce tableau de bord :**
    1. Les problèmes de qualité varient-ils au fil de l'année ? → onglet *Dans le temps*
    2. Certains départements sont-ils plus touchés que d'autres ? → onglet *Où ?*
    3. Peut-on faire confiance à ces chiffres ? → onglet *Qualité des données*
    """)
    st.subheader("Comment lire les données")
    st.markdown("""
    - **Un prélèvement** = un échantillon d'eau prélevé dans le réseau qui alimente les robinets.
    - **Bactériologie** : présence de microbes pouvant rendre malade (ex. E. coli).
    - **Chimie** : substances comme les nitrates ou les pesticides.
    - **Non conforme** = au moins une valeur dépasse une **limite de qualité** réglementaire.
      Cela signale un problème à corriger, sans signifier forcément un danger immédiat.
    """)
    st.info(f"Données : [Résultats du contrôle sanitaire de l'eau du robinet]({URL_JEU}) (année 2024), "
            "Ministère de la Santé — Licence Ouverte. Fichier utilisé : UDI_PLV "
            "(prélèvements sur les réseaux de distribution).")