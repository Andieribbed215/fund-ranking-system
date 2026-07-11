from __future__ import annotations

import pandas as pd

DEFAULT_PROFILES: dict[str, dict[str, float]] = {
    "aggressive": {
        "annual_return": 0.35,
        "sharpe": 0.20,
        "max_drawdown": 0.10,
        "calmar": 0.05,
        "annual_volatility": 0.10,
        "rolling_positive_ratio": 0.20,
    },
    "balanced": {
        "annual_return": 0.20,
        "sharpe": 0.25,
        "max_drawdown": 0.20,
        "calmar": 0.10,
        "annual_volatility": 0.10,
        "rolling_positive_ratio": 0.15,
    },
    "conservative": {
        "annual_return": 0.10,
        "sharpe": 0.25,
        "max_drawdown": 0.30,
        "calmar": 0.05,
        "annual_volatility": 0.15,
        "rolling_positive_ratio": 0.15,
    },
}

LOWER_IS_BETTER = {"annual_volatility"}


def percentile_scores(
    metrics: pd.DataFrame,
    weights: dict[str, float],
) -> pd.DataFrame:
    """Convert raw metrics to 0-100 percentile scores."""
    missing = [metric for metric in weights if metric not in metrics.columns]
    if missing:
        raise ValueError(f"Missing metrics for scoring: {missing}")

    scores = pd.DataFrame(index=metrics.index)
    for metric in weights:
        values = metrics[metric].copy()
        if metric in LOWER_IS_BETTER:
            values = -values

        if values.nunique(dropna=True) <= 1:
            percentile = pd.Series(50.0, index=metrics.index)
        else:
            percentile = values.rank(pct=True, method="average") * 100

        scores[f"{metric}_score"] = percentile.fillna(50.0)

    return scores


def score_funds(metrics: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    """Score funds with a weighted percentile model."""
    weight_sum = sum(weights.values())
    if weight_sum <= 0:
        raise ValueError("Weight sum must be positive.")

    normalized_weights = {key: value / weight_sum for key, value in weights.items()}
    factor_scores = percentile_scores(metrics, normalized_weights)

    composite = pd.Series(0.0, index=metrics.index)
    for metric, weight in normalized_weights.items():
        composite += factor_scores[f"{metric}_score"] * weight

    scored = metrics.join(factor_scores)
    scored["composite_score"] = composite
    scored["rank"] = scored["composite_score"].rank(ascending=False, method="min").astype(int)
    return scored.sort_values(["composite_score", "annual_return"], ascending=False)


def score_all_profiles(
    metrics: pd.DataFrame,
    profiles: dict[str, dict[str, float]] | None = None,
) -> pd.DataFrame:
    """Create one comparison table for all built-in investor profiles."""
    profiles = profiles or DEFAULT_PROFILES
    comparison = metrics.copy()

    for profile_name, weights in profiles.items():
        scored = score_funds(metrics, weights)
        comparison[f"{profile_name}_score"] = scored["composite_score"]
        comparison[f"{profile_name}_rank"] = scored["rank"]

    return comparison
