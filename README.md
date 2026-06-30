# Agriculture-Challenge — Togo AI Lab Data Challenge Défi 2

Dashboard analytique de résilience agricole territoriale au Togo.

## Contexte
Ce projet répond au Défi 2 du Data Challenge Agriculture organisé par le **Togo AI Lab** (#MESPTN #TogoAILab). Il identifie les zones du Togo où les infrastructures agricoles (élevage, eau, pisciculture, abattoirs) soutiennent l'économie locale, et propose un Top 10 des zones prioritaires pour de nouveaux investissements.

## Structure du projet
```
Agriculture-Challenge/
├── app.py                  # Point d'entrée du dashboard Dash
├── requirements.txt
├── README.md
├── assets/                 # CSS, logo
├── data/
│   ├── raw/                # Données brutes téléchargées
│   └── processed/          # Données nettoyées + data_dictionary.md
├── notebooks/
│   ├── 01_download.ipynb   # Collecte & exploration initiale
│   ├── 02_cleaning.ipynb   # Nettoyage & harmonisation
│   ├── 03_eda.ipynb        # Analyse exploratoire
│   ├── 04_geospatial.ipynb # Analyses spatiales
│   └── 05_resilience_index.ipynb  # Construction IRAT
├── src/                    # Modules Python réutilisables
│   ├── preprocessing.py
│   ├── indicators.py
│   ├── maps.py
│   └── utils.py
├── dashboard/              # Composants Dash
│   ├── layout.py
│   ├── callbacks.py
│   └── figures.py
└── presentation/           # PowerPoint + rapport méthodologique
```

## Installation & lancement
```bash
pip install -r requirements.txt
python app.py
```
Puis ouvrir http://localhost:8050

## Sources de données
- Élevage, abattoirs, pisciculture, retenues d'eau, barrages : [geodata.gouv.tg](https://geodata.gouv.tg)
- Valeur ajoutée agricole (séries temporelles) : [opendata.gouv.tg](https://opendata.gouv.tg)
- Limites administratives : [geodata.gouv.tg](https://geodata.gouv.tg) / HDX

## Méthodologie
L'**Indice de Résilience Agricole Territoriale (IRAT)** combine 5 piliers pondérés :

| Pilier | Poids |
|---|---|
| Accès à l'eau | 30% |
| Élevage | 25% |
| Pisciculture | 20% |
| Abattoirs | 15% |
| Performance agricole | 10% |

Chaque indicateur est normalisé 0-100 (min-max). 5 catégories finales : Très résilient → Très vulnérable.

## Auteur
Fadel ADAM — fadamgroup@gmail.com
