from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Mapping, Hashable, Optional, List, Literal, Union, Dict, Iterable, Tuple
from plotly.colors import qualitative as pq
from plotly.subplots import make_subplots

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

def plot_bar_subplots_by_administration(
    df, 
    variables, 
    colors, 
    title, 
    y_title="Promedio (%)", 
    x_title="Posiciones",
    show=False,
    fig_width: int = None,
    fig_height: int = None
):
    """
    Generate grouped bar charts by presidential administration for one or more variables.
    Now supports controlling figure width and height.

    Parameters
    ----------
    df : pandas.DataFrame
        ...

    fig_width : int, optional
        Width of the figure in pixels. If None, defaults to 900.

    fig_height : int, optional
        Height of the figure in pixels. If None, defaults to 500.
    """

    fig = make_subplots(
        rows=1,
        cols=len(variables),
        subplot_titles=variables,
        horizontal_spacing=0.04
    )

    ymax = (df.max().max()) * 1.2
    legend_added = set()

    for idx, var in enumerate(variables, start=1):
        s = df[var].sort_values(ascending=False)

        pres_labels = s.index.tolist()
        y_vals = s.values.tolist()
        positions = list(range(1, len(s) + 1))
        bar_colors = [colors.get(lbl, "#4E79A7") for lbl in pres_labels]

        for pos, lbl, y, c in zip(positions, pres_labels, y_vals, bar_colors):
            fig.add_trace(
                go.Bar(
                    x=[str(pos)],
                    y=[y],
                    marker_color=c,
                    name=lbl,
                    legendgroup=lbl,
                    hovertemplate=(
                        f"<b>{lbl}</b><br>{var}: {y:.2f}"
                        f"<br>Posición: {pos}<extra></extra>"
                    ),
                    showlegend=lbl not in legend_added,
                    text=[f"{y:.1f}"],
                    textposition="outside",
                    textfont=dict(size=11, color='steelblue')
                ),
                row=1, col=idx
            )
            legend_added.add(lbl)

        fig.update_xaxes(
            row=1, col=idx,
            tickangle=0,
            tickfont=dict(size=12, color="steelblue"),
            showticklabels=True,
            title_text=x_title,
            title_font=dict(size=12, color="salmon"),
        )

        fig.update_yaxes(
            row=1, col=idx,
            title_text=y_title if idx == 1 else None,
            title_font=dict(size=13, color="salmon"),
            showgrid=True,
            gridcolor="#FAF7F7",
            range=[0, ymax],
            showticklabels=False
        )

    # Uniformar estilo de títulos de subplots
    for anno in fig['layout']['annotations']:
        anno['font'] = dict(size=13.5, color="salmon")

    # Layout general
    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=title,
            x=0.5, xanchor="center",
            font=dict(size=18, color="steelblue")
        ),
        bargap=0.1,
        width=fig_width if fig_width is not None else 900,
        height=fig_height if fig_height is not None else 500,
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
    category_columns,
    title: str = '',
    xlabel: str = '',
    ylabel: str = '',
    colors=None,
    legend_title: str = 'Categories',
    barmode: str = 'relative',
    title_size: int = 16,
    axis_label_size: int = 14,
    legend_size: int = 12,
    width: int = 900,
    height: int = 500,
    decimals: int = 0
):
    """
    Plots a stacked or grouped bar chart using Plotly with a horizontal legend.
    """
    fig = go.Figure()

    # Colores por defecto (Plotly auto-asigna si None)
    if colors is None:
        colors = [None] * len(category_columns)

    # Trazas por categoría
    for column, color in zip(category_columns, colors):
        fig.add_trace(go.Bar(
            x=df.index,
            y=df[column].round(decimals),
            name=column,
            marker=dict(color=color) if color else None
        ))

    # Layout actualizado (sin titlefont)
    fig.update_layout(
        title=dict(text=title, font=dict(size=title_size)),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=axis_label_size)),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(size=axis_label_size)),
            tickformat=f",.{decimals}f"
        ),
        width=width,
        height=height,
        barmode=barmode,  # 'relative' (stacked) o 'group'
        legend=dict(
            orientation="h",
            x=0.5, y=-0.3,
            xanchor="center", yanchor="top",
            font=dict(size=legend_size)
        ),
        legend_title=dict(text=legend_title, font=dict(size=legend_size)),
        margin=dict(l=40, r=40, t=60, b=90)
    )

    return fig


