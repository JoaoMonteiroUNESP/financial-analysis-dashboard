from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.config import EXPECTED_YEARS, PROCESSED_DATA_DIR
from src.financial_metrics import calculate_financial_metrics


class DataSchemaError(ValueError):
    """Raised when a processed dataset does not follow the documented schema."""


@dataclass(frozen=True)
class FinancialData:
    income_statement: pd.DataFrame
    balance_sheet: pd.DataFrame
    cash_flow: pd.DataFrame
    indicators: pd.DataFrame
    reference_indicators: pd.DataFrame
    sources: pd.DataFrame
    data_dictionary: pd.DataFrame


SCHEMAS = {
    "dre.csv": {
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
        "Unidade_Monetaria",
        "Demonstrativo_Origem",
        "Arquivo_Fonte",
        "Observacao_Reapresentacao",
    },
    "balance_sheet.csv": {
        "Ano",
        "Caixa_Equivalentes",
        "Contas_Receber_Clientes_Circulante",
        "Estoques",
        "Ativo_Circulante",
        "Ativo_Nao_Circulante",
        "Ativo_Total",
        "Passivo_Circulante",
        "Passivo_Nao_Circulante",
        "Patrimonio_Liquido",
        "Emprestimos_Circulante",
        "Emprestimos_Nao_Circulante",
        "Arrendamentos_Circulante",
        "Arrendamentos_Nao_Circulante",
        "Divida_Bruta",
        "Capital_Terceiros",
        "Unidade_Monetaria",
        "Demonstrativo_Origem",
        "Arquivo_Fonte",
        "Observacao_Reapresentacao",
    },
    "cash_flow.csv": {
        "Ano",
        "Fluxo_Operacional",
        "Fluxo_Investimento",
        "Fluxo_Financiamento",
        "Variacao_Caixa",
        "Aquisicao_Imobilizado",
        "Aquisicao_Intangivel",
        "CAPEX",
        "Free_Cash_Flow",
        "Unidade_Monetaria",
        "Demonstrativo_Origem",
        "Arquivo_Fonte",
        "Observacao_Reapresentacao",
    },
}


def _read_csv(path: Path, required_columns: set[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        raise DataSchemaError(f"Arquivo processado não encontrado: {path}")
    frame = pd.read_csv(path)
    if required_columns:
        missing = required_columns.difference(frame.columns)
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise DataSchemaError(f"{path.name}: colunas obrigatórias ausentes: {missing_text}")
        columns_with_nulls = sorted(
            column for column in required_columns if frame[column].isna().any()
        )
        if columns_with_nulls:
            null_text = ", ".join(columns_with_nulls)
            raise DataSchemaError(f"{path.name}: valores ausentes em: {null_text}")
    return frame


def _validate_year_grain(frame: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    if "Ano" not in frame.columns:
        raise DataSchemaError(f"{dataset_name}: coluna Ano ausente")
    if frame["Ano"].isna().any():
        raise DataSchemaError(f"{dataset_name}: há anos ausentes")
    frame = frame.copy()
    frame["Ano"] = pd.to_numeric(frame["Ano"], errors="raise").astype(int)
    if frame["Ano"].duplicated().any():
        duplicates = sorted(frame.loc[frame["Ano"].duplicated(), "Ano"].unique())
        raise DataSchemaError(f"{dataset_name}: anos duplicados: {duplicates}")
    actual_years = tuple(sorted(frame["Ano"].tolist()))
    if actual_years != EXPECTED_YEARS:
        raise DataSchemaError(
            f"{dataset_name}: anos esperados {EXPECTED_YEARS}; encontrados {actual_years}"
        )
    return frame.sort_values("Ano").reset_index(drop=True)


def load_financial_data(data_dir: Path | None = None) -> FinancialData:
    """Load processed CSVs, validate their grain and recalculate indicators."""
    base_dir = Path(data_dir) if data_dir is not None else PROCESSED_DATA_DIR
    income_statement = _validate_year_grain(
        _read_csv(base_dir / "dre.csv", SCHEMAS["dre.csv"]), "DRE"
    )
    balance_sheet = _validate_year_grain(
        _read_csv(base_dir / "balance_sheet.csv", SCHEMAS["balance_sheet.csv"]),
        "Balanço",
    )
    cash_flow = _validate_year_grain(
        _read_csv(base_dir / "cash_flow.csv", SCHEMAS["cash_flow.csv"]),
        "Fluxo de caixa",
    )
    reference_indicators = _validate_year_grain(
        _read_csv(base_dir / "indicators.csv"), "Indicadores de referência"
    )
    sources = _read_csv(base_dir / "sources.csv")
    data_dictionary = _read_csv(base_dir / "data_dictionary.csv")

    indicators = calculate_financial_metrics(income_statement, balance_sheet, cash_flow)
    return FinancialData(
        income_statement=income_statement,
        balance_sheet=balance_sheet,
        cash_flow=cash_flow,
        indicators=indicators,
        reference_indicators=reference_indicators,
        sources=sources,
        data_dictionary=data_dictionary,
    )
