from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(13131)

n_investors = 2500
n_periods = 100

investors = pd.DataFrame({
    "investor_id": np.arange(1, n_investors + 1),
    "loss_aversion_lambda": np.clip(rng.normal(2.0, 0.45, n_investors), 1.0, 3.5),
    "curvature_eta": np.clip(rng.normal(0.88, 0.08, n_investors), 0.60, 1.00),
    "reference_point": rng.normal(100, 8, n_investors),
    "risk_tolerance": rng.uniform(0.50, 1.50, n_investors),
})

def prospect_value(x: np.ndarray, eta: np.ndarray, lamb: np.ndarray) -> np.ndarray:
    gains = np.power(np.maximum(x, 0), eta)
    losses = -lamb * np.power(np.maximum(-x, 0), eta)
    return gains + losses

rows = []
for period in range(1, n_periods + 1):
    current_price = 100 + rng.normal(0.10 * period, 7.5)
    paper_gain_loss = current_price - investors["reference_point"].to_numpy()

    subjective_value = prospect_value(
        paper_gain_loss,
        investors["curvature_eta"].to_numpy(),
        investors["loss_aversion_lambda"].to_numpy(),
    )

    sell_pressure = 1 / (1 + np.exp(-(subjective_value / 20 - investors["risk_tolerance"].to_numpy())))
    sell = rng.binomial(1, sell_pressure)

    rows.append(pd.DataFrame({
        "period": period,
        "investor_id": investors["investor_id"],
        "current_price": current_price,
        "reference_point": investors["reference_point"],
        "paper_gain_loss": paper_gain_loss,
        "loss_aversion_lambda": investors["loss_aversion_lambda"],
        "curvature_eta": investors["curvature_eta"],
        "subjective_value": subjective_value,
        "sell_pressure": sell_pressure,
        "sold": sell,
    }))

panel = pd.concat(rows, ignore_index=True)
summary = panel.groupby("period").agg(
    mean_price=("current_price", "mean"),
    mean_paper_gain_loss=("paper_gain_loss", "mean"),
    mean_subjective_value=("subjective_value", "mean"),
    sell_rate=("sold", "mean"),
).reset_index()

panel.to_csv(TABLES / "prospect_theory_investor_panel.csv", index=False)
summary.to_csv(TABLES / "prospect_theory_period_summary.csv", index=False)

print(summary.tail())
