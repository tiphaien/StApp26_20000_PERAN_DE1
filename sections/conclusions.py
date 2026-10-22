# insights, implications, next steps

import streamlit as st

from utils.prep import taux, taux_par


def render(plv):
    nat_bact = taux(plv, "Bactériologie")
    nat_chim = taux(plv, "Chimie")
    pires = taux_par(plv, "dept", "Bactériologie").sort_values("taux", ascending=False).head(3)
    m = taux_par(plv, "mois", "Bactériologie")

    st.subheader("Ce qu'il faut retenir")
    st.success(f"""
    1. **L'eau du robinet est très majoritairement conforme** : {nat_bact:.1f} % de prélèvements non
       conformes en bactériologie et {nat_chim:.1f} % en chimie sur l'année 2024.
    2. **Les problèmes bactériologiques sont très concentrés** : les départements les plus touchés
       ({", ".join(pires["dept"])}) atteignent jusqu'à {pires["taux"].max():.0f} % — surtout des territoires
       de montagne et ruraux.
    3. **Il y a un effet saison** : de {m["taux"].min():.1f} % au mois le plus calme à {m["taux"].max():.1f} %
       au mois le plus touché (octobre), un pic qui coïncide avec les inondations de l'épisode cévenol.
    """)

    st.subheader("Implications et prochaines étapes")
    st.markdown("""
    - **Agir en priorité** sur les petits réseaux des zones de montagne, où les non-conformités se concentrent.
    - **Renforcer la surveillance** après les épisodes de fortes pluies.
    - **Pour aller plus loin** : ajouter plusieurs années (2020-2024) pour distinguer un accident ponctuel
      d'une tendance, et croiser avec la taille des réseaux pour tester l'hypothèse des petits réseaux.
    """)