from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(21210)

n_agents = 3000
true_value = 65.0

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "adjustment_rate": rng.uniform(0.20, 0.95, n_agents),
    "numeracy": rng.uniform(0.20, 1.00, n_agents),
    "confidence": rng.uniform(0.10, 0.90, n_agents),
    "cognitive_load": rng.uniform(0.00, 0.50, n_agents),
    "domain_knowledge": rng.uniform(0.10, 1.00, n_agents),
})

def simulate_anchor_regime(
    regime_name: str,
    anchor_value: float,
    disclosure_quality: float,
    counter_anchor_support: float,
) -> pd.DataFrame:
    effective_adjustment = np.clip(
        agents["adjustment_rate"].to_numpy()
        + 0.18 * agents["domain_knowledge"].to_numpy()
        + 0.12 * agents["numeracy"].to_numpy()
        + 0.10 * disclosure_quality
        + 0.08 * counter_anchor_support
        - 0.20 * agents["cognitive_load"].to_numpy(),
        0,
        1,
    )

    estimate = anchor_value + effective_adjustment * (true_value - anchor_value)
    bias = estimate - true_value
    absolute_error = np.abs(bias)
    confidence_adjusted_error = absolute_error * (1 + agents["confidence"].to_numpy() * 0.25)
    anchor_distance = max(abs(anchor_value - true_value), 1)

    decision_quality = (
        1
        - absolute_error / anchor_distance
        + 0.05 * disclosure_quality
        + 0.04 * counter_anchor_support
    )

    welfare_proxy = (
        decision_quality
        - 0.10 * agents["cognitive_load"].to_numpy()
        - 0.05 * confidence_adjusted_error / 100
    )

    return pd.DataFrame({
        "agent_id": agents["agent_id"],
        "regime": regime_name,
        "true_value": true_value,
        "anchor_value": anchor_value,
        "adjustment_rate": agents["adjustment_rate"],
        "effective_adjustment": effective_adjustment,
        "numeracy": agents["numeracy"],
        "confidence": agents["confidence"],
        "cognitive_load": agents["cognitive_load"],
        "domain_knowledge": agents["domain_knowledge"],
        "disclosure_quality": disclosure_quality,
        "counter_anchor_support": counter_anchor_support,
        "estimate": estimate,
        "bias": bias,
        "absolute_error": absolute_error,
        "confidence_adjusted_error": confidence_adjusted_error,
        "decision_quality": decision_quality,
        "welfare_proxy": welfare_proxy,
        "low_anchor_treat": int(regime_name == "low_anchor_low_support"),
        "high_anchor_treat": int(regime_name == "high_anchor_low_support"),
        "counter_context_treat": int(regime_name == "high_anchor_with_counter_context"),
    })

panel = pd.concat([
    simulate_anchor_regime(
        regime_name="low_anchor_low_support",
        anchor_value=25,
        disclosure_quality=0.25,
        counter_anchor_support=0.10,
    ),
    simulate_anchor_regime(
        regime_name="neutral_anchor_with_context",
        anchor_value=65,
        disclosure_quality=0.75,
        counter_anchor_support=0.65,
    ),
    simulate_anchor_regime(
        regime_name="high_anchor_low_support",
        anchor_value=85,
        disclosure_quality=0.25,
        counter_anchor_support=0.10,
    ),
    simulate_anchor_regime(
        regime_name="high_anchor_with_counter_context",
        anchor_value=85,
        disclosure_quality=0.85,
        counter_anchor_support=0.85,
    ),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    mean_anchor=("anchor_value", "mean"),
    mean_estimate=("estimate", "mean"),
    mean_bias=("bias", "mean"),
    mean_absolute_error=("absolute_error", "mean"),
    mean_effective_adjustment=("effective_adjustment", "mean"),
    mean_decision_quality=("decision_quality", "mean"),
    mean_welfare_proxy=("welfare_proxy", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_anchoring_bias_panel.csv", index=False)
summary.to_csv(TABLES / "anchoring_bias_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_anchoring_bias_panel.csv", index=False)
summary.to_csv(PROCESSED / "anchoring_bias_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} anchoring-regime rows.")
print(summary)
