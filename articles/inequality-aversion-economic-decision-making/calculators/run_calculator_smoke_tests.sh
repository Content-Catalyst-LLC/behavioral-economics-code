#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p outputs
python3 python/behavioral_calculator.py --output ../outputs/calculator_result.json >/dev/null
if command -v Rscript >/dev/null 2>&1; then
  Rscript r/behavioral_calculator.R >/dev/null
else
  echo "Rscript not found; skipped R calculator smoke test."
fi
echo "Calculator smoke tests completed for $(basename "$(dirname "$PWD")")"
