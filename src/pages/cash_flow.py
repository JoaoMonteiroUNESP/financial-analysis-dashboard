from __future__ import annotations

import streamlit as st

from src.charts import grouped_money_bar
from src.data_loader import FinancialData
from src.ui import (
    AppSettings,
    format_money,
    percentage_delta,
    source_caption,
    value_for_year,
)


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("Fluxo de caixa")
    st.caption(
        "CAPEX inclui aquisições de imobilizado e intangível. O fluxo de caixa livre "
        "é uma medida simplificada: fluxo operacional menos CAPEX."
    )
    year = settings.year
    previous_year = year - 1
    cards = [
        ("Fluxo operacional", "Fluxo_Operacional"),
        ("Fluxo de investimento", "Fluxo_Investimento"),
        ("Fluxo de financiamento", "Fluxo_Financiamento"),
        ("Variação de caixa", "Variacao_Caixa"),
        ("CAPEX", "CAPEX"),
        ("Fluxo de caixa livre", "Free_Cash_Flow"),
    ]
    columns = st.columns(3)
    for index, (label, metric) in enumerate(cards):
        current = value_for_year(data.cash_flow, year, metric)
        previous = value_for_year(data.cash_flow, previous_year, metric)
        delta = (
            percentage_delta(current, previous)
            if settings.compare_previous and year > data.cash_flow["Ano"].min()
            else None
        )
        columns[index % 3].metric(label, format_money(current, settings.unit), delta)

    st.plotly_chart(
        grouped_money_bar(
            data.cash_flow,
            ["Fluxo_Operacional", "Fluxo_Investimento", "Fluxo_Financiamento"],
            ["Operacional", "Investimento", "Financiamento"],
            "Fluxos de caixa por atividade",
            "Valores consolidados; sinais mantidos conforme a demonstração",
            settings.unit,
            settings.theme,
        ),
        width="stretch",
    )
    st.plotly_chart(
        grouped_money_bar(
            data.cash_flow,
            ["CAPEX", "Free_Cash_Flow"],
            ["CAPEX", "Fluxo de caixa livre"],
            "CAPEX e fluxo de caixa livre",
            "FCF = fluxo operacional − aquisições de imobilizado e intangível",
            settings.unit,
            settings.theme,
        ),
        width="stretch",
    )

    st.markdown("#### Demonstração resumida")
    display_columns = [
        "Ano",
        "Fluxo_Operacional",
        "Fluxo_Investimento",
        "Fluxo_Financiamento",
        "Variacao_Caixa",
        "Aquisicao_Imobilizado",
        "Aquisicao_Intangivel",
        "CAPEX",
        "Free_Cash_Flow",
    ]
    table = data.cash_flow[display_columns].set_index("Ano")
    st.dataframe(table.style.format("{:,.0f}"), width="stretch")
    st.caption(source_caption(data.cash_flow, year))
