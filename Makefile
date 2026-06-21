SHELL := /bin/bash

.PHONY: test-structure smoke-calculators list-articles

test-structure:
	python3 tests/test_repository_structure.py

smoke-calculators:
	bash scripts/run_calculator_smoke_tests.sh

list-articles:
	find articles -maxdepth 1 -mindepth 1 -type d | sort
