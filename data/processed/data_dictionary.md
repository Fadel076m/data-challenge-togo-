# Dictionnaire des données — Agriculture Challenge Togo

> À compléter au fil du notebook `01_download.ipynb`. Une ligne par colonne, une table par source.

---

## 1. Élevage – Établissements
**Source :** geodata.gouv.tg — UUID `d10efb34-cac7-4913-a88e-c19b439a0b09`  
**Format :** (à remplir)  
**CRS :** (à remplir)  
**Nb lignes :** (à remplir)  
**Niveau géo :** (à remplir — point GPS / préfecture / canton ?)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 2. Abattoirs – Établissements
**Source :** geodata.gouv.tg — UUID `eefd3bb3-4f6c-4ddb-9a58-b6dd0a609085`  
**Format :** (à remplir)  
**CRS :** (à remplir)  
**Nb lignes :** (à remplir)  
**Niveau géo :** (à remplir)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 3. Zones de pisciculture
**Source :** geodata.gouv.tg — UUID `5c57b047-f1a1-4313-aff8-139afcf4cc1e`  
**Format :** (à remplir)  
**CRS :** (à remplir)  
**Nb lignes :** (à remplir)  
**Niveau géo :** (à remplir)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 4. Retenues d'eau collinaires
**Source :** geodata.gouv.tg — UUID `767b4228-cdab-4d80-8bdb-02e96d0239f7`  
**Format :** (à remplir)  
**CRS :** (à remplir)  
**Nb lignes :** (à remplir)  
**Niveau géo :** (à remplir)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 5. Digues et petits barrages
**Source :** geodata.gouv.tg — UUID `6d7f7dd5-49c4-4d36-b7b2-4532a5da21cf`  
**Format :** (à remplir)  
**CRS :** (à remplir)  
**Nb lignes :** (à remplir)  
**Niveau géo :** (à remplir)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 6. Agriculture & développement rural (Banque mondiale via opendata.gouv.tg)
**Source :** opendata.gouv.tg  
**Format :** (à remplir)  
**Granularité temporelle :** (à remplir)  
**Niveau géo :** National (Togo entier)

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 7. Valeur ajoutée agricole (% du PIB)
**Source :** opendata.gouv.tg  
**Format :** (à remplir)  
**Années disponibles :** (à remplir)  
**Niveau géo :** National

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 8. Valeur ajoutée agricole (croissance annuelle %)
**Source :** opendata.gouv.tg  
**Format :** (à remplir)  
**Années disponibles :** (à remplir)  
**Niveau géo :** National

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 9. Valeur ajoutée agricole (USD constants 2015)
**Source :** opendata.gouv.tg  
**Format :** (à remplir)  
**Années disponibles :** (à remplir)  
**Niveau géo :** National

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## 10. Valeur ajoutée agricole par travailleur (USD constants 2015)
**Source :** opendata.gouv.tg  
**Format :** (à remplir)  
**Années disponibles :** (à remplir)  
**Niveau géo :** National

| Colonne | Type | Description | Unité | Valeurs manquantes |
|---|---|---|---|---|
| (à compléter) | | | | |

---

## Shapefile — Limites administratives du Togo
**Source :** (à remplir — geodata.gouv.tg ou HDX)  
**Niveaux disponibles :** Région / Préfecture / Canton  
**CRS :** (à remplir)  
**Nb entités :** Régions: 5 · Préfectures: 39 · Cantons: ~394

| Colonne | Type | Description |
|---|---|---|
| (à compléter) | | |

---

## Notes méthodologiques
- Clé de jointure cible : **code préfecture / canton harmonisé** (cf. `utils.py::normalize_geoname()`)
- Les séries Banque mondiale (sources 6-10) sont **nationales** — pas de variation inter-préfecture. À utiliser comme contexte macro ou pour construire un proxy local justifié.
- Niveau d'analyse cible : **canton** (si shapefile dispo) ou **préfecture** (fallback).
