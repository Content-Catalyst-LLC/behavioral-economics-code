"""Synthetic governance-regime simulation.

This script supports the article:
"The Future of Behavioral Economics in Governance and Policy."

It compares enforcement-heavy, simplification-first, and trust-plus-salience
governance regimes using synthetic citizen-level data.
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

RNG = np.random.default_rng(123)


def build_population(n: int = 12_000) -> pd.DataFrame:
    """Create a synthetic population for behavioral-governance modeling."""
    citizens = pd.DataFrame(
        {
            "trust": np.clip(RNG.normal(0.55, 0.20, n), 0, 1),
            "salience": np.clip(RNG.normal(0.50, 0.18, n), 0, 1),
            "norm_sensitivity": np.clip(RNG.normal(0.45, 0.20, n), 0, 1),
            "burden_sensitivity": np.clip(RNG.normal(0.60, 0.16, n), 0, 1),
            "present_bias": np.clip(RNG.beta(2, 4, n), 0.05, 0.99),
            "income": RNG.lognormal(np.log(50_000), 0.55, n),
            "digital_access": np.clip(RNG.normal(0.72, 0.18, n), 0, 1),
        }
    )
    citizens.insert(0, "citizen_id", np.arange(1, n + 1))
    return citizens


def evaluate_regime(
    df: pd.DataFrame,
    admin_burden: float,
    reminder_salience: float,
    trust_signal: float,
    penalty_strength: float,
) -> dict[str, float]:
    """Evaluate a synthetic governance regime."""
    private_benefit = 0.8 * reminder_salience * df["salience"].to_numpy()
    norm_component = 0.7 * df["norm_sensitivity"].to_numpy()
    trust_component = 1.0 * trust_signal * df["trust"].to_numpy()
    digital_access_bonus = 0.25 * df["digital_access"].to_numpy()
    burden_cost = 1.2 * admin_burden * df["burden_sensitivity"].to_numpy()
    present_bias_cost = 0.7 * df["present_bias"].to_numpy() * admin_burden
    enforcement_component = 0.9 * penalty_strength

    utility_compliance = (
        private_benefit
        + norm_component
        + trust_component
        + digital_access_bonus
        + enforcement_component
        - burden_cost
        - present_bias_cost
    )

    compliance_prob = 1 / (1 + np.exp(-(utility_compliance - 0.5)))
    comply = RNG.binomial(1, compliance_prob)

    social_gain = 1.0 * comply
    admin_cost = 0.4 * admin_burden
    coercion_cost = 0.3 * penalty_strength
    welfare = utility_compliance + social_gain - admin_cost - coercion_cost

    return {
        "compliance_rate": float(comply.mean()),
        "mean_compliance_probability": float(compliance_prob.mean()),
        "mean_welfare": float(welfare.mean()),
    }


def main() -> None:
    citizens = build_population()
    citizens.to_csv(PROCESSED / "synthetic_citizens_generated.csv", index=False)

    regimes = {
        "enforcement_heavy": {
            "admin_burden": 0.35,
            "reminder_salience": 0.30,
            "trust_signal": 0.35,
            "penalty_strength": 0.85,
        },
        "simplification_first": {
            "admin_burden": 0.10,
            "reminder_salience": 0.55,
            "trust_signal": 0.50,
            "penalty_strength": 0.35,
        },
        "trust_plus_salience": {
            "admin_burden": 0.12,
            "reminder_salience": 0.80,
            "trust_signal": 0.80,
            "penalty_strength": 0.30,
        },
    }

    rows: list[dict[str, float | str]] = []
    for name, params in regimes.items():
        outcome = evaluate_regime(citizens, **params)
        outcome["regime"] = name
        rows.append(outcome)

    results = pd.DataFrame(rows)[
        ["regime", "compliance_rate", "mean_compliance_probability", "mean_welfare"]
    ].sort_values("mean_welfare", ascending=False)

    results.to_csv(OUTPUT_TABLES / "regime_summary.csv", index=False)
    print(results.to_string(index=False))

    citizens["income_quintile"] = pd.qcut(
        citizens["income"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"]
    )

    distribution_rows: list[dict[str, float | str]] = []
    for name, params in regimes.items():
        for quintile in citizens["income_quintile"].unique():
            subset = citizens.loc[citizens["income_quintile"] == quintile].copy()
            outcome = evaluate_regime(subset, **params)
            outcome["regime"] = name
            outcome["income_quintile"] = str(quintile)
            distribution_rows.append(outcome)

    distribution = pd.DataFrame(distribution_rows).sort_values(
        ["regime", "income_quintile"]
    )
    distribution.to_csv(OUTPUT_TABLES / "distributional_regime_summary.csv", index=False)


if __name__ == "__main__":
    main()
