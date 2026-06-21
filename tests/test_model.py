"""Tests for financial model projections."""

from src.model import FinancialModel
from src.scenarios import create_base_case


def test_base_case_year3_users() -> None:
    """Base case produces expected Year 3 user count."""
    model = FinancialModel(create_base_case())
    model.run()
    assert model.results[3].users == 600_000


def test_npv_runs_after_projection() -> None:
    """NPV can be calculated after model execution."""
    model = FinancialModel(create_base_case())
    model.run()
    assert isinstance(model.calculate_npv(), float)


def test_sensitivity_analysis_has_expected_points() -> None:
    """Sensitivity analysis returns seven 10-point increments from -30% to +30%."""
    model = FinancialModel(create_base_case())
    model.run()
    results = model.sensitivity_analysis("year1_arpu")
    assert list(results.keys()) == [-30, -20, -10, 0, 10, 20, 30]
