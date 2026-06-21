"""Tests for scenario analysis."""

from src.scenarios import run_scenario_analysis


def test_run_scenario_analysis_keys() -> None:
    """Scenario analysis returns all required cases."""
    results = run_scenario_analysis()
    assert set(results.keys()) == {"base", "pessimistic", "optimistic"}
