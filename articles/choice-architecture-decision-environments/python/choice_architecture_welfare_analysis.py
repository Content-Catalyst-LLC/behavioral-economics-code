"""Welfare, concentration, and distributional analysis for choice architecture."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAGNOSTICS = ROOT / "outputs" / "model_diagnostics"

DIAGNOSTICS.mkdir(parents=True, exist_ok=True)

data_path = TABLES / "synthetic_choice_architecture_experiment.csv"
if not data_path.exists():
    raise FileNotFoundError(
        "Synthetic experiment data not found. Run python/generate_synthetic_choice_architecture_panel.py first."
    )

df = pd.read_csv(data_path)

summary = df.groupby("regime").agg(
    users=("user_id", "count"),
    mean_realized_welfare=("realized_welfare", "mean"),
    mean_chosen_utility=("chosen_utility", "mean"),
    default_selection_rate=("selected_default", "mean"),
    high_value_selection_rate=("selected_high_value_option", "mean"),
    mean_cognitive_cost=("cognitive_cost", "mean"),
    mean_switching_cost=("switching_cost", "mean"),
).reset_index()

summary["utility_welfare_gap"] = summary["mean_chosen_utility"] - summary["mean_realized_welfare"]

# Choice concentration by regime.
shares = (
    df.groupby(["regime", "chosen_option"])
    .size()
    .reset_index(name="count")
)
shares["share"] = shares.groupby("regime")["count"].transform(lambda x: x / x.sum())

hhi = shares.groupby("regime").apply(
    lambda x: (x["share"] ** 2).sum(),
    include_groups=False,
).reset_index(name="choice_hhi")

summary = summary.merge(hhi, on="regime", how="left")
summary.to_csv(TABLES / "choice_architecture_welfare_summary.csv", index=False)
shares.to_csv(TABLES / "choice_architecture_option_shares.csv", index=False)

df["complexity_quartile"] = pd.qcut(df["complexity_sensitivity"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

distribution = df.groupby(["regime", "complexity_quartile"], observed=False).agg(
    users=("user_id", "count"),
    mean_realized_welfare=("realized_welfare", "mean"),
    mean_chosen_utility=("chosen_utility", "mean"),
    mean_cognitive_cost=("cognitive_cost", "mean"),
    mean_switching_cost=("switching_cost", "mean"),
).reset_index()

distribution.to_csv(TABLES / "choice_architecture_distributional_summary.csv", index=False)

# Sensitivity to alternative cognitive and switching-cost assumptions.
sensitivity_rows = []
for cognitive_weight in [0.50, 1.00, 1.50]:
    for switching_weight in [0.50, 1.00, 1.50]:
        alt_welfare = (
            df["realized_welfare"]
            - (cognitive_weight - 1.0) * df["cognitive_cost"]
            - (switching_weight - 1.0) * df["switching_cost"]
        )

        tmp = df.assign(alt_realized_welfare=alt_welfare)
        for regime, sub in tmp.groupby("regime"):
            sensitivity_rows.append({
                "cognitive_cost_weight": cognitive_weight,
                "switching_cost_weight": switching_weight,
                "regime": regime,
                "mean_alt_realized_welfare": sub["alt_realized_welfare"].mean(),
            })

pd.DataFrame(sensitivity_rows).to_csv(
    DIAGNOSTICS / "choice_architecture_welfare_sensitivity.csv", index=False
)

print("Wrote choice architecture welfare summary, distributional summary, and sensitivity diagnostics.")
print(summary)
