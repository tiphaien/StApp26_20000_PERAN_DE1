# 💧 L'eau du robinet est-elle sûre partout en France ?

Projet individuel Streamlit — EFREI Paris, Data Analysis & Visualization — [Prénom NOM], [groupe DE1]

Application de data storytelling sur la qualité de l'eau du robinet en France en 2024, à partir des
résultats officiels du contrôle sanitaire.

**Application en ligne :** [lien Streamlit Cloud, à ajouter après le déploiement]
**Vidéo de démonstration :** [lien, à ajouter]

## Données

| | |
|---|---|
| **Jeu de données** | Résultats du contrôle sanitaire de l'eau du robinet |
| **Producteur** | Ministère de la Santé (Agences régionales de santé) |
| **Lien** | https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet |
| **Licence** | Licence Ouverte / Open Licence |
| **Année utilisée** | 2024 |
| **Fichier utilisé** | `UDI_PLV_2024.txt` : 246 631 prélèvements, 101 départements |

### Pourquoi ce fichier parmi les 6 fournis

Le zip contient 3 points de contrôle × 2 types de fichiers :
- `CAP` = eau brute au captage, `TTP` = eau en sortie d'usine de traitement,
  `UDI` = eau dans le réseau de distribution, **celle qui arrive au robinet** ;
- `PLV` = un prélèvement par ligne avec le **verdict de conformité**,
  `RES` = le détail de chaque substance analysée.

Le sujet étant l'eau du robinet, seul `UDI_PLV` est utilisé : il contient directement le verdict
« conforme / non conforme » fixé par les autorités sanitaires.

## Le récit

**Public :** habitants, élus locaux, services des eaux.

**Questions :**
1. Les problèmes de qualité varient-ils au fil de l'année ?
2. Certains départements sont-ils plus touchés que d'autres ?
3. Peut-on faire confiance à ces chiffres ?

**Principaux constats :**
- L'eau est très majoritairement conforme : [1,8] % de non-conformités en bactériologie, [2,4] % en chimie.
- Les problèmes bactériologiques se concentrent dans les départements de montagne et ruraux
  (Lozère : [14,3] %, Corse, Hautes-Alpes…).
- Un pic marqué en octobre, qui coïncide avec les inondations de l'épisode cévenol
  (Ardèche + Lozère : [24,4] % de non-conformités ce mois-là).

## Méthode

- **Nettoyage** (`utils/prep.py`) : 5 colonnes conservées sur 41, codes lus comme du texte
  (zéros initiaux, Corse 2A/2B), codes département convertis de 3 à 2 caractères.
- **Indicateur** : taux de non-conformité = prélèvements non conformes ÷ prélèvements évalués.
  Les codes `S` (sans objet, analyse non réalisée) sont exclus du calcul.
- **Qualité des données** : valeurs manquantes, doublons et contrôles de validation affichés
  dans l'onglet 4 de l'application.

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

Les données préparées (`data/processed/prelevements_2024.parquet`) sont incluses.
Pour les régénérer depuis le fichier brut :
1. Télécharger le zip 2024 sur la page data.gouv.fr ci-dessus.
2. Le dézipper dans `data/eaurob-2024/`.
3. Lancer `python scripts/build_data.py`.

## Structure

```
app.py                  # page principale : filtres, KPI, onglets
sections/               # un fichier par onglet (intro, overview, deep_dives, quality, conclusions)
utils/io.py             # chargement des données (mis en cache)
utils/prep.py           # nettoyage et calcul des taux
utils/viz.py            # fonctions graphiques
scripts/build_data.py   # préparation des données depuis le fichier brut
data/processed/         # données préparées
assets/                 # contours des départements (GeoJSON)
explore_dataset.ipynb   # exploration initiale des données
```

## Limites

- Une seule année : variations saisonnières visibles, pas de tendance de long terme.
- Un prélèvement non conforme est un constat ponctuel, pas une eau dangereuse pour toute la commune.
- Les départements ne sont pas contrôlés au même rythme.
- Les explications avancées (relief, petits réseaux, pluies) sont des hypothèses : les données
  montrent des coïncidences, pas des causes.
- Coordonnées GPS du fichier inutilisables (projections mélangées) : carte par département.
- La carte couvre la métropole ; l'outre-mer apparaît dans le classement.

## Sources

- Données : https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet
- Contours des départements : https://github.com/gregoiredavid/france-geojson
- Contexte météo d'octobre 2024 : Météo-France, bilan climatique de l'automne 2024