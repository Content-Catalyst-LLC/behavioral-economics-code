#!/usr/bin/env bash
set -euo pipefail

ARTICLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ARTICLE_DIR}"

python3 python/src/generate_synthetic_microdata.py
python3 python/src/policy_microsimulation.py
python3 python/src/causal_inference_event_study.py
python3 python/src/sensitivity_analysis.py

echo "Python workflows complete."
