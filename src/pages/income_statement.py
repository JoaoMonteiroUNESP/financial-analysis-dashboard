from __future__ import annotations

import streamlit as st

from src.charts import grouped_money_bar, income_statement_waterfall
from src.data_loader import FinancialData
from src.ui import (
    AppSettings,
    format_money,
    percentage_delta,
    source_caption,
    value_for_year,
)


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("DRE e rentabilidade")
    st.caption("Receitas, custos, resultados e margens com os sinais contábeis publicados.")
    year = settings.year
    previous_year = year - 1

    card_columns = st.columns(5)
    cards = [
        ("Receita líquida", "Receita_Liquida"),
        ("Lucro bruto", "Lucro_Bruto"),
        ("Resultado operacional", "Resultado_Operacional"),
        ("Lucro antes de IR/CS", "Lucro_Antes_IR_CS"),
        ("Lucro líquido", "Lucro_Liquido"),
    ]
    for column, (label, metric) in zip(card_columns, cards, strict=True):
        current = value_for_year(data.income_statement, year, metric)
        previous = value_for_year(data.income_statement, previous_year, metric)
        delta = (
            percentage_delta(current, previous)
            if settings.compare_previous and year > data.income_statement["Ano"].min()
            else None
        )
        column.metric(label, format_money(current, settings.unit), delta)

    selected = data.income_statement.loc[data.income_statement["Ano"] == year].iloc[0]
    st.plotly_chart(
        income_statement_waterfall(selected, settings.unit, settings.theme),
        width="stretch",
    )

    st.plotly_chart(
        grouped_money_bar(
            data.income_statement,
            ["Lucro_Bruto", "Resultado_Operacional", "Lucro_Liquido"],
            ["Lucro bruto", "Resultado operacional", "Lucro líquido"],
            "Resultados por exercício",
            "Valores consolidados; barras partem de zero",
            settings.unit,
            settings.theme,
        ),
        width="stretch",
    )

    st.markdown("#### DRE consolidada")
    display_columns = [
        "Ano",
        "Receita_Liquida",
        "Custo_Produtos_Vendidos",
        "Lucro_Bruto",
        "Despesas_Vendas_Administrativas_Gerais",
        "Outras_Receitas_Despesas_Operacionais_Liquidas",
        "Resultado_Operacional",
        "Resultado_Financeiro",
        "Lucro_Antes_IR_CS",
        "Imposto_Renda_Contribuicao_Social",
        "Lucro_Liquido",
    ]
    table = data.income_statement[display_columns].set_index("Ano")
    st.dataframe(table.style.format("{:,.0f}"), width="stretch")
    st.caption(source_caption(data.income_statement, year))
