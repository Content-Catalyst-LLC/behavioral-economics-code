from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(22220)

n_agents = 3000
true_value = 0.35

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "alpha_availability": rng.uniform(0.00, 0.45, n_agents),
    "beta_representativeness": rng.uniform(0.00, 0.45, n_agents),
    "gamma_anchoring": rng.uniform(0.00, 0.45, n_agents),
    "delta_framing": rng.uniform(0.00, 0.35, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "domain_knowledge": rng.uniform(0.10, 1.00, n_agents),
    "cognitive_load": rng.uniform(0.00, 0.60, n_agents),
    "confidence": rng.uniform(0.10, 0.90, n_agents),
})

def simulate_environment(
    regime_name: str,
    signal_scale: float,
    disclosure_quality: float,
    debiasing_support: float,
) -> pd.DataFrame:
    availability_signal = rng.uniform(-0.25, 0.25, n_agents) * signal_scale
    representativeness_signal = rng.uniform(-0.25, 0.25, n_agents) * signal_scale
    anchor_signal = rng.uniform(-0.25, 0.25, n_agents) * signal_scale
    framing_signal = rng.uniform(-0.20, 0.20, n_agents) * signal_scale

    correction_capacity = np.clip(
        0.35 * agents["numeracy"].to_numpy()
        + 0.30 * agents["domain_knowledge"].to_numpy()
        + 0.20 * disclosure_quality
        + 0.15 * debiasing_support
        - 0.25 * agents["cognitive_load"].to_numpy(),
        0,
        1,
    )

    raw_error = (
        agents["alpha_availability"].to_numpy() * availability_signal
        + agents["beta_representativeness"].to_numpy() * representativeness_signal
        + agents["gamma_anchoring"].to_numpy() * anchor_signal
        + agents["delta_framing"].to_numpy() * framing_signal
    )

    corrected_error = raw_error * (1 - correction_capacity)
    estimated_value = np.clip(true_value + corrected_error, 0, 1)

    judgment_error = estimated_value - true_value
    absolute_error = np.abs(judgment_error)
    decision_quality = 1 - absolute_error
    confidence_adjusted_error = absolute_error * (1 + 0.25 * agents["confidence"].to_numpy())

    welfare_proxy = (
        decision_quality
        + 0.06 * disclosure_quality
        + 0.05 * debiasing_support
        - 0.08 * agents["cognitive_load"].to_numpy()
        - 0.04 * confidence_adjusted_error
    )

    return pd.DataFrame({
        "agent_id": agents["agent_id"],
        "regime": regime_name,
        "true_value": true_value,
        "estimated_value": estimated_value,
        "judgment_error": judgment_error,
        "absolute_error": absolute_error,
        "decision_quality": decision_quality,
        "welfare_proxy": welfare_proxy,
        "correction_capacity": correction_capacity,
        "availability_signal": availability_signal,
        "representativeness_signal": representativeness_signal,
        "anchor_signal": anchor_signal,
        "framing_signal": framing_signal,
        "numeracy": agents["numeracy"],
        "domain_knowledge": agents["domain_knowledge"],
        "cognitive_load": agents["cognitive_load"],
        "confidence": agents["confidence"],
        "disclosure_quality": disclosure_quality,
        "debiasing_support": debiasing_support,
        "medium_bias_treat": int(regime_name == "medium_bias_environment"),
        "high_bias_treat": int(regime_name == "high_bias_low_context"),
    })

panel = pd.concat([
    simulate_environment(
        regime_name="low_bias_with_context",
        signal_scale=0.60,
        disclosure_quality=0.80,
        debiasing_support=0.75,
    ),
    simulate_environment(
        regime_name="medium_bias_environment",
        signal_scale=1.00,
        disclosure_quality=0.50,
        debiasing_support=0.40,
    ),
    simulate_environment(
        regime_name="high_bias_low_context",
        signal_scale=1.50,
        disclosure_quality=0.20,
        debiasing_support=0.10,
    ),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_estimate=("estimated_value", "mean"),
    mean_judgment_error=("judgment_error", "mean"),
    mean_absolute_error=("absolute_error", "mean"),
    mean_decision_quality=("decision_quality", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
    mean_correction_capacity=("correction_capacity", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_heuristics_biases_panel.csv", index=False)
summary.to_csv(TABLES / "heuristics_biases_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_heuristics_biases_panel.csv", index=False)
summary.to_csv(PROCESSED / "heuristics_biases_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} heuristic-judgment rows.")
print(summary)
