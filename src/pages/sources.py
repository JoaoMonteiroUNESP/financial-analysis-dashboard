from __future__ import annotations

import streamlit as st

from src.config import INDEPENDENCE_NOTICE
from src.data_loader import FinancialData
from src.ui import AppSettings


def render(data: FinancialData, settings: AppSettings) -> None:
    del settings
    st.subheader("Fontes e limitações")
    st.caption("Rastreabilidade dos dados e escopo do estudo acadêmico.")

    st.markdown("#### Proveniência por demonstrativo e ano")
    st.dataframe(data.sources, width="stretch", hide_index=True)

    st.markdown("#### Dicionário de dados")
    st.dataframe(data.data_dictionary, width="stretch", hide_index=True)

    st.markdown("#### Limitações")
    st.write(
        "- A série contém somente 2021, 2022, 2023 e 2024; não há projeções, cenários ou "
        "anos simulados."
    )
    st.write(
        "- Os demonstrativos resumidos são apresentados em R$ mil e podem conter diferenças "
        "de R$ 1 mil por arredondamento."
    )
    st.write(
        "- O fluxo de caixa de 2023 usa a coluna reapresentada na publicação de 2024. "
        "O fluxo de 2022 usa o comparativo da publicação de 2023, que contém reclassificações."
    )
    st.write(
        "- ROA e ROE usam saldos de encerramento, não médias de saldos, para evitar inserir "
        "dados anteriores ao período declarado."
    )
    st.write(
        "- O estudo não incorpora preços de ações. BASF S.A. no Brasil e BASF SE são "
        "entidades jurídicas distintas; nenhuma série de mercado foi combinada com esta base."
    )
    st.write(
        "- Os PDFs-fonte e o Excel de trabalho permanecem em `data/raw` apenas no ambiente "
        "local e são excluídos do versionamento público."
    )

    st.warning(INDEPENDENCE_NOTICE)
