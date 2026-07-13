from __future__ import annotations

import streamlit as st

from src.data_loader import DataSchemaError, load_financial_data
from src.pages import (
    balance_sheet,
    cash_flow,
    income_statement,
    indicators,
    methodology,
    overview,
    sources,
)
from src.ui import apply_theme, render_footer, render_header, render_sidebar

st.set_page_config(
    page_title="Dashboard Acadêmico de Análise Financeira",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def _load_data():
    return load_financial_data()


PAGE_RENDERERS = {
    "Visão geral": overview.render,
    "DRE e rentabilidade": income_statement.render,
    "Balanço e estrutura patrimonial": balance_sheet.render,
    "Fluxo de caixa": cash_flow.render,
    "Indicadores e sinais de atenção": indicators.render,
    "Metodologia e validações": methodology.render,
    "Fontes e limitações": sources.render,
}


def main() -> None:
    try:
        data = _load_data()
    except (DataSchemaError, OSError, ValueError) as exc:
        st.error(f"Não foi possível carregar a base processada: {exc}")
        st.stop()

    settings = render_sidebar(data)
    apply_theme(settings.theme)
    render_header()
    PAGE_RENDERERS[settings.page](data, settings)
    render_footer()


if __name__ == "__main__":
    main()
