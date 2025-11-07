from dash import html, dcc
import dash_bootstrap_components as dbc

def kpi_card(title, id_value):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, className="text-muted small"),
            html.H3(id=id_value, className="mb-0 fw-bold"),
        ]),
        className="shadow-sm sneat-card"
    )

layout = dbc.Container(
    [
        # NAVBAR
        dbc.Navbar(
            dbc.Container([
                html.Div("informed_economist", className="navbar-brand fw-bold"),
                dbc.NavbarToggler(id="navbar-toggler"),
            ]),
            color="light",
            className="mb-3 rounded-3 shadow-sm sneat-navbar"
        ),

        # FILTROS
        dbc.Row([
            dbc.Col(dbc.Select(
                id="metric-select",
                options=[{"label":"YoY (%)","value":"YoY"},{"label":"QoQ (%)","value":"QoQ"}],
                value="YoY"
            ), md=2),
            dbc.Col(dbc.Select(
                id="scope-select",
                options=[{"label":"Gasto (C,I,G,X,M)","value":"componentes"},
                         {"label":"Industrias","value":"actividades"}],
                value="componentes"
            ), md=3),
            dbc.Col(dbc.Select(id="subgroup-select", options=[], placeholder="Subgrupo (opcional)"), md=4),
            dbc.Col(dbc.Button("Actualizar", id="apply-filters", color="primary"), md=2),
        ], className="g-3 mb-2"),

        # KPIs
        dbc.Row([
            dbc.Col(kpi_card("Mediana", "kpi-median"), md=3),
            dbc.Col(kpi_card("% positivo", "kpi-positive-share"), md=3),
            dbc.Col(kpi_card("IQR (p75–p25)", "kpi-iqr"), md=3),
            dbc.Col(kpi_card("Observaciones", "kpi-n"), md=3),
        ], className="g-3 mb-3"),

        # GRÁFICOS
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Distribución por Gobierno", className="card-title"),
                dcc.Loading(dcc.Graph(id="fig-violin"), type="dot"),
            ]), className="shadow-sm sneat-card"), md=12)
        ], className="g-3"),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Mediana por Gobierno", className="card-title"),
                dcc.Loading(dcc.Graph(id="fig-bars"), type="dot"),
            ]), className="shadow-sm sneat-card"), md=12)
        ], className="g-3 mt-1"),

        html.Hr(),
        html.Footer("© informed_economist", className="text-center text-muted my-4"),
    ],
    fluid=True,
    className="p-3 app-bg"
)
