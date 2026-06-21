"""Tests for calculation utilities."""

from src.calculations import calculate_cogs, calculate_margin, calculate_revenue


def test_revenue_formula() -> None:
    """Revenue equals users times monthly ARPU times 12."""
    assert calculate_revenue(100, 10.0) == 12_000.0


def test_cogs_formula() -> None:
    """COGS equals revenue times COGS percentage."""
    assert calculate_cogs(100_000.0, 0.2) == 20_000.0


def test_margin_zero_division() -> None:
    """Margin returns zero when denominator is zero."""
    assert calculate_margin(10.0, 0.0) == 0.0
