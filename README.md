# Is tap water safe everywhere in France?

Individual Streamlit project — EFREI Paris, Data Analysis & Visualization — Tiphaine PERAN, group DE1

A data storytelling app on the quality of tap water in France in 2024, based on the official
results of the public health monitoring programme.

**Live app:** https://qualite-eau-robinet-de1.streamlit.app/
**Demo video:** [link, to be added]

## Data

| | |
|---|---|
| **Dataset** | Résultats du contrôle sanitaire de l'eau du robinet (tap water health monitoring results) |
| **Producer** | French Ministry of Health (Regional Health Agencies, ARS) |
| **Link** | https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet |
| **Licence** | Licence Ouverte / Open Licence |
| **Year used** | 2024 |
| **File used** | `UDI_PLV_2024.txt`: 246,631 samples, 101 départements |

### Why this file out of the 6 provided

The zip contains 3 monitoring points × 2 file types:
- `CAP` = raw water at the source, `TTP` = water leaving the treatment plant,
  `UDI` = water in the distribution network, **the water that reaches the tap**;
- `PLV` = one sample per row, with the **compliance verdict**,
  `RES` = the detailed result for each substance analysed.

Since the topic is tap water, only `UDI_PLV` is used: it directly contains the
"compliant / non-compliant" verdict set by the health authorities.

## The story

**Audience:** residents, local elected officials, water utilities.

**Questions:**
1. Do water quality problems vary over the year?
2. Are some départements more affected than others?
3. Can these figures be trusted?

**Key findings:**
- Water is overwhelmingly compliant : 1.8% of samples are non-compliant for bacteriology, 2.4% for chemistry.
- Bacteriological problems are concentrated in mountainous and rural départements.   
- A sharp peak in October, coinciding with the floods of the Cévennes rain episode (*épisode cévenol*)
  (Ardèche + Lozère: 24.4% of samples non-compliant that month).

## Method

- **Cleaning** (`utils/prep.py`) : 5 of 41 columns kept, codes read as text
  (leading zeros, Corsica 2A/2B), département codes converted from 3 to 2 characters.
- **Indicator** : non-compliance rate = non-compliant samples ÷ assessed samples.
  `S` codes (not applicable, analysis not performed) are excluded from the calculation.
- **Data quality** : missing values, duplicates and validation checks are shown
  in tab 4 of the app.

## Running the project

```bash
pip install -r requirements.txt
streamlit run app.py
```

The prepared data (`data/processed/prelevements_2024.parquet`) is included.
To regenerate it from the raw file:
1. Download the 2024 zip from the data.gouv.fr page above.
2. Unzip it into `data/eaurob-2024/`.
3. Run `python scripts/build_data.py`.

## Structure

```
app.py                  # main page: filters, KPIs, tabs
sections/               # one file per tab (intro, overview, deep_dives, quality, conclusions)
utils/io.py             # data loading (cached)
utils/prep.py           # cleaning and rate calculations
utils/viz.py            # chart functions
scripts/build_data.py   # data preparation from the raw file
data/processed/         # prepared data
assets/                 # département boundaries (GeoJSON)
explore_dataset.ipynb   # initial data exploration
```

## Limitations

- A single year: seasonal variations are visible, but not long-term trends.
- A non-compliant sample is a one-off finding, not proof that the whole municipality drank unsafe water.
- Départements are not monitored at the same frequency.
- The explanations put forward (terrain, small networks, rainfall) are hypotheses: the data
  shows coincidences, not causes.
- The GPS coordinates in the file are unusable (mixed projections): the map is by département.
- The map covers mainland France; overseas départements appear in the ranking.

## Sources

- Data: https://www.data.gouv.fr/datasets/resultats-du-controle-sanitaire-de-leau-du-robinet
- Département boundaries: https://github.com/gregoiredavid/france-geojson
- October 2024 weather context: Météo-France, autumn 2024 climate report