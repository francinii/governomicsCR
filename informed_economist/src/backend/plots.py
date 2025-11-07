from typing import Optional, Dict, List, Iterable
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import Optional, Dict, List, Iterable
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# Helpers de color
# =========================================================
def _build_color_map(
    categories: Iterable[str],
    colors: Optional[Dict[str, str]] = None,
    fallback_palette: Optional[List[str]] = None,
) -> Dict[str, str]:
    """
    Devuelve un dict {categoria: color}. Si 'colors' ya define algunas, se respetan.
    El resto se completa con una paleta de respaldo.
    """
    categories = list(dict.fromkeys(categories))  # preserva orden
    cmap = {} if colors is None else colors.copy()
    if fallback_palette is None:
        # Paleta neutra: 10 tonos; se recicla si hay más categorías
        fallback_palette = [
            "#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#76B7B2",
            "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"
        ]
    i = 0
    for c in categories:
        if c not in cmap or cmap[c] is None:
            cmap[c] = fallback_palette[i % len(fallback_palette)]
            i += 1
    return cmap

# =========================================================
# Layout base con template
# =========================================================
def _configure_layout(
    fig: go.Figure,
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    y_round: int = 1,
    y_suffix: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    showlegend: bool = True,
    legend_y: float = -0.2,
    template: str = "plotly_white",   # estilo predefinido
    show_y_grid: bool = False,         # líneas horizontales tenues
) -> None:
    tickformat = f",.{y_round}f"
    yaxis_kwargs = {
        "tickformat": tickformat,
        "showgrid": show_y_grid,
        "gridcolor": "#E5E5E5",
        "gridwidth": 0.8,
        "zeroline": False,
    }
    if y_suffix:
        yaxis_kwargs["ticksuffix"] = y_suffix

    fig.update_layout(
        template=template,
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        width=width,
        height=height,
        showlegend=showlegend,
        legend=dict(
            orientation="h", yanchor="bottom", y=legend_y, xanchor="center", x=0.5
        ),
        xaxis=dict(showgrid=False),
        yaxis=yaxis_kwargs,
        bargap=0.1,
        margin=dict(l=60, r=30, t=60, b=80),
        plot_bgcolor="white",   # para templates claros
        paper_bgcolor="white",
    )

# =========================================================
# Barplot general para series de tiempo
# =========================================================
def plot_timeseries_bars(
    df: pd.DataFrame,
    y_col: str,
    category_col: Optional[str] = None,     # p.ej. 'Label', 'President', 'Party'
    index_col: Optional[str] = None,        # si None usa el índice
    title: Optional[str] = None,
    x_title: Optional[str] = None,
    y_title: Optional[str] = None,
    y_round: int = 1,
    y_suffix: Optional[str] = None,
    start: Optional[pd.Timestamp] = None,   # recorte opcional (inicio)
    end: Optional[pd.Timestamp] = None,     # recorte opcional (fin)
    width: Optional[int] = None,
    height: Optional[int] = None,
    colors: Optional[Dict[str, str]] = None,# dict {categoria: "#RRGGBB"}
    zero_line: bool = True,                 # línea horizontal en y=0
    showlegend: bool = True,
    template: str = "plotly_white",         # estilo predefinido
    show_y_grid: bool = False,               # líneas horizontales tenues
) -> go.Figure:
    """
    Grafica barras por fecha (x) y valor (y_col). Si 'category_col' está definido,
    crea una traza por categoría (coloreadas y con leyenda).
    """
    # Preparar datos y eje X
    data = df.copy()
    if index_col is not None:
        data = data.set_index(index_col)
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index, errors="coerce")
    data = data.sort_index()

    # Recorte por fechas (si aplica)
    if start is not None:
        data = data[data.index >= pd.to_datetime(start)]
    if end is not None:
        data = data[data.index <= pd.to_datetime(end)]

    fig = go.Figure()

    # Barras (una o múltiples por categoría)
    if category_col and category_col in data.columns:
        cats = data[category_col].astype(str).fillna("N/D")
        cmap = _build_color_map(categories=cats.unique().tolist(), colors=colors)

        # Una traza por categoría, preservando orden temporal
        for cat in cats.unique():
            sub = data[cats == cat]
            fig.add_trace(
                go.Bar(
                    x=sub.index,
                    y=sub[y_col],
                    name=str(cat),
                    marker_color=cmap[str(cat)],
                    showlegend=showlegend,
                )
            )
    else:
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data[y_col],
                name=y_col,
                marker_color="#4E79A7",
                showlegend=showlegend,
            )
        )

    if zero_line:
        fig.add_hline(y=0, line_width=1, line_dash="solid", line_color="gray")

    _configure_layout(
        fig=fig,
        title=title,
        x_title=x_title,
        y_title=y_title,
        y_round=y_round,
        y_suffix=y_suffix,
        width=width,
        height=height,
        showlegend=showlegend,
        template=template,        # aplica el template aquí
        show_y_grid=show_y_grid,  # controla grilla horizontal
    )

    return fig

