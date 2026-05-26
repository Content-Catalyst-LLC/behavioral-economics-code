"""Synthetic organizational decision-making simulation.

This script supports the article:
"Behavioral Economics in Organizational Decision-Making."

It compares metric-heavy short-termism, balanced governance, and
high-accountability adaptive review using synthetic project data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(101)


def build_project_portfolio(n: int = 6000) -> pd.DataFrame:
    """Create a synthetic project portfolio."""
    projects = pd.DataFrame(
        {
            "project_id": np.arange(1, n + 1),
            "expected_payoff": RNG.normal(0.12, 0.10, n),
            "risk": np.clip(RNG.normal(0.25, 0.10, n), 0, 1),
            "sunk_cost": RNG.gamma(shape=3.0, scale=0.12, size=n),
            "prestige_value": np.clip(RNG.normal(0.18, 0.08, n), 0, 1),
            "complexity": np.clip(RNG.normal(0.35, 0.12, n), 0, 1),
            "overconfidence": np.clip(RNG.normal(0.20, 0.10, n), 0, 0.6),
            "long_horizon_value": np.clip(RNG.normal(0.20, 0.12, n), 0, 1),
        }
    )
    return projects


def evaluate_regime(
    df: pd.DataFrame,
    short_term_pressure: float,
    review_strength: float,
    conformity_pressure: float,
    long_horizon_weight: float,
) -> dict[str, float]:
    """Evaluate a synthetic organizational governance regime."""
    perceived_value = (
        df["expected_payoff"].to_numpy()
        + df["prestige_value"].to_numpy() * short_term_pressure
        - df["risk"].to_numpy()
        - df["complexity"].to_numpy()
        + 0.9 * df["sunk_cost"].to_numpy()
        + 0.7 * df["overconfidence"].to_numpy()
        - 0.8 * review_strength * df["sunk_cost"].to_numpy()
        - 0.5 * review_strength * df["overconfidence"].to_numpy()
        + long_horizon_weight * df["long_horizon_value"].to_numpy()
    )

    consensus = perceived_value.mean()
    adjusted_value = (
        (1 - conformity_pressure) * perceived_value
        + conformity_pressure * consensus
    )

    approve_prob = 1 / (1 + np.exp(-adjusted_value))
    approve = RNG.binomial(1, approve_prob)

    realized_welfare = (
        approve
        * (
            df["expected_payoff"].to_numpy()
            - df["risk"].to_numpy()
            - 0.5 * df["complexity"].to_numpy()
            + 0.6 * df["long_horizon_value"].to_numpy()
        )
        - approve * 0.4 * df["sunk_cost"].to_numpy()
    )

    escalation_risk = (
        (df["sunk_cost"].to_numpy() > 0.35)
        & (df["overconfidence"].to_numpy() > 0.25)
        & (approve == 1)
    )

    return {
        "approval_rate": float(approve.mean()),
        "mean_approval_prob": float(approve_prob.mean()),
        "mean_welfare": float(realized_welfare.mean()),
        "escalation_prone_approval_rate": float(escalation_risk.mean()),
    }


def main() -> None:
    projects = build_project_portfolio()
    projects.to_csv(PROCESSED / "synthetic_organizational_projects_generated.csv", index=False)

    regimes = {
        "metric_heavy_short_termism": {
            "short_term_pressure": 1.3,
            "review_strength": 0.15,
            "conformity_pressure": 0.65,
            "long_horizon_weight": 0.10,
        },
        "balanced_governance": {
            "short_term_pressure": 0.9,
            "review_strength": 0.55,
            "conformity_pressure": 0.35,
            "long_horizon_weight": 0.35,
        },
        "high_accountability_adaptive_review": {
            "short_term_pressure": 0.7,
            "review_strength": 0.85,
            "conformity_pressure": 0.20,
            "long_horizon_weight": 0.60,
        },
    }

    rows: list[dict[str, float | str]] = []

    for name, params in regimes.items():
        result = evaluate_regime(projects, **params)
        result["regime"] = name
        rows.append(result)

    results = pd.DataFrame(rows)[
        [
            "regime",
            "approval_rate",
            "mean_approval_prob",
            "mean_welfare",
            "escalation_prone_approval_rate",
        ]
    ].sort_values("mean_welfare", ascending=False)

    print(results.to_string(index=False))
    results.to_csv(OUTPUT_TABLES / "organizational_regime_summary.csv", index=False)

    projects["risk_quintile"] = pd.qcut(
        projects["risk"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"]
    )

    distribution_rows: list[dict[str, float | str]] = []

    for name, params in regimes.items():
        for quintile in projects["risk_quintile"].unique():
            subset = projects.loc[projects["risk_quintile"] == quintile].copy()
            result = evaluate_regime(subset, **params)
            result["regime"] = name
            result["risk_quintile"] = str(quintile)
            distribution_rows.append(result)

    distribution = pd.DataFrame(distribution_rows).sort_values(
        ["regime", "risk_quintile"]
    )
    distribution.to_csv(
        OUTPUT_TABLES / "organizational_regime_risk_distribution.csv", index=False
    )


if __name__ == "__main__":
    main()
