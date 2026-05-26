from __future__ import annotations

from pathlib import Path
import itertools
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
for folder in [TABLES, DIAG]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(21211)

n = 2500
true_value = 65.0

base = pd.DataFrame({
    "adjustment_rate": rng.uniform(0.20, 0.95, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "confidence": rng.uniform(0.10, 0.90, n),
    "cognitive_load": rng.uniform(0.00, 0.50, n),
    "domain_knowledge": rng.uniform(0.10, 1.00, n),
})

grid = list(itertools.product(
    [25, 45, 65, 85, 105],
    [0.20, 0.45, 0.70, 0.90],
    [0.10, 0.35, 0.65, 0.90],
))

rows = []
for anchor_value, disclosure_quality, counter_anchor_support in grid:
    effective_adjustment = np.clip(
        base["adjustment_rate"].to_numpy()
        + 0.18 * base["domain_knowledge"].to_numpy()
        + 0.12 * base["numeracy"].to_numpy()
        + 0.10 * disclosure_quality
        + 0.08 * counter_anchor_support
        - 0.20 * base["cognitive_load"].to_numpy(),
        0,
        1,
    )

    estimate = anchor_value + effective_adjustment * (true_value - anchor_value)
    bias = estimate - true_value
    absolute_error = np.abs(bias)
    anchor_distance = max(abs(anchor_value - true_value), 1)

    decision_quality = (
        1
        - absolute_error / anchor_distance
        + 0.05 * disclosure_quality
        + 0.04 * counter_anchor_support
    )
    welfare_proxy = (
        decision_quality
        - 0.10 * base["cognitive_load"].to_numpy()
        - 0.05 * absolute_error * (1 + base["confidence"].to_numpy() * 0.25) / 100
    )

    rows.append({
        "anchor_value": anchor_value,
        "disclosure_quality": disclosure_quality,
        "counter_anchor_support": counter_anchor_support,
        "mean_estimate": float(np.mean(estimate)),
        "mean_bias": float(np.mean(bias)),
        "mean_absolute_error": float(np.mean(absolute_error)),
        "mean_effective_adjustment": float(np.mean(effective_adjustment)),
        "mean_decision_quality": float(np.mean(decision_quality)),
        "mean_welfare_proxy": float(np.mean(welfare_proxy)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "anchoring_design_sensitivity.csv", index=False)
sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(15).to_csv(
    DIAG / "anchoring_design_top_welfare_regimes.csv",
    index=False,
)

print(sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(10))
