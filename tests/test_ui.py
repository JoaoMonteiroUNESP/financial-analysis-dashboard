from src.ui import format_money, format_percent, format_ratio, percentage_delta


def test_money_format_uses_brazilian_separators_in_thousands() -> None:
    assert format_money(21_386_145, "R$ mil") == "R$ 21.386.145 mil"


def test_money_format_uses_brazilian_separators_in_millions() -> None:
    assert format_money(21_386_145, "R$ milhões") == "R$ 21.386,1 mi"


def test_ratios_percentages_and_deltas_use_brazilian_decimal_separator() -> None:
    assert format_percent(0.046) == "4,6%"
    assert format_ratio(1.2) == "1,20x"
    assert percentage_delta(104.0, 100.0) == "+4,0% vs. anterior"
