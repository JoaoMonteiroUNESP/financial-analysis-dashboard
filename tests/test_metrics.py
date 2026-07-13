import pandas as pd

from src.financial_metrics import calculate_financial_metrics


def test_metrics_use_documented_formulas() -> None:
    income = pd.DataFrame(
        {
            "Ano": [2024],
            "Receita_Liquida": [1_000.0],
            "Lucro_Bruto": [300.0],
            "Resultado_Operacional": [120.0],
            "Lucro_Liquido": [60.0],
        }
    )
    balance = pd.DataFrame(
        {
            "Ano": [2024],
            "Ativo_Circulante": [500.0],
            "Estoques": [100.0],
            "Passivo_Circulante": [250.0],
            "Passivo_Nao_Circulante": [150.0],
            "Ativo_Total": [800.0],
            "Patrimonio_Liquido": [400.0],
            "Divida_Bruta": [80.0],
        }
    )
    cash_flow = pd.DataFrame(
        {
            "Ano": [2024],
            "Fluxo_Operacional": [140.0],
            "CAPEX": [40.0],
            "Free_Cash_Flow": [100.0],
        }
    )

    metrics = calculate_financial_metrics(income, balance, cash_flow).iloc[0]

    assert metrics["Liquidez_Corrente"] == 2.0
    assert metrics["Liquidez_Seca"] == 1.6
    assert metrics["Margem_Bruta"] == 0.3
    assert metrics["Margem_Operacional"] == 0.12
    assert metrics["Margem_Liquida"] == 0.06
    assert metrics["ROA"] == 0.075
    assert metrics["ROE"] == 0.15
    assert metrics["Giro_Ativo"] == 1.25
    assert metrics["Capital_Giro_Liquido"] == 250.0
    assert metrics["Endividamento_Geral"] == 0.5
    assert metrics["Composicao_Endividamento"] == 0.625
    assert metrics["Divida_Bruta_sobre_Ativo"] == 0.1
    assert metrics["Free_Cash_Flow"] == 100.0


def test_zero_denominator_returns_missing_value() -> None:
    income = pd.DataFrame(
        {
            "Ano": [2024],
            "Receita_Liquida": [0.0],
            "Lucro_Bruto": [0.0],
            "Resultado_Operacional": [0.0],
            "Lucro_Liquido": [0.0],
        }
    )
    balance = pd.DataFrame(
        {
            "Ano": [2024],
            "Ativo_Circulante": [0.0],
            "Estoques": [0.0],
            "Passivo_Circulante": [0.0],
            "Passivo_Nao_Circulante": [0.0],
            "Ativo_Total": [0.0],
            "Patrimonio_Liquido": [0.0],
            "Divida_Bruta": [0.0],
        }
    )
    cash_flow = pd.DataFrame(
        {
            "Ano": [2024],
            "Fluxo_Operacional": [0.0],
            "CAPEX": [0.0],
            "Free_Cash_Flow": [0.0],
        }
    )

    metrics = calculate_financial_metrics(income, balance, cash_flow).iloc[0]
    assert pd.isna(metrics["Liquidez_Corrente"])
    assert pd.isna(metrics["Margem_Liquida"])
    assert pd.isna(metrics["ROE"])


def test_negative_results_and_cash_flow_keep_their_signs() -> None:
    income = pd.DataFrame(
        {
            "Ano": [2024],
            "Receita_Liquida": [1_000.0],
            "Lucro_Bruto": [-100.0],
            "Resultado_Operacional": [-120.0],
            "Lucro_Liquido": [-60.0],
        }
    )
    balance = pd.DataFrame(
        {
            "Ano": [2024],
            "Ativo_Circulante": [500.0],
            "Estoques": [100.0],
            "Passivo_Circulante": [250.0],
            "Passivo_Nao_Circulante": [150.0],
            "Ativo_Total": [800.0],
            "Patrimonio_Liquido": [400.0],
            "Divida_Bruta": [80.0],
        }
    )
    cash_flow = pd.DataFrame(
        {
            "Ano": [2024],
            "Fluxo_Operacional": [-20.0],
            "CAPEX": [5.0],
            "Free_Cash_Flow": [-25.0],
        }
    )

    metrics = calculate_financial_metrics(income, balance, cash_flow).iloc[0]
    assert metrics["Margem_Bruta"] == -0.1
    assert metrics["Margem_Operacional"] == -0.12
    assert metrics["Margem_Liquida"] == -0.06
    assert metrics["ROA"] == -0.075
    assert metrics["ROE"] == -0.15
    assert metrics["Free_Cash_Flow"] == -25.0
