from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(21212)

n = 3500

consumers = pd.DataFrame({
    "consumer_id": np.arange(1, n + 1),
    "price_sensitivity": rng.uniform(0.40, 1.60, n),
    "anchor_sensitivity": rng.uniform(0.10, 0.90, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "budget_pressure": rng.uniform(0.00, 0.60, n),
})

actual_price = rng.uniform(80, 140, n)
reference_price = actual_price * rng.choice([1.00, 1.25, 1.50, 1.75, 2.00], n, p=[0.20, 0.25, 0.25, 0.20, 0.10])
market_value = actual_price * rng.uniform(0.90, 1.15, n)

perceived_savings = np.maximum(reference_price - actual_price, 0)
reference_price_utility = consumers["anchor_sensitivity"].to_numpy() * perceived_savings / 100
total_cost_penalty = consumers["price_sensitivity"].to_numpy() * actual_price / 100
budget_penalty = consumers["budget_pressure"].to_numpy() * actual_price / 150
numeracy_correction = consumers["numeracy"].to_numpy() * np.maximum(reference_price - market_value, 0) / 100

purchase_utility = (
    1.0
    + reference_price_utility
    - total_cost_penalty
    - budget_penalty
    - numeracy_correction
)

purchase = (purchase_utility > 0.35).astype(int)

df = consumers.assign(
    actual_price=actual_price,
    reference_price=reference_price,
    market_value=market_value,
    perceived_savings=perceived_savings,
    purchase_utility=purchase_utility,
    purchase=purchase,
)

summary = df.groupby(pd.cut(df["reference_price"] / df["actual_price"], bins=[0.99, 1.25, 1.50, 1.75, 2.01])).agg(
    consumers=("consumer_id", "count"),
    purchase_rate=("purchase", "mean"),
    mean_actual_price=("actual_price", "mean"),
    mean_reference_price=("reference_price", "mean"),
    mean_perceived_savings=("perceived_savings", "mean"),
    mean_purchase_utility=("purchase_utility", "mean"),
).reset_index().rename(columns={"reference_price": "reference_price_ratio_bin"})

df.to_csv(TABLES / "reference_price_simulation.csv", index=False)
summary.to_csv(TABLES / "reference_price_simulation_summary.csv", index=False)

print(summary)
