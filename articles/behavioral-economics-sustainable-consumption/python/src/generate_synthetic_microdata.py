"""
Generate synthetic household microdata for behavioral economics and sustainable consumption.

This script creates a panel-style synthetic dataset suitable for adoption modeling,
policy microsimulation, difference-in-differences scaffolding, and event-study examples.
The data are synthetic and designed for research workflow demonstration.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
OUT_SYNTH = DATA_DIR / "synthetic"
OUT_PROCESSED = DATA_DIR / "processed"


def generate_households(n: int = 12000, seed: int = 20260525) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    income = rng.lognormal(mean=np.log(65000), sigma=0.55, size=n)
    urban = rng.binomial(1, 0.72, size=n)
    renter = rng.binomial(1, np.where(income < np.median(income), 0.55, 0.28), size=n)

    households = pd.DataFrame(
        {
            "household_id": np.arange(1, n + 1),
            "income": income,
            "urban": urban,
            "renter": renter,
            "baseline_consumption_intensity": rng.gamma(shape=4.0, scale=0.7, size=n),
            "environmental_concern": np.clip(rng.normal(0.58, 0.19, n), 0, 1),
            "present_bias": np.clip(rng.beta(2.2, 5.0, n), 0.03, 0.98),
            "loss_aversion": np.clip(rng.normal(2.05, 0.45, n), 1.05, 4.25),
            "norm_sensitivity": np.clip(rng.normal(0.50, 0.21, n), 0, 1),
            "friction_sensitivity": np.clip(rng.normal(0.56, 0.20, n), 0, 1),
            "quality_uncertainty": np.clip(rng.normal(0.31, 0.16, n), 0, 1),
            "infrastructure_access": np.clip(
                0.25 + 0.35 * urban + rng.normal(0.15, 0.17, n), 0, 1
            ),
        }
    )

    households["income_quintile"] = pd.qcut(
        households["income"], q=5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"]
    )

    return households


def generate_panel(households: pd.DataFrame, periods: int = 8, seed: int = 20260526) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    panel = households.loc[households.index.repeat(periods)].copy()
    panel["period"] = np.tile(np.arange(1, periods + 1), len(households))

    # Staggered synthetic rollout: some localities receive a green-default policy after period 4 or 5.
    locality = rng.integers(1, 101, size=len(households))
    adoption_period_by_locality = {
        loc: rng.choice([0, 5, 6], p=[0.42, 0.30, 0.28]) for loc in np.unique(locality)
    }

    panel["locality_id"] = np.repeat(locality, periods)
    panel["policy_start_period"] = panel["locality_id"].map(adoption_period_by_locality)
    panel["treated_locality"] = (panel["policy_start_period"] > 0).astype(int)
    panel["post_policy"] = (
        (panel["policy_start_period"] > 0) & (panel["period"] >= panel["policy_start_period"])
    ).astype(int)

    panel["default_green"] = panel["post_policy"]
    panel["subsidy"] = np.where(panel["post_policy"] == 1, 0.04, 0.00)
    panel["norm_signal"] = np.clip(
        0.42
        + 0.08 * panel["period"]
        + 0.13 * panel["post_policy"]
        + rng.normal(0, 0.06, len(panel)),
        0,
        1,
    )
    panel["friction"] = np.clip(
        0.22 - 0.11 * panel["post_policy"] - 0.08 * panel["infrastructure_access"],
        0.02,
        0.35,
    )

    return panel


def adoption_probability(df: pd.DataFrame) -> np.ndarray:
    affordability = 1 / np.log(df["income"].to_numpy())
    effective_price_premium = np.maximum(0.10 - df["subsidy"].to_numpy(), 0)

    utility_diff = (
        -0.65
        + 1.10 * df["environmental_concern"].to_numpy()
        + 0.72 * df["default_green"].to_numpy()
        + 0.85 * df["norm_sensitivity"].to_numpy() * df["norm_signal"].to_numpy()
        + 0.55 * df["infrastructure_access"].to_numpy()
        - 1.75 * effective_price_premium * affordability * 100
        - 1.25 * df["friction"].to_numpy() * df["friction_sensitivity"].to_numpy()
        - 0.38 * df["present_bias"].to_numpy()
        - 0.35 * df["loss_aversion"].to_numpy() * effective_price_premium
        - 0.62 * df["quality_uncertainty"].to_numpy()
        - 0.12 * df["renter"].to_numpy()
    )

    return 1 / (1 + np.exp(-utility_diff))


def assign_outcomes(panel: pd.DataFrame, seed: int = 20260527) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = panel.copy()

    df["adoption_probability"] = adoption_probability(df)
    df["adopted"] = rng.binomial(1, df["adoption_probability"])

    df["private_welfare"] = (
        1.0
        + 0.35 * df["adopted"]
        + 0.18 * df["environmental_concern"] * df["adopted"]
        - 0.10 * df["friction"] * df["friction_sensitivity"]
        - 0.05 * df["quality_uncertainty"]
    )
    df["external_benefit"] = 0.90 * df["adopted"]
    df["fiscal_cost"] = df["subsidy"] * df["adopted"]
    df["total_welfare"] = df["private_welfare"] + df["external_benefit"] - df["fiscal_cost"]

    return df


def main() -> None:
    OUT_SYNTH.mkdir(parents=True, exist_ok=True)
    OUT_PROCESSED.mkdir(parents=True, exist_ok=True)

    households = generate_households()
    panel = generate_panel(households)
    panel = assign_outcomes(panel)

    households.to_csv(OUT_SYNTH / "synthetic_households.csv", index=False)
    panel.to_csv(OUT_PROCESSED / "synthetic_sustainable_consumption_panel.csv", index=False)

    print("Wrote:")
    print(OUT_SYNTH / "synthetic_households.csv")
    print(OUT_PROCESSED / "synthetic_sustainable_consumption_panel.csv")
    print(panel.head())


if __name__ == "__main__":
    main()
