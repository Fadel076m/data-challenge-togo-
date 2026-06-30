"""
dashboard/figures.py
Factory des figures Plotly pour le dashboard IRAT — Agriculture Challenge Togo
"""

import json
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata
import re

# ── Palettes et constantes ────────────────────────────────────────
CAT_ORDER = ['Très résilient', 'Résilient', 'Moyen', 'Vulnérable', 'Très vulnérable']
CAT_COLORS = {
    'Très résilient':  '#1a7340',
    'Résilient':       '#52b788',
    'Moyen':           '#f4d03f',
    'Vulnérable':      '#e67e22',
    'Très vulnérable': '#c0392b',
}

MAP_CENTER = {'lat': 8.6, 'lon': 0.82}
MAP_ZOOM   = 5.5

SCORE_COLS   = ['Score_Eau', 'Score_Elevage', 'Score_Pisciculture', 'Score_Abattoirs', 'Score_Performance']
SCORE_LABELS = ['Eau', 'Élevage', 'Pisciculture', 'Abattoirs', 'Performance']


def _normalize(s):
    if pd.isna(s): return ''
    s = str(s).lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[\-/]', ' ', s)
    s = re.sub(r'\b(prefecture de|prefecture du|district de|commune de)\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def load_geojson(shp_path, df):
    """Fusionne le shapefile ADM2 avec df_final et retourne admin_gdf + admin_json."""
    admin2 = gpd.read_file(shp_path)
    admin2['pref_norm'] = admin2['adm2_name'].apply(_normalize)
    # S'assurer que df possède une colonne pref_norm pour la jointure
    df_copy = df.copy()
    if 'pref_norm' not in df_copy.columns:
        df_copy['pref_norm'] = df_copy['prefecture'].apply(_normalize)
    merged = admin2.merge(df_copy, on='pref_norm', how='left')
    clean  = merged.drop(columns=['valid_on', 'valid_to'], errors='ignore')
    return clean, json.loads(clean.to_json())


# ── Page Vue générale ─────────────────────────────────────────────

def fig_carte_irat(admin_gdf, admin_json):
    fig = px.choropleth_mapbox(
        admin_gdf, geojson=admin_json, locations=admin_gdf.index,
        color='IRAT', hover_name='prefecture',
        hover_data={'IRAT': ':.1f', 'Categorie': True, 'region': True},
        color_continuous_scale='RdYlGn', range_color=[0, 100],
        mapbox_style='carto-positron', zoom=MAP_ZOOM, center=MAP_CENTER, opacity=0.8,
        labels={'IRAT': 'Score IRAT'},
    )
    fig.update_layout(
        height=480, margin=dict(t=10, b=10, l=10, r=10),
        coloraxis_colorbar=dict(title='IRAT', tickvals=[0, 20, 40, 60, 80, 100]),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def fig_donut_categories(df):
    counts = df['Categorie'].value_counts().reindex(CAT_ORDER, fill_value=0)
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values, hole=0.55,
        marker_colors=[CAT_COLORS[c] for c in counts.index],
        textinfo='label+value',
        hovertemplate='<b>%{label}</b><br>%{value} préfecture(s)<extra></extra>',
    ))
    fig.update_layout(
        height=280, margin=dict(t=10, b=10, l=10, r=10), showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text=f'<b>{len(df)}</b><br>préf.', x=0.5, y=0.5,
                          font_size=14, showarrow=False)],
    )
    return fig


# ── Page Résilience ───────────────────────────────────────────────

