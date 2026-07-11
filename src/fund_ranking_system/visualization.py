from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from .metrics import drawdown_series


def _finish_plot(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def plot_top_scores(scored: pd.DataFrame, path: str | Path, top_n: int = 10) -> Path:
    top = scored.head(top_n).sort_values("composite_score")
    plt.figure(figsize=(10, 6))
    plt.barh(top.index, top["composite_score"], color="#2f6f9f")
    plt.xlabel("Composite Score")
    plt.title(f"Top {top_n} Funds by Multi-factor Score")
    return _finish_plot(path)


def plot_risk_return(scored: pd.DataFrame, path: str | Path, top_n: int = 10) -> Path:
    plt.figure(figsize=(9, 6))
    scatter = plt.scatter(
        scored["annual_volatility"],
        scored["annual_return"],
        c=scored["composite_score"],
        cmap="viridis",
        s=60,
        alpha=0.82,
    )
    plt.colorbar(scatter, label="Composite Score")
    plt.xlabel("Annualized Volatility")
    plt.ylabel("Annualized Return")
    plt.title("Risk-return Distribution")

    for fund, row in scored.head(top_n).iterrows():
        plt.annotate(
            fund.replace("Fund_", "F"),
            (row["annual_volatility"], row["annual_return"]),
            fontsize=8,
            xytext=(4, 4),
            textcoords="offset points",
        )

    return _finish_plot(path)


def plot_nav(nav: pd.DataFrame, funds: list[str], path: str | Path) -> Path:
    plt.figure(figsize=(10, 6))
    normalized = nav[funds] / nav[funds].iloc[0]
    for fund in funds:
        plt.plot(normalized.index, normalized[fund], label=fund)
    plt.ylabel("Normalized NAV")
    plt.title("Top Fund NAV Trend")
    plt.legend(fontsize=8)
    return _finish_plot(path)


def plot_drawdown(nav: pd.DataFrame, funds: list[str], path: str | Path) -> Path:
    plt.figure(figsize=(10, 6))
    drawdowns = drawdown_series(nav, funds)
    for fund in funds:
        plt.plot(drawdowns.index, drawdowns[fund], label=fund)
    plt.ylabel("Drawdown")
    plt.title("Top Fund Drawdown Trend")
    plt.legend(fontsize=8)
    return _finish_plot(path)

