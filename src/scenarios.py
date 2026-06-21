"""Scenario definitions and scenario analysis helpers."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict

from .model import Assumptions, FinancialModel


def create_base_case() -> Assumptions:
    """Create base-case assumptions.

    Returns:
        Assumptions for expected execution.
    """
    return Assumptions(
        year1_users=100_000,
        year1_arpu=9.99,
        user_growth_y1_y2=3.0,
        user_growth_y2_y3=2.0,
        arpu_growth=0.10,
        cogs_percent_revenue=0.15,
        opex_base=8_000_000,
        opex_growth=0.10,
        tax_rate=0.21,
        discount_rate=0.10,
        cac=18.00,
        monthly_churn=0.035,
        gross_revenue_retention=0.86,
        net_revenue_retention=1.12,
        starting_cash=12_000_000,
    )


def create_pessimistic_case() -> Assumptions:
    """Create pessimistic assumptions.

    Returns:
        Assumptions for downside execution.
    """
    return Assumptions(
        year1_users=50_000,
        year1_arpu=7.99,
        user_growth_y1_y2=1.5,
        user_growth_y2_y3=1.3,
        arpu_growth=0.04,
        cogs_percent_revenue=0.25,
        opex_base=10_000_000,
        opex_growth=0.15,
        tax_rate=0.21,
        discount_rate=0.15,
        cac=34.00,
        monthly_churn=0.060,
        gross_revenue_retention=0.72,
        net_revenue_retention=0.92,
        starting_cash=12_000_000,
    )


def create_optimistic_case() -> Assumptions:
    """Create optimistic assumptions.

    Returns:
        Assumptions for upside execution.
    """
    return Assumptions(
        year1_users=150_000,
        year1_arpu=12.99,
        user_growth_y1_y2=5.0,
        user_growth_y2_y3=3.0,
        arpu_growth=0.15,
        cogs_percent_revenue=0.10,
        opex_base=7_000_000,
        opex_growth=0.08,
        tax_rate=0.21,
        discount_rate=0.08,
        cac=14.00,
        monthly_churn=0.020,
        gross_revenue_retention=0.91,
        net_revenue_retention=1.28,
        starting_cash=12_000_000,
    )


def get_assumptions_for_scenario(scenario: str) -> Assumptions:
    """Resolve a scenario name into assumptions.

    Parameters:
        scenario: One of base, pessimistic, or optimistic.

    Returns:
        Assumptions for the selected scenario.
    """
    scenario_map = {
        "base": create_base_case,
        "pessimistic": create_pessimistic_case,
        "optimistic": create_optimistic_case,
    }
    if scenario not in scenario_map:
        raise ValueError(f"Unsupported scenario: {scenario}")
    return scenario_map[scenario]()


def run_scenario_analysis() -> Dict[str, Dict[str, float | int | Dict[str, float | int]]]:
    """Run base, pessimistic, and optimistic scenarios.

    Returns:
        Comparative scenario result dictionary.
    """
    output: Dict[str, Dict[str, float | int | Dict[str, float | int]]] = {}
    for scenario_name in ["base", "pessimistic", "optimistic"]:
        assumptions = get_assumptions_for_scenario(scenario_name)
        model = FinancialModel(assumptions)
        model.run()
        y3 = model.results[3]
        output[scenario_name] = {
            "assumptions": asdict(assumptions),
            "year3_revenue": y3.revenue,
            "year3_ebitda": y3.ebitda,
            "year3_net_income": y3.net_income,
            "year3_ebitda_margin": y3.ebitda_margin,
            "npv_3_year": model.calculate_npv(),
            "year3_users": y3.users,
            "ltv_cac_ratio_y3": y3.ltv_cac_ratio,
            "payback_months_y3": y3.payback_months,
            "ending_cash_y3": y3.ending_cash,
        }
    return output
