from __future__ import annotations

from pathlib import Path

import pandas as pd

from .metadata import display_fund


def build_sensitivity_table(all_profiles: pd.DataFrame) -> pd.DataFrame:
    """Compare rank stability across investor profiles."""
    rank_columns = [column for column in all_profiles.columns if column.endswith("_rank")]
    score_columns = [column for column in all_profiles.columns if column.endswith("_score")]

    if not rank_columns:
        raise ValueError("No profile rank columns found for sensitivity analysis.")

    metadata_columns = [column for column in ["fund_name"] if column in all_profiles.columns]
    summary = all_profiles[metadata_columns + rank_columns + score_columns].copy()
    summary["best_rank"] = summary[rank_columns].min(axis=1)
    summary["worst_rank"] = summary[rank_columns].max(axis=1)
    summary["rank_spread"] = summary["worst_rank"] - summary["best_rank"]
    summary["avg_rank"] = summary[rank_columns].mean(axis=1)
    return summary.sort_values(["avg_rank", "rank_spread"])


def build_sensitivity_markdown(
    sensitivity: pd.DataFrame,
    top_n: int = 10,
) -> str:
    """Create a concise Markdown explanation of ranking sensitivity."""
    rank_columns = _profile_rank_columns(sensitivity)
    stable = sensitivity.sort_values(["rank_spread", "avg_rank"]).head(top_n)
    sensitive = sensitivity.sort_values(["rank_spread", "avg_rank"], ascending=[False, True]).head(top_n)

    lines = [
        "# 权重敏感性分析",
        "",
        "本分析比较同一批基金在激进型、平衡型、稳健型三类投资者画像下的排名变化。",
        "`rank_spread` 表示一只基金在不同画像下的最好排名与最差排名之差，数值越小，说明排名对权重假设越不敏感。",
        "",
        "## 排名较稳定的基金",
        "",
        _rank_table(stable, rank_columns),
        "",
        "## 排名变化较大的基金",
        "",
        _rank_table(sensitive, rank_columns),
        "",
        "## 模型解释",
        "",
        "权重并不是客观唯一的参数，而是投资者风险偏好的表达。"
        "因此我没有只给出一组排名，而是设计了多种风险偏好画像，并比较排名变化。"
        "如果某只基金在不同画像下都排名靠前，说明它的综合表现相对稳健；"
        "如果排名波动很大，说明它可能依赖某类特定指标，例如高收益或低回撤。",
    ]
    return "\n".join(lines)


def save_sensitivity_outputs(
    sensitivity: pd.DataFrame,
    csv_path: str | Path,
    markdown_path: str | Path,
    top_n: int = 10,
) -> tuple[Path, Path]:
    csv_path = Path(csv_path)
    markdown_path = Path(markdown_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    sensitivity.to_csv(csv_path)
    markdown_path.write_text(build_sensitivity_markdown(sensitivity, top_n), encoding="utf-8")
    return csv_path, markdown_path


def _rank_table(frame: pd.DataFrame, rank_columns: list[str]) -> str:
    headers = ["基金", *[column.replace("_rank", "") for column in rank_columns], "rank_spread"]
    rows = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]

    for fund, row in frame.iterrows():
        values = [display_fund(str(fund), row)]
        values.extend(str(int(row[column])) for column in rank_columns)
        values.append(str(int(row["rank_spread"])))
        rows.append("| " + " | ".join(values) + " |")

    return "\n".join(rows)


def _profile_rank_columns(frame: pd.DataFrame) -> list[str]:
    return [
        column
        for column in frame.columns
        if column.endswith("_rank") and column not in {"best_rank", "worst_rank", "avg_rank"}
    ]
