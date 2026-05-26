package main

import "fmt"

func userWelfare(clicked, exposureQuality, cognitiveOverload, privacySensitivity, dataExtractionIntensity, consented, friction float64) float64 {
	return clicked*exposureQuality -
		0.30*cognitiveOverload -
		0.45*privacySensitivity*dataExtractionIntensity*consented -
		0.15*friction
}

func main() {
	w := userWelfare(1.0, 0.52, 0.42, 0.55, 0.10, 1.0, 0.18)
	fmt.Printf("Synthetic platform user welfare: %.3f\n", w)
}
