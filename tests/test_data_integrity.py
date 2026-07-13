import shutil

import pandas as pd
import pytest

from src.config import EXPECTED_YEARS, PROCESSED_DATA_DIR
from src.data_loader import DataSchemaError, load_financial_data


def _copy_processed_data(tmp_path):
    target = tmp_path / "processed"
    shutil.copytree(PROCESSED_DATA_DIR, target)
    return target


def test_processed_datasets_have_expected_grain_and_no_missing_core_values() -> None:
    data = load_financial_data()
    datasets = (data.income_statement, data.balance_sheet, data.cash_flow, data.indicators)

    for frame in datasets:
        assert tuple(frame["Ano"]) == EXPECTED_YEARS
        assert not frame["Ano"].duplicated().any()

    assert not data.income_statement.isna().any().any()
    assert not data.balance_sheet.isna().any().any()
    assert not data.cash_flow.isna().any().any()
    assert not data.indicators.isna().any().any()


def test_reference_indicator_extract_matches_runtime_recalculation() -> None:
    data = load_financial_data()
    pd.testing.assert_frame_equal(
        data.indicators,
        data.reference_indicators[data.indicators.columns],
        check_exact=False,
        rtol=1e-10,
        atol=1e-10,
    )


def test_source_lineage_covers_each_statement_and_year() -> None:
    data = load_financial_data()
    expected = {
        (year, dataset)
        for year in EXPECTED_YEARS
        for dataset in ("DRE", "Balanco", "FluxoCaixa", "Indicadores")
    }
    actual = set(zip(data.sources["Ano"], data.sources["Conjunto"], strict=True))

    assert actual == expected
    assert (
        data.sources[
            [
                "Pagina_ou_Secao",
                "Unidade",
                "Arquivo_Fonte",
                "Base_Utilizada",
                "Natureza_Valores",
                "Transformacao",
                "Diferenca_Arredondamento",
            ]
        ]
        .notna()
        .all()
        .all()
    )


def test_capex_definition_is_consistent_across_all_years() -> None:
    data = load_financial_data()
    expected_capex = (
        data.cash_flow["Aquisicao_Imobilizado"] + data.cash_flow["Aquisicao_Intangivel"]
    )
    expected_fcf = data.cash_flow["Fluxo_Operacional"] - expected_capex

    pd.testing.assert_series_equal(data.cash_flow["CAPEX"], expected_capex, check_names=False)
    pd.testing.assert_series_equal(
        data.cash_flow["Free_Cash_Flow"], expected_fcf, check_names=False
    )


def test_representative_published_values_match_documented_sources() -> None:
    data = load_financial_data()
    income = data.income_statement.set_index("Ano")
    balance = data.balance_sheet.set_index("Ano")
    cash = data.cash_flow.set_index("Ano")

    expected_income = {
        2021: (20_914_334, 2_415_961, 1_632_182),
        2022: (24_457_959, 3_050_299, 1_417_662),
        2023: (20_562_335, 1_557_231, 835_558),
        2024: (21_386_145, 2_098_939, 976_041),
    }
    expected_balance = {
        2021: (18_901_356, 11_668_973, 737_838, 6_494_545),
        2022: (20_688_067, 12_674_242, 822_853, 7_190_972),
        2023: (18_009_272, 10_810_043, 657_323, 6_541_905),
        2024: (19_895_240, 12_428_674, 700_548, 6_766_018),
    }
    expected_cash = {
        2021: (1_293_167, -586_623, -99_097, 607_447, 542_821, 38_609),
        2022: (-319_007, -575_997, 37_476, -857_528, 494_189, 239),
        2023: (878_168, -505_867, -717_358, -345_057, 454_658, 4_045),
        2024: (3_131_759, -436_822, -1_870_456, 824_481, 382_734, 24_660),
    }

    for year in EXPECTED_YEARS:
        assert (
            tuple(income.loc[year, ["Receita_Liquida", "Resultado_Operacional", "Lucro_Liquido"]])
            == expected_income[year]
        )
        assert (
            tuple(
                balance.loc[
                    year,
                    [
                        "Ativo_Total",
                        "Passivo_Circulante",
                        "Passivo_Nao_Circulante",
                        "Patrimonio_Liquido",
                    ],
                ]
            )
            == expected_balance[year]
        )
        assert (
            tuple(
                cash.loc[
                    year,
                    [
                        "Fluxo_Operacional",
                        "Fluxo_Investimento",
                        "Fluxo_Financiamento",
                        "Variacao_Caixa",
                        "Aquisicao_Imobilizado",
                        "Aquisicao_Intangivel",
                    ],
                ]
            )
            == expected_cash[year]
        )


