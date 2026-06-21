#!/usr/bin/env python3
"""Self-contained behavioral calculator for Behavioral Economics in Organizational Decision-Making.

This educational calculator produces transparent behavioral scores and
probability-like outputs from value, default, salience, effort, and norm inputs.
It is intentionally simple and does not require third-party packages.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def logistic(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def behavioral_score(value: float, default: float, salience: float, effort_cost: float, norm_signal: float) -> float:
    return value + 0.60 * default + 0.35 * salience - 0.45 * effort_cost + 0.30 * norm_signal


def main() -> None:
    parser = argparse.ArgumentParser(description="Behavioral-science calculator scaffold")
    parser.add_argument("--value", type=float, default=0.20)
    parser.add_argument("--default", type=float, default=1.00)
    parser.add_argument("--salience", type=float, default=0.50)
    parser.add_argument("--effort-cost", type=float, default=0.20)
    parser.add_argument("--norm-signal", type=float, default=0.10)
    parser.add_argument("--output", default="../outputs/calculator_result.json")
    args = parser.parse_args()

    score = behavioral_score(args.value, args.default, args.salience, args.effort_cost, args.norm_signal)
    probability = logistic(score)
    result = {
        "series": 'Behavioral Economics',
        "article": 'Behavioral Economics in Organizational Decision-Making',
        "model": "transparent_behavioral_score_v1",
        "inputs": {
            "value": args.value,
            "default": args.default,
            "salience": args.salience,
            "effort_cost": args.effort_cost,
            "norm_signal": args.norm_signal,
        },
        "behavioral_score": score,
        "choice_probability": probability,
        "responsible_use": "Educational scaffold only; not a validated behavioral or policy model."
    }

    out = Path(args.output)
    if not out.is_absolute():
        out = Path(__file__).resolve().parent / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
