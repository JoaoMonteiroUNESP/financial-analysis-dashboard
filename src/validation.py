from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from src.config import ROUNDING_TOLERANCE_RL_THOUSAND
from src.data_loader import FinancialData


def _result(
    year: int,
    check: str,
    actual: float | None,
    expected: float | None,
    note: str,
    tolerance: float = ROUNDING_TOLERANCE_RL_THOUSAND,
) -> dict[str, object]:
    if actual is None or expected is None or pd.isna(actual) or pd.isna(expected):
        difference = None
        status = "Limitação"
    else:
        difference = float(actual) - float(expected)
        status = "OK" if abs(difference) <= tolerance else "Falha"
    return {
        "Ano": year,
        "Verificacao": check,
        "Valor_Observado": actual,
        "Valor_Esperado": expected,
        "Diferenca": difference,
        "Tolerancia": tolerance,
        "Status": status,
        "Observacao": note,
    }


def _row_for_year(frame: pd.DataFrame, year: int) -> pd.Series | None:
    rows = frame.loc[frame["Ano"] == year]
    return None if rows.empty else rows.iloc[0]


def validate_financial_statements(
    data: FinancialData,
    years: Iterable[int] | None = None,
) -> pd.DataFrame:
    """Run accounting reconciliations for every requested year."""
    selected_years = tuple(years) if years is not None else tuple(data.indicators["Ano"])
    results: list[dict[str, object]] = []

    for year in selected_years:
        dre = _row_for_year(data.income_statement, year)
        balance = _row_for_year(data.balance_sheet, year)
        cash = _row_for_year(data.cash_flow, year)

        if balance is not None:
            expected_assets = (
                balance["Passivo_Circulante"]
                + balance["Passivo_Nao_Circulante"]
                + balance["Patrimonio_Liquido"]
            )
            results.append(
                _result(
                    year,
                    "Equação patrimonial",
                    balance["Ativo_Total"],
                    expected_assets,
                    "Ativo total = passivos circulante e não circulante + patrimônio líquido.",
                )
            )

        if dre is not None:
            results.extend(
                [
                    _result(
                        year,
                        "Lucro bruto",
                        dre["Lucro_Bruto"],
                        dre["Receita_Liquida"] + dre["Custo_Produtos_Vendidos"],
                        "O CPV é armazenado com sinal negativo.",
                    ),
                    _result(
                        year,
                        "Resultado operacional",
                        dre["Resultado_Operacional"],
                        dre["Receita_Liquida"]
                        + dre["Custo_Produtos_Vendidos"]
                        + dre["Despesas_Vendas_Administrativas_Gerais"]
                        + dre["Outras_Receitas_Despesas_Operacionais_Liquidas"],
                        "Soma das linhas operacionais disponíveis no demonstrativo resumido.",
                    ),
                    _result(
                        year,
                        "Lucro antes de IR/CS",
                        dre["Lucro_Antes_IR_CS"],
                        dre["Resultado_Operacional"] + dre["Resultado_Financeiro"],
                        "Resultado operacional + resultado financeiro líquido.",
                    ),
                    _result(
                        year,
                        "Lucro líquido",
                        dre["Lucro_Liquido"],
                        dre["Lucro_Antes_IR_CS"] + dre["Imposto_Renda_Contribuicao_Social"],
                        "Inclui imposto de renda e contribuição social conforme publicado.",
                    ),
                ]
            )

        if cash is not None:
            results.extend(
                [
                    _result(
                        year,
                        "CAPEX",
                        cash["CAPEX"],
                        cash["Aquisicao_Imobilizado"] + cash["Aquisicao_Intangivel"],
                        "CAPEX inclui aquisições de imobilizado e intangível.",
                    ),
                    _result(
                        year,
                        "Fluxo de caixa livre",
                        cash["Free_Cash_Flow"],
                        cash["Fluxo_Operacional"] - cash["CAPEX"],
                        "FCF simplificado = fluxo operacional - CAPEX.",
                    ),
                    _result(
                        year,
                        "Variação de caixa",
                        cash["Variacao_Caixa"],
                        cash["Fluxo_Operacional"]
                        + cash["Fluxo_Investimento"]
                        + cash["Fluxo_Financiamento"],
                        (
                            "Não há linha adicional de efeito cambial nos demonstrativos "
                            "resumidos usados."
                        ),
                    ),
                ]
            )

    return pd.DataFrame(results)
