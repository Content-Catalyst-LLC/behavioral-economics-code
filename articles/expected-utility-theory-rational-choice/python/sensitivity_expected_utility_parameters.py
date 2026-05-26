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

rng = np.random.default_rng(23232)

def crra_utility(x, rho):
    x_arr = np.asarray(x, dtype=float)
    rho_arr = np.asarray(rho, dtype=float)
    return np.where(
        np.isclose(rho_arr, 1.0),
        np.log(x_arr),
        (x_arr ** (1 - rho_arr)) / (1 - rho_arr),
    )

def cara_utility(x, a):
    return -np.exp(-a * np.asarray(x, dtype=float))

n = 2500
wealth = rng.uniform(5_000, 100_000, n)

grid = list(itertools.product(
    [0.25, 0.75, 1.25, 2.00, 3.00],
    [0.02, 0.05, 0.10],
    [10_000, 20_000, 40_000],
    [1.05, 1.25, 1.50],
))

rows = []
for rho, loss_probability, loss_amount, premium_loading in grid:
    expected_loss = loss_probability * loss_amount
    premium = expected_loss * premium_loading

    eu_uninsured = (
        loss_probability * crra_utility(np.maximum(wealth - loss_amount, 1), rho)
        + (1 - loss_probability) * crra_utility(wealth, rho)
    )
    eu_insured = crra_utility(wealth - premium, rho)

    formal_takeup = (eu_insured > eu_uninsured).astype(int)

    rows.append({
        "rho": rho,
        "loss_probability": loss_probability,
        "loss_amount": loss_amount,
        "premium_loading": premium_loading,
        "expected_loss": expected_loss,
        "premium": premium,
        "formal_insurance_takeup_rate": float(np.mean(formal_takeup)),
        "mean_wealth": float(np.mean(wealth)),
    })

sensitivity = pd.DataFrame(rows)
sensitivity.to_csv(TABLES / "expected_utility_insurance_sensitivity.csv", index=False)

# CRRA vs CARA comparison for one stylized gamble.
compare_rows = []
for rho in [0.25, 0.75, 1.00, 1.50, 2.50]:
    eu_certain = crra_utility(50_000 + 100, rho)
    eu_risky = 0.5 * crra_utility(50_000 + 40, rho) + 0.5 * crra_utility(50_000 + 220, rho)
    compare_rows.append({
        "utility_family": "CRRA",
        "parameter": rho,
        "choose_risky": int(eu_risky > eu_certain),
        "eu_certain": float(eu_certain),
        "eu_risky": float(eu_risky),
    })

for a in [0.000005, 0.000010, 0.000025, 0.000050]:
    eu_certain = cara_utility(50_000 + 100, a)
    eu_risky = 0.5 * cara_utility(50_000 + 40, a) + 0.5 * cara_utility(50_000 + 220, a)
    compare_rows.append({
        "utility_family": "CARA",
        "parameter": a,
        "choose_risky": int(eu_risky > eu_certain),
        "eu_certain": float(eu_certain),
        "eu_risky": float(eu_risky),
    })

comparison = pd.DataFrame(compare_rows)
comparison.to_csv(DIAG / "crra_cara_choice_comparison.csv", index=False)

print(sensitivity.head())
print(comparison)
