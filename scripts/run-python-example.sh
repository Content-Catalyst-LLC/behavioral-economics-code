#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs/tables
python3 _shared/python/decision_regime_simulation.py
