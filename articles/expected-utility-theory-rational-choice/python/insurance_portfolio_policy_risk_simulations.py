from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(23231)

def crra_utility(x, rho):
    x_arr = np.asarray(x, dtype=float)
    rho_arr = np.asarray(rho, dtype=float)
    return np.where(
        np.isclose(rho_arr, 1.0),
        np.log(x_arr),
        (x_arr ** (1 - rho_arr)) / (1 - rho_arr),
    )

n = 3500

agents = pd.DataFrame({
    "agent_id": np.arange(1, n + 1),
    "wealth": rng.uniform(10_000, 120_000, n),
    "rho": rng.uniform(0.25, 3.00, n),
    "trust": rng.uniform(0.20, 1.00, n),
    "liquidity_constraint": rng.uniform(0.00, 0.50, n),
})

# Insurance demand simulation.
loss_probability = 0.05
loss_amount = 20_000
expected_loss = loss_probability * loss_amount
premium_loading = rng.uniform(1.05, 1.50, n)
premium = expected_loss * premium_loading

eu_uninsured = (
    loss_probability * crra_utility(np.maximum(agents["wealth"] - loss_amount, 1), agents["rho"])
    + (1 - loss_probability) * crra_utility(agents["wealth"], agents["rho"])
)

eu_insured = crra_utility(agents["wealth"] - premium, agents["rho"])

formal_insurance_takeup = (eu_insured > eu_uninsured).astype(int)
observed_insurance_takeup = (
    (formal_insurance_takeup == 1)
    & (agents["liquidity_constraint"].to_numpy() < 0.42)
    & (agents["trust"].to_numpy() > 0.35)
).astype(int)

insurance_df = agents.assign(
    loss_probability=loss_probability,
    loss_amount=loss_amount,
    expected_loss=expected_loss,
    premium_loading=premium_loading,
    premium=premium,
    eu_uninsured=eu_uninsured,
    eu_insured=eu_insured,
    formal_insurance_takeup=formal_insurance_takeup,
    observed_insurance_takeup=observed_insurance_takeup,
)

insurance_summary = insurance_df.agg(
    agents=("agent_id", "count"),
    formal_insurance_takeup_rate=("formal_insurance_takeup", "mean"),
    observed_insurance_takeup_rate=("observed_insurance_takeup", "mean"),
    mean_premium=("premium", "mean"),
    mean_expected_loss=("expected_loss", "mean"),
).to_frame().T

# Portfolio share simulation.
risk_free_return = 0.02
risky_expected_return = 0.07
risky_volatility = 0.18
risky_shares = np.linspace(0.0, 1.0, 21)

portfolio_rows = []
for _, row in agents.iterrows():
    best_share = 0.0
    best_eu = -np.inf
    for share in risky_shares:
        good_return = share * (risky_expected_return + risky_volatility) + (1 - share) * risk_free_return
        bad_return = share * (risky_expected_return - risky_volatility) + (1 - share) * risk_free_return
        eu = 0.50 * crra_utility(row["wealth"] * (1 + good_return), row["rho"]) + 0.50 * crra_utility(row["wealth"] * (1 + bad_return), row["rho"])
        if eu > best_eu:
            best_eu = float(eu)
            best_share = float(share)
    portfolio_rows.append({
        "agent_id": row["agent_id"],
        "wealth": row["wealth"],
        "rho": row["rho"],
        "optimal_risky_share": best_share,
        "expected_utility": best_eu,
    })

portfolio_df = pd.DataFrame(portfolio_rows)
portfolio_summary = portfolio_df.groupby(pd.qcut(portfolio_df["rho"], 4, labels=["Q1", "Q2", "Q3", "Q4"]), observed=False).agg(
    agents=("agent_id", "count"),
    mean_rho=("rho", "mean"),
    mean_optimal_risky_share=("optimal_risky_share", "mean"),
).reset_index().rename(columns={"rho": "rho_quartile"})

# Policy-risk simulation.
policy = pd.DataFrame({
    "policy": ["resilience_investment", "high_return_low_resilience"],
    "p_good": [0.90, 0.96],
    "good_outcome": [120, 150],
    "p_bad": [0.10, 0.04],
    "bad_outcome": [60, -300],
})

policy_rows = []
for rho_value in [0.50, 1.00, 2.00, 3.00]:
    for _, policy_row in policy.iterrows():
        eu_policy = (
            policy_row["p_good"] * crra_utility(1000 + policy_row["good_outcome"], rho_value)
            + policy_row["p_bad"] * crra_utility(1000 + policy_row["bad_outcome"], rho_value)
        )
        policy_rows.append({
            "rho": rho_value,
            "policy": policy_row["policy"],
            "expected_monetary_value": policy_row["p_good"] * policy_row["good_outcome"] + policy_row["p_bad"] * policy_row["bad_outcome"],
            "expected_utility": float(eu_policy),
        })

policy_results = pd.DataFrame(policy_rows)

insurance_df.to_csv(TABLES / "insurance_demand_simulation.csv", index=False)
insurance_summary.to_csv(TABLES / "insurance_demand_summary.csv", index=False)
portfolio_df.to_csv(TABLES / "portfolio_choice_simulation.csv", index=False)
portfolio_summary.to_csv(TABLES / "portfolio_choice_summary.csv", index=False)
policy_results.to_csv(TABLES / "expected_utility_policy_risk_example.csv", index=False)

print("Insurance, portfolio, and policy-risk simulations complete.")
print(insurance_summary)
print(portfolio_summary)
print(policy_results)