def format_y_axis(fig: go.Figure, decimals: int = 2, secondary_decimals: int | None = None) -> None:
    """
    Formatea ejes Y (primario y secundario si existe) con miles y decimales.
    """
    fig.update_layout(yaxis=dict(tickformat=f",.{decimals}f"))
    if "yaxis2" in fig.layout and fig.layout.yaxis2 is not None:
        s = secondary_decimals if secondary_decimals is not None else decimals
        fig.update_layout(yaxis2=dict(tickformat=f",.{s}f"))

def simple_linegraph(
    df: pd.DataFrame,
    y_columns,
    title: str = '',
    title_color: str = "black",
    xaxis_title: str = '',
    yaxis_title: str = '',
    width: int = 700,
    height: int = 300,
    decimals: int = 2,
    secondary_y: str | None = None,
    secondary_y_title: str = '',
    line_colors: list[str] | None = None,
    yaxis_title_color: str = "black",
    secondary_yaxis_title_color: str = "black"
) -> go.Figure:
    """
    Crea un gráfico de líneas con soporte para eje Y secundario y formateo.
    """
    fig = go.Figure()

    if isinstance(y_columns, str):
        y_columns = [y_columns]

    if line_colors is None:
        line_colors = [None] * len(y_columns)
    if len(line_colors) != len(y_columns):
        raise ValueError("The number of colors provided must match the number of y_columns.")

    # Series
    for column, color in zip(y_columns, line_colors):
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            name=column,
            line=dict(color=color) if color else None,
            yaxis="y2" if (secondary_y and column == secondary_y) else "y"
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(color=title_color)),
        xaxis=dict(title=dict(text=xaxis_title)),
        yaxis=dict(
            title=dict(text=yaxis_title, font=dict(color=yaxis_title_color))
        ),
        width=width,
        height=height,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            x=0.5, y=-0.2,
            xanchor="center", yanchor="top"
        )
    )

    # Eje secundario (si aplica)
    if secondary_y:
        fig.update_layout(
            yaxis2=dict(
                title=dict(
                    text=secondary_y_title if secondary_y_title else secondary_y,
                    font=dict(color=secondary_yaxis_title_color)
                ),
                overlaying="y",
                side="right",
                showgrid=False
            )
        )

    # Formato de miles/decimales en Y (y Y2 si existe)
    format_y_axis(fig, decimals=decimals)

    return fig

def create_pie_chart(df, names_column, values_column, title_text, subtitle_text):
    """
    Crea un gráfico de pastel y actualiza el layout para centrar el título y añadir un subtítulo.

    Args:
    df (pd.DataFrame): DataFrame con los datos para el gráfico de pastel.
    names_column (str): Nombre de la columna que contiene las categorías.
    values_column (str): Nombre de la columna que contiene los valores.
    title_text (str): Texto para el título del gráfico.
    subtitle_text (str): Texto para el subtítulo del gráfico.

    Returns:
    go.Figure: Objeto de figura de Plotly.
    """
    # Ordenar el DataFrame de mayor a menor según los valores
    df = df.sort_values(by=values_column, ascending=False)

    # Crear el gráfico de pastel
    fig = px.pie(df, names=names_column, values=values_column)

    # Actualizar el layout para centrar el título, añadir el subtítulo y ubicar las leyendas debajo del gráfico
    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 30}
        },
        annotations=[
            dict(
                text=subtitle_text,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=1,
                xanchor='center',
                yanchor='bottom',
                font=dict(size=14)
            )
        ],
        margin=dict(t=120),  # Añadir margen superior para evitar solapamiento
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,  # Posición debajo del gráfico
            xanchor="center",
            x=0.5
        )
    )

    return fig


