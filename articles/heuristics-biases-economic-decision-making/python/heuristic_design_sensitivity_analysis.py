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

rng = np.random.default_rng(22221)

n = 2500
true_value = 0.35

base = pd.DataFrame({
    "alpha_availability": rng.uniform(0.00, 0.45, n),
    "beta_representativeness": rng.uniform(0.00, 0.45, n),
    "gamma_anchoring": rng.uniform(0.00, 0.45, n),
    "delta_framing": rng.uniform(0.00, 0.35, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "domain_knowledge": rng.uniform(0.10, 1.00, n),
    "cognitive_load": rng.uniform(0.00, 0.60, n),
    "confidence": rng.uniform(0.10, 0.90, n),
})

grid = list(itertools.product(
    [0.50, 0.80, 1.10, 1.50],
    [0.20, 0.45, 0.70, 0.90],
    [0.10, 0.35, 0.65, 0.90],
))

rows = []
for signal_scale, disclosure_quality, debiasing_support in grid:
    availability_signal = rng.uniform(-0.25, 0.25, n) * signal_scale
    representativeness_signal = rng.uniform(-0.25, 0.25, n) * signal_scale
    anchor_signal = rng.uniform(-0.25, 0.25, n) * signal_scale
    framing_signal = rng.uniform(-0.20, 0.20, n) * signal_scale

    correction_capacity = np.clip(
        0.35 * base["numeracy"].to_numpy()
        + 0.30 * base["domain_knowledge"].to_numpy()
        + 0.20 * disclosure_quality
        + 0.15 * debiasing_support
        - 0.25 * base["cognitive_load"].to_numpy(),
        0,
        1,
    )

    raw_error = (
        base["alpha_availability"].to_numpy() * availability_signal
        + base["beta_representativeness"].to_numpy() * representativeness_signal
        + base["gamma_anchoring"].to_numpy() * anchor_signal
        + base["delta_framing"].to_numpy() * framing_signal
    )

    corrected_error = raw_error * (1 - correction_capacity)
    estimated_value = np.clip(true_value + corrected_error, 0, 1)
    judgment_error = estimated_value - true_value
    absolute_error = np.abs(judgment_error)
    decision_quality = 1 - absolute_error

    confidence_adjusted_error = absolute_error * (1 + 0.25 * base["confidence"].to_numpy())

    welfare_proxy = (
        decision_quality
        + 0.06 * disclosure_quality
        + 0.05 * debiasing_support
        - 0.08 * base["cognitive_load"].to_numpy()
        - 0.04 * confidence_adjusted_error
    )

    rows.append({
        "signal_scale": signal_scale,
        "disclosure_quality": disclosure_quality,
        "debiasing_support": debiasing_support,
        "mean_estimate": float(np.mean(estimated_value)),
        "mean_judgment_error": float(np.mean(judgment_error)),
        "mean_absolute_error": float(np.mean(absolute_error)),
        "mean_correction_capacity": float(np.mean(correction_capacity)),
        "mean_decision_quality": float(np.mean(decision_quality)),
        "mean_welfare_proxy": float(np.mean(welfare_proxy)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "heuristic_design_sensitivity.csv", index=False)
sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(15).to_csv(
    DIAG / "heuristic_design_top_welfare_regimes.csv",
    index=False,
)

print(sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(10))