def plot_bar_subplots_by_administration(df, variables, colors, title, y_title = "Promedio (%)", x_title = "Posiciones", show = False):
    """
    Generate grouped bar charts by presidential administration for one or more variables.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame where:
            - The index contains presidential administrations (e.g., "Alvarado", "Solís", ...).
            - The columns contain numerical variables to plot (e.g., "Consumo Hogares", "Inversión").
            Each cell should represent a summary statistic (e.g., mean, median, percentile, etc.)
            of the variable for the given administration.

        Example structure:
                          Consumo Hogares  Consumo Gobierno  Inversión  Exportaciones  Importaciones
        Administración
        Alvarado                   64.2              14.8       19.5           34.7           33.8
        Solís                      65.1              14.5       18.8           35.2           34.1
        ...

    variables : list of str
        List of column names from `df` to be plotted as subplots.
    title : str
        Title of the entire figure.
    y_title : str, optional (default="Promedio (%)")
        Label for the y-axis (only shown on the first subplot).
    show : bool, optional (default=False)
        If True, immediately displays the figure. If False, only returns the figure.

    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        A Plotly Figure object with subplots of bar charts. Each subplot corresponds
        to one variable in `variables`, and bars are ranked from highest to lowest
        across administrations. Bar colors are consistent by administration and linked
        in the legend for interactive filtering.

    Notes
    -----
    - Bars are ordered from highest to lowest value per variable.
    - The x-axis shows the ranking position (1, 2, 3, ...), not the administration names,
      to avoid redundancy. Administration names are instead displayed in the legend and tooltips.
    - Colors must be provided via a global `colors` dictionary mapping administration names to hex codes.
    """
    fig = make_subplots(
        rows=1, cols=len(variables),
        subplot_titles=variables,
        horizontal_spacing=0.04
    )

    ymax = (df.max().max()) * 1.2

    # Para controlar la leyenda: trackeamos si ya agregamos cada presidente
    legend_added = set()

    for idx, var in enumerate(variables, start=1):
        # Orden de mayor a menor y construcción de ranking 1..N
        s = df[var].sort_values(ascending=False)
        pres_labels = s.index.tolist()          # nombres de presidentes (para leyenda/hover)
        y_vals = s.values.tolist()
        positions = list(range(1, len(s) + 1))  # 1, 2, 3, ...
        bar_colors = [colors.get(lbl, "#4E79A7") for lbl in pres_labels]

        for pos, lbl, y, c in zip(positions, pres_labels, y_vals, bar_colors):
            fig.add_trace(
                go.Bar(
                    x=[str(pos)],               # mostramos posición en el eje X
                    y=[y],
                    marker_color=c,
                    name=lbl,
                    legendgroup=lbl,            # vincula todas las trazas del mismo presidente
                    hovertemplate=(
                        f"<b>{lbl}</b><br>{var}: {y:.2f}"
                        f"<br>Posición: {pos}<extra></extra>"
                    ),
                    showlegend=lbl not in legend_added,
                    text=[f"{y:.1f}"],          # valor sobre la barra
                    textposition="outside",
                    textfont=dict(size=11, color = 'steelblue')
                ),
                row=1, col=idx
            )
            legend_added.add(lbl)

        fig.update_xaxes(
            row=1, col=idx,
            tickangle=0,
            tickfont=dict(size=12, color="steelblue"), # color y tamaño de los valores del eje
            showticklabels=True,
            title_text = x_title,
            title_font=dict(size=12, color="salmon"),  # color y tamaño del título del eje
            
        )
        fig.update_yaxes(
            row=1, col=idx,
            title_text=y_title if idx == 1 else None,
            title_font=dict(size=13, color="salmon"),
            showgrid=True, gridcolor="#FAF7F7",
            range=[0, ymax],
            showticklabels=False
        )

    for anno in fig['layout']['annotations']:
        anno['font'] = dict(size=13.5, color="salmon")

    # --- Layout con leyenda horizontal abajo ---
    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=title,
            x=0.5, xanchor="center",
            font=dict(size=18, color="steelblue")
        ),
        bargap=0.1,
        width=900,
        height=500,
        margin=dict(l=60, r=30, t=80, b=100),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=13, color="steelblue")
        )
    )

    if show:
        fig.show()
    
    return fig


def plot_stacked_bars(
    df: pd.DataFrame,
    category_columns: list[str],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    colors: list[str] | None = None,
    legend_title: str = "Categories",
    barmode: str = "relative",
    title_size: int = 16,
    axis_label_size: int = 14,
    legend_size: int = 12,
    width: int = 900,
    height: int = 500,
    decimals: int = 1,
    as_percent: bool = False,  # 👈 nuevo parámetro
):
    """
    Stacked/grouped bar chart con opción de graficar porcentajes.
    """

    # Validaciones rápidas
    missing = [c for c in category_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Columnas no encontradas en df: {missing}")

    df_plot = df.copy()

    # --- Si se solicita graficar como porcentaje ---
    if as_percent:
        df_sum = df_plot[category_columns].sum(axis=1)
        df_plot[category_columns] = (
            df_plot[category_columns].div(df_sum, axis=0) * 100
        )  # convierte a %
        ylabel = ylabel or "Porcentaje (%)"
        decimals = 1

    fig = go.Figure()

    if colors is None:
        colors = [None] * len(category_columns)
    elif len(colors) != len(category_columns):
        raise ValueError("colors debe tener la misma longitud que category_columns")

    for column, color in zip(category_columns, colors):
        yvals = pd.to_numeric(df_plot[column], errors="coerce").round(decimals)
        fig.add_trace(
            go.Bar(
                x=df_plot.index,
                y=yvals,
                name=column,
                marker=dict(color=color) if color else None,
            )
        )

    # Layout general
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_size)),
        width=width,
        height=height,
        barmode=barmode,
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.3,
            xanchor="center",
            yanchor="top",
            font=dict(size=legend_size),
        ),
        legend_title=dict(text=legend_title, font=dict(size=legend_size)),
        margin=dict(l=40, r=40, t=60, b=90),
    )

    fig.update_xaxes(
        title_text=xlabel,
        title_font=dict(size=axis_label_size),
        tickangle=-45,
    )

    tickfmt = f",.{decimals}f"
    if as_percent:
        tickfmt = ".1f"  # sin separadores, solo decimales
    fig.update_yaxes(
        title_text=ylabel,
        title_font=dict(size=axis_label_size),
        tickformat=tickfmt,
    )

    return fig