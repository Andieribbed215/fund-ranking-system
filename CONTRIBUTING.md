# Contributing

Thanks for considering a contribution. This project is a local-first research and portfolio project for public mutual fund risk-return analysis.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e . pytest
python -m pytest -q
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e . pytest
.\.venv\Scripts\python.exe -m pytest -q
```

## Good First Contributions

- Improve documentation, screenshots, or demo instructions.
- Add tests for scoring, data quality checks, or report generation.
- Improve error messages when AkShare data fetching fails.
- Add small, well-explained fund metadata features.

## Contribution Rules

- Keep the project local-first and reproducible.
- Do not add personalized investment advice or buy/sell recommendations.
- Keep financial claims clearly tied to historical data and validation results.
- Add or update tests when changing behavior.
- Avoid committing generated local files under `data/` or `reports/`.

## Pull Request Checklist

- Tests pass with `python -m pytest -q`.
- README or docs are updated when user-facing behavior changes.
- New finance-related wording keeps the research-only boundary clear.
