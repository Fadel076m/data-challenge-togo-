"""
dashboard/callbacks.py
Callbacks Dash — Agriculture Challenge Togo AI Lab
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, html
import plotly.graph_objects as go

from dashboard.figures import (
    fig_carte_irat, fig_donut_categories, fig_bar_irat, fig_radar_prefecture,
    fig_carte_infra, fig_bar_infra_region, fig_top10, CAT_COLORS,
)

LAYER_TITLES = {
    'n_elevage':         'Élevage — nb établissements',
    'n_abattoirs':       'Abattoirs — nb établissements',
    'n_pisciculture':    'Pisciculture — nb zones',
    'n_retenues_eau':    'Retenues d\'eau — nb',
    'n_barrages':        'Barrages — nb',
    'dist_abattoir_km':  'Distance à l\'abattoir le plus proche (km)',
    'dist_eau_km':       'Distance à l\'infra hydraulique la plus proche (km)',
}

LAYER_SCALES = {
    'n_elevage': 'YlGn', 'n_abattoirs': 'OrRd', 'n_pisciculture': 'Blues',
    'n_retenues_eau': 'GnBu', 'n_barrages': 'Purples',
    'dist_abattoir_km': 'RdYlGn_r', 'dist_eau_km': 'RdYlBu_r',
}


def register_callbacks(app, df, df_top10, admin_gdf, admin_json):
    """Enregistre tous les callbacks Dash."""

    # ── Navigation onglets ────────────────────────────────────────
    from dashboard.layout import build_layout
    _, pages = build_layout(df, df_top10)

    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'active_tab')
    )
    def render_tab(active_tab):
        mapping = {
            'tab-general':    pages['general'],
            'tab-resilience': pages['resilience'],
            'tab-infra':      pages['infra'],
            'tab-invest':     pages['invest'],
            'tab-story':      pages['story'],
        }
        return mapping.get(active_tab, pages['general'])

    # ── Page Vue générale ─────────────────────────────────────────
    @app.callback(
        Output('carte-irat-general', 'figure'),
        Output('donut-categories', 'figure'),
        Input('tabs', 'active_tab')
    )
    def update_general(tab):
        return fig_carte_irat(admin_gdf, admin_json), fig_donut_categories(df)

    # ── Page Résilience ───────────────────────────────────────────
    @app.callback(
        Output('bar-irat', 'figure'),
        Output('carte-irat-resilience', 'figure'),
        Output('radar-prefecture', 'figure'),
        Output('detail-prefecture', 'children'),
        Input('dropdown-prefecture', 'value'),
    )
    def update_resilience(pref):
        row = df[df['prefecture'] == pref].iloc[0] if pref and pref in df['prefecture'].values else df.iloc[0]
        cat    = row.get('Categorie', '')
        color  = CAT_COLORS.get(cat, '#888')
        detail = dbc.Row([
            dbc.Col([
                html.H5(row['prefecture'], style={'fontWeight': '700', 'marginBottom': '2px'}),
                html.Small(f"Région : {row['region']}", style={'color': '#666'}),
            ]),
            dbc.Col([
                html.H3(f"{row['IRAT']:.1f}", style={'color': color, 'fontWeight': '700',
                                                      'marginBottom': '0'}),
                html.Small('Score IRAT'),
            ], style={'textAlign': 'center'}),
            dbc.Col([
                dbc.Badge(cat, style={'backgroundColor': color, 'fontSize': '0.85rem',
                                      'padding': '6px 12px'}),
            ], style={'textAlign': 'right', 'paddingTop': '8px'}),
        ], className='mb-3 align-items-center')
        return (
            fig_bar_irat(df, highlight=pref),
            fig_carte_irat(admin_gdf, admin_json),
            fig_radar_prefecture(row),
            detail,
        )

    # ── Page Infrastructures ──────────────────────────────────────
    @app.callback(
        Output('bar-infra-region', 'figure'),
        Output('carte-infra', 'figure'),
        Input('radio-infra-layer', 'value'),
    )
    def update_infra(layer):
        titre = LAYER_TITLES.get(layer, layer)
        scale = LAYER_SCALES.get(layer, 'YlGn')
        return fig_bar_infra_region(df), fig_carte_infra(admin_gdf, admin_json, layer, titre, scale)

    # ── Page Investissements ──────────────────────────────────────
    @app.callback(
        Output('fig-top10', 'figure'),
        Output('table-top10', 'children'),
        Input('tabs', 'active_tab'),
    )
    def update_invest(tab):
        # Tableau détail Top 10
        rows = []
        for _, row in df_top10.iterrows():
            rang = row.get('rang', row.name)
            rows.append(
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col(
                            html.Strong(f"#{int(rang)} {row['prefecture']}",
                                        style={'color': CAT_COLORS.get(row['Categorie'], '#888')}),
                            md=5),
                        dbc.Col(
                            html.Span(f"IRAT {row['IRAT']:.1f} · Priorité {row['score_priorite']:.1f}",
                                      style={'fontSize': '0.8rem', 'color': '#555'}),
                            md=4),
                        dbc.Col(
                            dbc.Badge(row['Categorie'],
                                      style={'backgroundColor': CAT_COLORS.get(row['Categorie'], '#888'),
                                             'fontSize': '0.7rem'}),
                            md=3, style={'textAlign': 'right'}),
                    ]),
                    html.Small(row.get('justification', ''), style={'color': '#777', 'display': 'block',
                                                                     'marginTop': '2px'}),
                ])
            )
        table = dbc.ListGroup(rows, flush=True, style={'fontSize': '0.85rem'})
        return fig_top10(df_top10), table
