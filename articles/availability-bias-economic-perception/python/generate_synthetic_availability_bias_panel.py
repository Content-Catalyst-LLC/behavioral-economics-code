from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20200)

n_agents = 3000
true_probability = 0.12

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "availability_sensitivity": rng.uniform(0.10, 0.90, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "trust_in_statistics": rng.uniform(0.20, 1.00, n_agents),
    "risk_tolerance": rng.uniform(0.10, 0.90, n_agents),
    "prior_experience": rng.binomial(1, 0.25, n_agents),
})

def simulate_availability_environment(
    regime_name: str,
    salience_scale: float,
    base_rate_disclosure: float,
    emotional_intensity: float,
) -> pd.DataFrame:
    recency_signal = rng.uniform(0, 1, n_agents) * salience_scale
    vividness_signal = rng.uniform(0, 1, n_agents) * salience_scale
    media_signal = rng.uniform(0, 1, n_agents) * salience_scale
    social_repetition_signal = rng.uniform(0, 1, n_agents) * salience_scale

    availability_score = (
        0.25 * recency_signal
        + 0.25 * vividness_signal
        + 0.25 * media_signal
        + 0.25 * social_repetition_signal
        + 0.20 * agents["prior_experience"].to_numpy() * emotional_intensity
    )

    base_rate_correction = (
        base_rate_disclosure
        * agents["numeracy"].to_numpy()
        * agents["trust_in_statistics"].to_numpy()
        * 0.18
    )

    subjective_probability = np.clip(
        true_probability
        + agents["availability_sensitivity"].to_numpy() * availability_score * 0.25
        - base_rate_correction,
        0,
        1,
    )

    calibration_error = subjective_probability - true_probability

    participate_in_risky_asset = (
        subjective_probability < (0.18 + agents["risk_tolerance"].to_numpy() * 0.12)
    ).astype(int)

    insurance_demand = (
        subjective_probability > (0.16 - agents["prior_experience"].to_numpy() * 0.03)
    ).astype(int)

    policy_support = (
        subjective_probability
        + 0.10 * emotional_intensity
        + 0.05 * agents["trust_in_statistics"].to_numpy()
        > 0.25
    ).astype(int)

    welfare_proxy = (
        1
        - np.abs(calibration_error)
        - 0.08 * emotional_intensity * availability_score
        + 0.05 * base_rate_disclosure * agents["numeracy"].to_numpy()
    )

    return pd.DataFrame({
        "agent_id": agents["agent_id"],
        "regime": regime_name,
        "true_probability": true_probability,
        "availability_sensitivity": agents["availability_sensitivity"],
        "numeracy": agents["numeracy"],
        "trust_in_statistics": agents["trust_in_statistics"],
        "risk_tolerance": agents["risk_tolerance"],
        "prior_experience": agents["prior_experience"],
        "recency_signal": recency_signal,
        "vividness_signal": vividness_signal,
        "media_signal": media_signal,
        "social_repetition_signal": social_repetition_signal,
        "availability_score": availability_score,
        "base_rate_disclosure": base_rate_disclosure,
        "emotional_intensity": emotional_intensity,
        "subjective_probability": subjective_probability,
        "calibration_error": calibration_error,
        "participate_in_risky_asset": participate_in_risky_asset,
        "insurance_demand": insurance_demand,
        "policy_support": policy_support,
        "welfare_proxy": welfare_proxy,
        "medium_availability_treat": int(regime_name == "medium_availability_environment"),
        "high_availability_treat": int(regime_name == "high_availability_no_base_rates"),
    })

panel = pd.concat([
    simulate_availability_environment(
        regime_name="low_availability_with_base_rates",
        salience_scale=0.60,
        base_rate_disclosure=0.80,
        emotional_intensity=0.25,
    ),
    simulate_availability_environment(
        regime_name="medium_availability_environment",
        salience_scale=1.00,
        base_rate_disclosure=0.45,
        emotional_intensity=0.55,
    ),
    simulate_availability_environment(
        regime_name="high_availability_no_base_rates",
        salience_scale=1.50,
        base_rate_disclosure=0.10,
        emotional_intensity=0.85,
    ),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_availability_score=("availability_score", "mean"),
    mean_subjective_probability=("subjective_probability", "mean"),
    mean_calibration_error=("calibration_error", "mean"),
    share_participating_risky_asset=("participate_in_risky_asset", "mean"),
    insurance_demand_rate=("insurance_demand", "mean"),
    policy_support_rate=("policy_support", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_availability_bias_panel.csv", index=False)
summary.to_csv(TABLES / "availability_bias_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_availability_bias_panel.csv", index=False)
summary.to_csv(PROCESSED / "availability_bias_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} availability-regime rows.")
print(summary)