def fig_bar_irat(df, highlight=None):
    df_s = df.sort_values('IRAT').copy()
    colors = [CAT_COLORS.get(c, '#888') for c in df_s['Categorie']]
    if highlight:
        colors = ['#2c7bb6' if p == highlight else c
                  for p, c in zip(df_s['prefecture'], colors)]
    fig = go.Figure(go.Bar(
        x=df_s['IRAT'], y=df_s['prefecture'], orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>IRAT: %{x:.1f}<extra></extra>',
    ))
    fig.add_vline(x=df['IRAT'].mean(), line_dash='dash', line_color='#555',
                  annotation_text=f"Moy. {df['IRAT'].mean():.1f}",
                  annotation_position='top right', annotation_font_size=11)
    fig.update_layout(
        height=700, xaxis=dict(title='Score IRAT (0-100)', range=[0, 105]),
        yaxis_title='', margin=dict(t=10, b=40, l=160, r=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def _hex_to_rgba(hex_color, alpha=0.2):
    """Convertit un hex (#rrggbb) en rgba(r,g,b,a) pour Plotly."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'


def fig_radar_prefecture(row):
    values = [row[c] for c in SCORE_COLS] + [row[SCORE_COLS[0]]]
    labels = SCORE_LABELS + [SCORE_LABELS[0]]
    color  = CAT_COLORS.get(row.get('Categorie', 'Moyen'), '#888')
    fig = go.Figure(go.Scatterpolar(
        r=values, theta=labels, fill='toself',
        fillcolor=_hex_to_rgba(color, 0.22), line=dict(color=color, width=2),
        hovertemplate='<b>%{theta}</b>: %{r:.1f}<extra></extra>',
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont_size=9)),
        height=300, margin=dict(t=20, b=20, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# ── Page Infrastructures ──────────────────────────────────────────

def fig_carte_infra(admin_gdf, admin_json, colonne, titre, scale='YlGn'):
    fig = px.choropleth_mapbox(
        admin_gdf, geojson=admin_json, locations=admin_gdf.index,
        color=colonne, hover_name='prefecture',
        hover_data={colonne: True, 'region': True},
        color_continuous_scale=scale,
        mapbox_style='carto-positron', zoom=MAP_ZOOM, center=MAP_CENTER, opacity=0.8,
    )
    fig.update_layout(
        title=dict(text=titre, font_size=13), height=400,
        margin=dict(t=35, b=5, l=5, r=5), paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def fig_bar_infra_region(df):
    infra_cols   = ['n_elevage', 'n_abattoirs', 'n_pisciculture', 'n_retenues_eau', 'n_barrages']
    infra_labels = ['Élevage', 'Abattoirs', 'Pisciculture', 'Retenues eau', 'Barrages']
    colors       = ['#006a4e', '#e8b400', '#2a7fb5', '#1a9c7c', '#8e7fc2']
    by_reg = df.groupby('region')[infra_cols].sum().reset_index()
    fig = go.Figure()
    for col, label, color in zip(infra_cols, infra_labels, colors):
        fig.add_trace(go.Bar(
            name=label, x=by_reg['region'], y=by_reg[col], marker_color=color,
            hovertemplate=f'<b>%{{x}}</b><br>{label}: %{{y}}<extra></extra>',
        ))
    fig.update_layout(
        barmode='stack', height=350, xaxis_title='', yaxis_title="Nb d'infrastructures",
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=40, b=40, l=50, r=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# ── Page Top 10 investissements ───────────────────────────────────

def fig_top10(df_top10):
    df_t = df_top10.reset_index().copy()
    # Colonne rang : index ou colonne 'rang'
    if 'rang' in df_t.columns:
        df_t['label'] = df_t.apply(lambda r: f"#{int(r['rang'])}  {r['prefecture']}", axis=1)
    else:
        df_t['label'] = df_t.apply(lambda r: f"#{r.name+1}  {r['prefecture']}", axis=1)
    df_t = df_t.sort_values('score_priorite')
    fig = go.Figure(go.Bar(
        x=df_t['score_priorite'], y=df_t['label'], orientation='h',
        marker=dict(
            color=df_t['IRAT'], colorscale='RdYlGn', cmin=0, cmax=100,
            colorbar=dict(title='IRAT', len=0.6), showscale=True,
        ),
        hovertemplate=(
            '<b>%{y}</b><br>Score priorité : %{x:.1f}<br>'
            'IRAT : %{marker.color:.1f}<extra></extra>'
        ),
    ))
    fig.update_layout(
        height=420, xaxis=dict(title="Score de priorité d'investissement", range=[0, 105]),
        yaxis_title='', margin=dict(t=10, b=40, l=200, r=20),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig
