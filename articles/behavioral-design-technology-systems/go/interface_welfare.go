package main

import (
	"fmt"
	"math"
)

func userWelfare(joined, baselineValue, rewardIntensity, frictionAsymmetry, autonomyPreference, privacyCost, cognitiveOverload float64) float64 {
	autonomyCost := 0.7 * math.Max(frictionAsymmetry, 0.0) * autonomyPreference
	return joined*(baselineValue+0.35*rewardIntensity) - autonomyCost - privacyCost - 0.45*cognitiveOverload
}

func main() {
	w := userWelfare(1.0, 0.45, 0.35, 0.0, 0.58, 0.05, 0.42)
	fmt.Printf("Synthetic user welfare: %.3f\n", w)
}
