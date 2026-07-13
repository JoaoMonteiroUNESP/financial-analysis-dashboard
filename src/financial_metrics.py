from __future__ import annotations

import pandas as pd


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Divide two aligned series and returns NA for zero denominators."""
    valid_denominator = denominator.where(denominator.ne(0))
    return numerator.astype(float).div(valid_denominator.astype(float))


def calculate_financial_metrics(
    income_statement: pd.DataFrame,
    balance_sheet: pd.DataFrame,
    cash_flow: pd.DataFrame,
) -> pd.DataFrame:
    """Recalculate every displayed metric from the accounting statements.

    Percentage metrics are stored as decimals. ROA, ROE and asset turnover use
    closing balances because the public dataset intentionally starts in 2021 and
    does not include a 2020 opening balance for every denominator.
    """
    merged = income_statement.merge(
        balance_sheet,
        on="Ano",
        how="inner",
        validate="one_to_one",
        suffixes=("_dre", "_balanco"),
    ).merge(
        cash_flow[["Ano", "Fluxo_Operacional", "CAPEX", "Free_Cash_Flow"]],
        on="Ano",
        how="inner",
        validate="one_to_one",
    )

    capital_terceiros = merged["Passivo_Circulante"] + merged["Passivo_Nao_Circulante"]
    metrics = pd.DataFrame({"Ano": merged["Ano"].astype(int)})
    metrics["Liquidez_Corrente"] = _safe_divide(
        merged["Ativo_Circulante"], merged["Passivo_Circulante"]
    )
    metrics["Liquidez_Seca"] = _safe_divide(
        merged["Ativo_Circulante"] - merged["Estoques"],
        merged["Passivo_Circulante"],
    )
    metrics["Margem_Bruta"] = _safe_divide(merged["Lucro_Bruto"], merged["Receita_Liquida"])
    metrics["Margem_Operacional"] = _safe_divide(
        merged["Resultado_Operacional"], merged["Receita_Liquida"]
    )
    metrics["Margem_Liquida"] = _safe_divide(merged["Lucro_Liquido"], merged["Receita_Liquida"])
    metrics["ROA"] = _safe_divide(merged["Lucro_Liquido"], merged["Ativo_Total"])
    metrics["ROE"] = _safe_divide(merged["Lucro_Liquido"], merged["Patrimonio_Liquido"])
    metrics["Giro_Ativo"] = _safe_divide(merged["Receita_Liquida"], merged["Ativo_Total"])
    metrics["Capital_Giro_Liquido"] = merged["Ativo_Circulante"] - merged["Passivo_Circulante"]
    metrics["Endividamento_Geral"] = _safe_divide(capital_terceiros, merged["Ativo_Total"])
    metrics["Composicao_Endividamento"] = _safe_divide(
        merged["Passivo_Circulante"], capital_terceiros
    )
    metrics["Divida_Bruta_sobre_Ativo"] = _safe_divide(
        merged["Divida_Bruta"], merged["Ativo_Total"]
    )
    metrics["Free_Cash_Flow"] = merged["Fluxo_Operacional"] - merged["CAPEX"]
    return metrics.sort_values("Ano").reset_index(drop=True)
