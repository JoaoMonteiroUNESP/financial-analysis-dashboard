from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
EXPECTED_YEARS = (2021, 2022, 2023, 2024)
ROUNDING_TOLERANCE_RL_THOUSAND = 1.0

INDEPENDENCE_NOTICE = (
    "Projeto acadêmico independente, desenvolvido para fins educacionais e de portfólio. "
    "Não representa, não foi patrocinado e não foi validado oficialmente pela BASF."
)
