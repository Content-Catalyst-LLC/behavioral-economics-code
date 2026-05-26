from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(25250)
n_agents = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n_agents),
    "alpha_gain": rng.uniform(0.75, 1.0, n_agents),
    "beta_loss": rng.uniform(0.75, 1.0, n_agents),
    "gamma_weight": rng.uniform(0.55, 1.0, n_agents),
    "rho_crra": rng.uniform(0.25, 2.50, n_agents),
    "wealth": rng.uniform(5_000, 100_000, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "income_security": rng.uniform(0.10, 1.00, n_agents),
    "trust": rng.uniform(0.20, 1.00, n_agents),
    "prior_loss_exposure": rng.binomial(1, 0.35, n_agents),
})

def prospect_value(x, lam, alpha, beta):
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** alpha, -lam * ((-x_arr) ** beta))

def probability_weight(p, gamma):
    p_arr = np.asarray(p, dtype=float)
    return (p_arr ** gamma) / ((p_arr ** gamma + (1 - p_arr) ** gamma) ** (1 / gamma))

def crra_utility(x, rho):
    x_arr = np.asarray(x, dtype=float)
    rho_arr = np.asarray(rho, dtype=float)
    return np.where(
        np.isclose(rho_arr, 1.0),
        np.log(x_arr),
        (x_arr ** (1 - rho_arr)) / (1 - rho_arr),
    )

def simulate_frame(frame: str) -> pd.DataFrame:
    rows = []

    for _, row in agents.iterrows():
        lam = row["lambda_loss"]
        alpha = row["alpha_gain"]
        beta = row["beta_loss"]
        gamma = row["gamma_weight"]
        rho = row["rho_crra"]
        wealth = row["wealth"]

        if frame == "gain":
            sure_outcome = 200
            risky_outcomes = np.array([600, 0])
            risky_probabilities = np.array([1 / 3, 2 / 3])
        elif frame == "loss":
            sure_outcome = -400
            risky_outcomes = np.array([-600, 0])
            risky_probabilities = np.array([2 / 3, 1 / 3])
        elif frame == "mixed_gamble":
            sure_outcome = 0
            risky_outcomes = np.array([240, -100])
            risky_probabilities = np.array([0.5, 0.5])
        else:
            raise ValueError(f"Unknown frame: {frame}")

        pt_sure = prospect_value(sure_outcome, lam, alpha, beta)
        pt_risky = np.sum(
            probability_weight(risky_probabilities, gamma)
            * prospect_value(risky_outcomes, lam, alpha, beta)
        )

        eu_sure = crra_utility(np.maximum(wealth + sure_outcome, 1), rho)
        eu_risky = np.sum(
            risky_probabilities
            * crra_utility(np.maximum(wealth + risky_outcomes, 1), rho)
        )

        rows.append({
            "agent_id": row["agent_id"],
            "frame": frame,
            "pt_sure_value": float(pt_sure),
            "pt_risky_value": float(pt_risky),
            "eu_sure_value": float(eu_sure),
            "eu_risky_value": float(eu_risky),
            "choose_risky_pt": int(pt_risky > pt_sure),
            "choose_risky_eu": int(eu_risky > eu_sure),
        })

    return pd.DataFrame(rows)

panel = pd.concat([
    simulate_frame("gain"),
    simulate_frame("loss"),
    simulate_frame("mixed_gamble"),
], ignore_index=True)

panel = panel.merge(agents, on="agent_id", how="left")
panel["loss_frame_treat"] = (panel["frame"] == "loss").astype(int)
panel["mixed_gamble_treat"] = (panel["frame"] == "mixed_gamble").astype(int)
panel["pt_eu_disagreement"] = (panel["choose_risky_pt"] != panel["choose_risky_eu"]).astype(int)

summary = panel.groupby("frame").agg(
    agents=("agent_id", "count"),
    share_choose_risky_pt=("choose_risky_pt", "mean"),
    share_choose_risky_eu=("choose_risky_eu", "mean"),
    disagreement_rate=("pt_eu_disagreement", "mean"),
    mean_pt_risky_value=("pt_risky_value", "mean"),
    mean_lambda=("lambda_loss", "mean"),
    mean_gamma=("gamma_weight", "mean"),
    mean_income_security=("income_security", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_prospect_theory_panel.csv", index=False)
summary.to_csv(TABLES / "prospect_theory_frame_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_prospect_theory_panel.csv", index=False)
summary.to_csv(PROCESSED / "prospect_theory_frame_summary.csv", index=False)

print(f"Wrote {len(panel):,} prospect-theory rows.")
print(summary)
