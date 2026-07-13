from __future__ import annotations

import streamlit as st

from src.charts import percentage_bar, ratio_bar
from src.data_loader import FinancialData
from src.narratives import attention_signals
from src.ui import AppSettings, format_percent, format_ratio


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("Indicadores de estrutura financeira e sinais de atenção")
    st.caption(
        "Esta página substitui os antigos medidores de Altman e Kanitz. A base não contém "
        "todas as entradas necessárias para aplicar esses modelos sem aproximações."
    )

    metrics = data.indicators.copy()
    selected = metrics.loc[metrics["Ano"] == settings.year].iloc[0]
    columns = st.columns(4)
    columns[0].metric("Liquidez corrente", format_ratio(selected["Liquidez_Corrente"]))
    columns[1].metric("Liquidez seca", format_ratio(selected["Liquidez_Seca"]))
    columns[2].metric("Margem líquida", format_percent(selected["Margem_Liquida"]))
    columns[3].metric("ROE", format_percent(selected["ROE"]))

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            ratio_bar(
                metrics,
                ["Liquidez_Corrente", "Liquidez_Seca", "Giro_Ativo"],
                ["Liquidez corrente", "Liquidez seca", "Giro do ativo"],
                "Indicadores em múltiplos",
                "Índices calculados com saldos de encerramento",
                settings.theme,
            ),
            width="stretch",
        )
    with right:
        st.plotly_chart(
            percentage_bar(
                metrics,
                ["Endividamento_Geral", "Composicao_Endividamento", "Divida_Bruta_sobre_Ativo"],
                [
                    "Capital de terceiros / ativo",
                    "Passivo circulante / obrigações",
                    "Dívida bruta / ativo",
                ],
                "Estrutura de obrigações",
                "Percentuais calculados a partir do balanço consolidado",
                settings.theme,
            ),
            width="stretch",
        )

    st.markdown(f"#### Leituras descritivas — {settings.year}")
    st.dataframe(attention_signals(data, settings.year), width="stretch", hide_index=True)
    st.caption(
        "Os indicadores descrevem relações contábeis históricas. Isoladamente, não permitem "
        "concluir solvência, insolvência, qualidade de crédito ou atratividade de investimento."
    )

    st.markdown("#### Série completa de indicadores")
    percentage_columns = [
        "Margem_Bruta",
        "Margem_Operacional",
        "Margem_Liquida",
        "ROA",
        "ROE",
        "Endividamento_Geral",
        "Composicao_Endividamento",
        "Divida_Bruta_sobre_Ativo",
    ]
    formatters = {column: "{:.2%}" for column in percentage_columns}
    formatters.update(
        {
            "Liquidez_Corrente": "{:.2f}",
            "Liquidez_Seca": "{:.2f}",
            "Giro_Ativo": "{:.2f}",
            "Capital_Giro_Liquido": "{:,.0f}",
            "Free_Cash_Flow": "{:,.0f}",
        }
    )
    st.dataframe(metrics.set_index("Ano").style.format(formatters), width="stretch")
