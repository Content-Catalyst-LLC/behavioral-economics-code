package main

import "fmt"

func clamp(x, low, high float64) float64 {
	if x < low {
		return low
	}
	if x > high {
		return high
	}
	return x
}

func heuristicEstimate(
	trueValue,
	availabilityWeight,
	availabilitySignal,
	representativenessWeight,
	representativenessSignal,
	anchorWeight,
	anchorSignal,
	framingWeight,
	framingSignal,
	correctionCapacity float64,
) float64 {
	rawError := availabilityWeight*availabilitySignal +
		representativenessWeight*representativenessSignal +
		anchorWeight*anchorSignal +
		framingWeight*framingSignal

	estimate := trueValue + rawError*(1.0-correctionCapacity)
	return clamp(estimate, 0.0, 1.0)
}

func main() {
	estimate := heuristicEstimate(0.35, 0.30, 0.10, 0.25, -0.05, 0.40, 0.12, 0.20, -0.08, 0.55)
	fmt.Printf("Synthetic heuristic estimate: %.3f\n", estimate)
	fmt.Printf("Synthetic judgment error: %.3f\n", estimate-0.35)
}
