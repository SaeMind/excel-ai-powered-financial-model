# Excel Financial Model for a Health-Tech Startup

## Overview

This project generates a professional, formula-driven Excel financial model for a health-tech startup. It is built as a Clinical Data Science portfolio artifact with clean Python architecture, mypy-friendly type hints, healthcare SaaS metrics, scenario analysis, and timestamped exports.

The model includes:

- Three-year P&L projection
- Editable assumptions sheet
- Formula-driven Excel workbook
- Base, pessimistic, and optimistic scenarios
- SaaS unit economics: CAC, LTV, LTV:CAC, churn, GRR, NRR, payback, burn multiple
- Executive dashboard with KPI cards and charts
- Sensitivity analysis CSV for tornado-diagram workflows
- JSON export for downstream analytics

## Model Structure

```text
/excel-financial-model
├── /src
│   ├── model.py
│   ├── excel_writer.py
│   ├── scenarios.py
│   ├── calculations.py
│   └── config.py
├── /outputs
├── /tests
├── requirements.txt
├── .env.example
├── README.md
└── generate_model.py
```

## Workbook Tabs

| Sheet | Purpose |
|---|---|
| Dashboard | Executive KPI cards and charts |
| Assumptions | Editable model inputs with input cells highlighted |
| P&L Projection | Formula-driven 3-year financial projection |
| SaaS Metrics | CAC, LTV, LTV:CAC, payback, retention, burn multiple |
| Scenario Comparison | Base, pessimistic, and optimistic scenario summary |

## How to Use

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the base-case Excel model:

```bash
python generate_model.py --scenario base
```

Generate downside or upside cases:

```bash
python generate_model.py --scenario pessimistic
python generate_model.py --scenario optimistic
```

Generate scenario-only comparison JSON:

```bash
python generate_model.py --scenario all
```

Choose a custom output directory:

```bash
python generate_model.py --scenario base --output-dir outputs
```

## Outputs

Every generated artifact is timestamped:

```text
outputs/
├── financial_model_base_YYYYMMDD_HHMMSS.xlsx
├── scenario_summary_base_YYYYMMDD_HHMMSS.json
└── sensitivity_analysis_base_YYYYMMDD_HHMMSS.csv
```

## Sensitivity Analysis

The CSV output varies key assumptions from -30% to +30% in 10-point increments and records NPV impact.

Parameters tested:

- `year1_users`
- `year1_arpu`
- `user_growth_y1_y2`
- `cogs_percent_revenue`
- `opex_base`
- `cac`
- `monthly_churn`

Use this file to build a tornado diagram in Excel, Python, or BI tools.

## Healthcare SaaS Metrics

The model includes investor-grade SaaS and health-tech operating metrics:

| Metric | Why It Matters |
|---|---|
| CAC | Acquisition efficiency |
| LTV | Gross-margin adjusted user lifetime value |
| LTV:CAC | Unit economic quality |
| CAC Payback | Time to recover acquisition cost |
| GRR | Revenue retention before expansion |
| NRR | Revenue retention after expansion |
| Burn Multiple | Capital efficiency during growth |

## Financial Formatting

The workbook follows standard financial-modeling conventions:

- Blue font and yellow fill: editable hardcoded inputs
- Green font: linked formulas pulling from other worksheets
- Black font: calculations and local formulas
- Negative numbers: red and in parentheses
- Zeros: shown as `-`
- Gridlines hidden
- Total rows bordered

## Quality Checks

Run tests:

```bash
pytest
```

Run type checks:

```bash
mypy src generate_model.py
```

## Technologies Used

- Python
- openpyxl
- pandas
- xlwings
- pytest
- mypy

## Portfolio Positioning

This project demonstrates:

- Financial modeling fluency
- Healthcare SaaS business-model literacy
- Python package structure
- Excel automation
- Scenario analysis
- Sensitivity analysis
- Testable business logic
- Executive-ready reporting
