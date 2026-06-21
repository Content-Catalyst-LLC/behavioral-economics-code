"""Shared behavioral-science model helpers.

These functions are intentionally simple, transparent, and dependency-light.
They are scaffolds for article-level examples, not validated operational models.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable, List, Dict


def logistic(x: float) -> float:
    """Return a numerically stable logistic probability."""
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def prospect_value(x: float, alpha: float = 0.88, beta: float = 0.88, loss_lambda: float = 2.25) -> float:
    """Simplified prospect-theory value function."""
    if x >= 0:
        return x ** alpha
    return -loss_lambda * ((-x) ** beta)


def default_effect_score(value: float, default: float = 0.0, salience: float = 0.0, effort_cost: float = 0.0, norm_signal: float = 0.0) -> float:
    """Transparent behavioral score combining value, default, salience, effort, and norm signals."""
    return value + 0.60 * default + 0.35 * salience - 0.45 * effort_cost + 0.30 * norm_signal


def choice_probability(value: float, default: float = 0.0, salience: float = 0.0, effort_cost: float = 0.0, norm_signal: float = 0.0) -> float:
    """Convert a behavioral score to a probability-like quantity."""
    return logistic(default_effect_score(value, default, salience, effort_cost, norm_signal))


def simulate_choice_panel(n: int = 250, seed: int = 2727) -> List[Dict[str, float]]:
    """Generate a small synthetic panel for examples and smoke tests."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        value = rng.uniform(-1.0, 1.0)
        default = rng.choice([0.0, 1.0])
        salience = rng.uniform(0.0, 1.0)
        effort = rng.uniform(0.0, 1.0)
        norm = rng.uniform(-0.5, 0.5)
        p = choice_probability(value, default, salience, effort, norm)
        rows.append({
            "agent_id": i + 1,
            "value": value,
            "default": default,
            "salience": salience,
            "effort_cost": effort,
            "norm_signal": norm,
            "choice_probability": p,
            "choice": 1.0 if rng.random() < p else 0.0,
        })
    return rows