def plot_bars(
    data: pd.Series | pd.DataFrame,
    *,
    category_col: str | None = None,
    value_col: str | None = None,
    group_labels: Optional[Mapping[str, Hashable] | pd.Series] = None,

    orientation: str = "h",               # "h" horizontal | "v" vertical
    color_mode: str = "single",           # "single" | "by_groups"
    bar_color: str = "rgb(33,150,243)",
    palette: Optional[Mapping[Hashable, str]] = None,
    bar_opacity: float = 0.95,
    show_group_legend: bool = True,

    sort: str = "desc",                   # "none" | "asc" | "desc" | "abs_desc"
    top_n: int | None = None,

    show_labels: bool = True,
    decimals: int = 1,
    label_with_sign: bool = False,
    label_suffix: str = "",
    custom_hovertemplate: str | None = None,
    subtitle: str | None = None,

    title: str = "Bar Chart",
    xaxis_title: str = "",
    yaxis_title: str = "",
    value_axis_tickformat: str | None = None,
    category_tickangle: int = 0,

    width: int = 950,
    height: int = 600,
    title_size: int = 20,
    axis_label_size: int = 14,
    margins: tuple[int, int, int, int] = (80, 40, 90, 60),

    show_zero_line: bool = True,
    zero_line_dash: str = "dot",
    zero_line_color: str = "rgba(120,120,120,0.6)",
):
    # ---- Normalizar a Serie ----
    if isinstance(data, pd.Series):
        s = data.copy().dropna()
    else:
        if category_col is None or value_col is None:
            raise ValueError("With DataFrame, `category_col` and `value_col` are required.")
        s = pd.Series(data[value_col].values, index=data[category_col].values).dropna()

    # ---- Orden y top_n ----
    if sort == "asc":
        s = s.sort_values(ascending=True)
    elif sort == "desc":
        s = s.sort_values(ascending=False)
    elif sort == "abs_desc":
        s = s.reindex(s.abs().sort_values(ascending=False).index)
    elif sort != "none":
        raise ValueError("sort must be one of: 'none','asc','desc','abs_desc'")

    if top_n is not None:
        s = s.iloc[:top_n]

    categories = s.index.tolist()
    values = s.values.tolist()

    # ---- Etiquetas ----
    sign = "+" if label_with_sign else ""
    label_fmt = f"{sign}{{v:.{decimals}f}}{label_suffix}"
    labels = [label_fmt.format(v=v) for v in values] if show_labels else None

    # ---- Hover ----
    if custom_hovertemplate is None:
        hover_tmpl = (
            ("<b>%{y}</b><br>Valor: %{x:." + str(decimals) + "f}" + label_suffix + "<extra></extra>")
            if orientation == "h"
            else ("<b>%{x}</b><br>Valor: %{y:." + str(decimals) + "f}" + label_suffix + "<extra></extra>")
        )
    else:
        hover_tmpl = custom_hovertemplate

    fig = go.Figure()

    # ---- Colores ----
    if color_mode == "single":
        # ✅ FIX x/y según orientación
        fig.add_trace(go.Bar(
            x=values if orientation == "v" else values,
            y=categories if orientation == "h" else categories,
            orientation=orientation,
            marker=dict(color=bar_color, opacity=bar_opacity),
            text=labels,
            textposition="outside" if show_labels else None,
            cliponaxis=False,
            hovertemplate=hover_tmpl,
            name=""
        ))
        showlegend = False

    elif color_mode == "by_groups":
        if group_labels is None:
            raise ValueError("With color_mode='by_groups', provide `group_labels` (Series or dict).")
        group_map = group_labels.to_dict() if isinstance(group_labels, pd.Series) else dict(group_labels)
        groups_for_s = [group_map.get(cat, None) for cat in categories]

        if palette is None:
            base = pq.D3 + pq.Set2 + pq.Set3
            uniq = []
            for g in groups_for_s:
                if g not in uniq:
                    uniq.append(g)
            palette = {g: base[i % len(base)] for i, g in enumerate(uniq)}

        if show_group_legend:
            # Una traza por grupo
            by_group: dict[Hashable, list[tuple[str, float]]] = {}
            for cat, val, g in zip(categories, values, groups_for_s):
                by_group.setdefault(g, []).append((cat, val))

            for g, items in by_group.items():
                cats_g = [c for c, _ in items]
                vals_g = [v for _, v in items]
                fig.add_trace(go.Bar(
                    x=vals_g if orientation == "v" else vals_g,   # ✅ FIX
                    y=cats_g if orientation == "h" else cats_g,   # ✅ FIX
                    orientation=orientation,
                    marker=dict(color=palette.get(g, "gray"), opacity=bar_opacity),
                    text=[label_fmt.format(v=v) for v in vals_g] if show_labels else None,
                    textposition="outside" if show_labels else None,
                    cliponaxis=False,
                    hovertemplate=hover_tmpl,
                    name=str(g)
                ))
            showlegend = True
        else:
            colors = [palette.get(g, "gray") for g in groups_for_s]
            fig.add_trace(go.Bar(
                x=values if orientation == "v" else values, 
                y=categories if orientation == "h" else categories,
                orientation=orientation,
                marker=dict(color=colors, opacity=bar_opacity),
                text=labels,
                textposition="outside" if show_labels else None,
                cliponaxis=False,
                hovertemplate=hover_tmpl,
                name=""
            ))
            showlegend = False
    else:
        raise ValueError("color_mode must be 'single' or 'by_groups'")

    # ---- Títulos ----
    full_title = f"{title}<br><sup>{subtitle}</sup>" if subtitle else title

    tickfmt = value_axis_tickformat or f",.{decimals}f"
    if orientation == "h":
        fig.update_layout(
            title=dict(text=full_title, font=dict(size=title_size)),
            xaxis=dict(
                title=dict(text=xaxis_title, font=dict(size=axis_label_size)),
                tickformat=tickfmt,
                zeroline=True, zerolinewidth=1, zerolinecolor=zero_line_color,
                gridcolor="rgba(200,200,200,0.35)"
            ),
            yaxis=dict(
                title=dict(text=yaxis_title, font=dict(size=axis_label_size)),
                tickangle=category_tickangle,
                categoryorder="array",
                categoryarray=categories
            ),
            width=width, height=height,
            margin=dict(l=margins[0], r=margins[1], t=margins[2], b=margins[3]),
            showlegend=showlegend,
            legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top") if showlegend else dict()
        )
    else:
        fig.update_layout(
            title=dict(text=full_title, font=dict(size=title_size)),
            xaxis=dict(
                title=dict(text=xaxis_title, font=dict(size=axis_label_size)),
                tickangle=category_tickangle,
                categoryorder="array",
                categoryarray=categories
            ),
            yaxis=dict(
                title=dict(text=yaxis_title, font=dict(size=axis_label_size)),
                tickformat=tickfmt,
                zeroline=True, zerolinewidth=1, zerolinecolor=zero_line_color,
                gridcolor="rgba(200,200,200,0.35)"
            ),
            width=width, height=height,
            margin=dict(l=margins[0], r=margins[1], t=margins[2], b=margins[3]),
            showlegend=showlegend,
            legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center", yanchor="top") if showlegend else dict()
        )

    # ---- Línea 0 y padding de rango ----
    if show_zero_line:
        (fig.add_vline(x=0, line_width=1, line_dash=zero_line_dash, line_color=zero_line_color)
         if orientation == "h" else
         fig.add_hline(y=0, line_width=1, line_dash=zero_line_dash, line_color=zero_line_color))

    vmin, vmax = min(0, min(values)), max(0, max(values))
    pad = max(abs(vmin), abs(vmax)) * 0.07 if vmin != vmax else 1
    if orientation == "h":
        fig.update_xaxes(range=[vmin - pad, vmax + pad])
    else:
        fig.update_yaxes(range=[vmin - pad, vmax + pad])

    return fig

