from dataclasses import replace

from src.data_loader import load_financial_data
from src.validation import validate_financial_statements


def test_all_accounting_checks_are_within_rounding_tolerance() -> None:
    data = load_financial_data()
    results = validate_financial_statements(data)

    assert not results.empty
    assert len(results) == 32
    assert set(results["Status"]) == {"OK"}
    assert results["Diferenca"].abs().max() <= 1


def test_balance_sheet_failure_is_detected() -> None:
    data = load_financial_data()
    modified_balance = data.balance_sheet.copy()
    modified_balance.loc[modified_balance["Ano"] == 2024, "Ativo_Total"] += 10
    modified_data = replace(data, balance_sheet=modified_balance)

    results = validate_financial_statements(modified_data, years=[2024])
    balance_check = results.loc[results["Verificacao"] == "Equação patrimonial"].iloc[0]

    assert balance_check["Status"] == "Falha"
    assert balance_check["Diferenca"] == 10


def test_known_rounding_differences_are_preserved() -> None:
    results = validate_financial_statements(load_financial_data())
    differences = results.set_index(["Ano", "Verificacao"])["Diferenca"]

    assert differences.loc[(2022, "Resultado operacional")] == -1
    assert differences.loc[(2023, "Equação patrimonial")] == 1
    assert differences.loc[(2023, "Lucro líquido")] == -1


def test_cash_reconciliation_failure_is_detected() -> None:
    data = load_financial_data()
    modified_cash = data.cash_flow.copy()
    modified_cash.loc[modified_cash["Ano"] == 2024, "Fluxo_Financiamento"] += 2
    modified_data = replace(data, cash_flow=modified_cash)

    results = validate_financial_statements(modified_data, years=[2024])
    cash_check = results.loc[results["Verificacao"] == "Variação de caixa"].iloc[0]

    assert cash_check["Status"] == "Falha"
    assert cash_check["Diferenca"] == -2
