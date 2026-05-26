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

rng = np.random.default_rng(19191)
n = 2500

base = pd.DataFrame({
    "loss_aversion": rng.uniform(1.0, 3.0, n),
    "curvature": rng.uniform(0.70, 1.00, n),
    "numeracy": rng.uniform(0.20, 1.00, n),
    "trust": rng.uniform(0.20, 1.00, n),
    "decision_fatigue": rng.uniform(0.00, 0.40, n),
})

def prospect_value(x: np.ndarray | float, lam: np.ndarray, eta: np.ndarray) -> np.ndarray:
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** eta, -lam * ((-x_arr) ** eta))

grid = list(itertools.product(
    ["gain_frame", "loss_frame", "balanced_absolute_risk_frame"],
    [0.15, 0.40, 0.70, 0.90],
    [0.35, 0.60, 0.85, 0.95],
    [0.25, 0.50, 0.75, 0.95],
))

rows = []
for frame, frame_strength, disclosure_quality, salience in grid:
    if frame == "gain_frame":
        certain = 200
        risky_values = np.array([600, 0])
        risky_probabilities = np.array([1/3, 2/3])
        frame_shift_multiplier = -20
    elif frame == "loss_frame":
        certain = -400
        risky_values = np.array([-600, 0])
        risky_probabilities = np.array([2/3, 1/3])
        frame_shift_multiplier = 22
    else:
        certain = 200
        risky_values = np.array([600, 0])
        risky_probabilities = np.array([1/3, 2/3])
        frame_shift_multiplier = 5

    certain_value = prospect_value(certain, base["loss_aversion"].to_numpy(), base["curvature"].to_numpy())
    risky_value = (
        risky_probabilities[0] * prospect_value(risky_values[0], base["loss_aversion"].to_numpy(), base["curvature"].to_numpy())
        + risky_probabilities[1] * prospect_value(risky_values[1], base["loss_aversion"].to_numpy(), base["curvature"].to_numpy())
    )

    comprehension = np.clip(
        disclosure_quality * base["numeracy"].to_numpy()
        + 0.20 * base["trust"].to_numpy()
        - 0.25 * base["decision_fatigue"].to_numpy(),
        0,
        1,
    )

    if frame == "loss_frame":
        framing_shift = frame_strength * salience * base["loss_aversion"].to_numpy() * frame_shift_multiplier
    elif frame == "gain_frame":
        framing_shift = frame_strength * salience * frame_shift_multiplier
    else:
        framing_shift = 0.05 * salience * frame_shift_multiplier

    adjusted_risky_value = risky_value + framing_shift + comprehension * 5
    choose_risky = (adjusted_risky_value >= certain_value).astype(int)
    welfare_proxy = np.where(choose_risky == 1, risky_value, certain_value) + comprehension * 10 - base["decision_fatigue"].to_numpy() * 5

    manipulation_risk = frame_strength * salience * (1 - comprehension)
    decision_quality_index = welfare_proxy + 5 * comprehension - 3 * manipulation_risk

    rows.append({
        "frame": frame,
        "frame_strength": frame_strength,
        "disclosure_quality": disclosure_quality,
        "salience": salience,
        "risky_choice_rate": float(np.mean(choose_risky)),
        "mean_comprehension": float(np.mean(comprehension)),
        "mean_welfare_proxy": float(np.mean(welfare_proxy)),
        "mean_manipulation_risk": float(np.mean(manipulation_risk)),
        "mean_decision_quality_index": float(np.mean(decision_quality_index)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "framing_design_sensitivity.csv", index=False)
sensitivity.sort_values("mean_decision_quality_index", ascending=False).head(15).to_csv(
    DIAG / "framing_design_top_decision_quality_regimes.csv",
    index=False,
)

print(sensitivity.sort_values("mean_decision_quality_index", ascending=False).head(10))
