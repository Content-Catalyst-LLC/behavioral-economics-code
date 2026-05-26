from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(24242)

n = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "lambda_loss": rng.uniform(1.0, 3.0, n),
    "income_security": rng.uniform(0.10, 1.00, n),
    "trust": rng.uniform(0.20, 1.00, n),
    "status_quo_attachment": rng.uniform(0.00, 1.00, n),
})

# Endowment effect: WTA exceeds WTP when ownership creates perceived loss.
market_value = rng.uniform(20, 200, n)
owned = rng.binomial(1, 0.50, n)
wtp = market_value * rng.uniform(0.75, 1.05, n)
wta = market_value * (1 + owned * agents["lambda_loss"].to_numpy() * rng.uniform(0.15, 0.45, n))

endowment = agents.assign(
    market_value=market_value,
    owned=owned,
    willingness_to_pay=wtp,
    willingness_to_accept=wta,
    endowment_gap=wta - wtp,
)

endowment_summary = endowment.groupby("owned").agg(
    agents=("agent_id", "count"),
    mean_wtp=("willingness_to_pay", "mean"),
    mean_wta=("willingness_to_accept", "mean"),
    mean_endowment_gap=("endowment_gap", "mean"),
    mean_lambda=("lambda_loss", "mean"),
).reset_index()

# Consumer loss framing: cancellation / downgrade choice.
monthly_savings_from_cancel = rng.uniform(5, 60, n)
perceived_lost_benefits = rng.uniform(10, 100, n) * agents["lambda_loss"].to_numpy()
cancellation_friction = rng.uniform(0, 1, n)
cancel_score = (
    0.05 * monthly_savings_from_cancel
    - 0.035 * perceived_lost_benefits
    - 0.80 * cancellation_friction
    + 0.45 * agents["trust"].to_numpy()
    + rng.normal(0, 0.35, n)
)
cancel_probability = 1 / (1 + np.exp(-cancel_score))
cancel = rng.binomial(1, cancel_probability)

consumer = agents.assign(
    monthly_savings_from_cancel=monthly_savings_from_cancel,
    perceived_lost_benefits=perceived_lost_benefits,
    cancellation_friction=cancellation_friction,
    cancel_probability=cancel_probability,
    cancel=cancel,
)

consumer_summary = consumer.agg(
    agents=("agent_id", "count"),
    cancellation_rate=("cancel", "mean"),
    mean_monthly_savings=("monthly_savings_from_cancel", "mean"),
    mean_perceived_lost_benefits=("perceived_lost_benefits", "mean"),
    mean_friction=("cancellation_friction", "mean"),
).to_frame().T

# Policy transition: concentrated losses, diffuse gains, and support.
policy_gain = rng.uniform(30, 180, n)
policy_loss = rng.choice([0, 20, 60, 120, 250], n, p=[0.45, 0.20, 0.15, 0.12, 0.08])
distributional_weight = np.where(policy_loss >= 120, 1.4, 1.0)
transition_support = rng.uniform(0, 120, n)
net_reference_value = policy_gain - agents["lambda_loss"].to_numpy() * np.maximum(policy_loss - transition_support, 0) * distributional_weight

support_score = (
    -0.25
    + 0.012 * net_reference_value
    + 0.65 * agents["trust"].to_numpy()
    - 0.45 * agents["status_quo_attachment"].to_numpy()
    + rng.normal(0, 0.45, n)
)
support_probability = 1 / (1 + np.exp(-support_score))
support_policy = rng.binomial(1, support_probability)

policy = agents.assign(
    policy_gain=policy_gain,
    policy_loss=policy_loss,
    transition_support=transition_support,
    distributional_weight=distributional_weight,
    net_reference_value=net_reference_value,
    support_probability=support_probability,
    support_policy=support_policy,
)

policy_summary = policy.groupby(pd.cut(policy["policy_loss"], bins=[-1, 0, 50, 150, 300], labels=["none", "low", "medium", "high"]), observed=False).agg(
    agents=("agent_id", "count"),
    support_rate=("support_policy", "mean"),
    mean_policy_gain=("policy_gain", "mean"),
    mean_policy_loss=("policy_loss", "mean"),
    mean_transition_support=("transition_support", "mean"),
    mean_net_reference_value=("net_reference_value", "mean"),
).reset_index().rename(columns={"policy_loss": "policy_loss_bin"})

endowment.to_csv(TABLES / "endowment_effect_simulation.csv", index=False)
endowment_summary.to_csv(TABLES / "endowment_effect_summary.csv", index=False)
consumer.to_csv(TABLES / "consumer_loss_framing_simulation.csv", index=False)
consumer_summary.to_csv(TABLES / "consumer_loss_framing_summary.csv", index=False)
policy.to_csv(TABLES / "policy_transition_loss_distribution.csv", index=False)
policy_summary.to_csv(TABLES / "policy_transition_loss_distribution_summary.csv", index=False)

print(endowment_summary)
print(consumer_summary)
print(policy_summary)
