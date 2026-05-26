from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"
for folder in [TABLES, PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(18180)

n_agents = 3000

agents = pd.DataFrame({
    "agent_id": np.arange(1, n_agents + 1),
    "switch_cost": rng.uniform(0.05, 0.45, n_agents),
    "loss_aversion": rng.uniform(1.00, 3.25, n_agents),
    "status_quo_premium": rng.uniform(0.02, 0.30, n_agents),
    "uncertainty_sensitivity": rng.uniform(0.05, 0.35, n_agents),
    "decision_fatigue": rng.uniform(0.00, 0.35, n_agents),
    "sophistication": rng.uniform(0.20, 1.00, n_agents),
})

def simulate_default_regime(
    regime_name: str,
    default_shift: float,
    switching_support: float,
    disclosure_quality: float,
) -> pd.DataFrame:
    value_status_quo = rng.uniform(0.45, 0.60, n_agents)
    value_alternative = value_status_quo + rng.uniform(0.02, 0.25, n_agents)

    perceived_loss = rng.uniform(0.02, 0.20, n_agents)

    effective_switch_cost = np.maximum(
        agents["switch_cost"].to_numpy()
        - switching_support * agents["sophistication"].to_numpy() * 0.20,
        0,
    )

    effective_status_quo_premium = np.maximum(
        agents["status_quo_premium"].to_numpy()
        + agents["decision_fatigue"].to_numpy()
        - default_shift * 0.18
        - disclosure_quality * agents["sophistication"].to_numpy() * 0.12,
        0,
    )

    effective_perceived_loss = np.maximum(
        perceived_loss
        + agents["uncertainty_sensitivity"].to_numpy()
        - disclosure_quality * 0.10,
        0,
    )

    utility_status_quo = value_status_quo + effective_status_quo_premium

    utility_alternative = (
        value_alternative
        - effective_switch_cost
        - agents["loss_aversion"].to_numpy() * effective_perceived_loss
    )

    choose_alternative = (utility_alternative >= utility_status_quo).astype(int)

    welfare = np.where(
        choose_alternative == 1,
        value_alternative - effective_switch_cost,
        value_status_quo,
    )

    return pd.DataFrame({
        "agent_id": agents["agent_id"],
        "regime": regime_name,
        "value_status_quo": value_status_quo,
        "value_alternative": value_alternative,
        "objective_gain": value_alternative - value_status_quo,
        "switch_cost": agents["switch_cost"],
        "effective_switch_cost": effective_switch_cost,
        "loss_aversion": agents["loss_aversion"],
        "status_quo_premium": agents["status_quo_premium"],
        "uncertainty_sensitivity": agents["uncertainty_sensitivity"],
        "decision_fatigue": agents["decision_fatigue"],
        "sophistication": agents["sophistication"],
        "effective_status_quo_premium": effective_status_quo_premium,
        "perceived_loss": perceived_loss,
        "effective_perceived_loss": effective_perceived_loss,
        "utility_status_quo": utility_status_quo,
        "utility_alternative": utility_alternative,
        "choose_alternative": choose_alternative,
        "welfare": welfare,
        "default_shift": default_shift,
        "switching_support": switching_support,
        "disclosure_quality": disclosure_quality,
        "active_choice_treat": int(regime_name == "active_choice_with_disclosure"),
        "pro_switching_treat": int(regime_name == "pro_switching_default_with_support"),
    })

panel = pd.concat([
    simulate_default_regime(
        regime_name="passive_status_quo_default",
        default_shift=0.00,
        switching_support=0.00,
        disclosure_quality=0.10,
    ),
    simulate_default_regime(
        regime_name="active_choice_with_disclosure",
        default_shift=0.35,
        switching_support=0.35,
        disclosure_quality=0.55,
    ),
    simulate_default_regime(
        regime_name="pro_switching_default_with_support",
        default_shift=0.75,
        switching_support=0.70,
        disclosure_quality=0.80,
    ),
], ignore_index=True)

summary = panel.groupby("regime").agg(
    agents=("agent_id", "count"),
    adoption_rate=("choose_alternative", "mean"),
    mean_welfare=("welfare", "mean"),
    mean_objective_gain=("objective_gain", "mean"),
    mean_effective_switch_cost=("effective_switch_cost", "mean"),
    mean_status_quo_premium=("effective_status_quo_premium", "mean"),
    mean_effective_perceived_loss=("effective_perceived_loss", "mean"),
).reset_index()

panel.to_csv(TABLES / "synthetic_status_quo_bias_panel.csv", index=False)
summary.to_csv(TABLES / "status_quo_bias_regime_summary.csv", index=False)
panel.to_csv(PROCESSED / "synthetic_status_quo_bias_panel.csv", index=False)
summary.to_csv(PROCESSED / "status_quo_bias_regime_summary.csv", index=False)

print(f"Wrote {len(panel):,} decision-regime rows.")
print(summary)
