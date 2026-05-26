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

grid = list(itertools.product(
    [1.0, 1.5, 2.0, 2.5, 3.0],
    [0.75, 0.88, 1.0],
    [0.75, 0.88, 1.0],
    [100, 150, 200, 300],
    [50, 100, 150, 200],
))

rows = []
for lam, alpha, beta, gain, loss in grid:
    mixed_value = 0.5 * prospect_value(gain, lam, alpha, beta) + 0.5 * prospect_value(-loss, lam, alpha, beta)
    accept_mixed_gamble = int(mixed_value > 0)
    rows.append({
        "lambda_loss": lam,
        "alpha_gain": alpha,
        "beta_loss": beta,
        "gain": gain,
        "loss": loss,
        "mixed_gamble_value": float(mixed_value),
        "accept_mixed_gamble": accept_mixed_gamble,
        "gain_loss_ratio": gain / loss,
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "loss_aversion_parameter_sensitivity.csv", index=False)

thresholds = []
for lam in [1.0, 1.5, 2.0, 2.5, 3.0]:
    for loss in [50, 100, 200, 500]:
        minimum_gain = lam * loss
        thresholds.append({
            "lambda_loss": lam,
            "loss": loss,
            "linear_minimum_gain_to_accept_50_50_gamble": minimum_gain,
        })

pd.DataFrame(thresholds).to_csv(DIAG / "linear_loss_aversion_acceptance_thresholds.csv", index=False)

print(sensitivity.head(20))
print(pd.DataFrame(thresholds).head())
