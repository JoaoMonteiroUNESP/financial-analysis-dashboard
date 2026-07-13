from __future__ import annotations

import streamlit as st

from src.data_loader import FinancialData
from src.ui import AppSettings
from src.validation import validate_financial_statements

FORMULAS = {
    "Liquidez corrente": "Ativo circulante ÷ Passivo circulante",
    "Liquidez seca": "(Ativo circulante − Estoques) ÷ Passivo circulante",
    "Margem bruta": "Lucro bruto ÷ Receita líquida",
    "Margem operacional": "Resultado operacional ÷ Receita líquida",
    "Margem líquida": "Lucro líquido ÷ Receita líquida",
    "ROA": "Lucro líquido ÷ Ativo total no encerramento",
    "ROE": "Lucro líquido ÷ Patrimônio líquido no encerramento",
    "Giro do ativo": "Receita líquida ÷ Ativo total no encerramento",
    "Capital de giro líquido": "Ativo circulante − Passivo circulante",
    "Endividamento geral": "(Passivo circulante + Passivo não circulante) ÷ Ativo total",
    "Composição do endividamento": "Passivo circulante ÷ Capital de terceiros",
    "Dívida bruta": "Empréstimos + passivos de arrendamento, circulantes e não circulantes",
    "Fluxo de caixa livre": "Fluxo operacional − CAPEX",
    "CAPEX": "Aquisição de imobilizado + Aquisição de intangível",
}


def render(data: FinancialData, settings: AppSettings) -> None:
    st.subheader("Metodologia e validações")
    st.caption("Fórmulas, convenções e reconciliações executadas automaticamente.")

    st.markdown("#### Fórmulas utilizadas")
    formula_rows = [{"Indicador": name, "Definição": formula} for name, formula in FORMULAS.items()]
    st.dataframe(formula_rows, width="stretch", hide_index=True)

    st.markdown("#### Convenções")
    st.write(
        "- Valores monetários são apresentados em R$ mil na base e podem ser exibidos em "
        "R$ milhões sem alteração do dado de origem."
    )
    st.write("- Percentuais são armazenados como decimais; não há heurística de escala.")
    st.write(
        "- ROA, ROE e giro do ativo usam saldos de encerramento para manter os quatro anos "
        "comparáveis sem introduzir dados de 2020."
    )
    st.write(
        "- A tolerância contábil é de R$ 1 mil, compatível com arredondamentos dos "
        "demonstrativos resumidos."
    )

    st.markdown("#### Resultado das verificações")
    validations = validate_financial_statements(data)
    show_all = st.checkbox("Mostrar todos os anos", value=False)
    if not show_all:
        validations = validations.loc[validations["Ano"] == settings.year]
    st.dataframe(
        validations.style.format(
            {
                "Valor_Observado": "{:,.0f}",
                "Valor_Esperado": "{:,.0f}",
                "Diferenca": "{:+,.0f}",
                "Tolerancia": "{:,.0f}",
            },
            na_rep="—",
        ),
        width="stretch",
        hide_index=True,
    )

    failures = validations.loc[validations["Status"] == "Falha"]
    if failures.empty:
        st.success("Nenhuma diferença acima da tolerância nos anos exibidos.")
    else:
        st.error("Há diferenças acima da tolerância. Consulte as linhas marcadas como Falha.")

    st.markdown("#### Modelos não mantidos")
    st.info(
        "Altman e Kanitz foram removidos porque a base resumida não contém, com a "
        "granularidade necessária, todas as variáveis das variantes consideradas. "
        "Patrimônio líquido não é usado como substituto silencioso de lucros retidos."
    )
