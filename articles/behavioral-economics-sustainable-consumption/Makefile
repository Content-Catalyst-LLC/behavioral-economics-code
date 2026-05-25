.PHONY: python r julia test all

python:
	python3 python/src/generate_synthetic_microdata.py
	python3 python/src/policy_microsimulation.py
	python3 python/src/causal_inference_event_study.py
	python3 python/src/sensitivity_analysis.py

r:
	Rscript r/behavioral_adoption_model.R

julia:
	julia julia/sustainable_consumption_microsimulation.jl

test:
	cd python && python3 -m pytest tests || true

all: python r julia
