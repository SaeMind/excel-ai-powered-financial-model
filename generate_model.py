"""Command-line entry point for generating the financial model artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

from src.config import ModelConfig
from src.excel_writer import ExcelFinancialModel
from src.model import FinancialModel
from src.scenarios import get_assumptions_for_scenario, run_scenario_analysis


def write_json(path: Path, payload: Dict[str, object]) -> None:
    """Write JSON output.

    Parameters:
        path: Destination path.
        payload: JSON-serializable content.

    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_sensitivity_csv(path: Path, model: FinancialModel, parameters: List[str]) -> None:
    """Write sensitivity analysis tornado data to CSV.

    Parameters:
        path: Destination CSV path.
        model: Financial model to test.
        parameters: Assumption fields to vary.

    Returns:
        None.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["parameter", "pct_change", "npv"])
        writer.writeheader()
        for parameter in parameters:
            for pct_change, npv in model.sensitivity_analysis(parameter).items():
                writer.writerow({"parameter": parameter, "pct_change": pct_change, "npv": round(npv, 2)})


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed argparse namespace.
    """
    parser = argparse.ArgumentParser(description="Generate health-tech financial model artifacts.")
    parser.add_argument("--scenario", default="base", choices=["base", "pessimistic", "optimistic", "all"])
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    """Generate Excel, JSON, and sensitivity outputs.

    Returns:
        None.
    """
    args = parse_args()
    config = ModelConfig.from_env(args.output_dir)
    config.output_dir.mkdir(parents=True, exist_ok=True)

    print("Health-Tech Financial Model Generator")
    print("=" * 48)

    if args.scenario == "all":
        scenario_results = run_scenario_analysis()
        scenario_path = config.output_path("scenario_summary", ".json")
        write_json(scenario_path, {"scenarios": scenario_results})
        print(f"Scenario summary: {scenario_path}")
        return

    assumptions = get_assumptions_for_scenario(args.scenario)
    model = FinancialModel(assumptions)
    model.run()

    excel_path = config.output_path(f"financial_model_{args.scenario}", ".xlsx")
    scenario_path = config.output_path(f"scenario_summary_{args.scenario}", ".json")
    sensitivity_path = config.output_path(f"sensitivity_analysis_{args.scenario}", ".csv")

    ExcelFinancialModel(model, excel_path).write_model()
    write_json(scenario_path, model.to_dict())
    write_sensitivity_csv(
        sensitivity_path,
        model,
        ["year1_users", "year1_arpu", "user_growth_y1_y2", "cogs_percent_revenue", "opex_base", "cac", "monthly_churn"],
    )

    y3 = model.results[3]
    print(f"Scenario: {args.scenario}")
    print(f"Year 3 Revenue: ${y3.revenue:,.0f}")
    print(f"Year 3 EBITDA: ${y3.ebitda:,.0f} ({y3.ebitda_margin:.1%})")
    print(f"Year 3 Users: {y3.users:,}")
    print(f"3-Year NPV: ${model.calculate_npv():,.0f}")
    print("\nGenerated:")
    print(f"- {excel_path}")
    print(f"- {scenario_path}")
    print(f"- {sensitivity_path}")


if __name__ == "__main__":
    main()
