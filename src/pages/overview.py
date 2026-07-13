from __future__ import annotations

import streamlit as st

from src.charts import money_bar, percentage_bar
from src.data_loader import FinancialData
from src.narratives import overview_narrative
from src.ui import (
    AppSettings,
    format_money,
    format_percent,
    format_ratio,
    percentage_delta,
    source_caption,
    value_for_year,
)


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("Visão geral")
    st.caption("Indicadores calculados exclusivamente a partir dos demonstrativos consolidados.")

    year = settings.year
    previous_year = year - 1
    cards = [
        ("Receita líquida", data.income_statement, "Receita_Liquida", "money"),
        ("Lucro líquido", data.income_statement, "Lucro_Liquido", "money"),
        ("Fluxo operacional", data.cash_flow, "Fluxo_Operacional", "money"),
        ("Fluxo de caixa livre", data.cash_flow, "Free_Cash_Flow", "money"),
        ("Liquidez corrente", data.indicators, "Liquidez_Corrente", "ratio"),
        ("Capital de terceiros / ativo", data.indicators, "Endividamento_Geral", "percent"),
    ]
    columns = st.columns(3)
    for index, (label, frame, column, kind) in enumerate(cards):
        current = value_for_year(frame, year, column)
        previous = value_for_year(frame, previous_year, column)
        if kind == "money":
            display = format_money(current, settings.unit)
        elif kind == "ratio":
            display = format_ratio(current)
        else:
            display = format_percent(current)
        delta = (
            percentage_delta(current, previous)
            if settings.compare_previous and year > data.income_statement["Ano"].min()
            else None
        )
        columns[index % 3].metric(label, display, delta)

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            money_bar(
                data.income_statement,
                "Receita_Liquida",
                "Receita líquida",
                "Receita líquida por exercício",
                "Demonstrações consolidadas, 2021–2024",
                settings.unit,
                settings.theme,
            ),
            width="stretch",
        )
    with right:
        st.plotly_chart(
            percentage_bar(
                data.indicators,
                ["Margem_Bruta", "Margem_Operacional", "Margem_Liquida"],
                ["Margem bruta", "Margem operacional", "Margem líquida"],
                "Margens por exercício",
                "Percentuais sobre a receita líquida",
                settings.theme,
            ),
            width="stretch",
        )

    st.markdown("#### Leitura descritiva")
    narrative = overview_narrative(data, year)
    if narrative:
        for statement in narrative:
            st.write(f"- {statement}")
    else:
        st.info("Não há período anterior suficiente para uma comparação determinística.")

    st.caption(source_caption(data.income_statement, year))
