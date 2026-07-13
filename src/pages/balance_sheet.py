from __future__ import annotations

import streamlit as st

from src.charts import stacked_money_bar
from src.data_loader import FinancialData
from src.ui import (
    AppSettings,
    format_money,
    percentage_delta,
    source_caption,
    value_for_year,
)


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("Balanço e estrutura patrimonial")
    st.caption(
        "Capital de terceiros corresponde a passivos circulantes e não circulantes. "
        "Dívida bruta corresponde apenas a empréstimos e arrendamentos."
    )
    year = settings.year
    previous_year = year - 1
    cards = [
        ("Ativo total", "Ativo_Total"),
        ("Passivo circulante", "Passivo_Circulante"),
        ("Passivo não circulante", "Passivo_Nao_Circulante"),
        ("Patrimônio líquido", "Patrimonio_Liquido"),
        ("Capital de terceiros", "Capital_Terceiros"),
        ("Dívida bruta", "Divida_Bruta"),
    ]
    columns = st.columns(3)
    for index, (label, metric) in enumerate(cards):
        current = value_for_year(data.balance_sheet, year, metric)
        previous = value_for_year(data.balance_sheet, previous_year, metric)
        delta = (
            percentage_delta(current, previous)
            if settings.compare_previous and year > data.balance_sheet["Ano"].min()
            else None
        )
        columns[index % 3].metric(label, format_money(current, settings.unit), delta)

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            stacked_money_bar(
                data.balance_sheet,
                ["Ativo_Circulante", "Ativo_Nao_Circulante"],
                ["Ativo circulante", "Ativo não circulante"],
                "Composição do ativo",
                "Valores consolidados por exercício",
                settings.unit,
                settings.theme,
            ),
            width="stretch",
        )
    with right:
        st.plotly_chart(
            stacked_money_bar(
                data.balance_sheet,
                ["Passivo_Circulante", "Passivo_Nao_Circulante", "Patrimonio_Liquido"],
                ["Passivo circulante", "Passivo não circulante", "Patrimônio líquido"],
                "Financiamento do ativo",
                "Passivos e patrimônio líquido por exercício",
                settings.unit,
                settings.theme,
            ),
            width="stretch",
        )

    st.markdown("#### Balanço resumido")
    display_columns = [
        "Ano",
        "Caixa_Equivalentes",
        "Contas_Receber_Clientes_Circulante",
        "Estoques",
        "Ativo_Circulante",
        "Ativo_Nao_Circulante",
        "Ativo_Total",
        "Passivo_Circulante",
        "Passivo_Nao_Circulante",
        "Patrimonio_Liquido",
        "Divida_Bruta",
    ]
    table = data.balance_sheet[display_columns].set_index("Ano")
    st.dataframe(table.style.format("{:,.0f}"), width="stretch")
    st.caption(source_caption(data.balance_sheet, year))
