package main

import "fmt"

func main() {
	values := []float64{0.20, 0.35, 0.62, 0.75, 0.91, 0.55}
	aspiration := 0.70
	searchCost := 0.02

	optimal := values[0]
	for _, value := range values {
		if value > optimal {
			optimal = value
		}
	}

	chosenIndex := len(values)
	chosenValue := values[len(values)-1]

	for i, value := range values {
		if value >= aspiration {
			chosenIndex = i + 1
			chosenValue = value
			break
		}
	}

	netValue := chosenValue - searchCost*float64(chosenIndex)

	fmt.Printf("Chosen index: %d\n", chosenIndex)
	fmt.Printf("Chosen value: %.3f\n", chosenValue)
	fmt.Printf("Optimal value: %.3f\n", optimal)
	fmt.Printf("Net value: %.3f\n", netValue)
	fmt.Printf("Optimization gap: %.3f\n", optimal-chosenValue)
}
