#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
count=0
for script in "$ROOT"/articles/*/calculators/run_calculator_smoke_tests.sh; do
  [ -f "$script" ] || continue
  bash "$script"
  count=$((count + 1))
done
echo "Completed calculator smoke tests for $count article folder(s)."
