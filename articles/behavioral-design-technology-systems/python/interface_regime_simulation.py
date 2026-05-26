"""Synthetic behavioral-design interface simulation.

This script supports the article:
"Behavioral Design in Technology Systems."

It compares user-supportive, engagement-maximizing, and friction-heavy
lock-in interface regimes using synthetic user-level data.
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

RNG = np.random.default_rng(202)


def build_users(n: int = 9000) -> pd.DataFrame:
    """Create a synthetic user population."""
    users = pd.DataFrame(
        {
            "user_id": np.arange(1, n + 1),
            "baseline_value": RNG.normal(0.45, 0.18, n),
            "salience_sensitivity": np.clip(RNG.normal(0.55, 0.18, n), 0, 1),
            "default_sensitivity": np.clip(RNG.normal(0.50, 0.20, n), 0, 1),
            "friction_sensitivity": np.clip(RNG.normal(0.60, 0.16, n), 0, 1),
            "reward_sensitivity": np.clip(RNG.normal(0.58, 0.17, n), 0, 1),
            "cognitive_overload": np.clip(RNG.normal(0.42, 0.15, n), 0, 1),
            "privacy_sensitivity": np.clip(RNG.normal(0.55, 0.20, n), 0, 1),
            "autonomy_preference": np.clip(RNG.normal(0.58, 0.18, n), 0, 1),
        }
    )
    return users


def evaluate_interface(
    df: pd.DataFrame,
    salience: float,
    default_on: int,
    entry_friction: float,
    exit_friction: float,
    reward_intensity: float,
    data_extraction_intensity: float,
) -> dict[str, float]:
    """Evaluate a synthetic interface regime."""
    join_score = (
        df["baseline_value"].to_numpy()
        + df["salience_sensitivity"].to_numpy() * salience
        + df["default_sensitivity"].to_numpy() * default_on
        - df["friction_sensitivity"].to_numpy() * entry_friction
        + df["reward_sensitivity"].to_numpy() * reward_intensity
        - df["cognitive_overload"].to_numpy() * 0.4
    )

    join_prob = 1 / (1 + np.exp(-join_score))
    joined = RNG.binomial(1, join_prob)

    stay_score = (
        df["baseline_value"].to_numpy() * 0.5
        + df["reward_sensitivity"].to_numpy() * reward_intensity
        + df["default_sensitivity"].to_numpy() * default_on
        + df["friction_sensitivity"].to_numpy() * exit_friction
        - df["cognitive_overload"].to_numpy() * 0.35
    )

    retain_prob = 1 / (1 + np.exp(-stay_score))
    retained = np.where(joined == 1, RNG.binomial(1, retain_prob), 0)

    friction_asymmetry = exit_friction - entry_friction

    autonomy_cost = (
        0.7
        * np.maximum(friction_asymmetry, 0)
        * df["autonomy_preference"].to_numpy()
    )

    privacy_cost = (
        data_extraction_intensity
        * df["privacy_sensitivity"].to_numpy()
        * joined
    )

    welfare = (
        joined * (df["baseline_value"].to_numpy() + 0.4 * reward_intensity)
        - 0.8 * np.maximum(friction_asymmetry, 0)
        - 0.5 * df["cognitive_overload"].to_numpy()
        - autonomy_cost
        - privacy_cost
    )

    platform_value = (
        1.2 * joined
        + 1.6 * retained
        + 1.0 * data_extraction_intensity * joined
    )

    return {
        "join_rate": float(joined.mean()),
        "retention_rate": float(retained.mean()),
        "mean_user_welfare": float(welfare.mean()),
        "mean_platform_value": float(platform_value.mean()),
        "friction_asymmetry": float(friction_asymmetry),
        "welfare_platform_gap": float(platform_value.mean() - welfare.mean()),
    }


def main() -> None:
    users = build_users()
    users.to_csv(PROCESSED / "synthetic_users_generated.csv", index=False)

    regimes = {
        "user_supportive_design": {
            "salience": 0.55,
            "default_on": 0,
            "entry_friction": 0.08,
            "exit_friction": 0.08,
            "reward_intensity": 0.35,
            "data_extraction_intensity": 0.10,
        },
        "engagement_maximizing_design": {
            "salience": 0.85,
            "default_on": 1,
            "entry_friction": 0.03,
            "exit_friction": 0.22,
            "reward_intensity": 0.80,
            "data_extraction_intensity": 0.45,
        },
        "friction_heavy_lock_in": {
            "salience": 0.75,
            "default_on": 1,
            "entry_friction": 0.02,
            "exit_friction": 0.60,
            "reward_intensity": 0.55,
            "data_extraction_intensity": 0.60,
        },
    }

    rows: list[dict[str, float | str]] = []

    for name, params in regimes.items():
        out = evaluate_interface(users, **params)
        out["regime"] = name
        rows.append(out)

    results = pd.DataFrame(rows)[
        [
            "regime",
            "join_rate",
            "retention_rate",
            "mean_user_welfare",
            "mean_platform_value",
            "friction_asymmetry",
            "welfare_platform_gap",
        ]
    ].sort_values("mean_user_welfare", ascending=False)

    print(results.to_string(index=False))
    results.to_csv(OUTPUT_TABLES / "interface_regime_comparison.csv", index=False)

    users["overload_group"] = pd.qcut(
        users["cognitive_overload"],
        4,
        labels=["low", "medium", "high", "very_high"],
    )

    dist_rows: list[dict[str, float | str]] = []

    for name, params in regimes.items():
        for group in users["overload_group"].unique():
            subset = users.loc[users["overload_group"] == group].copy()
            out = evaluate_interface(subset, **params)
            out["regime"] = name
            out["overload_group"] = str(group)
            dist_rows.append(out)

    distribution = pd.DataFrame(dist_rows).sort_values(["regime", "overload_group"])
    distribution.to_csv(
        OUTPUT_TABLES / "interface_regime_overload_distribution.csv", index=False
    )


if __name__ == "__main__":
    main()
