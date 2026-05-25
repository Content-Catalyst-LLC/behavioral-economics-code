#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs/tables
Rscript _shared/r/behavioral_friction_model.R