TotalMode = Literal["sum", "provided", "none"]

def plot_contributions(
    df: pd.DataFrame,
    cols: Optional[List[str]] = None,
    title: str = "",
    yaxis_title: str = "Contribución (pp)",
    total_mode: TotalMode = "sum",
    total_series: Optional[pd.Series] = None,
    total_name: str = "Total",
    total_color: Optional[str] = "#2E86AB",  # 🎨 NUEVO parámetro
    colors: Optional[Union[Dict[str, str], List[str]]] = None,
    height: int = 500,
    width: int = 950,
) -> go.Figure:
    """
    Plot stacked contributions as bars and their row-wise sum as a line.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("df.index must be a DatetimeIndex.")
    if cols is None:
        cols = list(df.columns)
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Columns not found: {missing}")

    _df = df[cols].copy()

    # Total
    if total_mode == "sum":
        total = _df.sum(axis=1)
    elif total_mode == "provided":
        if total_series is None:
            raise ValueError("total_series is required when total_mode='provided'.")
        total = total_series.reindex(_df.index)
    else:
        total = None

    # Colors
    if isinstance(colors, dict):
        color_map = {c: colors.get(c) for c in cols}
    elif isinstance(colors, list):
        color_map = {c: colors[i % len(colors)] for i, c in enumerate(cols)}
    else:
        color_map = {c: None for c in cols}

    # Figure
    fig = go.Figure()

    # Barras
    for c in cols:
        fig.add_trace(
            go.Bar(
                x=_df.index,
                y=_df[c],
                name=c,
                marker_color=color_map.get(c),
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>%{customdata}<br>Valor: %{y:.2f}<extra></extra>",
                customdata=[c] * len(_df),
            )
        )

    # Línea total (con color personalizado)
    if total is not None:
        fig.add_trace(
            go.Scatter(
                x=total.index,
                y=total.values,
                mode="lines",
                name=total_name,
                line=dict(width=2.2, color=total_color),  # 👈 aquí se aplica
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>"+total_name+": %{y:.2f}<extra></extra>",
            )
        )

    # Layout
    fig.update_layout(
        title=title,
        barmode="relative",
        height=height,
        width=width,
        legend=dict(orientation="h", y=-0.15, x=0.0),
        margin=dict(l=60, r=20, t=60, b=60),
    )
    fig.update_yaxes(title=yaxis_title, zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0,0,0,0.25)")
    fig.update_xaxes(type="date", showspikes=True, spikemode="across", spikethickness=1)

    return fig


def plot_admin_sector_dumbbell(
    summary: pd.DataFrame,
    admin_order: List[str],
    presidential_colors: Dict[str, str],
    x_range: Optional[Tuple[float, float]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    title: str = "Actividad con mayor y menor crecimiento promedio del PIB por Administración",
    title_color: str = "black",
    axis_label_color: str = "black",
    tick_color: str = "black",
    legend_color: str = "black",
    shade_by_zero: bool = True,
    neg_bg_color: str = "rgba(255, 200, 200, 0.25)",   # rojo pastel muy tenue
    pos_bg_color: str = "rgba(200, 255, 200, 0.25)",   # verde pastel muy tenue
) -> go.Figure:
    """
    Dumbbell chart showing, for each administration, the economic activity with 
    the highest and lowest average interannual GDP growth.
    """

    # --- Filtra admins en el orden dado ---
    admins = [a for a in admin_order if a in summary.index]
    df_plot = summary.loc[admins].copy()

    y_labels = admins
    admin_colors = [presidential_colors.get(a, "#444444") for a in admins]

    # --- Determinar rango X si no se pasó ---
    if x_range is None:
        xmin = df_plot["Min_Growth"].min()
        xmax = df_plot["Max_Growth"].max()
        if xmax == xmin:
            padding = 1.0
        else:
            padding = (xmax - xmin) * 0.10
        x_range = (xmin - padding, xmax + padding)

    fig = go.Figure()

    # === Fondo dividido por cero (rojo < 0, verde > 0) ===
    if shade_by_zero:
        # banda negativa (si hay parte negativa)
        if x_range[0] < 0:
            fig.add_shape(
                type="rect",
                xref="x", yref="paper",
                x0=x_range[0], x1=min(0, x_range[1]),
                y0=0, y1=1,
                fillcolor=neg_bg_color,
                line=dict(width=0),
                layer="below",
            )
        # banda positiva (si hay parte positiva)
        if x_range[1] > 0:
            fig.add_shape(
                type="rect",
                xref="x", yref="paper",
                x0=max(0, x_range[0]), x1=x_range[1],
                y0=0, y1=1,
                fillcolor=pos_bg_color,
                line=dict(width=0),
                layer="below",
            )

    # --- 1) Líneas min → max por administración ---
    for admin, color in zip(admins, admin_colors):
        row = df_plot.loc[admin]
        fig.add_trace(
            go.Scatter(
                x=[row["Min_Growth"], row["Max_Growth"]],
                y=[admin, admin],
                mode="lines",
                line=dict(color=color, width=4),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # --- 2) Punto mínimo (círculo) ---
    fig.add_trace(
        go.Scatter(
            x=df_plot["Min_Growth"],
            y=y_labels,
            mode="markers+text",
            marker=dict(size=10, symbol="circle", color=admin_colors),
            text=[
                f"{act} {g:.1f}%"
                for act, g in zip(df_plot["Min_Activity"], df_plot["Min_Growth"])
            ],
            textposition="middle left",
            textfont=dict(size=11, color="gray"),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 3) Punto máximo (cuadrado) ---
    fig.add_trace(
        go.Scatter(
            x=df_plot["Max_Growth"],
            y=y_labels,
            mode="markers+text",
            marker=dict(size=12, symbol="square", color=admin_colors),
            text=[
                f"{act} {g:.1f}%"
                for act, g in zip(df_plot["Max_Activity"], df_plot["Max_Growth"])
            ],
            textposition="middle right",
            textfont=dict(size=11, color="black"),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 4) Leyenda neutra ---
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="circle", size=10, color=legend_color),
            name="Actividad con menor crecimiento",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="square", size=12, color=legend_color),
            name="Actividad con mayor crecimiento",
        )
    )

    # --- 5) Layout ---
    layout_kwargs = dict(
        title=dict(
            text=title,
            font=dict(color=title_color),
        ),
        xaxis_title=dict(text="Crecimiento promedio (%)", font=dict(color=axis_label_color)),
        yaxis_title=dict(text="Administración", font=dict(color=axis_label_color)),
        template="plotly_white",
        margin=dict(l=120, r=120, t=80, b=80),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.20,
            yanchor="top",
        ),
    )

    if width is not None:
        layout_kwargs["width"] = width
    if height is not None:
        layout_kwargs["height"] = height

    fig.update_layout(**layout_kwargs)

    # Color del texto de la leyenda
    fig.update_layout(
        legend_font=dict(color="steelblue", size=12)
    )

    # --- Ejes ---
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=y_labels,
        autorange="reversed",
        tickfont=dict(color=tick_color),
    )

    fig.update_xaxes(
        tickfont=dict(color=tick_color),
        range=list(x_range),
        zeroline=False,
        zerolinecolor="gray",
        zerolinewidth=1,
    )

    return fig


def plot_activity_dumbbell(
    summary: pd.DataFrame,
    presidential_colors: Dict[str, str],
    x_range: Optional[Tuple[float, float]] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    title: str = "Administración con mayor y menor crecimiento interanual promedio por Actividad Aconómica",
    title_color: str = "black",
    axis_label_color: str = "black",
    tick_color: str = "black",
    legend_color: str = "black",
    line_color: str = "#1f77b4",
    line_width: int = 4,
    shade_by_zero: bool = True,
    neg_bg_color: str = "rgba(255, 200, 200, 0.25)",   # rojo pastel muy tenue
    pos_bg_color: str = "rgba(200, 255, 200, 0.25)",   # verde pastel muy tenue
) -> go.Figure:
    """
    Plot a dumbbell-style comparison of the administration with the highest
    and the lowest average GDP growth for each economic activity.

    The background canvas is optionally shaded:
    - x < 0 in a soft red (neg_bg_color)
    - x > 0 in a soft green (pos_bg_color)
    """

    # Copia para no tocar el original
    df_plot = summary.copy()

    # Etiquetas del eje Y = índice del DataFrame
    activities = list(df_plot.index)

    # Rango X automático si no se pasa
    if x_range is None:
        xmin = df_plot["Tasa_menor"].min()
        xmax = df_plot["Tasa_mayor"].max()
        if xmax == xmin:
            padding = 1.0
        else:
            padding = (xmax - xmin) * 0.1
        x_range = (xmin - padding, xmax + padding)

    fig = go.Figure()

    # --- (0) Pintar lienzo según signo (rojo < 0, verde > 0) ---
    if shade_by_zero:
        # Zona negativa
        if x_range[0] < 0:
            fig.add_shape(
                type="rect",
                xref="x", yref="paper",
                x0=x_range[0],
                x1=min(0, x_range[1]),
                y0=0,
                y1=1,
                fillcolor=neg_bg_color,
                line=dict(width=0),
                layer="below",
            )
        # Zona positiva
        if x_range[1] > 0:
            fig.add_shape(
                type="rect",
                xref="x", yref="paper",
                x0=max(0, x_range[0]),
                x1=x_range[1],
                y0=0,
                y1=1,
                fillcolor=pos_bg_color,
                line=dict(width=0),
                layer="below",
            )

    # --- 1) Líneas horizontales min-max (estilo unificado) ---
    for act, row in df_plot.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[row["Tasa_menor"], row["Tasa_mayor"]],
                y=[act, act],
                mode="lines",
                line=dict(color=line_color, width=line_width),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Colores por administración para los puntos
    min_colors = [
        presidential_colors.get(admin, "#444444")
        for admin in df_plot["Admin_menor"]
    ]
    max_colors = [
        presidential_colors.get(admin, "#444444")
        for admin in df_plot["Admin_mayor"]
    ]

    # --- 2) Punto mínimo (círculo, color presidencial, sin leyenda propia) ---
    fig.add_trace(
        go.Scatter(
            x=df_plot["Tasa_menor"],
            y=activities,
            mode="markers+text",
            marker=dict(size=10, symbol="circle", color=min_colors),
            text=[
                f"{admin} {g:.1f}%"
                for admin, g in zip(df_plot["Admin_menor"], df_plot["Tasa_menor"])
            ],
            textposition="middle left",
            textfont=dict(size=11, color="gray"),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 3) Punto máximo (cuadrado, color presidencial, sin leyenda propia) ---
    fig.add_trace(
        go.Scatter(
            x=df_plot["Tasa_mayor"],
            y=activities,
            mode="markers+text",
            marker=dict(size=12, symbol="square", color=max_colors),
            text=[
                f"{admin} {g:.1f}%"
                for admin, g in zip(df_plot["Admin_mayor"], df_plot["Tasa_mayor"])
            ],
            textposition="middle right",
            textfont=dict(size=11, color="black"),
            hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>",
            showlegend=False,
        )
    )

    # --- 4) Leyenda neutra consistente con plot_admin_sector_dumbbell ---
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="circle", size=10, color=legend_color),
            name="Administración con menor crecimiento",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="square", size=12, color=legend_color),
            name="Administración con mayor crecimiento",
        )
    )

    # --- Layout general (armonizado) ---
    layout_kwargs = dict(
        title=dict(
            text=title,
            font=dict(color=title_color),
        ),
        xaxis_title=dict(
            text="Crecimiento promedio (%)",
            font=dict(color=axis_label_color),
        ),
        yaxis_title=dict(
            text="Actividad económica",
            font=dict(color=axis_label_color),
        ),
        template="plotly_white",
        margin=dict(l=120, r=120, t=100, b=40),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.10,        # abajo del gráfico
            yanchor="top",
        ),
    )

    if width is not None:
        layout_kwargs["width"] = width
    if height is not None:
        layout_kwargs["height"] = height

    fig.update_layout(**layout_kwargs)

    # Eje Y: categorías en el orden del índice
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=activities,
        autorange="reversed",  # arriba la primera actividad
        tickfont=dict(color=tick_color),
    )

    # Eje X: ticks + rango, SIN zeroline
    fig.update_xaxes(
        tickfont=dict(color=tick_color),
        range=list(x_range),
        zeroline=False,
    )

    return fig


