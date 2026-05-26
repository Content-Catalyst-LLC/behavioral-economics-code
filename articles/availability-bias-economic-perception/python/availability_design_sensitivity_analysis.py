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

rng = np.random.default_rng(20201)

n = 2500
true_probability = 0.12

base = pd.DataFrame({
    "availability_sensitivity": rng.uniform(0.10, 0.90, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "trust_in_statistics": rng.uniform(0.20, 1.00, n),
    "risk_tolerance": rng.uniform(0.10, 0.90, n),
    "prior_experience": rng.binomial(1, 0.25, n),
})

grid = list(itertools.product(
    [0.50, 0.80, 1.10, 1.50],
    [0.10, 0.35, 0.60, 0.85],
    [0.20, 0.45, 0.70, 0.90],
))

rows = []
for salience_scale, base_rate_disclosure, emotional_intensity in grid:
    recency_signal = rng.uniform(0, 1, n) * salience_scale
    vividness_signal = rng.uniform(0, 1, n) * salience_scale
    media_signal = rng.uniform(0, 1, n) * salience_scale
    social_signal = rng.uniform(0, 1, n) * salience_scale

    availability_score = (
        0.25 * recency_signal
        + 0.25 * vividness_signal
        + 0.25 * media_signal
        + 0.25 * social_signal
        + 0.20 * base["prior_experience"].to_numpy() * emotional_intensity
    )

    base_rate_correction = (
        base_rate_disclosure
        * base["numeracy"].to_numpy()
        * base["trust_in_statistics"].to_numpy()
        * 0.18
    )

    subjective_probability = np.clip(
        true_probability
        + base["availability_sensitivity"].to_numpy() * availability_score * 0.25
        - base_rate_correction,
        0,
        1,
    )

    calibration_error = subjective_probability - true_probability
    insurance_demand = (
        subjective_probability > (0.16 - base["prior_experience"].to_numpy() * 0.03)
    ).astype(int)
    policy_support = (
        subjective_probability
        + 0.10 * emotional_intensity
        + 0.05 * base["trust_in_statistics"].to_numpy()
        > 0.25
    ).astype(int)

    welfare_proxy = (
        1
        - np.abs(calibration_error)
        - 0.08 * emotional_intensity * availability_score
        + 0.05 * base_rate_disclosure * base["numeracy"].to_numpy()
    )

    rows.append({
        "salience_scale": salience_scale,
        "base_rate_disclosure": base_rate_disclosure,
        "emotional_intensity": emotional_intensity,
        "mean_availability_score": float(np.mean(availability_score)),
        "mean_subjective_probability": float(np.mean(subjective_probability)),
        "mean_calibration_error": float(np.mean(calibration_error)),
        "mean_absolute_calibration_error": float(np.mean(np.abs(calibration_error))),
        "insurance_demand_rate": float(np.mean(insurance_demand)),
        "policy_support_rate": float(np.mean(policy_support)),
        "mean_welfare_proxy": float(np.mean(welfare_proxy)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "availability_design_sensitivity.csv", index=False)
sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(15).to_csv(
    DIAG / "availability_design_top_welfare_regimes.csv",
    index=False,
)

print(sensitivity.sort_values("mean_welfare_proxy", ascending=False).head(10))
