import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

# External stylesheets (Bootstrap + Bootstrap Icons)
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # útil si despliegas en la nube

# -------------------------
# Sidebar con Bootstrap Icons
# -------------------------
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [html.I(className="bi bi-speedometer2 me-2"), "Overview"],
            href="/overview",
            active="exact",
        ),
        dbc.NavLink(
            [html.I(className="bi bi-bar-chart-line me-2"), "Demanda"],
            href="/demand",
            active="exact",
        ),
        dbc.NavLink(
            [html.I(className="bi bi-building me-2"), "Oferta"],
            href="/supply",
            active="exact",
        ),
        dbc.NavLink(
            [html.I(className="bi bi-diagram-3 me-2"), "Régimen"],
            href="/regime",
            active="exact",
        ),
    ],
    vertical=True,
    pills=True,
    className="bg-light vh-100 p-3 sidebar",
)

# -------------------------
# Área de contenido (dinámica)
# -------------------------
content = html.Div(id="page-content", className="p-4")

# -------------------------
# Layout principal
# -------------------------
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),  # almacena la ruta actual
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(content, width=10),
            ]
        ),
    ],
    fluid=True,
)

# -------------------------
# Callbacks de enrutamiento
# -------------------------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/overview":
        return html.H4("Página de Overview (esqueleto)")
    elif pathname == "/demand":
        return html.H4("Página de Demanda (esqueleto)")
    elif pathname == "/supply":
        return html.H4("Página de Oferta (esqueleto)")
    elif pathname == "/regime":
        return html.H4("Página de Régimen (esqueleto)")
    else:
        # Ruta desconocida
        return html.Div(
            [
                html.H4("404 - Página no encontrada"),
                html.P("Seleccione una opción en la barra lateral para continuar."),
            ]
        )

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8060)
