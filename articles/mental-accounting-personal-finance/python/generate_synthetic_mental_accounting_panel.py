from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(15150)

n_households = 3000

base = pd.DataFrame({
    "household_id": np.arange(1, n_households + 1),
    "monthly_income": rng.uniform(2500, 6500, n_households),
    "liquid_savings": rng.uniform(500, 12000, n_households),
    "emergency_reserve": rng.uniform(0, 8000, n_households),
    "credit_card_debt": rng.uniform(0, 9000, n_households),
    "windfall": rng.uniform(0, 3500, n_households),
    "savings_label_strength": rng.uniform(0.2, 1.3, n_households),
    "emergency_need_risk": rng.uniform(0.02, 0.25, n_households),
    "present_bias": rng.uniform(0.55, 1.00, n_households),
})

def simulate_regime(df: pd.DataFrame, regime: str) -> pd.DataFrame:
    out = df.copy()
    out["regime"] = regime

    if regime == "segmented_mental_accounts":
        windfall_spent_share = np.clip(rng.normal(0.58, 0.18, len(out)), 0, 1)
        label_penalty = out["savings_label_strength"].to_numpy()
        integrated_prompt = 0.0
        savings_reallocation_base = 0.32

    elif regime == "integrated_balance_sheet_prompt":
        windfall_spent_share = np.clip(rng.normal(0.42, 0.16, len(out)), 0, 1)
        label_penalty = out["savings_label_strength"].to_numpy() * 0.65
        integrated_prompt = 1.0
        savings_reallocation_base = 0.46

    elif regime == "unified_fungible_money":
        windfall_spent_share = np.clip(rng.normal(0.25, 0.12, len(out)), 0, 1)
        label_penalty = out["savings_label_strength"].to_numpy() * 0.30
        integrated_prompt = 1.0
        savings_reallocation_base = 0.62

    else:
        raise ValueError(f"Unknown regime: {regime}")

    out["windfall_consumption"] = out["windfall"] * windfall_spent_share
    out["windfall_debt_payment"] = out["windfall"] * (1 - windfall_spent_share) * 0.75

    protected_liquidity = 3 * out["monthly_income"].to_numpy() * out["emergency_need_risk"].to_numpy()

    out["savings_available_for_debt"] = np.maximum(
        out["liquid_savings"].to_numpy() - protected_liquidity,
        0,
    )

    savings_use_rate = np.maximum(
        0,
        savings_reallocation_base - 0.22 * label_penalty + 0.05 * integrated_prompt,
    )

    out["savings_used_for_debt"] = np.where(
        out["credit_card_debt"].to_numpy() > 0,
        out["savings_available_for_debt"].to_numpy() * savings_use_rate,
        0,
    )

    out["total_debt_payment"] = np.minimum(
        out["credit_card_debt"].to_numpy(),
        out["windfall_debt_payment"].to_numpy() + out["savings_used_for_debt"].to_numpy(),
    )

    out["remaining_debt"] = np.maximum(
        out["credit_card_debt"].to_numpy() - out["total_debt_payment"].to_numpy(),
        0,
    )

    out["remaining_liquid_savings"] = np.maximum(
        out["liquid_savings"].to_numpy() - out["savings_used_for_debt"].to_numpy(),
        0,
    )

    out["inefficiency_gap"] = np.where(
        out["remaining_debt"].to_numpy() > 0,
        np.minimum(out["remaining_liquid_savings"].to_numpy(), out["remaining_debt"].to_numpy()),
        0,
    )

    out["annual_interest_cost"] = out["remaining_debt"] * 0.22

    out["resilience_index"] = (
        out["remaining_liquid_savings"]
        + out["emergency_reserve"]
        - out["remaining_debt"]
        - out["annual_interest_cost"]
    )

    out["integrated_prompt_treat"] = int(regime == "integrated_balance_sheet_prompt")
    out["unified_money_treat"] = int(regime == "unified_fungible_money")

    return out

panel = pd.concat([
    simulate_regime(base, "segmented_mental_accounts"),
    simulate_regime(base, "integrated_balance_sheet_prompt"),
    simulate_regime(base, "unified_fungible_money"),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    households=("household_id", "count"),
    mean_windfall_consumption=("windfall_consumption", "mean"),
    mean_total_debt_payment=("total_debt_payment", "mean"),
    mean_remaining_debt=("remaining_debt", "mean"),
    mean_remaining_liquid_savings=("remaining_liquid_savings", "mean"),
    mean_inefficiency_gap=("inefficiency_gap", "mean"),
    mean_annual_interest_cost=("annual_interest_cost", "mean"),
    mean_resilience_index=("resilience_index", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_mental_accounting_household_panel.csv", index=False)
summary.to_csv(TABLES / "mental_accounting_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_mental_accounting_household_panel.csv", index=False)
summary.to_csv(PROCESSED / "mental_accounting_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} household-regime rows.")
print(summary)
