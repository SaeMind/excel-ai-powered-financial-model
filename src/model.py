"""Financial model domain objects and projection engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Tuple

from .calculations import (
    calculate_cogs,
    calculate_ebitda,
    calculate_gross_profit,
    calculate_margin,
    calculate_net_income,
    calculate_npv,
    calculate_revenue,
    calculate_tax,
)


@dataclass(frozen=True)
class Assumptions:
    """Financial model assumptions.

    Attributes:
        year1_users: Year 1 monetized users.
        year1_arpu: Average monthly revenue per user.
        user_growth_y1_y2: User multiplier from year 1 to year 2.
        user_growth_y2_y3: User multiplier from year 2 to year 3.
        arpu_growth: Annual ARPU growth rate.
        cogs_percent_revenue: COGS as percentage of revenue.
        opex_base: Year 1 operating expense.
        opex_growth: Annual opex growth rate.
        tax_rate: Corporate tax rate.
        discount_rate: Discount rate for NPV.
        cac: Customer acquisition cost per new user.
        monthly_churn: Monthly logo churn rate.
        gross_revenue_retention: Gross revenue retention.
        net_revenue_retention: Net revenue retention.
        starting_cash: Starting cash balance.
    """

    year1_users: int
    year1_arpu: float
    user_growth_y1_y2: float
    user_growth_y2_y3: float
    arpu_growth: float
    cogs_percent_revenue: float
    opex_base: float
    opex_growth: float
    tax_rate: float
    discount_rate: float
    cac: float
    monthly_churn: float
    gross_revenue_retention: float
    net_revenue_retention: float
    starting_cash: float


@dataclass(frozen=True)
class YearResult:
    """Annual financial result.

    Attributes:
        year: Projection year number.
        users: Ending monetized users.
        arpu_monthly: Monthly ARPU.
        revenue: Annual revenue.
        cogs: Cost of goods sold.
        gross_profit: Revenue less COGS.
        gross_margin: Gross margin percentage.
        opex: Operating expenses.
        ebitda: EBITDA.
        ebitda_margin: EBITDA margin percentage.
        tax: Tax expense.
        net_income: Net income.
        net_margin: Net margin percentage.
        new_users: Incremental users acquired during the year.
        sales_marketing_spend: Implied acquisition spend.
        ltv: Gross-margin-adjusted lifetime value.
        ltv_cac_ratio: LTV divided by CAC.
        payback_months: CAC payback period in months.
        burn_multiple: Net burn divided by net new ARR.
        ending_cash: Ending cash balance after net income.
    """

    year: int
    users: int
    arpu_monthly: float
    revenue: float
    cogs: float
    gross_profit: float
    gross_margin: float
    opex: float
    ebitda: float
    ebitda_margin: float
    tax: float
    net_income: float
    net_margin: float
    new_users: int
    sales_marketing_spend: float
    ltv: float
    ltv_cac_ratio: float
    payback_months: float
    burn_multiple: float
    ending_cash: float


class FinancialModel:
    """Three-year financial model for a health-tech startup.

    The model projects users, revenue, profitability, cash balance, SaaS metrics,
    NPV, and sensitivity impact across editable assumptions.
    """

    def __init__(self, assumptions: Assumptions) -> None:
        """Initialize model with assumptions.

        Parameters:
            assumptions: Financial model inputs.
        """
        self.assumptions = assumptions
        self.results: Dict[int, YearResult] = {}

    def run(self) -> Dict[int, YearResult]:
        """Run the three-year projection.

        Returns:
            Dictionary mapping year number to YearResult.
        """
        self.results = {}
        for year in range(1, 4):
            self.results[year] = self._calculate_year(year)
        return self.results

    def _calculate_year(self, year: int) -> YearResult:
        """Calculate financials for a single year.

        Parameters:
            year: Projection year from 1 to 3.

        Returns:
            YearResult for the requested year.
        """
        if year == 1:
            users = self.assumptions.year1_users
            arpu = self.assumptions.year1_arpu
            opex = self.assumptions.opex_base
            prior_users = 0
            prior_revenue = 0.0
            prior_cash = self.assumptions.starting_cash
        elif year == 2:
            prior = self.results[1]
            users = int(prior.users * self.assumptions.user_growth_y1_y2)
            arpu = prior.arpu_monthly * (1 + self.assumptions.arpu_growth)
            opex = prior.opex * (1 + self.assumptions.opex_growth)
            prior_users = prior.users
            prior_revenue = prior.revenue
            prior_cash = prior.ending_cash
        elif year == 3:
            prior = self.results[2]
            users = int(prior.users * self.assumptions.user_growth_y2_y3)
            arpu = prior.arpu_monthly * (1 + self.assumptions.arpu_growth)
            opex = prior.opex * (1 + self.assumptions.opex_growth)
            prior_users = prior.users
            prior_revenue = prior.revenue
            prior_cash = prior.ending_cash
        else:
            raise ValueError("Model supports years 1 through 3 only.")

        revenue = calculate_revenue(users, arpu)
        cogs = calculate_cogs(revenue, self.assumptions.cogs_percent_revenue)
        gross_profit = calculate_gross_profit(revenue, cogs)
        gross_margin = calculate_margin(gross_profit, revenue)
        ebitda = calculate_ebitda(gross_profit, opex)
        ebitda_margin = calculate_margin(ebitda, revenue)
        tax = calculate_tax(ebitda, self.assumptions.tax_rate)
        net_income = calculate_net_income(ebitda, tax)
        net_margin = calculate_margin(net_income, revenue)
        new_users = max(users - prior_users, 0)
        sales_marketing_spend = new_users * self.assumptions.cac
        ltv = (arpu * 12 * gross_margin) / max(self.assumptions.monthly_churn * 12, 0.0001)
        ltv_cac_ratio = ltv / self.assumptions.cac if self.assumptions.cac else 0.0
        payback_months = self.assumptions.cac / max(arpu * gross_margin, 0.0001)
        net_new_arr = max(revenue - prior_revenue, 0.0)
        burn_multiple = abs(min(net_income, 0.0)) / net_new_arr if net_new_arr else 0.0
        ending_cash = prior_cash + net_income

        return YearResult(
            year=year,
            users=users,
            arpu_monthly=arpu,
            revenue=revenue,
            cogs=cogs,
            gross_profit=gross_profit,
            gross_margin=gross_margin,
            opex=opex,
            ebitda=ebitda,
            ebitda_margin=ebitda_margin,
            tax=tax,
            net_income=net_income,
            net_margin=net_margin,
            new_users=new_users,
            sales_marketing_spend=sales_marketing_spend,
            ltv=ltv,
            ltv_cac_ratio=ltv_cac_ratio,
            payback_months=payback_months,
            burn_multiple=burn_multiple,
            ending_cash=ending_cash,
        )

    def calculate_npv(self) -> float:
        """Calculate net present value from projected net income.

        Returns:
            Three-year NPV in dollars.
        """
        if not self.results:
            self.run()
        return calculate_npv((result.net_income for result in self.results.values()), self.assumptions.discount_rate)

    def to_dict(self) -> Dict[str, object]:
        """Serialize model assumptions and results.

        Returns:
            JSON-ready dictionary.
        """
        if not self.results:
            self.run()
        return {
            "assumptions": asdict(self.assumptions),
            "results": {str(year): asdict(result) for year, result in self.results.items()},
            "npv_3_year": self.calculate_npv(),
        }

    def sensitivity_analysis(self, parameter: str, range_pct: Tuple[int, int] = (-30, 30)) -> Dict[int, float]:
        """Vary a parameter and calculate resulting NPV.

        Parameters:
            parameter: Assumption field to test.
            range_pct: Inclusive percentage range in 10-point increments.

        Returns:
            Mapping from percentage change to NPV.
        """
        if not hasattr(self.assumptions, parameter):
            raise ValueError(f"Unknown assumption parameter: {parameter}")

        base_value = getattr(self.assumptions, parameter)
        results: Dict[int, float] = {}
        for pct in range(range_pct[0], range_pct[1] + 1, 10):
            modified = dict(asdict(self.assumptions))
            modified[parameter] = base_value * (1 + pct / 100)
            if parameter == "year1_users":
                modified[parameter] = int(modified[parameter])
            model = FinancialModel(Assumptions(**modified))
            model.run()
            results[pct] = model.calculate_npv()
        return results