def test_accounting_sign_conventions_are_preserved() -> None:
    data = load_financial_data()
    assert data.income_statement["Custo_Produtos_Vendidos"].lt(0).all()
    assert data.income_statement["Despesas_Vendas_Administrativas_Gerais"].lt(0).all()
    assert data.income_statement["Imposto_Renda_Contribuicao_Social"].lt(0).all()
    assert data.cash_flow["Fluxo_Investimento"].lt(0).all()
    assert data.cash_flow["Aquisicao_Imobilizado"].gt(0).all()
    assert data.cash_flow["Aquisicao_Intangivel"].gt(0).all()
    assert data.cash_flow.set_index("Ano").loc[2022, "Fluxo_Operacional"] < 0
    assert data.cash_flow.set_index("Ano").loc[2022, "Free_Cash_Flow"] < 0


def test_gross_debt_equals_published_loan_and_lease_components() -> None:
    balance = load_financial_data().balance_sheet
    expected = (
        balance["Emprestimos_Circulante"]
        + balance["Emprestimos_Nao_Circulante"]
        + balance["Arrendamentos_Circulante"]
        + balance["Arrendamentos_Nao_Circulante"]
    )
    pd.testing.assert_series_equal(balance["Divida_Bruta"], expected, check_names=False)
    assert balance.set_index("Ano").loc[2024, "Emprestimos_Nao_Circulante"] == 0


def test_2022_comparative_reclassification_preserves_cash_change() -> None:
    selected = load_financial_data().cash_flow.set_index("Ano").loc[2022]
    original = {
        "Fluxo_Operacional": -298_298,
        "Fluxo_Investimento": -579_084,
        "Fluxo_Financiamento": 19_854,
        "Variacao_Caixa": -857_528,
    }

    assert selected["Fluxo_Operacional"] - original["Fluxo_Operacional"] == -20_709
    assert selected["Fluxo_Investimento"] - original["Fluxo_Investimento"] == 3_087
    assert selected["Fluxo_Financiamento"] - original["Fluxo_Financiamento"] == 17_622
    assert selected["Variacao_Caixa"] == original["Variacao_Caixa"]


def test_2023_restatement_reclassifies_cash_without_changing_total() -> None:
    selected = load_financial_data().cash_flow.set_index("Ano").loc[2023]
    original = {
        "Fluxo_Operacional": 706_090,
        "Fluxo_Investimento": -505_867,
        "Fluxo_Financiamento": -545_280,
        "Variacao_Caixa": -345_057,
    }

    assert selected["Fluxo_Operacional"] - original["Fluxo_Operacional"] == 172_078
    assert selected["Fluxo_Investimento"] == original["Fluxo_Investimento"]
    assert selected["Fluxo_Financiamento"] - original["Fluxo_Financiamento"] == -172_078
    assert selected["Variacao_Caixa"] == original["Variacao_Caixa"]


def test_missing_required_column_is_rejected(tmp_path) -> None:
    data_dir = _copy_processed_data(tmp_path)
    path = data_dir / "dre.csv"
    frame = pd.read_csv(path).drop(columns="Receita_Liquida")
    frame.to_csv(path, index=False)

    with pytest.raises(DataSchemaError, match="colunas obrigatórias ausentes"):
        load_financial_data(data_dir)


def test_missing_core_value_is_rejected(tmp_path) -> None:
    data_dir = _copy_processed_data(tmp_path)
    path = data_dir / "balance_sheet.csv"
    frame = pd.read_csv(path)
    frame.loc[frame["Ano"] == 2024, "Ativo_Total"] = None
    frame.to_csv(path, index=False)

    with pytest.raises(DataSchemaError, match="valores ausentes"):
        load_financial_data(data_dir)


def test_duplicate_year_is_rejected(tmp_path) -> None:
    data_dir = _copy_processed_data(tmp_path)
    path = data_dir / "cash_flow.csv"
    frame = pd.read_csv(path)
    frame.loc[frame["Ano"] == 2024, "Ano"] = 2023
    frame.to_csv(path, index=False)

    with pytest.raises(DataSchemaError, match="anos duplicados"):
        load_financial_data(data_dir)


def test_missing_processed_file_is_rejected(tmp_path) -> None:
    data_dir = _copy_processed_data(tmp_path)
    (data_dir / "dre.csv").unlink()

    with pytest.raises(DataSchemaError, match="Arquivo processado não encontrado"):
        load_financial_data(data_dir)


def test_public_csv_metadata_contains_no_local_paths() -> None:
    for path in PROCESSED_DATA_DIR.glob("*.csv"):
        text = path.read_text(encoding="utf-8")
        assert "C:\\Users\\" not in text
        assert "data/raw/" not in text
