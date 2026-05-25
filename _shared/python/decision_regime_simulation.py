"""
Synthetic behavioral economics simulation.

Compares classical-like and behaviorally modified decision regimes.
Educational scaffold only; not empirical behavioral data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RegimeConfig:
    name: str
    behavioral_scale: float
    default_bonus: float
    effort_penalty: float


def logistic(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def simulate_regime(config: RegimeConfig, n_agents: int = 2500, seed: int = 2727) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    base_value = rng.normal(0.15, 0.20, n_agents)
    framing = rng.normal(0, 0.15, n_agents) * config.behavioral_scale
    loss = rng.normal(-0.04, 0.16, n_agents) * config.behavioral_scale
    time_bias = rng.normal(-0.05, 0.14, n_agents) * config.behavioral_scale
    social = rng.normal(0.03, 0.12, n_agents) * config.behavioral_scale
    trust = rng.normal(0.08, 0.10, n_agents) * config.behavioral_scale
    default_status = rng.binomial(1, 0.50, n_agents)
    effort_cost = rng.uniform(0.02, 0.35, n_agents)

    latent = (
        base_value
        + framing
        + loss
        + time_bias
        + social
        + trust
        + config.default_bonus * default_status
        - config.effort_penalty * effort_cost
    )

    uptake_probability = logistic(latent)
    choose_option = rng.binomial(1, uptake_probability)

    return pd.DataFrame(
        {
            "regime": config.name,
            "base_value": base_value,
            "framing_signal": framing,
            "loss_signal": loss,
            "time_signal": time_bias,
            "social_signal": social,
            "trust_signal": trust,
            "default_status": default_status,
            "effort_cost": effort_cost,
            "uptake_probability": uptake_probability,
            "choose_option": choose_option,
        }
    )


def main() -> None:
    regimes = [
        RegimeConfig("classical_like", 0.20, 0.02, 0.20),
        RegimeConfig("behavioral_moderate", 1.00, 0.18, 0.65),
        RegimeConfig("behavioral_high", 1.60, 0.28, 0.95),
    ]

    frames = [simulate_regime(config, seed=2727 + i) for i, config in enumerate(regimes)]
    results = pd.concat(frames, ignore_index=True)

    summary = (
        results.groupby("regime", as_index=False)
        .agg(
            mean_uptake_probability=("uptake_probability", "mean"),
            observed_choice_share=("choose_option", "mean"),
            mean_effort_cost=("effort_cost", "mean"),
            default_share=("default_status", "mean"),
        )
        .sort_values("observed_choice_share", ascending=False)
    )

    print(summary.to_string(index=False))
    results.to_csv("outputs/tables/python_decision_regime_simulation.csv", index=False)


if __name__ == "__main__":
    main()
