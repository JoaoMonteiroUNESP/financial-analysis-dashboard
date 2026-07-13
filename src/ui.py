from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src.config import INDEPENDENCE_NOTICE
from src.data_loader import FinancialData


@dataclass(frozen=True)
class AppSettings:
    page: str
    year: int
    compare_previous: bool
    unit: str
    theme: str


PAGES = (
    "Visão geral",
    "DRE e rentabilidade",
    "Balanço e estrutura patrimonial",
    "Fluxo de caixa",
    "Indicadores e sinais de atenção",
    "Metodologia e validações",
    "Fontes e limitações",
)


def render_sidebar(data: FinancialData) -> AppSettings:
    years = data.income_statement["Ano"].astype(int).tolist()
    with st.sidebar:
        st.markdown("### Análise financeira")
        st.caption("Estudo acadêmico · dados consolidados")
        page = st.radio("Navegação", PAGES)
        st.divider()
        year = int(st.selectbox("Ano de referência", years, index=len(years) - 1))
        compare_previous = st.checkbox(
            "Comparar com o ano anterior",
            value=True,
            disabled=year == min(years),
        )
        unit = st.radio("Unidade monetária", ("R$ mil", "R$ milhões"), horizontal=True)
        theme = st.radio("Tema", ("Claro", "Escuro"), horizontal=True)
        st.divider()
        st.caption(INDEPENDENCE_NOTICE)
    return AppSettings(page, year, compare_previous, unit, theme)


def apply_theme(theme: str) -> None:
    if theme == "Escuro":
        colors = {
            "background": "#0F172A",
            "surface": "#172033",
            "text": "#E5E7EB",
            "muted": "#A8B3C7",
            "border": "#334155",
            "accent": "#60A5FA",
            "notice": "#172554",
        }
    else:
        colors = {
            "background": "#F8FAFC",
            "surface": "#FFFFFF",
            "text": "#172033",
            "muted": "#5F6B7A",
            "border": "#DCE3EC",
            "accent": "#2563EB",
            "notice": "#EFF6FF",
        }
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {colors["background"]}; color: {colors["text"]}; }}
        [data-testid="stHeader"] {{ background: {colors["background"]}; }}
        [data-testid="stMainBlockContainer"] {{
            max-width: 1280px;
            padding-left: 3rem;
            padding-right: 3rem;
        }}
        [data-testid="stSidebar"] {{
            background: {colors["surface"]};
            border-right: 1px solid {colors["border"]};
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
        [data-testid="stSidebar"] [data-baseweb="radio"] *,
        [data-testid="stSidebar"] [data-baseweb="checkbox"] * {{
            color: {colors["text"]} !important;
        }}
        [data-testid="stMetric"] {{
            background: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-radius: 12px;
            padding: 14px 16px;
        }}
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {{ color: {colors["text"]} !important; }}
        [data-testid="stMetricValue"] {{ font-size: 1.65rem; }}
        .academic-header {{
            background: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-top: 4px solid {colors["accent"]};
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 12px;
        }}
        .academic-header h1 {{ color: {colors["text"]}; margin: 0 0 4px; font-size: 1.8rem; }}
        .academic-header p {{ color: {colors["muted"]}; margin: 0; }}
        .independence-notice {{
            background: {colors["notice"]};
            border-left: 4px solid {colors["accent"]};
            border-radius: 8px;
            color: {colors["text"]};
            padding: 12px 14px;
            margin: 0 0 22px;
            font-size: 0.9rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="academic-header">
            <h1>Dashboard Acadêmico de Análise Financeira</h1>
            <p>Estudo de caso: demonstrações consolidadas da BASF S.A. — 2021 a 2024</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="independence-notice">{INDEPENDENCE_NOTICE}</div>',
        unsafe_allow_html=True,
    )


def format_money(value: float, unit: str) -> str:
    if pd.isna(value):
        return "—"
    scaled = value / 1_000 if unit == "R$ milhões" else value
    suffix = "mi" if unit == "R$ milhões" else "mil"
    decimals = 1 if unit == "R$ milhões" else 0
    formatted = f"{scaled:,.{decimals}f}".translate(str.maketrans({",": ".", ".": ","}))
    return f"R$ {formatted} {suffix}"


def format_percent(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:.1%}".replace(".", ",")


def format_ratio(value: float) -> str:
    return "—" if pd.isna(value) else f"{value:.2f}x".replace(".", ",")


def percentage_delta(current: float, previous: float) -> str | None:
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None
    delta = (current - previous) / abs(previous)
    formatted = f"{delta:+.1%}".replace(".", ",")
    return f"{formatted} vs. anterior"


def value_for_year(frame: pd.DataFrame, year: int, column: str) -> float:
    rows = frame.loc[frame["Ano"] == year, column]
    return float("nan") if rows.empty else float(rows.iloc[0])


def source_caption(frame: pd.DataFrame, year: int) -> str:
    row = frame.loc[frame["Ano"] == year].iloc[0]
    return (
        f"Fonte: {row['Arquivo_Fonte']} · {row['Demonstrativo_Origem']} · "
        f"{row['Unidade_Monetaria']}. {row['Observacao_Reapresentacao']}"
    )


def render_footer() -> None:
    st.divider()
    st.caption(
        "Dados históricos de 2021 a 2024. O conteúdo é descritivo, não constitui laudo, "
        "recomendação financeira ou ferramenta institucional."
    )
