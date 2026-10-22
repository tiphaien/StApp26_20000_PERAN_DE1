# cleaning, normalization, feature engineering
"""Nettoyage des données et calcul des indicateurs."""
import pandas as pd

COLONNES = ["dateprel", "cddept", "nomcommune", "plvconformitebacterio", "plvconformitechimique"]

# Pour chaque type de contrôle : (colonne non conforme, colonne évalué)
INDICATEURS = {
    "Bactériologie": ("bacterio_nc", "bacterio_evalue"),
    "Chimie": ("chimique_nc", "chimique_evalue"),
}

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def nettoyer(plv: pd.DataFrame) -> pd.DataFrame:
    """Dates, codes département et indicateurs de conformité."""
    plv = plv.copy()
    plv["dateprel"] = pd.to_datetime(plv["dateprel"])
    plv["mois"] = plv["dateprel"].dt.month
    plv["dept"] = plv["cddept"].str.replace(r"^0", "", regex=True)   # "001" -> "01"
    # Les codes "S" (sans objet) ne sont pas comptés comme évalués
    plv["bacterio_evalue"] = plv["plvconformitebacterio"].isin(["C", "N"])
    plv["bacterio_nc"] = plv["plvconformitebacterio"] == "N"
    plv["chimique_evalue"] = plv["plvconformitechimique"].isin(["C", "N", "D"])
    plv["chimique_nc"] = plv["plvconformitechimique"] == "N"
    return plv


def taux(df: pd.DataFrame, indicateur: str) -> float:
    """Pourcentage de prélèvements non conformes parmi ceux évalués."""
    col_nc, col_eval = INDICATEURS[indicateur]
    return df[col_nc].sum() / df[col_eval].sum() * 100


def taux_par(df: pd.DataFrame, par: str, indicateur: str) -> pd.DataFrame:
    """Taux de non-conformité pour chaque valeur de `par` (mois, dept…)."""
    col_nc, col_eval = INDICATEURS[indicateur]
    g = df.groupby(par)[[col_nc, col_eval]].sum().reset_index()
    g["taux"] = g[col_nc] / g[col_eval] * 100
    return g