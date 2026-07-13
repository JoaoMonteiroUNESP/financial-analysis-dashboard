from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
import plotly.graph_objects as go

PALETTES = {
    "Claro": {
        "blue": "#2563EB",
        "gold": "#D97706",
        "slate": "#64748B",
        "ink": "#172033",
        "grid": "#E2E8F0",
        "background": "rgba(255,255,255,0)",
    },
    "Escuro": {
        "blue": "#60A5FA",
        "gold": "#FBBF24",
        "slate": "#94A3B8",
        "ink": "#E5E7EB",
        "grid": "#334155",
        "background": "rgba(15,23,42,0)",
    },
}


def _palette(theme: str) -> dict[str, str]:
    return PALETTES.get(theme, PALETTES["Claro"])


def _scale(values: pd.Series, unit: str) -> pd.Series:
    return values / 1_000 if unit == "R$ milhões" else values


def _money_axis_title(unit: str) -> str:
    return "R$ milhões" if unit == "R$ milhões" else "R$ mil"


def _finish(
    figure: go.Figure,
    title: str,
    subtitle: str,
    theme: str,
    y_title: str,
) -> go.Figure:
    palette = _palette(theme)
    figure.update_layout(
        title={
            "text": f"{title}<br><sup>{subtitle}</sup>",
            "x": 0,
            "xanchor": "left",
        },
        paper_bgcolor=palette["background"],
        plot_bgcolor=palette["background"],
        font={"color": palette["ink"], "family": "Arial, sans-serif"},
        margin={"l": 24, "r": 16, "t": 78, "b": 36},
        legend={"orientation": "h", "y": 1.02, "x": 0},
        hovermode="x unified",
        height=390,
    )
    figure.update_xaxes(
        type="category",
        showgrid=False,
        linecolor=palette["grid"],
        tickmode="array",
    )
    figure.update_yaxes(
        title=y_title,
        rangemode="tozero",
        gridcolor=palette["grid"],
        zerolinecolor=palette["slate"],
    )
    return figure


def money_bar(
    frame: pd.DataFrame,
    column: str,
    label: str,
    title: str,
    subtitle: str,
    unit: str,
    theme: str,
) -> go.Figure:
    palette = _palette(theme)
    values = _scale(frame[column], unit)
    figure = go.Figure(
        go.Bar(
            x=frame["Ano"].astype(str),
            y=values,
            name=label,
            marker_color=palette["blue"],
            text=values,
            texttemplate="%{text:,.1f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=f"%{{x}}<br>{label}: %{{y:,.1f}}<extra></extra>",
        )
    )
    return _finish(figure, title, subtitle, theme, _money_axis_title(unit))


def grouped_money_bar(
    frame: pd.DataFrame,
    columns: Sequence[str],
    labels: Sequence[str],
    title: str,
    subtitle: str,
    unit: str,
    theme: str,
) -> go.Figure:
    palette = _palette(theme)
    colors = [palette["blue"], palette["gold"], palette["slate"]]
    figure = go.Figure()
    for index, (column, label) in enumerate(zip(columns, labels, strict=True)):
        values = _scale(frame[column], unit)
        figure.add_bar(
            x=frame["Ano"].astype(str),
            y=values,
            name=label,
            marker_color=colors[index % len(colors)],
            hovertemplate=f"%{{x}}<br>{label}: %{{y:,.1f}}<extra></extra>",
        )
    figure.update_layout(barmode="group")
    return _finish(figure, title, subtitle, theme, _money_axis_title(unit))


def stacked_money_bar(
    frame: pd.DataFrame,
    columns: Sequence[str],
    labels: Sequence[str],
    title: str,
    subtitle: str,
    unit: str,
    theme: str,
) -> go.Figure:
    figure = grouped_money_bar(frame, columns, labels, title, subtitle, unit, theme)
    figure.update_layout(barmode="stack")
    return figure


def percentage_bar(
    frame: pd.DataFrame,
    columns: Sequence[str],
    labels: Sequence[str],
    title: str,
    subtitle: str,
    theme: str,
) -> go.Figure:
    palette = _palette(theme)
    colors = [palette["blue"], palette["gold"], palette["slate"]]
    figure = go.Figure()
    for index, (column, label) in enumerate(zip(columns, labels, strict=True)):
        values = frame[column] * 100
        figure.add_bar(
            x=frame["Ano"].astype(str),
            y=values,
            name=label,
            marker_color=colors[index % len(colors)],
            hovertemplate=f"%{{x}}<br>{label}: %{{y:.1f}}%<extra></extra>",
        )
    figure.update_layout(barmode="group")
    return _finish(figure, title, subtitle, theme, "%")


def ratio_bar(
    frame: pd.DataFrame,
    columns: Sequence[str],
    labels: Sequence[str],
    title: str,
    subtitle: str,
    theme: str,
) -> go.Figure:
    palette = _palette(theme)
    colors = [palette["blue"], palette["gold"], palette["slate"]]
    figure = go.Figure()
    for index, (column, label) in enumerate(zip(columns, labels, strict=True)):
        figure.add_bar(
            x=frame["Ano"].astype(str),
            y=frame[column],
            name=label,
            marker_color=colors[index % len(colors)],
            hovertemplate=f"%{{x}}<br>{label}: %{{y:.2f}}x<extra></extra>",
        )
    figure.update_layout(barmode="group")
    return _finish(figure, title, subtitle, theme, "Índice (x)")


def income_statement_waterfall(
    row: pd.Series,
    unit: str,
    theme: str,
) -> go.Figure:
    palette = _palette(theme)
    divisor = 1_000 if unit == "R$ milhões" else 1
    labels = [
        "Receita líquida",
        "CPV",
        "Lucro bruto",
        "Despesas VAG",
        "Outras operacionais",
        "Resultado operacional",
        "Resultado financeiro",
        "Lucro antes de IR/CS",
        "IR/CS",
        "Lucro líquido",
    ]
    measures = [
        "absolute",
        "relative",
        "total",
        "relative",
        "relative",
        "total",
        "relative",
        "total",
        "relative",
        "total",
    ]
    values = [
        row["Receita_Liquida"],
        row["Custo_Produtos_Vendidos"],
        row["Lucro_Bruto"],
        row["Despesas_Vendas_Administrativas_Gerais"],
        row["Outras_Receitas_Despesas_Operacionais_Liquidas"],
        row["Resultado_Operacional"],
        row["Resultado_Financeiro"],
        row["Lucro_Antes_IR_CS"],
        row["Imposto_Renda_Contribuicao_Social"],
        row["Lucro_Liquido"],
    ]
    figure = go.Figure(
        go.Waterfall(
            x=labels,
            y=[value / divisor for value in values],
            measure=measures,
            connector={"line": {"color": palette["slate"]}},
            increasing={"marker": {"color": palette["blue"]}},
            decreasing={"marker": {"color": palette["gold"]}},
            totals={"marker": {"color": palette["slate"]}},
            hovertemplate="%{x}<br>%{y:,.1f}<extra></extra>",
        )
    )
    return _finish(
        figure,
        f"Formação do resultado — {int(row['Ano'])}",
        "Valores consolidados; custos, despesas e tributos mantêm o sinal contábil",
        theme,
        _money_axis_title(unit),
    )
