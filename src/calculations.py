"""Reusable financial calculation utilities for the health-tech model."""

from __future__ import annotations

from typing import Iterable


def calculate_revenue(users: int, arpu_monthly: float) -> float:
    """Calculate annual recurring revenue.

    Parameters:
        users: Number of monetized users.
        arpu_monthly: Average revenue per user per month.

    Returns:
        Annual revenue in dollars.
    """
    return float(users * arpu_monthly * 12)


def calculate_cogs(revenue: float, cogs_percent_revenue: float) -> float:
    """Calculate cost of goods sold.

    Parameters:
        revenue: Annual revenue in dollars.
        cogs_percent_revenue: COGS as a decimal percentage of revenue.

    Returns:
        Annual COGS in dollars.
    """
    return float(revenue * cogs_percent_revenue)


def calculate_gross_profit(revenue: float, cogs: float) -> float:
    """Calculate gross profit.

    Parameters:
        revenue: Annual revenue in dollars.
        cogs: Annual cost of goods sold in dollars.

    Returns:
        Gross profit in dollars.
    """
    return float(revenue - cogs)


def calculate_margin(numerator: float, denominator: float) -> float:
    """Calculate a margin with divide-by-zero protection.

    Parameters:
        numerator: Profit or metric numerator.
        denominator: Revenue or metric denominator.

    Returns:
        Decimal margin; returns 0.0 when denominator is zero.
    """
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def calculate_ebitda(gross_profit: float, opex: float) -> float:
    """Calculate EBITDA.

    Parameters:
        gross_profit: Gross profit in dollars.
        opex: Operating expenses in dollars.

    Returns:
        EBITDA in dollars.
    """
    return float(gross_profit - opex)


def calculate_tax(ebitda: float, tax_rate: float) -> float:
    """Calculate taxes on positive EBITDA only.

    Parameters:
        ebitda: EBITDA in dollars.
        tax_rate: Corporate tax rate as a decimal.

    Returns:
        Tax expense in dollars.
    """
    return float(max(0.0, ebitda * tax_rate))


def calculate_net_income(ebitda: float, tax: float) -> float:
    """Calculate net income.

    Parameters:
        ebitda: EBITDA in dollars.
        tax: Tax expense in dollars.

    Returns:
        Net income in dollars.
    """
    return float(ebitda - tax)


def calculate_npv(cash_flows: Iterable[float], discount_rate: float) -> float:
    """Calculate net present value of annual cash flows.

    Parameters:
        cash_flows: Annual cash flows ordered from year 1 onward.
        discount_rate: Discount rate as a decimal.

    Returns:
        NPV in dollars.
    """
    return float(sum(cf / ((1 + discount_rate) ** year) for year, cf in enumerate(cash_flows, start=1)))
