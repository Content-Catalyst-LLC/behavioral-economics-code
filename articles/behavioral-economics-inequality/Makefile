SHELL := /bin/bash

.PHONY: smoke-calculators python-calculator r-calculator

smoke-calculators:
	bash calculators/run_calculator_smoke_tests.sh

python-calculator:
	cd calculators && python3 python/behavioral_calculator.py

r-calculator:
	cd calculators && Rscript r/behavioral_calculator.R
