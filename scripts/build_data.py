"""Prepares the app data from the raw file UDI_PLV_2024.txt.

Source: https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet
Usage: unzip the 2024 file into data/raw/eaurob-2024/, then run
    python scripts/build_data.py
"""
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE))# to import utils

from utils.prep import COLONNES, nettoyer

FICHIER_BRUT = RACINE / "data" / "eaurob-2024" / "UDI_PLV_2024.txt"
SORTIE = RACINE / "data" / "processed" / "prelevements_2024.parquet"


def main():
    brut = pd.read_csv(FICHIER_BRUT, sep=",", usecols=COLONNES, dtype=str)
    print(f"Lu : {len(brut)} prélèvements")
    plv = nettoyer(brut)
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    plv.to_parquet(SORTIE, index=False)
    print(f"Sauvegardé : {SORTIE}")


if __name__ == "__main__":
    main()