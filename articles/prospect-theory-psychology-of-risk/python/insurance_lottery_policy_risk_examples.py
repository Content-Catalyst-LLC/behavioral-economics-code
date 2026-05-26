from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(25252)

def prospect_value(x, lam, alpha, beta):
    x_arr = np.asarray(x, dtype=float)
    return np.where(x_arr >= 0, x_arr ** alpha, -lam * ((-x_arr) ** beta))

def probability_weight(p, gamma):
    p_arr = np.asarray(p, dtype=float)
    return (p_arr ** gamma) / ((p_arr ** gamma + (1 - p_arr) ** gamma) ** (1 / gamma))

n = 3500

agents = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n),
    "alpha_gain": rng.uniform(0.75, 1.0, n),
    "beta_loss": rng.uniform(0.75, 1.0, n),
    "gamma_weight": rng.uniform(0.55, 1.0, n),
    "income_security": rng.uniform(0.10, 1.00, n),
    "trust": rng.uniform(0.20, 1.00, n),
})

rows = []

for _, row in agents.iterrows():
    lam = row["lambda_loss"]
    alpha = row["alpha_gain"]
    beta = row["beta_loss"]
    gamma = row["gamma_weight"]

    # Insurance example: pay a certain premium to avoid rare loss.
    rare_loss_probability = 0.03
    catastrophic_loss = 2000
    premium = 95
    no_insurance_value = (
        probability_weight(rare_loss_probability, gamma) * prospect_value(-catastrophic_loss, lam, alpha, beta)
        + probability_weight(1 - rare_loss_probability, gamma) * prospect_value(0, lam, alpha, beta)
    )
    insurance_value = prospect_value(-premium, lam, alpha, beta)

    # Lottery example: pay small ticket price for rare large gain.
    lottery_probability = 0.01
    lottery_gain = 5000
    ticket_cost = 20
    lottery_value = (
        probability_weight(lottery_probability, gamma) * prospect_value(lottery_gain - ticket_cost, lam, alpha, beta)
        + probability_weight(1 - lottery_probability, gamma) * prospect_value(-ticket_cost, lam, alpha, beta)
    )

    # Policy-risk example: immediate cost for avoided future loss.
    transition_cost = 140
    avoided_loss_probability = 0.08
    avoided_loss = 2500
    climate_action_value = (
        probability_weight(avoided_loss_probability, gamma) * prospect_value(avoided_loss - transition_cost, lam, alpha, beta)
        + probability_weight(1 - avoided_loss_probability, gamma) * prospect_value(-transition_cost, lam, alpha, beta)
    )
    no_action_value = (
        probability_weight(avoided_loss_probability, gamma) * prospect_value(-avoided_loss, lam, alpha, beta)
        + probability_weight(1 - avoided_loss_probability, gamma) * prospect_value(0, lam, alpha, beta)
    )

    rows.append({
        "agent_id": row["agent_id"],
        "lambda_loss": lam,
        "gamma_weight": gamma,
        "income_security": row["income_security"],
        "trust": row["trust"],
        "insurance_value": float(insurance_value),
        "no_insurance_value": float(no_insurance_value),
        "choose_insurance": int(insurance_value > no_insurance_value),
        "lottery_value": float(lottery_value),
        "buy_lottery": int(lottery_value > 0),
        "climate_action_value": float(climate_action_value),
        "no_action_value": float(no_action_value),
        "support_climate_action": int(climate_action_value > no_action_value),
    })

df = pd.DataFrame(rows)

summary = df.agg(
    agents=("agent_id", "count"),
    insurance_takeup=("choose_insurance", "mean"),
    lottery_takeup=("buy_lottery", "mean"),
    climate_action_support=("support_climate_action", "mean"),
    mean_lambda=("lambda_loss", "mean"),
    mean_gamma=("gamma_weight", "mean"),
    mean_trust=("trust", "mean"),
).to_frame().T

df.to_csv(TABLES / "insurance_lottery_policy_risk_examples.csv", index=False)
summary.to_csv(TABLES / "insurance_lottery_policy_risk_summary.csv", index=False)

print(summary)
