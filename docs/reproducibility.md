# Reproducibility Guide

Suggested setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas matplotlib
python _shared/python/decision_regime_simulation.py
Rscript _shared/r/behavioral_friction_model.R
```

Compiled examples can be run with standard local compilers when available:

```bash
g++ _shared/cpp/prospect_value.cpp -o outputs/prospect_value && ./outputs/prospect_value
gcc _shared/c/default_effect_model.c -lm -o outputs/default_effect_model && ./outputs/default_effect_model
gfortran _shared/fortran/intertemporal_discounting.f90 -o outputs/intertemporal_discounting && ./outputs/intertemporal_discounting
go run _shared/go/policy_uptake_simulation.go
rustc _shared/rust/social_preference_cli.rs -o outputs/social_preference_cli && ./outputs/social_preference_cli
```
