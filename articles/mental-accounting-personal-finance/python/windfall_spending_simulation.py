from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(15151)

n_households = 2500
n_events = 24

households = pd.DataFrame({
    "household_id": np.arange(1, n_households + 1),
    "monthly_income": rng.uniform(2500, 6500, n_households),
    "debt_burden": rng.uniform(0, 9000, n_households),
    "liquidity_buffer": rng.uniform(500, 10000, n_households),
    "present_bias": rng.uniform(0.55, 1.0, n_households),
    "label_strength": rng.uniform(0.2, 1.3, n_households),
})

rows = []
for event_id in range(1, n_events + 1):
    windfall_amount = rng.uniform(100, 3500, n_households)
    prompt_type = rng.choice(["no_prompt", "savings_label", "debt_prompt", "split_prompt"], n_households)

    spend_share = (
        0.60
        - 0.12 * (prompt_type == "debt_prompt")
        - 0.18 * (prompt_type == "split_prompt")
        - 0.08 * (prompt_type == "savings_label")
        + 0.18 * (1 - households["present_bias"].to_numpy())
        + rng.normal(0, 0.08, n_households)
    )
    spend_share = np.clip(spend_share, 0, 1)

    debt_share = (
        0.20
        + 0.22 * (prompt_type == "debt_prompt")
        + 0.18 * (prompt_type == "split_prompt")
        + 0.10 * (households["debt_burden"].to_numpy() / 9000)
        + rng.normal(0, 0.06, n_households)
    )
    debt_share = np.clip(debt_share, 0, 1 - spend_share)

    savings_share = 1 - spend_share - debt_share

    rows.append(pd.DataFrame({
        "event_id": event_id,
        "household_id": households["household_id"],
        "prompt_type": prompt_type,
        "windfall_amount": windfall_amount,
        "spending": windfall_amount * spend_share,
        "debt_repayment": windfall_amount * debt_share,
        "savings_allocation": windfall_amount * savings_share,
        "monthly_income": households["monthly_income"],
        "debt_burden": households["debt_burden"],
        "liquidity_buffer": households["liquidity_buffer"],
        "present_bias": households["present_bias"],
        "label_strength": households["label_strength"],
    }))

history = pd.concat(rows, ignore_index=True)

summary = history.groupby("prompt_type").agg(
    observations=("event_id", "count"),
    mean_windfall=("windfall_amount", "mean"),
    mean_spending=("spending", "mean"),
    mean_debt_repayment=("debt_repayment", "mean"),
    mean_savings_allocation=("savings_allocation", "mean"),
).reset_index()

history.to_csv(TABLES / "windfall_spending_history.csv", index=False)
summary.to_csv(TABLES / "windfall_prompt_summary.csv", index=False)

print(summary)
