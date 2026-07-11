from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_fund_metadata(path: str | Path) -> pd.DataFrame:
    """Load fund code/name metadata from a CSV file."""
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=["fund_code", "fund_name"]).set_index("fund_code")

    metadata = pd.read_csv(path, dtype={"fund_code": str})
    required_columns = {"fund_code", "fund_name"}
    missing = required_columns - set(metadata.columns)
    if missing:
        raise ValueError(f"Fund metadata is missing columns: {missing}")

    metadata["fund_code"] = metadata["fund_code"].str.zfill(6)
    metadata["fund_name"] = metadata["fund_name"].fillna(metadata["fund_code"])
    return metadata.drop_duplicates("fund_code").set_index("fund_code")


def attach_fund_metadata(metrics: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Attach fund names to a metrics table indexed by fund code."""
    if metadata.empty:
        return metrics

    enriched = metrics.copy()
    aligned = metadata.reindex(enriched.index.astype(str))
    enriched.insert(0, "fund_name", aligned["fund_name"].fillna(pd.Series(enriched.index, index=enriched.index)))
    return enriched


def display_fund(fund_code: str, row: pd.Series) -> str:
    """Format a fund as 'code name' when metadata is available."""
    fund_name = row.get("fund_name")
    if pd.isna(fund_name) or not fund_name:
        return str(fund_code)
    return f"{fund_code} {fund_name}"
