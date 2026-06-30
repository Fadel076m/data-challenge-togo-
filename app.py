"""
app.py — Dashboard Résilience Agricole Territoriale — Togo AI Lab Data Challenge Défi 2
Auteur : Fadel ADAM · fadamgroup@gmail.com
Lancer : python app.py  →  http://localhost:8050
"""

import pandas as pd
from pathlib import Path
import dash
import dash_bootstrap_components as dbc

from dashboard.figures import load_geojson
from dashboard.layout import build_layout
from dashboard.callbacks import register_callbacks

# ── Chemins ──────────────────────────────────────────────────────
BASE    = Path(__file__).parent
PROC    = BASE / 'data' / 'processed'
HDX_DIR = BASE / 'data' / 'raw' / 'admin_togo_hdx'

# ── Chargement des données ────────────────────────────────────────
print('Chargement des données...')
df     = pd.read_csv(PROC / 'df_final.csv')
top10  = pd.read_csv(PROC / 'top10_investissement.csv')

print(f'  df_final    : {len(df)} préfectures')
print(f'  top10       : {len(top10)} zones')

print('Chargement du shapefile...')
admin_gdf, admin_json = load_geojson(HDX_DIR / 'tgo_admin2.shp', df)
print(f'  Shapefile   : {len(admin_gdf)} entités')

# ── Initialisation Dash ───────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title='Résilience Agricole Togo',
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
)

# ── Layout ────────────────────────────────────────────────────────
layout, _ = build_layout(df, top10)
app.layout = layout

# ── Callbacks ─────────────────────────────────────────────────────
register_callbacks(app, df, top10, admin_gdf, admin_json)

# ── Exposition WSGI (Gunicorn / Render) ──────────────────────────
server = app.server

# ── Lancement ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print('\n✓ Dashboard prêt → http://localhost:8050\n')
    app.run(debug=False, port=8050)
