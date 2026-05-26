from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
DIAG = ROOT / "outputs" / "model_diagnostics"
DIAG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLES / "synthetic_prospect_theory_panel.csv")

comparison = df.groupby("frame").agg(
    agents=("agent_id", "count"),
    pt_risky_share=("choose_risky_pt", "mean"),
    eu_risky_share=("choose_risky_eu", "mean"),
    disagreement_rate=("pt_eu_disagreement", "mean"),
    mean_lambda=("lambda_loss", "mean"),
    mean_gamma=("gamma_weight", "mean"),
    mean_rho=("rho_crra", "mean"),
    mean_wealth=("wealth", "mean"),
).reset_index()

comparison["pt_minus_eu_risky_share"] = comparison["pt_risky_share"] - comparison["eu_risky_share"]
comparison.to_csv(TABLES / "prospect_theory_expected_utility_comparison.csv", index=False)

cell = df.groupby(["frame", "choose_risky_pt", "choose_risky_eu"]).agg(
    agents=("agent_id", "count"),
    mean_lambda=("lambda_loss", "mean"),
    mean_gamma=("gamma_weight", "mean"),
    mean_rho=("rho_crra", "mean"),
    mean_wealth=("wealth", "mean"),
).reset_index()
cell.to_csv(DIAG / "pt_eu_choice_crosswalk.csv", index=False)

print(comparison)
print(cell.head())
