from __future__ import annotations

import numpy as np
import pandas as pd

from .data import TRADING_DAYS_PER_YEAR


def daily_returns(nav: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily percentage returns from NAV data."""
    return nav.sort_index().pct_change().replace([np.inf, -np.inf], np.nan)


def max_drawdown(nav: pd.DataFrame | pd.Series) -> pd.Series | float:
    """Calculate maximum drawdown for each fund."""
    is_series = isinstance(nav, pd.Series)
    frame = nav.to_frame() if is_series else nav
    running_max = frame.cummax()
    drawdown = frame / running_max - 1
    result = drawdown.min()
    return float(result.iloc[0]) if is_series else result


def calculate_metrics(
    nav: pd.DataFrame,
    risk_free_rate: float = 0.02,
    rolling_window: int = 60,
) -> pd.DataFrame:
    """Calculate core risk-return indicators for every fund."""
    returns = daily_returns(nav)
    rows: list[dict[str, float | int | str]] = []

    for fund in nav.columns:
        series = nav[fund].dropna()
        fund_returns = returns[fund].dropna()
        observations = len(fund_returns)

        if observations < 2:
            continue

        total_return = series.iloc[-1] / series.iloc[0] - 1
        annual_return = (1 + total_return) ** (TRADING_DAYS_PER_YEAR / observations) - 1
        annual_volatility = fund_returns.std(ddof=1) * np.sqrt(TRADING_DAYS_PER_YEAR)

        running_max = series.cummax()
        drawdown = series / running_max - 1
        fund_max_drawdown = float(drawdown.min())

        sharpe = np.nan
        if annual_volatility and annual_volatility > 0:
            sharpe = (annual_return - risk_free_rate) / annual_volatility

        calmar = np.nan
        if fund_max_drawdown < 0:
            calmar = annual_return / abs(fund_max_drawdown)

        rolling_return = series / series.shift(rolling_window) - 1
        rolling_valid = rolling_return.dropna()
        rolling_positive_ratio = (
            float((rolling_valid > 0).mean()) if not rolling_valid.empty else np.nan
        )

        rows.append(
            {
                "fund": fund,
                "observations": observations,
                "cumulative_return": total_return,
                "annual_return": annual_return,
                "annual_volatility": annual_volatility,
                "max_drawdown": fund_max_drawdown,
                "sharpe": sharpe,
                "calmar": calmar,
                "rolling_positive_ratio": rolling_positive_ratio,
            }
        )

    if not rows:
        raise ValueError("Not enough observations to calculate fund metrics.")

    metrics = pd.DataFrame(rows).set_index("fund")
    return metrics.sort_values("annual_return", ascending=False)


def drawdown_series(nav: pd.DataFrame, funds: list[str]) -> pd.DataFrame:
    """Return drawdown time series for selected funds."""
    selected = nav[funds].dropna(how="all")
    running_max = selected.cummax()
    return selected / running_max - 1

