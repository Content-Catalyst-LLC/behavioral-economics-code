from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_expected_utility_panel.csv")

summary = df.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_wealth=("wealth", "mean"),
    mean_rho=("rho", "mean"),
    median_rho=("rho", "median"),
    share_choose_risky_eu=("choose_risky_eu", "mean"),
    share_choose_risky_observed=("observed_choose_risky", "mean"),
    mean_certainty_equivalent=("certainty_equivalent_payoff", "mean"),
    median_certainty_equivalent=("certainty_equivalent_payoff", "median"),
    mean_risk_premium=("risk_premium", "mean"),
    median_risk_premium=("risk_premium", "median"),
).reset_index()

summary.to_csv(TABLES / "certainty_equivalent_risk_premium_summary.csv", index=False)

rows = []
for wealth_bin, sub_w in df.groupby(pd.qcut(df["wealth"], 5, labels=["W1", "W2", "W3", "W4", "W5"]), observed=False):
    for rho_bin, sub in sub_w.groupby(pd.qcut(sub_w["rho"], 5, labels=["R1", "R2", "R3", "R4", "R5"]), observed=False):
        rows.append({
            "wealth_bin": wealth_bin,
            "rho_bin": rho_bin,
            "agents": len(sub),
            "mean_wealth": sub["wealth"].mean(),
            "mean_rho": sub["rho"].mean(),
            "mean_certainty_equivalent": sub["certainty_equivalent_payoff"].mean(),
            "mean_risk_premium": sub["risk_premium"].mean(),
            "share_choose_risky_eu": sub["choose_risky_eu"].mean(),
            "share_choose_risky_observed": sub["observed_choose_risky"].mean(),
        })

pd.DataFrame(rows).to_csv(DIAG / "certainty_equivalent_wealth_rho_grid.csv", index=False)

print(summary)
