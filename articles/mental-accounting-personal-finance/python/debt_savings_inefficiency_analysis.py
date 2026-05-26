from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_mental_accounting_household_panel.csv")

summary = df.groupby("regime").agg(
    households=("household_id", "count"),
    mean_windfall_consumption=("windfall_consumption", "mean"),
    mean_windfall_debt_payment=("windfall_debt_payment", "mean"),
    mean_savings_used_for_debt=("savings_used_for_debt", "mean"),
    mean_total_debt_payment=("total_debt_payment", "mean"),
    mean_remaining_debt=("remaining_debt", "mean"),
    mean_remaining_liquid_savings=("remaining_liquid_savings", "mean"),
    mean_inefficiency_gap=("inefficiency_gap", "mean"),
    mean_annual_interest_cost=("annual_interest_cost", "mean"),
    mean_resilience_index=("resilience_index", "mean"),
).reset_index()

summary["debt_reduction_liquidity_tradeoff"] = (
    summary["mean_total_debt_payment"] - 0.25 * summary["mean_remaining_liquid_savings"]
)

summary.to_csv(TABLES / "mental_accounting_debt_savings_summary.csv", index=False)

rows = []
for debt_rate in [0.15, 0.22, 0.29]:
    for liquidity_weight in [0.75, 1.00, 1.25]:
        for label_weight in [0.75, 1.00, 1.25]:
            alt_interest_cost = df["remaining_debt"] * debt_rate
            alt_resilience = (
                liquidity_weight * df["remaining_liquid_savings"]
                + df["emergency_reserve"]
                - df["remaining_debt"]
                - alt_interest_cost
                - label_weight * df["savings_label_strength"] * 50
            )
            tmp = df.assign(
                alt_interest_cost=alt_interest_cost,
                alt_resilience=alt_resilience,
            )
            for regime, sub in tmp.groupby("regime"):
                rows.append({
                    "debt_interest_rate": debt_rate,
                    "liquidity_weight": liquidity_weight,
                    "label_weight": label_weight,
                    "regime": regime,
                    "mean_alt_interest_cost": sub["alt_interest_cost"].mean(),
                    "mean_alt_resilience": sub["alt_resilience"].mean(),
                })

pd.DataFrame(rows).to_csv(DIAG / "mental_accounting_resilience_sensitivity.csv", index=False)

print(summary)
