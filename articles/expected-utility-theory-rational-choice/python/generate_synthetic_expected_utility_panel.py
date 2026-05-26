from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(23230)
n_agents = 3000

def crra_utility(x: np.ndarray | float, rho: np.ndarray | float) -> np.ndarray:
    x_arr = np.asarray(x, dtype=float)
    rho_arr = np.asarray(rho, dtype=float)
    return np.where(
        np.isclose(rho_arr, 1.0),
        np.log(x_arr),
        (x_arr ** (1 - rho_arr)) / (1 - rho_arr),
    )

def inverse_crra_utility(u: np.ndarray | float, rho: np.ndarray | float) -> np.ndarray:
    u_arr = np.asarray(u, dtype=float)
    rho_arr = np.asarray(rho, dtype=float)
    return np.where(
        np.isclose(rho_arr, 1.0),
        np.exp(u_arr),
        (u_arr * (1 - rho_arr)) ** (1 / (1 - rho_arr)),
    )

def simulate_population(regime_name: str, rho_low: float, rho_high: float) -> pd.DataFrame:
    wealth = rng.uniform(5_000, 100_000, n_agents)
    rho = rng.uniform(rho_low, rho_high, n_agents)
    numeracy = rng.uniform(0.20, 1.00, n_agents)
    liquidity_constraint = rng.uniform(0.00, 0.50, n_agents)
    trust = rng.uniform(0.20, 1.00, n_agents)

    payoff_a = 100
    payoff_b_low = 40
    payoff_b_high = 220
    p_low = 0.50
    p_high = 0.50

    eu_a = crra_utility(wealth + payoff_a, rho)
    eu_b = (
        p_low * crra_utility(wealth + payoff_b_low, rho)
        + p_high * crra_utility(wealth + payoff_b_high, rho)
    )

    expected_value_b = p_low * payoff_b_low + p_high * payoff_b_high

    certainty_equivalent_total_wealth = inverse_crra_utility(eu_b, rho)
    certainty_equivalent_payoff = certainty_equivalent_total_wealth - wealth
    risk_premium = expected_value_b - certainty_equivalent_payoff

    choose_risky_eu = (eu_b > eu_a).astype(int)

    observed_choose_risky = (
        (choose_risky_eu == 1)
        & (numeracy > 0.25)
        & (liquidity_constraint < 0.45)
        & (trust > 0.30)
    ).astype(int)

    return pd.DataFrame({
        "agent_id": np.arange(1, n_agents + 1),
        "regime": regime_name,
        "wealth": wealth,
        "rho": rho,
        "numeracy": numeracy,
        "liquidity_constraint": liquidity_constraint,
        "trust": trust,
        "eu_certain": eu_a,
        "eu_risky": eu_b,
        "expected_value_risky": expected_value_b,
        "certainty_equivalent_payoff": certainty_equivalent_payoff,
        "risk_premium": risk_premium,
        "choose_risky_eu": choose_risky_eu,
        "observed_choose_risky": observed_choose_risky,
        "medium_risk_aversion_treat": int(regime_name == "medium_risk_aversion"),
        "high_risk_aversion_treat": int(regime_name == "high_risk_aversion"),
    })

panel = pd.concat([
    simulate_population("low_risk_aversion", 0.10, 0.80),
    simulate_population("medium_risk_aversion", 0.80, 1.50),
    simulate_population("high_risk_aversion", 1.50, 3.00),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_wealth=("wealth", "mean"),
    mean_rho=("rho", "mean"),
    share_choose_risky_eu=("choose_risky_eu", "mean"),
    share_choose_risky_observed=("observed_choose_risky", "mean"),
    mean_certainty_equivalent=("certainty_equivalent_payoff", "mean"),
    mean_risk_premium=("risk_premium", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_expected_utility_panel.csv", index=False)
summary.to_csv(TABLES / "expected_utility_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_expected_utility_panel.csv", index=False)
summary.to_csv(PROCESSED / "expected_utility_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} expected-utility rows.")
print(summary)
