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

def prospect_value(x, lam, alpha, beta):
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** alpha, -lam * ((-x_arr) ** beta))

def probability_weight(p, gamma):
    p_arr = np.asarray(p, dtype=float)
    return (p_arr ** gamma) / ((p_arr ** gamma + (1 - p_arr) ** gamma) ** (1 / gamma))

grid = list(itertools.product(
    [1.0, 1.5, 2.0, 2.5, 3.0],
    [0.75, 0.88, 1.0],
    [0.75, 0.88, 1.0],
    [0.55, 0.70, 0.85, 1.0],
    [100, 150, 240, 300],
    [50, 100, 150, 200],
))

rows = []
for lam, alpha, beta, gamma, gain, loss in grid:
    mixed_value = (
        probability_weight(0.5, gamma) * prospect_value(gain, lam, alpha, beta)
        + probability_weight(0.5, gamma) * prospect_value(-loss, lam, alpha, beta)
    )
    rows.append({
        "lambda_loss": lam,
        "alpha_gain": alpha,
        "beta_loss": beta,
        "gamma_weight": gamma,
        "gain": gain,
        "loss": loss,
        "mixed_gamble_value": float(mixed_value),
        "accept_mixed_gamble": int(mixed_value > 0),
        "gain_loss_ratio": gain / loss,
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "prospect_theory_parameter_sensitivity.csv", index=False)

prob_rows = []
for gamma in [0.55, 0.70, 0.85, 1.0]:
    for p in [0.01, 0.03, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]:
        prob_rows.append({
            "gamma_weight": gamma,
            "objective_probability": p,
            "decision_weight": float(probability_weight(p, gamma)),
            "weight_minus_probability": float(probability_weight(p, gamma) - p),
        })

pd.DataFrame(prob_rows).to_csv(DIAG / "probability_weighting_grid.csv", index=False)

thresholds = []
for lam in [1.0, 1.5, 2.0, 2.5, 3.0]:
    for loss in [50, 100, 200, 500]:
        thresholds.append({
            "lambda_loss": lam,
            "loss": loss,
            "linear_minimum_gain_to_accept_50_50_gamble": lam * loss,
        })

pd.DataFrame(thresholds).to_csv(DIAG / "linear_mixed_gamble_acceptance_thresholds.csv", index=False)

print(sensitivity.head(20))
print(pd.DataFrame(prob_rows).head())
