"""
Policy microsimulation for sustainable consumption.

Economist-oriented example comparing information, default, subsidy,
and combined behavioral-policy regimes using synthetic microdata.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "synthetic" / "synthetic_households.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_MODELS = ROOT / "outputs" / "models"


SCENARIOS = {
    "information_only": {"subsidy": 0.00, "default_green": 0, "norm_signal": 0.50, "friction": 0.18},
    "green_default": {"subsidy": 0.00, "default_green": 1, "norm_signal": 0.65, "friction": 0.08},
    "subsidy": {"subsidy": 0.05, "default_green": 0, "norm_signal": 0.50, "friction": 0.15},
    "subsidy_plus_default": {"subsidy": 0.05, "default_green": 1, "norm_signal": 0.70, "friction": 0.08},
    "regulation_plus_support": {"subsidy": 0.04, "default_green": 1, "norm_signal": 0.75, "friction": 0.05},
}


def evaluate_policy(df: pd.DataFrame, subsidy: float, default_green: int, norm_signal: float, friction: float) -> pd.DataFrame:
    out = df.copy()

    effective_premium = max(0.10 - subsidy, 0.0)
    affordability_pressure = 1 / np.log(out["income"].to_numpy())

    immediate_cost = (
        effective_premium * affordability_pressure * 100
        + friction * out["friction_sensitivity"].to_numpy()
    )

    future_private_benefit = 0.50 * out["environmental_concern"].to_numpy()
    norm_benefit = 0.70 * out["norm_sensitivity"].to_numpy() * norm_signal
    default_bonus = 0.60 * default_green
    infrastructure_bonus = 0.45 * out["infrastructure_access"].to_numpy()
    quality_penalty = 0.60 * out["quality_uncertainty"].to_numpy()

    discounted_future_value = (1 - out["present_bias"].to_numpy() * 0.5) * future_private_benefit
    perceived_loss = out["loss_aversion"].to_numpy() * immediate_cost

    conventional_utility = np.full(len(out), 1.0)
    sustainable_utility = (
        1.0
        + discounted_future_value
        + norm_benefit
        + default_bonus
        + infrastructure_bonus
        - perceived_loss
        - quality_penalty
    )

    out["sustainable_utility"] = sustainable_utility
    out["conventional_utility"] = conventional_utility
    out["adopted"] = (sustainable_utility > conventional_utility).astype(int)
    out["adoption_probability_proxy"] = 1 / (1 + np.exp(-(sustainable_utility - conventional_utility)))

    out["private_welfare"] = np.where(out["adopted"] == 1, sustainable_utility, conventional_utility)
    out["external_benefit"] = 0.90 * out["adopted"]
    out["fiscal_cost"] = subsidy * out["adopted"]
    out["total_welfare"] = out["private_welfare"] + out["external_benefit"] - out["fiscal_cost"]

    return out


def summarize_policy(df: pd.DataFrame, scenario: str) -> dict[str, float | str]:
    return {
        "scenario": scenario,
        "adoption_rate": df["adopted"].mean(),
        "mean_private_welfare": df["private_welfare"].mean(),
        "mean_external_benefit": df["external_benefit"].mean(),
        "mean_fiscal_cost": df["fiscal_cost"].mean(),
        "mean_total_welfare": df["total_welfare"].mean(),
    }


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    OUT_MODELS.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run python/src/generate_synthetic_microdata.py first."
        )

    households = pd.read_csv(DATA_PATH)
    rows = []
    distributional_rows = []

    for scenario, params in SCENARIOS.items():
        evaluated = evaluate_policy(households, **params)
        rows.append(summarize_policy(evaluated, scenario))

        for q, group_df in evaluated.groupby("income_quintile"):
            summary = summarize_policy(group_df, scenario)
            summary["income_quintile"] = q
            distributional_rows.append(summary)

        evaluated.to_csv(OUT_MODELS / f"{scenario}_micro_outcomes.csv", index=False)

    summary_df = pd.DataFrame(rows).sort_values("mean_total_welfare", ascending=False)
    distributional_df = pd.DataFrame(distributional_rows).sort_values(["scenario", "income_quintile"])

    summary_df.to_csv(OUT_TABLES / "policy_microsimulation_summary.csv", index=False)
    distributional_df.to_csv(OUT_TABLES / "distributional_policy_summary.csv", index=False)

    print(summary_df)
    print(distributional_df.head(15))


if __name__ == "__main__":
    main()
