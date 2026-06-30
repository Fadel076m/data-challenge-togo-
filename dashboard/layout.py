"""
dashboard/layout.py - Agriculture Challenge Togo AI Lab
Design : epure, moderne, Poppins, rouge minimise
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

VERT    = '#006a4e'
OR      = '#e8b400'
MUTED   = '#6b7c74'
BG      = '#f8fafb'
BORDER  = '#e8edf0'


def _kpi(label, value, sub='', accent=VERT):
    return html.Div([
        html.Div(value, className='kpi-value', style={'color': accent}),
        html.Div(label, className='kpi-label'),
        html.Div(sub,   className='kpi-sub'),
    ], className='kpi-card h-100')


def _ctx(text):
    """Legende contextuelle sous un graphique."""
    return html.Div(text, className='fig-context')


def build_layout(df, df_top10):
    n_elev   = int(df['n_elevage'].sum())
    n_ab     = int(df['n_abattoirs'].sum())
    n_pisc   = int(df['n_pisciculture'].sum())
    n_eau    = int(df['n_retenues_eau'].sum() + df['n_barrages'].sum())
    irat_moy = df['IRAT'].mean()
    n_vuln   = int((df['IRAT'] < 40).sum())
    dist_max = df['dist_abattoir_km'].max() if 'dist_abattoir_km' in df.columns else 0
    pref_opts  = [{'label': p, 'value': p} for p in sorted(df['prefecture'].dropna())]
    pref_worst = df.loc[df['IRAT'].idxmin(), 'prefecture']
    ratio_ab   = n_elev // max(n_ab, 1)

    # Navbar
    navbar = dbc.Navbar(
        dbc.Container([
            html.Img(src='/assets/logo_togo.svg', height='58px',
                     style={'marginRight': '16px', 'flexShrink': '0'}),
            dbc.NavbarBrand('Resilience Agricole & Infrastructures - Togo',
                            style={'fontWeight': '700', 'fontSize': '1.15rem'}),
            html.Div([
                html.Span('Togo AI Lab · Data Challenge · Defi 2',
                          style={'color': 'rgba(255,255,255,0.65)', 'fontSize': '0.75rem',
                                 'display': 'block'}),
                html.Span('Fadel ADAM · fadamgroup@gmail.com · +221 76 674 48 09',
                          style={'color': 'rgba(255,255,255,0.45)', 'fontSize': '0.7rem'}),
            ], style={'marginLeft': 'auto', 'textAlign': 'right'}),
        ], fluid=True),
        color=VERT, dark=True, sticky='top',
    )

    tricolor = html.Div(className='tricolor-band')

    insight_bar = html.Div([
        html.Span('4 092 infrastructures · ', style={'fontWeight': '700'}),
        html.Span(f'{n_elev:,} elevages (73.4%)', className='insight-pill'),
        html.Span(' · '),
        html.Span(f'{n_eau} ouvrages hydrauliques', className='insight-pill',
                  style={'borderColor': '#1a9c7c', 'color': '#0d5c47'}),
        html.Span(' · '),
        html.Span(f'{n_pisc} zones piscicoles', className='insight-pill',
                  style={'borderColor': '#2a7fb5', 'color': '#1a4f72'}),
        html.Span(' · '),
        html.Span(f'1 abattoir pour {ratio_ab} elevages', className='insight-pill',
                  style={'borderColor': OR, 'color': '#7a5900'}),
    ], className='insight-bar')

    tabs = dbc.Tabs([
        dbc.Tab(label='Vue generale',    tab_id='tab-general'),
        dbc.Tab(label='Resilience IRAT', tab_id='tab-resilience'),
        dbc.Tab(label='Infrastructures', tab_id='tab-infra'),
        dbc.Tab(label='Investissements', tab_id='tab-invest'),
        dbc.Tab(label='Storytelling',    tab_id='tab-story'),
    ], id='tabs', active_tab='tab-general')

    # Bloc IRAT definition
    irat_def = html.Div([
        html.Strong('IRAT '),
        html.Span('= Indice de Resilience Agricole Territoriale · Score 0-100 · '
                  'Formule : 30% Eau + 25% Elevage + 20% Pisciculture + 15% Abattoirs + 10% Performance. '
                  'Plus le score est eleve, plus la prefecture resiste aux chocs agricoles.'),
    ], className='irat-def')

    # Vue generale
    page_general = html.Div([
        irat_def,
        dbc.Row([
            dbc.Col(_kpi('Elevages', f'{n_elev:,}', '73.4% des infrastructures'), md=2),
            dbc.Col(_kpi('Abattoirs', str(n_ab), f'1 pour {ratio_ab} elevages', accent='#d4a017'), md=2),
            dbc.Col(_kpi('Pisciculture', str(n_pisc), '3.4% — levier sous-exploite', accent='#2a7fb5'), md=2),
            dbc.Col(_kpi('Eau', str(n_eau), 'barrages + retenues collinaires', accent='#1a9c7c'), md=2),
            dbc.Col(_kpi('IRAT moyen national', f'{irat_moy:.1f}', '/100 — seuil resilience = 60'), md=2),
            dbc.Col(_kpi('Zones vulnerables', str(n_vuln), 'IRAT < 40 / 40 prefectures', accent='#c0392b'), md=2),
        ], className='g-3 mb-3'),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader('Carte IRAT — Score de resilience par prefecture'),
                dbc.CardBody(dcc.Graph(id='carte-irat-general', config={'displayModeBar': False})),
                _ctx('Vert = resilient (IRAT > 60) · Jaune = moyen (40-60) · Rouge = vulnerable (< 40). '
                     'Survolez une prefecture pour voir son score. Cliquez pour le detail.'),
            ]), md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Repartition par niveau de resilience'),
                    dbc.CardBody(dcc.Graph(id='donut-categories', config={'displayModeBar': False})),
                    _ctx('5 categories : Tres resilient (>80) · Resilient (60-80) · '
                         'Moyen (40-60) · Vulnerable (20-40) · Tres vulnerable (<20).'),
                ]),
                html.Div([
                    html.Strong(f'{n_vuln}/40 prefectures vulnerables'),
                    html.Span(f' — IRAT < 40', style={'color': MUTED}),
                    html.Br(),
                    html.Span(f'Distance max a un abattoir : {dist_max:.0f} km',
                              style={'color': MUTED, 'fontSize': '0.8rem'}),
                ], className='callout-or', style={'marginTop': '12px'}),
            ], md=4),
        ], className='g-3'),
    ], style={'padding': '20px', 'backgroundColor': BG})

    # Resilience
    page_resilience = html.Div([
        irat_def,
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader('Classement IRAT — 40 prefectures (du plus vulnerable au plus resilient)'),
                dbc.CardBody(dcc.Graph(id='bar-irat', config={'displayModeBar': False})),
                _ctx('Chaque barre = une prefecture. Ligne pointillee = moyenne nationale. '
                     'Couleur : vert = resilient · orange = vulnerable · rouge = tres vulnerable. '
                     'La prefecture selectionnee est mise en bleu.'),
            ]), md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.Div([
                        html.Span('Profil detaille — '),
                        dcc.Dropdown(id='dropdown-prefecture', options=pref_opts,
                                     value=pref_worst, clearable=False,
                                     style={'display': 'inline-block', 'width': '200px',
                                            'verticalAlign': 'middle', 'fontSize': '0.84rem'}),
                    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'})),
                    dbc.CardBody([
                        html.Div(id='detail-prefecture'),
                        dcc.Graph(id='radar-prefecture', config={'displayModeBar': False}),
                        _ctx('Radar : chaque axe = 1 pilier IRAT (0-100). '
                             'Grande surface = prefecture forte sur ce pilier. '
                             "Pilier creux = levier d'investissement cible."),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader('Carte choroplethe — IRAT par prefecture'),
                    dbc.CardBody(dcc.Graph(id='carte-irat-resilience',
                                           config={'displayModeBar': False})),
                    _ctx('Survol = score IRAT + categorie + region.'),
                ], style={'marginTop': '12px'}),
            ], md=6),
        ], className='g-3'),
    ], style={'padding': '20px', 'backgroundColor': BG})

    # Infrastructures
    page_infra = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Repartition des infrastructures par region — 5 types d'equipements"),
                dbc.CardBody(dcc.Graph(id='bar-infra-region', config={'displayModeBar': False})),
                _ctx('Barres empilees : chaque couleur = 1 type. '
                     'Elevage (vert) domine toutes les regions. '
                     'Eau (teal) et Pisciculture (bleu) restent faibles dans le Nord.'),
            ]), md=12),
        ], className='g-3 mb-3'),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader('Selectionner la couche'),
                dbc.CardBody([
                    dcc.RadioItems(
                        id='radio-infra-layer',
                        options=[
                            {'label': ' Elevage — nb etablissements',    'value': 'n_elevage'},
                            {'label': ' Abattoirs — nb etablissements',  'value': 'n_abattoirs'},
                            {'label': ' Pisciculture — nb zones',        'value': 'n_pisciculture'},
                            {'label': ' Retenues eau — nb ouvrages',     'value': 'n_retenues_eau'},
                            {'label': ' Barrages — nb ouvrages',         'value': 'n_barrages'},
                            {'label': ' Distance abattoir (km)',         'value': 'dist_abattoir_km'},
                            {'label': ' Distance eau (km)',              'value': 'dist_eau_km'},
                        ],
                        value='n_elevage',
                        inputStyle={'marginRight': '6px'},
                        labelStyle={'display': 'block', 'marginBottom': '10px', 'fontSize': '0.83rem'},
                    ),
                    html.Hr(style={'margin': '10px 0'}),
                    html.Div('Distances : couleur claire = zone eloignee (risque). '
                             'Comptages : couleur foncee = zone bien equipee.',
                             style={'fontSize': '0.72rem', 'color': MUTED}),
                ]),
            ]), md=2),
            dbc.Col(dbc.Card([
                dbc.CardHeader('Carte — infrastructure selectionnee par prefecture'),
                dbc.CardBody(dcc.Graph(id='carte-infra', config={'displayModeBar': False})),
                _ctx('Survol = valeur exacte + region. Changez la couche a gauche pour explorer.'),
            ]), md=10),
        ], className='g-3'),
    ], style={'padding': '20px', 'backgroundColor': BG})

    # Investissements
    page_invest = html.Div([
        html.Div([
            html.Strong('Methodologie · '),
            html.Span("Score priorite = 70% vulnerabilite (IRAT bas) + 30% potentiel existant. "
                      "Une zone tres vulnerable avec un debut d'activite est priorisee sur une zone "
                      "aussi vulnerable mais sans aucune infrastructure de base."),
        ], className='callout-vert', style={'marginBottom': '16px', 'fontSize': '0.83rem'}),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader('Top 10 zones prioritaires pour investissement public'),
                dbc.CardBody(dcc.Graph(id='fig-top10', config={'displayModeBar': False})),
                _ctx('Longueur de barre = score de priorite. '
                     'Couleur = score IRAT actuel (rouge = tres vulnerable, vert = plus resilient). '
                     'Les zones en haut sont les plus urgentes.'),
            ]), md=6),
            dbc.Col(dbc.Card([
                dbc.CardHeader('Detail — score, categorie & justification'),
                dbc.CardBody(html.Div(id='table-top10'), style={'padding': '8px'}),
                _ctx("IRAT = resilience actuelle · Score priorite = urgence d'investissement."),
            ]), md=6),
        ], className='g-3'),
    ], style={'padding': '20px', 'backgroundColor': BG})

    # Storytelling
    story_insights = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Strong('73.4% des infrastructures sont des elevages. '),
            (f'{n_elev:,} etablissements sur 4 092. '
             'Base productive reelle, mais chaine de valeur incomplete sans abattage ni transformation.'),
        ]),
        dbc.ListGroupItem([
            html.Strong('Chaine de valeur incomplete : 1 abattoir pour 83 elevages. '),
            (f'{n_ab} abattoirs pour {n_elev:,} elevages. '
             f'15 prefectures sans aucun abattoir. '
             f'Distance maximale : {dist_max:.0f} km.'),
        ]),
        dbc.ListGroupItem([
            html.Strong(f'{n_pisc} zones piscicoles — levier de diversification sous-exploite. '),
            (f'{n_pisc} zones (3.4% des infrastructures), concentrees Plateaux/Maritime. '
             "Seul pilier diversifiant l'economie agricole hors elevage terrestre. "
             'Fort potentiel dans les zones riveraines (Mono, Zio, Lac Togo).'),
        ]),
        dbc.ListGroupItem([
            html.Strong(f'{n_eau} ouvrages hydrauliques — atout strategique a valoriser. '),
            (f'{n_eau} barrages et retenues collinaires. '
             'Conditionnent elevage (abreuvement), pisciculture (etangs) et cultures irriguees. '
             '20 prefectures ont un score Eau < 30/100.'),
        ]),
        dbc.ListGroupItem([
            html.Strong('80% des prefectures vulnerables (IRAT < 40). '),
            ("Potentiel elevage non soutenu par les infrastructures aval. "
             "Absence conjointe d'eau, d'abattoirs et de zones piscicoles."),
        ]),
        dbc.ListGroupItem([
            html.Strong('Un seul pole resilient : Agou (60/100). '),
            'Coexistence elevage + pisciculture + eau dans les Plateaux. Modele a repliquer.',
        ]),
        dbc.ListGroupItem([
            html.Strong('Plaine du Mo : cas critique (IRAT = 7.7). '),
            'Aucun abattoir, eau insuffisante, aucune zone piscicole. Priorite absolue.',
        ]),
        dbc.ListGroupItem([
            html.Strong('Savanes : fort potentiel pastoral, infrastructure quasi-absente. '),
            ("Fort elevage traditionnel, quasi-absence d'abattoirs, "
             "de retenues d'eau et de pisciculture."),
        ]),
    ], flush=True)

    story_reco = dbc.ListGroup([
        dbc.ListGroupItem([
            html.Strong('Court terme (0-2 ans) — Abattoirs. '),
            ('1 abattoir dans les 15 prefectures depourvues. '
             'Ratio cible : 30 elevages/abattoir. '
             'Priorite : Plaine du Mo, Naki-Ouest, Oti-Sud, Tchamba.'),
        ]),
        dbc.ListGroupItem([
            html.Strong('Court terme (0-2 ans) — Hydraulique. '),
            (f'{n_eau} ouvrages recenses. Rehabiliter en priorite les 20 prefectures '
             "avec score Eau < 30/100. L'eau est le prerequis de tout le reste."),
        ]),
        dbc.ListGroupItem([
            html.Strong('Moyen terme (2-5 ans) — Pisciculture hors Plateaux. '),
            (f'Etendre depuis les {n_pisc} zones actuelles vers Savanes (fleuve Oti) et Kara. '
             'Creer des etangs adosses aux retenues collinaires — double valorisation.'),
        ]),
        dbc.ListGroupItem([
            html.Strong('Long terme — Poles agro-industriels integres. '),
            ('Elevage + abattoir + transformation + commercialisation, '
             'eau et pisciculture comme piliers de resilience. '
             'Cible : 10 zones du Top 10.'),
        ]),
    ], flush=True)

    story_limits = dbc.ListGroup([
        dbc.ListGroupItem(
            'Date de collecte des donnees non precisee — certains etablissements ont pu evoluer.'),
        dbc.ListGroupItem(
            'Pilier Performance (10%) : proxy densite elevage — '
            'donnees Banque mondiale nationales, non ventilees par prefecture.'),
        dbc.ListGroupItem(
            'Kpendjal-Ouest (creee post-2021) rattachee a Kpendjal dans le shapefile HDX.'),
        dbc.ListGroupItem('Lome Commune (District autonome) incluse comme 40e entite.'),
    ], flush=True)

    page_story = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5('Enseignements cles — Elevage, Eau & Pisciculture',
                            style={'color': VERT, 'fontWeight': '700', 'marginBottom': '14px'}),
                    story_insights,
                    html.H5('Recommandations strategiques',
                            style={'color': VERT, 'fontWeight': '700',
                                   'marginTop': '24px', 'marginBottom': '14px'}),
                    story_reco,
                    html.H5('Limites methodologiques',
                            style={'color': MUTED, 'fontWeight': '700',
                                   'marginTop': '24px', 'marginBottom': '14px'}),
                    story_limits,
                ])
            ]), md=12),
        ], className='g-3'),
    ], style={'padding': '20px', 'backgroundColor': BG})

    footer = html.Footer([
        html.Span('Resilience Agricole Togo · Togo AI Lab Data Challenge Defi 2 · '),
        html.Span('Fadel ADAM · fadamgroup@gmail.com · +221 76 674 48 09 · '),
        html.Span('Sources : geodata.gouv.tg · opendata.gouv.tg · HDX INSEED/ITOS'),
    ], className='dashboard-footer')

    layout = html.Div([
        navbar, tricolor, insight_bar, tabs,
        html.Div(id='tab-content', style={'minHeight': '80vh', 'backgroundColor': BG}),
        footer,
    ])

    return layout, {
        'general':    page_general,
        'resilience': page_resilience,
        'infra':      page_infra,
        'invest':     page_invest,
        'story':      page_story,
    }
