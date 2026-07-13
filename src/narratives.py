from __future__ import annotations

import pandas as pd

from src.data_loader import FinancialData


def _pt_decimal(value: float, format_spec: str) -> str:
    return format(value, format_spec).replace(".", ",")


def _pt_grouped(value: float) -> str:
    return f"{value:,.0f}".translate(str.maketrans({",": ".", ".": ","}))


def percentage_change(current: float, previous: float) -> float | None:
    if pd.isna(current) or pd.isna(previous) or previous == 0:
        return None
    return (float(current) - float(previous)) / abs(float(previous))


def _value(frame: pd.DataFrame, year: int, column: str) -> float:
    rows = frame.loc[frame["Ano"] == year, column]
    return float("nan") if rows.empty else float(rows.iloc[0])


def overview_narrative(data: FinancialData, year: int) -> list[str]:
    """Create cautious, deterministic statements from published values."""
    previous_year = year - 1
    statements: list[str] = []

    revenue = _value(data.income_statement, year, "Receita_Liquida")
    previous_revenue = _value(data.income_statement, previous_year, "Receita_Liquida")
    revenue_change = percentage_change(revenue, previous_revenue)
    if revenue_change is not None:
        direction = "aumentou" if revenue_change >= 0 else "diminuiu"
        statements.append(
            f"A receita líquida {direction} "
            f"{_pt_decimal(abs(revenue_change), '.1%')} em {year} "
            f"na comparação com {previous_year}."
        )

    margin = _value(data.indicators, year, "Margem_Liquida")
    previous_margin = _value(data.indicators, previous_year, "Margem_Liquida")
    if not pd.isna(margin):
        if not pd.isna(previous_margin):
            delta_pp = (margin - previous_margin) * 100
            direction = "aumentou" if delta_pp >= 0 else "diminuiu"
            statements.append(
                f"A margem líquida foi de {_pt_decimal(margin, '.1%')} e {direction} "
                f"{_pt_decimal(abs(delta_pp), '.1f')} p.p. frente a {previous_year}."
            )
        else:
            statements.append(f"A margem líquida foi de {_pt_decimal(margin, '.1%')} em {year}.")

    operating_cash = _value(data.cash_flow, year, "Fluxo_Operacional")
    if not pd.isna(operating_cash):
        signal = "positivo" if operating_cash >= 0 else "negativo"
        statements.append(
            f"O fluxo de caixa operacional foi {signal} em {year}; o indicador isolado "
            "não identifica as causas da variação."
        )

    return statements


def attention_signals(data: FinancialData, year: int) -> pd.DataFrame:
    """Return descriptive signals without insolvency or investment diagnoses."""
    metrics = data.indicators.loc[data.indicators["Ano"] == year].iloc[0]
    cash = data.cash_flow.loc[data.cash_flow["Ano"] == year].iloc[0]

    liquidity = metrics["Liquidez_Corrente"]
    liquidity_reading = (
        "O ativo circulante supera o passivo circulante. A leitura não avalia a "
        "liquidez individual dos ativos."
        if liquidity >= 1
        else "O ativo circulante é inferior ao passivo circulante; a composição e os "
        "vencimentos precisam ser analisados antes de qualquer conclusão."
    )
    working_capital = metrics["Capital_Giro_Liquido"]
    cash_reading = (
        "Houve geração operacional de caixa no período."
        if cash["Fluxo_Operacional"] >= 0
        else "Houve consumo operacional de caixa no período."
    )

    return pd.DataFrame(
        [
            {
                "Indicador": "Liquidez corrente",
                "Valor": f"{_pt_decimal(liquidity, '.2f')}x",
                "Leitura descritiva": liquidity_reading,
            },
            {
                "Indicador": "Capital de giro líquido",
                "Valor": f"R$ {_pt_grouped(working_capital)} mil",
                "Leitura descritiva": (
                    "Diferença entre ativo circulante e passivo circulante; não equivale "
                    "a caixa disponível."
                ),
            },
            {
                "Indicador": "Fluxo operacional",
                "Valor": f"R$ {_pt_grouped(cash['Fluxo_Operacional'])} mil",
                "Leitura descritiva": cash_reading,
            },
            {
                "Indicador": "Capital de terceiros / ativo",
                "Valor": _pt_decimal(metrics["Endividamento_Geral"], ".1%"),
                "Leitura descritiva": (
                    "Representa passivos circulantes e não circulantes sobre o ativo; "
                    "não é sinônimo de dívida financeira."
                ),
            },
            {
                "Indicador": "Margem líquida",
                "Valor": _pt_decimal(metrics["Margem_Liquida"], ".1%"),
                "Leitura descritiva": (
                    "Relaciona lucro líquido e receita líquida; deve ser lida em conjunto "
                    "com itens operacionais, financeiros e tributários."
                ),
            },
        ]
    )
